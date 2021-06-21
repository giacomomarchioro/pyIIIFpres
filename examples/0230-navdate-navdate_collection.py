# https://iiif.io/api/cookbook/recipe/0230-navdate/navdate-collection.json
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0230-navdate"
manifest_1 = iiifpapi3.Manifest()
manifest_1.set_id(extendbase_url="navdate_map_1-manifest.json")
manifest_1.add_label("en","1987 Chesapeake and Ohio Canal, Washington, D.C., Maryland, West Virginia, official map and guide")
manifest_1.set_navDate("1987-01-01T00:00:00+00:00")
canvas = manifest_1.add_canvas_to_items()
canvas.set_id(extendbase_url=["canvas","p1"])
canvas.set_height(7072)
canvas.set_width(5212)
canvas.add_label("en","1987 Map, recto and verso, with a date of publication")
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["page","p1","1"])
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["annotation","p0001-image"])
annotation.body.set_height(7072)
annotation.body.set_width(5212)
annotation.body.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-88695674/full/max/0/default.jpg")
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
s = annotation.body.add_service()
s.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-88695674/")
s.set_type("ImageService3")
s.set_profile("level1")

manifest_2 = iiifpapi3.Manifest()
manifest_2.set_id(extendbase_url="navdate_map_2-manifest.json")
manifest_2.add_label("en","1986 Chesapeake and Ohio Canal, Washington, D.C., Maryland, West Virginia, official map and guide")
manifest_2.set_navDate("1986-01-01T00:00:00+00:00")
canvas = manifest_2.add_canvas_to_items()
canvas.set_id(extendbase_url=["canvas","p1"])
canvas.set_height(1765)
canvas.set_width(1286)
canvas.add_label("en","1986 Map, recto and verso, with a date of publication"   )
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["page","p1","1"])
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["annotation","p0001-image"])
annotation.body.set_height(1765)
annotation.body.set_width(1286)
annotation.body.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-87691274-1986/full/max/0/default.jpg")
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
s = annotation.body.add_service()
s.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-87691274-1986/")
s.set_type("ImageService3")
s.set_profile("level1")


collection = iiifpapi3.Collection()
collection.set_id("https://iiif.io/api/cookbook/recipe/0230-navdate/navdate-collection.json")
collection.add_label(language='en',text="Chesapeake and Ohio Canal map and guide pamphlets")
tbn = collection.add_thumbnail()
tbn.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-88695674/full/max/0/default.jpg")
tbn.set_type('Image')
tbn.set_format('image/jpeg')
tbn.set_height(300)
tbn.set_width(221)
srv = tbn.add_service()
srv.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-88695674")
srv.set_profile('level1')
srv.set_type('ImageService3')
collection.add_manifest_to_items(manifest_2)
collection.add_manifest_to_items(manifest_1)