# Pipa la jirafita — 3D

Personalidad: alta, ve todo desde arriba y avisa. Altura al lado de Coco: 2 de Coco (por el cuello).
Accesorio: collar de perlas chiquitas en la base del cuello (elegido por Gino).

- `pipa-cuerpo-2d.png` → **cuerpo entero 2D plano** (de `codigo/cuerpos.py`, con la cara oficial de `amigos.py`): la referencia de diseño para el 3D.
- `pipa-cara-2d-oficial.png` → solo la cara, por si hace falta un primer plano.
- `pipa-hoja-3d.jpg` → ✅ **ingrediente para Flow** (generada el 24/11/2026).

## Cómo generar la hoja 3D (paso a paso)
1. En Flow elegí crear **imagen** (o usá la app de Gemini si Flow te cobra créditos por imágenes).
2. Subí **2 imágenes de referencia**:
   - `personajes/coco/coco-hoja-3d.jpg` → para copiar el **estilo** (peluche, luz, fondo, 4 vistas).
   - `pipa-cuerpo-2d.png` → para copiar el **diseño** del personaje (colores, ropa, forma).
3. Pegá el prompt de abajo. Generá varias y quedate con la que tenga las 4 vistas iguales entre sí.
4. Revisá: mismos colores en las 4 vistas, sin texto, sin un monito colado (a veces copia a Coco).
5. Mandámela y la subo al repo.

## Prompt de la hoja
```
Character turnaround reference sheet in exactly the same 3D plush style, lighting and layout as the attached monkey sheet, but the character is: Pipa, a cute baby giraffe with soft velvety plush yellow fur with soft round orange spots, a cream-colored muzzle, two short horns with round brown tips, small rounded ears, big glossy dark eyes with small eyelashes, a sweet smile, rosy cheeks, a long neck, slim legs with little brown hooves, a short tail with a brown tuft, wearing a delicate necklace of small white pearls at the base of her neck. Based on the attached flat 2D full-body design, keeping its colors, clothes and shapes. Four full-body views in one row on a plain warm cream background: front, three-quarter, side profile, back. Same size in all four views, neutral standing pose, arms slightly away from the body, soft contact shadow under the feet. Only this character, no monkey. No text, no labels.
```

## [PERSONAJE] — bloque para los prompts de escena
```
Pipa, a cute baby giraffe with soft velvety plush yellow fur with soft round orange spots, a cream-colored muzzle, two short horns with round brown tips, small rounded ears, big glossy dark eyes with small eyelashes, a sweet smile, rosy cheeks, a long neck, slim legs with little brown hooves, a short tail with a brown tuft, wearing a delicate necklace of small white pearls at the base of her neck. Exactly as in the attached character sheet.
```
