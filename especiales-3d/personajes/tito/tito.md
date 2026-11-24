# Tito el elefantito — 3D

Personalidad: grandote, tierno y tímido. Altura al lado de Coco: 1,4 de Coco.
Accesorio (aprobado): Jardinero (shorts con tiradores) rojo, para que contraste con el celeste.

- `tito-cuerpo-2d.png` → **cuerpo entero 2D plano** (de `codigo/cuerpos.py`, con la cara oficial de `amigos.py`): la referencia de diseño para el 3D.
- `tito-cara-2d-oficial.png` → solo la cara, por si hace falta un primer plano.
- `tito-hoja-3d.jpg` → **falta**: cuando la generes, guardala con este nombre en esta carpeta.

## Cómo generar la hoja 3D (paso a paso)
1. En Flow elegí crear **imagen** (o usá la app de Gemini si Flow te cobra créditos por imágenes).
2. Subí **2 imágenes de referencia**:
   - `personajes/coco/coco-hoja-3d.jpg` → para copiar el **estilo** (peluche, luz, fondo, 4 vistas).
   - `tito-cuerpo-2d.png` → para copiar el **diseño** del personaje (colores, ropa, forma).
3. Pegá el prompt de abajo. Generá varias y quedate con la que tenga las 4 vistas iguales entre sí.
4. Revisá: mismos colores en las 4 vistas, sin texto, sin un monito colado (a veces copia a Coco).
5. Mandámela y la subo al repo.

## Prompt de la hoja
```
Character turnaround reference sheet in exactly the same 3D plush style, lighting and layout as the attached monkey sheet, but the character is: Tito, a cute chubby baby elephant with soft velvety plush light blue skin, a big round head, large round ears with soft pink inside, a short trunk that curls up at the tip, big glossy dark eyes, a shy gentle smile, rosy cheeks, chunky round legs with light cream toenails, a small tail with a tuft, wearing small red overall shorts with two straps. Based on the attached flat 2D full-body design, keeping its colors, clothes and shapes. Four full-body views in one row on a plain warm cream background: front, three-quarter, side profile, back. Same size in all four views, neutral standing pose, arms slightly away from the body, soft contact shadow under the feet. Only this character, no monkey. No text, no labels.
```

## [PERSONAJE] — bloque para los prompts de escena
```
Tito, a cute chubby baby elephant with soft velvety plush light blue skin, a big round head, large round ears with soft pink inside, a short trunk that curls up at the tip, big glossy dark eyes, a shy gentle smile, rosy cheeks, chunky round legs with light cream toenails, a small tail with a tuft, wearing small red overall shorts with two straps. Exactly as in the attached character sheet.
```
