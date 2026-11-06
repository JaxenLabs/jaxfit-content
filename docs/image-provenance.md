# Image mapping and provenance

Each cover is a **stylized labeled illustration, not a photograph**. The generator loads the exact recipe.json, renders its title and semantic food ID on the cover, and records an `assets.json` mapping per locale with the image path, recipe path, file bytes, and SHA-256. It checks unique IDs, WebP format, 100 KB per image and 20 MB per folder. The dish rendering is schematic and must not be represented as accurate recipe photography.
