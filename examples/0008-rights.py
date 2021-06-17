# https://iiif.io/api/cookbook/recipe/0008-rights/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0008-rights" # do not place final /
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Picture of Göttingen taken during the 2019 IIIF Conference")
manifest.add_summary(language="en",text="<p>Picture taken by the <a href=\"https://github.com/glenrobson\">IIIF Technical Coordinator</a></p>")
manifest.set_rights("http://creativecommons.org/licenses/by-sa/3.0/")
reqst = manifest.add_requiredStatement()
reqst.add_label(label="Attribution", language="en")
reqst.add_value(value="<span>Glen Robson, IIIF Technical Coordinator. <a href=\"https://creativecommons.org/licenses/by-sa/3.0\">CC BY-SA 3.0</a> <a href=\"https://creativecommons.org/licenses/by-sa/3.0\" title\"CC BY-SA 3.0\"><img src=\"https://licensebuttons.net/l/by-sa/3.0/88x31.png\"/></a></span>", language="en")
canvas = manifest.add_canvastoitems()
canvas.set_id(extendbase_url=["canvas","p1"])
canvas.set_height(3024)
canvas.set_width(4032)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["page","p1","1"])
annotation = annopage.add_annotation_toitems(target=canvas.id) 
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
    manifest.json_save("0008-rights_manifest.json")