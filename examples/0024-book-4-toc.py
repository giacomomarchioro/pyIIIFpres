# https://iiif.io/api/cookbook/recipe/0024-book-4-toc
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0024-book-4-toc"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Ethiopic Ms 10")

data = [('f. 1r',
  1768,
  2504,
  'https://iiif.io/api/image/3.0/example/reference/d3bbf5397c6df6b894c5991195c912ab-1-21198-zz001d8m41_774608_master',
  '/full/max/0/default.jpg'),
 ('f. 1v',
  1792,
  2512,
  'https://iiif.io/api/image/3.0/example/reference/d3bbf5397c6df6b894c5991195c912ab-2-21198-zz001d8m5j_774612_master',
  '/full/max/0/default.jpg'),
 ('f. 2r',
  1792,
  2456,
  'https://iiif.io/api/image/3.0/example/reference/d3bbf5397c6df6b894c5991195c912ab-3-21198-zz001d8tm5_775004_master',
  '/full/max/0/default.jpg'),
 ('f. 2v',
  1760,
  2440,
  'https://iiif.io/api/image/3.0/example/reference/d3bbf5397c6df6b894c5991195c912ab-4-21198-zz001d8tnp_775007_master',
  '/full/max/0/default.jpg'),
 ('f. 3r',
  1776,
  2416,
  'https://iiif.io/api/image/3.0/example/reference/d3bbf5397c6df6b894c5991195c912ab-5-21198-zz001d8v6f_775077_master',
  '/full/max/0/default.jpg'),
 ('f. 3v',
  1776,
  2416,
  'https://iiif.io/api/image/3.0/example/reference/d3bbf5397c6df6b894c5991195c912ab-6-21198-zz001d8v7z_775085_master',
  '/full/max/0/default.jpg')]

for idx,d in enumerate(data):
    idx+=1 
    canvas = manifest.add_canvas_to_items()
    canvas.set_id(extendbase_url="canvas/p%s"%idx) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("en",d[0])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url="page/p%s/1"%idx)
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url="annotation/p%s-image"%str(idx).zfill(4))
    annotation.set_motivation("painting")
    annotation.body.set_id("".join(d[3:]))
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jpeg")
    annotation.body.set_width(d[1])
    annotation.body.set_height(d[2])
    s = annotation.body.add_service()
    s.set_id(d[3])
    s.set_type("ImageService3")
    s.set_profile("level1")

rng = manifest.add_range_to_structures()
rng.set_id(extendbase_url="range/r0")
rng.add_label('en',"Table of Contents")
r1  = rng.add_range_to_items()
r1.set_id(extendbase_url="range/r1")
r1.add_label('gez',"Tabiba Tabiban [ጠቢበ ጠቢባን]")
r1.add_canvas_to_items(manifest.items[0].id)
r1.add_canvas_to_items(manifest.items[1].id)
r2 = rng.add_range_to_items()
r2.set_id(extendbase_url="range/r2")
r2.add_label('gez',"Arede'et [አርድዕት]")
r2_1 = r2.add_range_to_items()
r2_1.add_label('en','Monday')
r2_1.set_id(extendbase_url="range/r2/1")
r2_1.add_canvas_to_items(manifest.items[2].id)
r2_1.add_canvas_to_items(manifest.items[3].id)
r2_2 = r2.add_range_to_items()
r2_2.set_id(extendbase_url="range/r2/2")
r2_2.add_label('en','Tuesday')
r2_2.add_canvas_to_items(manifest.items[4].id)
r2_2.add_canvas_to_items(manifest.items[5].id)

if __name__ == "__main__":
    manifest.json_save("manifest.json")