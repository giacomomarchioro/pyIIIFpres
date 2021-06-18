# https://iiif.io/api/cookbook/recipe/0002-mvm-audio/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0002-mvm-audio"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Simplest Audio Example 1")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url=["canvas"])
# this should be fixed using a set
canvas.set_duration(1985.024)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["canvas","page"])
annotation = annopage.add_annotation_to_items(target=annopage.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["canvas","page","annotation"])
annotation.body.set_id("https://fixtures.iiif.io/audio/indiana/mahler-symphony-3/CD1/medium/128Kbps.mp4")
annotation.body.set_format("audio/mp4")
annotation.body.set_type("Sound")
annotation.body.set_duration(1985.024)
if __name__ == "__main__":
    manifest.json_save("0002-mvm-audio_manifest.json")