#!/usr/bin/env python3
"""Generate deterministic, lightweight illustrated JaxFit recipe covers.
These are original vector-style food illustrations, not photographs.
Requires Pillow. Uses recipe IDs as deterministic seeds.
"""
from __future__ import annotations
import hashlib, json, math, pathlib, random, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/"v1"/"content"
FOLDERS=["in","bd","us","gb","de","jp","kr","br","global_default"]
PALETTES={
"in":("#f7e8cd","#d8a13b","#769a45"),"bd":("#f2e6d6","#c88b3f","#5b984b"),
"us":("#e6e8d4","#c48a56","#448b62"),"gb":("#e6e8df","#bc9665","#6a945a"),
"de":("#e9e2d2","#bb9a58","#699453"),"jp":("#e9e5da","#c79463","#628c62"),
"kr":("#eae0d5","#ba654c","#57906c"),"br":("#e8ebd7","#c39b47","#57a258"),
"global_default":("#eae6d9","#c19b5e","#668f5b")
}
def rgb(s):return tuple(bytes.fromhex(s.strip("#")))
def lerp(a,b,k):return tuple(round(x*(1-k)+y*k) for x,y in zip(a,b))
def cover(folder,id,title,meal,path):
 r=random.Random(int(hashlib.sha256(id.encode()).hexdigest()[:16],16))
 bg,grain,green=map(rgb,PALETTES[folder])
 im=Image.new("RGB",(320,320),bg)
 d=ImageDraw.Draw(im)
 # Subtle tabletop grain, shaded radial ceramic plate and rim.
 for i in range(36):
  x=r.randrange(320);y=r.randrange(320); l=r.randrange(5,55)
  c=lerp(bg,(255,255,255),r.uniform(.03,.13))
  d.line((x,y,x+l,y),fill=c,width=1)
 d.ellipse((15,21,307,313),fill=lerp(bg,(64,66,60),.20))
 d.ellipse((17,15,303,301),fill=(246,244,232))
 d.ellipse((29,27,291,289),fill=(226,221,203))
 d.ellipse((37,35,283,281),fill=(250,247,230))
 # Main dish: soup, porridge, flatbread or composed plate.
 low=title.lower()
 soup=meal=="hy" or any(k in low for k in ("soup","broth","guk","dashi","jhol","canja","caldo","rasam"))
 porridge=any(k in low for k in ("porridge","juk","okay","oat","mingau","khich","zosui","upma","poha","rice"))
 pancake=any(k in low for k in ("chilla","pancake","toast","roti","tapioca","dhokla","idli","onigiri"))
 if soup:
  d.ellipse((45,44,276,276),fill=(103,90,65))
  d.ellipse((53,52,268,268),fill=lerp(grain,(255,240,177),.43))
  for _ in range(48):
   x=r.randrange(75,250);y=r.randrange(80,249)
   if (x-160)**2+(y-160)**2>88**2:continue
   c=r.choice([green,(230,115,67),(245,202,95),(245,229,178)])
   d.ellipse((x,y,x+r.randrange(7,17),y+r.randrange(6,16)),fill=c)
 elif pancake:
  for j in range(4):
   cx=157+r.randrange(-24,25);cy=155+r.randrange(-24,25)
   d.ellipse((cx-88,cy-55+j*9,cx+81,cy+50+j*9),fill=lerp(grain,(255,206,98),r.uniform(.2,.6)),outline=(167,116,60),width=2)
  for _ in range(24):
   x=r.randrange(80,240);y=r.randrange(86,233)
   d.ellipse((x,y,x+5,y+4),fill=r.choice([green,(99,113,52),(175,90,48)]))
 elif porridge:
  d.ellipse((48,47,274,277),fill=(237,231,197),outline=(190,176,132),width=4)
  for _ in range(110):
   x=r.randrange(68,262);y=r.randrange(67,260)
   if (x-161)**2+(y-160)**2>95**2:continue
   c=r.choice([grain,lerp(grain,(255,242,188),.45),(236,177,91),green])
   d.ellipse((x,y,x+r.randrange(4,12),y+r.randrange(3,9)),fill=c)
 else:
  for _ in range(105):
   x=r.randrange(56,252);y=r.randrange(61,258)
   if (x-160)**2+(y-157)**2>99**2:continue
   c=r.choice([grain,green,(229,151,77),(237,218,146),(176,111,75),(111,135,78)])
   w=r.randrange(8,27);h=r.randrange(6,20)
   d.rounded_rectangle((x,y,x+w,y+h),radius=4,fill=c)
 # Visible garnishes: herb leaves, sesame and highlight.
 for _ in range(13):
  x=r.randrange(93,234);y=r.randrange(96,222)
  d.ellipse((x-4,y-7,x+7,y+3),fill=lerp(green,(35,90,43),r.random()*.5))
 for _ in range(14):
  x=r.randrange(80,245);y=r.randrange(90,244)
  d.ellipse((x,y,x+2,y+2),fill=(252,244,210))
 # Exact ID and recipe title visibly associate the illustration with its JSON.
 d.rounded_rectangle((10,220,310,312),radius=12,fill=(251,250,245))
 fontpath="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
 small=ImageFont.truetype(fontpath,12)
 big=ImageFont.truetype(fontpath,15)
 d.text((20,228),id,fill=(33,91,57),font=small)
 for n,line in enumerate(textwrap.wrap(title,31,break_long_words=False)[:2]):
  d.text((20,247+n*20),line,fill=(38,41,36),font=big)
 path.parent.mkdir(parents=True,exist_ok=True)
 for quality in (76,66,56,46,36):
  im.save(path,"WEBP",quality=quality,method=6)
  if path.stat().st_size<=100000:break
 if path.stat().st_size>100000:raise RuntimeError(f"oversize: {path}")
 with Image.open(path) as check:
  if check.format!="WEBP" or check.size!=(320,320):raise RuntimeError(f"bad image: {path}")
 return path.stat().st_size

def main():
 total=0;count=0
 for folder in FOLDERS:
  base=BASE/folder
  indexpath=base/"index.json"
  index=json.loads(indexpath.read_text(encoding="utf-8"))
  budget=0
  assets={}
  for id in index["recipeIds"]:
   recipepath=base/"recipes"/id/"recipe.json"
   recipe=json.loads(recipepath.read_text(encoding="utf-8"))
   img=recipepath.parent/recipe["coverImage"]
   if recipe["id"]!=id or img.parent.name!=id: raise RuntimeError("foodId mismatch: "+id)
   size=cover(folder,id,recipe["title"],id.split("_")[2],img)
   assets[id]={"foodId":id,"title":recipe["title"],"recipe":"recipes/"+id+"/recipe.json","image":"recipes/"+id+"/cover.webp","bytes":size,"sha256":hashlib.sha256(img.read_bytes()).hexdigest(),"kind":"labeled_illustration"}
   budget+=size
   count+=1
  if budget>20000000:raise RuntimeError(f"{folder} exceeds 20 MB: {budget}")
  (base/"assets.json").write_text(json.dumps({"locale":folder,"imageType":"labeled_illustration","assets":assets},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
  index["coverReady"]=True
  indexpath.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(f"{folder}: 120 covers, {budget} bytes")
  total+=budget
 manifestpath=BASE/"manifest.json"
 manifest=json.loads(manifestpath.read_text(encoding="utf-8"))
 manifest["imageStatus"]="ready_illustrated"
 manifestpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(f"Generated {count} WebP covers, {total} bytes in total")

if __name__=="__main__":main()
