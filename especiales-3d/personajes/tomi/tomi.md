# Tomi la tortuguita — 3D

Personalidad: lenta y sabia, siempre llega. Altura al lado de Coco: 0,8 de Coco.
Accesorio (aprobado): Bufandita naranja. Parada en dos patitas, como Coco.

- `tomi-cuerpo-2d.png` → **cuerpo entero 2D plano** (de `codigo/cuerpos.py`, con la cara oficial de `amigos.py`): la referencia de diseño para el 3D.
- `tomi-cara-2d-oficial.png` → solo la cara, por si hace falta un primer plano.
- `tomi-hoja-3d.jpg` → **falta**: cuando la generes, guardala con este nombre en esta carpeta.

## Cómo generar la hoja 3D (paso a paso)
1. En Flow elegí crear **imagen** (o usá la app de Gemini si Flow te cobra créditos por imágenes).
2. Subí **2 imágenes de referencia**:
   - `personajes/coco/coco-hoja-3d.jpg` → para copiar el **estilo** (peluche, luz, fondo, 4 vistas).
   - `tomi-cuerpo-2d.png` → para copiar el **diseño** del personaje (colores, ropa, forma).
3. Pegá el prompt de abajo. Generá varias y quedate con la que tenga las 4 vistas iguales entre sí.
4. Revisá: mismos colores en las 4 vistas, sin texto, sin un monito colado (a veces copia a Coco).
5. Mandámela y la subo al repo.

## Prompt de la hoja
```
Character turnaround reference sheet in exactly the same 3D plush style, lighting and layout as the attached monkey sheet, but the character is: Tomi, a cute baby turtle with soft velvety plush green skin, a round head, big glossy dark eyes, a happy open smile, rosy cheeks, a brown dome shell with lighter beige-brown rounded patches, a cream belly plate, short chubby arms and legs, standing upright on two legs like a toddler, wearing a small orange scarf. Based on the attached flat 2D full-body design, keeping its colors, clothes and shapes. Four full-body views in one row on a plain warm cream background: front, three-quarter, side profile, back. Same size in all four views, neutral standing pose, arms slightly away from the body, soft contact shadow under the feet. Only this character, no monkey. No text, no labels.
```

## [PERSONAJE] — bloque para los prompts de escena
```
Tomi, a cute baby turtle with soft velvety plush green skin, a round head, big glossy dark eyes, a happy open smile, rosy cheeks, a brown dome shell with lighter beige-brown rounded patches, a cream belly plate, short chubby arms and legs, standing upright on two legs like a toddler, wearing a small orange scarf. Exactly as in the attached character sheet.
```
