# https://iiif.io/api/cookbook/recipe/0003-mvm-video/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0003-mvm-video"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Video Example 3")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url=["canvas"])
canvas.set_height(360)
canvas.set_width(640)
# this should be fixed using a set
canvas.duration = 572.034
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["canvas","page"])
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["canvas","page","annotation"])
annotation.body.set_height(360)
annotation.body.set_width(480)
annotation.body.set_id("https://fixtures.iiif.io/video/indiana/lunchroom_manners/high/lunchroom_manners_1024kb.mp4")
annotation.body.set_format("video/mp4")
annotation.body.set_type("Video")
annotation.body.set_duration(572.034)
if __name__ == "__main__":
    manifest.json_save("0003-mvm-video_manifest.json")