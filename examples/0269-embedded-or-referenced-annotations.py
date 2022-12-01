# implementation of Image and Canvas with Differing Dimensions https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/" 
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Picture of Göttingen taken during the 2019 IIIF Conference")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas-1")
canvas.set_height(3024)
canvas.set_width(4032)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url="canvas-1/annopage-1")
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url="canvas-1/annopage-1/anno-1")
annotation.body.set_id("https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen/full/max/0/default.jpg")
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
annotation.body.set_height(3024)
annotation.body.set_width(4032)
srv = annotation.body.add_service()
srv.set_id("https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen")
srv.set_profile("level1")
srv.set_type("ImageService3")
# Add annotationpage to annotations of the canvas
cnvannop = canvas.add_annotationpage_to_annotations()
cnvannop.set_id("https://iiif.io/api/cookbook/recipe/0269-embedded-or-referenced-annotations/annotationpage.json")

if __name__ == "__main__":
    manifest.json_save("0266-full-canvas-annotation.json")