# https://iiif.io/api/cookbook/recipe/0230-navdate/navdate-collection.json
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0230-navdate/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="navdate_map_2-manifest.json")
manifest.add_label("en","1986 Chesapeake and Ohio Canal, Washington, D.C., Maryland, West Virginia, official map and guide")
manifest.set_navDate("1986-01-01T00:00:00+00:00")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas/p1")
canvas.set_height(1765)
canvas.set_width(1286)
canvas.add_label("en","1986 Map, recto and verso, with a date of publication"   )
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url="page/p1/1")
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url="annotation/p0001-image")
annotation.body.set_height(1765)
annotation.body.set_width(1286)
annotation.body.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-87691274-1986/full/max/0/default.jpg")
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
s = annotation.body.add_service()
s.set_id("https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-87691274-1986/")
s.set_type("ImageService3")
s.set_profile("level1")
if __name__ == "__main__":
    manifest.json_save("0230-navdate-navdate-collection_manifest.json")