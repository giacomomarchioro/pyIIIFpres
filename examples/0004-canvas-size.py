# implementation of Image and Canvas with Differing Dimensions https://iiif.io/api/cookbook/recipe/0004-canvas-size/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0004-canvas-size/"
# we need to add a non IANA media type
iiifpapi3.MEDIATYPES['image'].append('image/jpg')
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Still image from an opera performance at Indiana University")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas/p1")
canvas.set_height(1080)
canvas.set_width(1920)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url="page/p1/1")
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url="annotation/p0001-image")
annotation.body.set_height(360)
annotation.body.set_width(640)
annotation.body.set_id("https://fixtures.iiif.io/video/indiana/donizetti-elixir/act1-thumbnail.png")
annotation.body.set_format("image/jpg")
annotation.body.set_type("Image")
if __name__ == "__main__":
    manifest.json_save("0004-canvas-size_manifest.json")