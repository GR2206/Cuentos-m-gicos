# Especiales 3D — Cuentos mágicos de la selva

Serie especial en 3D (estilo peluche aterciopelado). El canal sigue en 2D plano; estos episodios se guardan
sin publicar hasta tener **al menos 5**, y después salen de a 1 o 2 por semana/mes como toque "elegante".
Cuando el canal genere plata: plan pago de Google y todo el canal pasa a 3D.

## Qué hay acá
| Carpeta / archivo | Contenido |
|---|---|
| `estilo-3d.md` | Bloques de prompt que se repiten en TODAS las escenas (estilo, cierre "sin música/voz/texto", trucos). |
| `personajes/<nombre>/` | Hoja 3D (ingrediente para Flow), cara 2D oficial del canal y el prompt para generar la hoja. |
| `escenas/espNN-.../` | Guion, narración para Malena y un prompt por escena de cada especial. |

**Los videos NO van al repo** (pesan mucho): guardalos en la PC (`E:\Cuentos mágicos de la Selva\especiales-3d\`) o en Drive,
con el mismo nombre que la escena: `esp01_e01.mp4`, `esp01_e02.mp4`… El `.gitignore` ya ignora los `.mp4`.

## Cómo generar en Google Flow (cuenta gratis, 50 créditos por día)
1. Entrá a flow.google.com → **New project** (uno por especial, así quedan juntos).
2. Elegí **Ingredients to Video**.
3. Subí como ingrediente la **hoja 3D** del personaje (`personajes/coco/coco-hoja-3d.jpg`).
   Si en la escena hay 2 personajes, subí las 2 hojas (Flow acepta hasta 3 ingredientes).
4. En la configuración (ícono de ajustes): **Outputs per prompt = 1** (x1, no x2), formato **16:9**.
5. Copiá el prompt de la escena tal cual (está en inglés porque Flow lo entiende mejor) y generá.
6. Si sale bien: descargalo en 720p y renombralo (`esp01_e03.mp4`). Si sale mal, anotá qué falló
   en la columna "Notas" del guion y probá de nuevo al otro día con el ajuste.
7. Marcá la escena como hecha en la tabla del guion (o pedímelo y lo actualizo yo).

## Cuando estén todas las escenas
Pasame los clips + el audio de Malena (ElevenLabs) y yo uno todo: narración, música suave original,
subtítulos, placa final de GR Producciones, y el short vertical (recorto el centro del cuadro;
por eso en los prompts Coco va siempre centrado).

## Estado de la serie
| # | Especial | Estado |
|---|---|---|
| 0 | Coco se va a dormir | ✅ generado (prueba, 1 escena de 8 s) |
| 1 | Coco y la semillita mágica | ✏️ guion listo, falta generar las 8 escenas |
| 2 | — | |
| 3 | — | |
| 4 | — | |

## Personajes 3D
| Personaje | Hoja 3D | Altura relativa (para escenas juntos) |
|---|---|---|
| Coco el monito | ✅ `coco/coco-hoja-3d.jpg` | 1 (referencia) |
| Lola la lorita | ✅ `lola/lola-hoja-3d.jpg` | 0,6 de Coco |
| Tito el elefantito | ✅ `tito/tito-hoja-3d.jpg` | 1,4 de Coco |
| Pipa la jirafita | ⬜ 2D + prompt listos | 2 de Coco (cuello largo) |
| Tomi la tortuguita | ⬜ 2D + prompt listos | 0,8 de Coco |
| Papá Coco / Mamá Coco | ⬜ más adelante | 1,6 de Coco |
