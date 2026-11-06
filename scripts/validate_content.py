#!/usr/bin/env python3
"""Standard-library-only shape, taxonomy, index and asset-budget checks."""
import json, pathlib, re, sys
root=pathlib.Path(__file__).resolve().parents[1]
base=root/"v1"/"content"
folders={"in":"sa","bd":"be","us":"am","gb":"br","de":"ge","jp":"ja","kr":"ko","br":"la","global_default":"un"}
types={"wo":"window_opener","mr":"main_refuel","hy":"hydration_broth","ld":"light_digest"}
keys={"id","title","description","cuisine","mealType","protocols","prepMinutes","servings","difficulty","digestiveLoad","whyItWorks","nutrition","ingredients","steps","coverImage"}
nutrition={"calories","proteinGrams","fatGrams","netCarbsGrams","fiberGrams","sodiumMg","potassiumMg"}
errors=[]
for folder,cuisine in folders.items():
 p=base/folder
 index=json.loads((p/"index.json").read_text())
 ids=index["recipeIds"]
 if len(ids)!=120 or len(set(ids))!=120:errors.append(folder+": expected 120 unique IDs")
 counts={t:0 for t in types}
 for rid in ids:
  m=re.fullmatch(r"(in|bd|us|gb|de|jp|kr|br|gl)_(sa|be|am|br|ge|ja|ko|la|un)_(wo|mr|hy|ld)_([0-9]{3})",rid)
  if not m:errors.append(rid+": invalid ID");continue
  country="gl" if folder=="global_default" else folder
  if m.group(1)!=country or m.group(2)!=cuisine:errors.append(rid+": namespace mismatch")
  counts[m.group(3)]+=1
  file=p/"recipes"/rid/"recipe.json"
  if not file.exists():errors.append(rid+": missing JSON");continue
  obj=json.loads(file.read_text())
  if set(obj)!=keys:errors.append(rid+": wrong top-level fields")
  if obj.get("id")!=rid or obj.get("mealType")!=types[m.group(3)]:errors.append(rid+": type mismatch")
  if obj.get("coverImage")!="cover.webp":errors.append(rid+": invalid cover filename")
  if set(obj.get("nutrition",{}))!=nutrition:errors.append(rid+": nutrition keys mismatch")
  if not isinstance(obj.get("ingredients"),list) or not isinstance(obj.get("steps"),list):errors.append(rid+": invalid instructions")
  cover=file.parent/"cover.webp"
  if cover.exists():
   if cover.stat().st_size>100000:errors.append(rid+": image exceeds 100KB")
   if cover.read_bytes()[:4]!=b"RIFF" or cover.read_bytes()[8:12]!=b"WEBP":errors.append(rid+": invalid WebP")
  elif index.get("coverReady",False):errors.append(rid+": missing published cover")
 if any(v!=30 for v in counts.values()):errors.append(folder+": incorrect section counts "+str(counts))
 asset_bytes=sum(f.stat().st_size for f in p.rglob("*") if f.is_file() and f.suffix.lower() in {".webp",".png",".jpg",".jpeg",".svg"})
 if asset_bytes>20000000:errors.append(folder+": assets exceed 20MB")
print("PASS: 9 locale folders x 120 recipes" if not errors else "\n".join(errors))
sys.exit(bool(errors))
