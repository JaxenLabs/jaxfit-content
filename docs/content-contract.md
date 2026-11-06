# JaxFit v1 content contract

- Countries: `in`, `bd`, `us`, `gb`, `de`, `jp`, `kr`, `br`, `global_default` (`gl` in IDs).
- Every recipe lives at `v1/content/{folder}/recipes/{id}/recipe.json`.
- Asset ID is the parent recipe ID; cover filename is `cover.webp` in the same folder. Recipe JSON uses exact 15 top-level fields.
- Each folder contains 30 recipes per `wo`,`mr`,`hy`,`ld` section (120 total). The index declares `coverReady: false` until actual imagery has been committed.
- Images are **not yet included**; do not request cover URLs until the file is present. Never fabricate image assets or claim placeholder paths are published.
- Once published, use immutable Git tag (such as `v1.0.0`) on jsDelivr. Do not assume a tag exists until created. Prefer revisioned manifests and local offline cache; never depend on a network connection at runtime.
- Limit each WebP to 100,000 bytes and total assets within each country folder to 20,000,000 bytes. Reject over-budget files in CI before merging.
- **Content caution:** Entries below are draft templates. Ingredient amounts and nutrition are *illustrative estimates*, not nutritionally verified recipe calculations. Steps are starter guidance, not lab-tested cooking instructions. Do not advertise clinical effects or use as patient-specific fasting advice. Independently review food safety, allergens, nutritional analysis and localization before shipping.
- The six variations of each base dish form 30 examples per section; replace drafts with professionally tested recipes before launch.
