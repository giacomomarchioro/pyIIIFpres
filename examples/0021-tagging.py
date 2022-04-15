# implementation of Image and Canvas with Differing Dimensions https://iiif.io/api/cookbook/recipe/0021-tagginge/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0021-tagging/" 
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Picture of Göttingen taken during the 2019 IIIF Conference")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas/p1")
canvas.set_height(3024)
canvas.set_width(4032)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url="page/p1/1")
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url="annotation/p0001-image")
annotation.body.set_id("https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen/full/max/0/default.jpg")
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
annotation.body.set_height(3024)
annotation.body.set_width(4032)
srv = annotation.body.add_service()
srv.set_id("https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen")
srv.set_profile("level1")
srv.set_type("ImageService3")
canvasannopage = canvas.add_annotationpage_to_annotations()
canvasannopage.set_id(extendbase_url="page/p2/1")
annotation2 = canvasannopage.add_annotation_to_items(target=canvas.id+"#xywh=265,661,1260,1239") 
annotation2.set_motivation("tagging")
annotation2.set_id(extendbase_url="annotation/p0002-tag")
annotation2.body.set_format("text/plain")
annotation2.body.set_type("TextualBody")
annotation2.body.set_value("Gänseliesel-Brunnen")
annotation2.body.set_language("de")
if __name__ == "__main__":
    manifest.json_save("0021-tagging_manifest.json")