# Cuentos mágicos de la selva — guía para Claude

Canal infantil de YouTube de Gino. Todo se dibuja con código (Python + pycairo) y se arma con ffmpeg.
Gino se describe como "medio novato": explicarle paso a paso lo que tenga que hacer a mano.

## Reglas de estilo (no cambiar sin que Gino lo pida)
- Estilo plano tipo dibujito infantil: formas redondas, contorno marrón oscuro `#3B2314` de ~6 px, colores vivos, cachetes rosados.
- Personajes SIEMPRE desde `codigo/amigos.py` (cabezas) o el cuerpo de Coco en `escena_noche.py` / `ep01_...py`. Nunca redibujarlos de cero: así se ven iguales en todos los videos.
- Cuerpos completos (para historias): `codigo/cuerpos.py` (`K.put(c, K.coco, x, y, escala, ...)`). Coco tiene expresiones (`mood`: smile, closed, sad, o, chew), Tito estira la trompa (`reach`), Pipa estira el cuello (`neck`), Lola aletea (`flap`), Tomi se esconde en el caparazón (`hide` 0–1), Tito abre las orejas como paraguas (`umbrella` 0–1), Coco puede estirar los brazos (`arm_len`, p. ej. para taparse los ojos).
- Personajes nuevos: agregarlos a `amigos.py` con el mismo estilo y sumarlos a `ALL` y `COLORS`.
- Música: siempre original o de dominio público. Nada de personajes, canciones o marcas con copyright (no imitar Peppa Pig ni otros).
- Historias cortitas, movimientos suaves, pensadas para ver muchas veces.
- Video: 1920×1080, 30 fps, H.264 `-crf 18 -preset veryfast -pix_fmt yuv420p`, audio AAC 192k.
- Tipografía de títulos: Fredoka Bold (`fuentes/Fredoka-Bold.ttf`, licencia OFL). Instalar con
  `mkdir -p ~/.fonts && cp fuentes/Fredoka-Bold.ttf ~/.fonts/ && fc-cache -f` (fontconfig la llama "Fredoka Light").

## Personajes
| Nombre | Animal | Personalidad | Color |
|---|---|---|---|
| Coco | monito | protagonista, curioso y alegre | `#A0582C` |
| Lola | lorita | charlatana, canta | `#E53935` |
| Tito | elefantito | grandote, tierno, tímido | `#8FB8E8` |
| Pipa | jirafita | alta, ve todo desde arriba y avisa | `#FFCF40` |
| Tomi | tortuguita | lenta y sabia, siempre llega | `#7CCB5B` |

## Entregables de cada episodio
Video para YouTube (intro + episodio), short vertical 1080×1920 de ≤60 s (`epXX_extras.py short`), miniatura 1280×720 (`epXX_extras.py miniatura`), y título/descripción/etiquetas.

## Tipos de video
- **Aventuritas** (2–3 min): historias cortas (cruzar el bosque, el puente del río, la lluvia…).
- **A dormir con…** (1–2 min): de noche, música lenta y suave.
- Todos arrancan con `videos/intro_canal.mp4`.

## Cómo renderizar
Cada script de escena escribe cuadros crudos por stdout; ejemplo:
```
cd codigo
python3 ep01_musica.py
python3 ep01_coco_se_va_a_dormir.py | ffmpeg -y -f rawvideo -pix_fmt bgra -s 1920x1080 -r 30 -i - \
  -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p video.mp4
ffmpeg -i video.mp4 -i sleep_music.wav -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```
Episodios largos: `python3 ep02_puente_del_rio.py range 0 63` renderiza solo un tramo (se pueden hacer dos tramos en paralelo y unirlos con el concat de ffmpeg).
Versión final para YouTube (intro + episodio, una sola codificación):
```
ffmpeg -i ../videos/intro_canal.mp4 -i episodio.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -profile:v high -preset slow -crf 16 -g 15 -bf 2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 384k -ar 48000 -ac 2 -movflags +faststart final.mp4
```
`python3 <script>.py stills 2.5 10` guarda cuadros sueltos para revisar antes del render completo.
