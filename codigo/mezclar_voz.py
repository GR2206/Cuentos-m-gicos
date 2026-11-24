"""Pone la voz en off (un solo audio con todas las frases del guion, p. ej. de ElevenLabs) sobre un episodio terminado.

Uso:  python3 mezclar_voz.py ep26_concierto voz.mp3 ../videos/ep26_concierto_youtube.mp4 ../videos/ep26_concierto_narrado_youtube.mp4
      (agregar --ver para solo mostrar cómo cortó las frases, sin mezclar)

1. Busca las pausas del audio y elige los cortes que mejor coinciden con el largo de cada frase de NARRACION.
2. Ubica cada frase en su momento (NARRACION + 5.5 s de intro); si una frase larga se pisa con la siguiente, corre la siguiente.
3. Baja la música debajo de la voz (curva de volumen + sidechain) y normaliza a -16 LUFS. El video se copia sin recodificar."""
import importlib, json, subprocess, sys
import numpy as np

INTRO = 5.5
SR = 48000

def load_mono(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)

def split_phrases(voz, texts, min_pause=0.15):
    hop = int(SR * 0.025); n = len(voz) // hop
    db = np.array([20 * np.log10(np.sqrt((voz[i * hop:(i + 1) * hop] ** 2).mean()) + 1e-9) for i in range(n)])
    thr = max(np.percentile(db, 10) + 15, -50)
    v = db > thr
    runs, cur, st = [], v[0], 0
    for i, x in enumerate(v):
        if x != cur: runs.append((cur, st * 0.025, i * 0.025)); cur, st = x, i
    runs.append((cur, st * 0.025, n * 0.025))
    start = next(r[1] for r in runs if r[0]); end = max(r[2] for r in runs if r[0])
    P = [(a, b) for (on, a, b) in runs if not on and b - a >= min_pause and a > start + 0.3 and b < end - 0.3]
    w = np.array([len(t) + 8 * t.count('...') + 4 * sum(t.count(p) for p in '.!?,:') for t in texts], float)
    exp = w / w.sum() * (end - start)
    pts = [start] + [(a + b) / 2 for a, b in P] + [end]; pd = [0] + [b - a for a, b in P] + [0]
    K, N = len(texts), len(pts)
    dp = np.full((K + 1, N), 1e9); bk = np.zeros((K + 1, N), int); dp[0][0] = 0
    for k in range(1, K + 1):
        for j in range(1, N):
            for i in range(j):
                if dp[k - 1][i] >= 1e9: continue
                cst = dp[k - 1][i] + (pts[j] - pts[i] - exp[k - 1]) ** 2 / exp[k - 1] - 0.8 * pd[j]
                if cst < dp[k][j]: dp[k][j], bk[k][j] = cst, i
    j, cuts = N - 1, []
    for k in range(K, 0, -1): i = bk[k][j]; cuts.append((i, j)); j = i
    segs = []
    for (i, j) in cuts[::-1]:
        s = start if i == 0 else P[i - 1][1]; e = end if j == N - 1 else P[j - 1][0]; segs.append((s, e))
    return segs, exp

def place(segs, narr):
    at, last = [], -1.0
    for (s, e), (a, b, _) in zip(segs, narr):
        t = max(a, last + 0.4); at.append(t); last = t + (e - s)
    return at

def mix(voice_path, segs, at, video_in, video_out):
    parts, labels, win = [], [], []
    for k, ((s, e), t) in enumerate(zip(segs, at)):
        s2 = max(0, s - 0.08); e2 = e + 0.15; d = int((t + INTRO - 0.08) * 1000)
        parts.append(f"[1:a]atrim={s2}:{e2},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={e2 - s2 - 0.1}:d=0.1,adelay={d}|{d}[v{k}]")
        labels.append(f"[v{k}]"); win.append((t + INTRO - 0.4, t + INTRO + (e - s) + 0.4))
    expr = None
    for (a, b) in win:
        tm = f"clip(min((t-{a - 0.35})/0.35,({b + 0.35}-t)/0.35),0,1)"
        expr = tm if expr is None else f"max({expr},{tm})"
    f = ";".join(parts) + (f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0,aresample={SR},highpass=f=70,"
         "acompressor=threshold=-18dB:ratio=2:attack=5:release=120,volume=1.3,aformat=channel_layouts=stereo,apad[voz];"
         "[voz]asplit[voz1][sc];"
         f"[0:a]aformat=channel_layouts=stereo,volume='1-0.62*{expr}':eval=frame[mus];"
         "[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=450:makeup=1[duck];"
         "[duck][voz1]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    tmp = video_out[:-4] + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video_in, '-i', voice_path, '-filter_complex', f,
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '384k', '-ar', str(SR),
                    '-movflags', '+faststart', tmp], check=True)
    subprocess.run(['mv', tmp, video_out], check=True)

if __name__ == '__main__':
    ep, voice, vin, vout = sys.argv[1:5]
    narr = importlib.import_module(ep).NARRACION
    voz = load_mono(voice)
    segs, exp = split_phrases(voz, [t for _, _, t in narr])
    at = place(segs, narr)
    for k, ((s, e), t, x) in enumerate(zip(segs, at, exp)):
        print(f'{k + 1:2d}. audio {s:6.2f}-{e:6.2f} ({e - s:4.1f}s, esperado {x:4.1f}s) -> {t:5.1f}s | {narr[k][2][:45]}')
    if '--ver' not in sys.argv:
        mix(voice, segs, at, vin, vout); print('listo:', vout)
