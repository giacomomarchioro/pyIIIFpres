# https://iiif.io/api/cookbook/recipe/0008-rights/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0008-rights" # do not place final /
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Picture of Göttingen taken during the 2019 IIIF Conference")
manifest.add_summary("en","<p>Picture taken by the <a href=\"https://github.com/glenrobson\">IIIF Technical Coordinator</a></p>")
canvas = manifest.add_canvastoitems()
canvas.set_id(extendbase_url=["canvas","p1"])
canvas.add_label("en","Canvas with a single IIIF image")
canvas.set_height(3024)
canvas.set_width(4032)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["page","p1","1"])
annotation = annopage.add_annotation_toitems(targetid=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["annotation","p0001-image"])
annotation.body.set_id("https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen/full/max/0/default.jpg")
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
annotation.body.set_height(3024)
annotation.body.set_width(4032)
srv = annotation.body.add_service()
srv.set_id("https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen")
srv.set_profile("level1")
srv.set_type("ImageService3")
if __name__ == "__main__":
    manifest.json_save("0005-image-service_manifest.json")