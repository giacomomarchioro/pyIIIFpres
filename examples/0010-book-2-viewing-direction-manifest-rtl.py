# https://iiif.io/api/cookbook/recipe/0010-book-2-viewing-direction
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0010-book-2-viewing-direction"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest-rtl.json")
manifest.add_label("en","Book with Right-to-Left Viewing Direction")
manifest.add_summary(language='en',text="Playbill for \"Akiba gongen kaisen-banashi,\" \"Futatsu chōchō kuruwa nikki\" and \"Godairiki koi no fūjime\" performed at the Chikugo Theater in Osaka from the fifth month of Kaei 2 (May, 1849); main actors: Gadō Kataoka II, Ebizō Ichikawa VI, Kitō Sawamura II, Daigorō Mimasu IV and Karoku Nakamura I; on front cover: producer Mominosuke Ichikawa's crest.")
manifest.set_viewingDirection("right-to-left")

data = [('front cover',
  3497,
  4823,
  'https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_001',
  '/full/max/0/default.jpg'),
 ('pages 1–2',
  6062,
  4804,
  'https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_002',
  '/full/max/0/default.jpg'),
 ('pages 3–4',
  6127,
  4776,
  'https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_003',
  '/full/max/0/default.jpg'),
 ('pages 5–6',
  6124,
  4751,
  'https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_004',
  '/full/max/0/default.jpg'),
 ('back cover',
  3510,
  4808,
  'https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_005',
  '/full/max/0/default.jpg')]
  
for idx,d in enumerate(data):
    idx+=1 
    canvas = manifest.add_canvas_to_items()
    canvas.set_id(extendbase_url=["canvas","p%s"%idx]) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("en",d[0])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url=["page","p%s"%idx,"1"])
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url=["annotation","p%s-image"%str(idx).zfill(4)])
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
if __name__ == "__main__":
    manifest.json_save("0010-book-2-viewing-direction_manifest.json")