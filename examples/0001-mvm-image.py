# https://iiif.io/api/cookbook/recipe/0001-mvm-image/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0001-mvm-image"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Image 1")
canvas = manifest.add_annotation_to_items()
canvas.set_id(extendbase_url=["canvas","p1"])
canvas.set_height(1800)
canvas.set_width(1200)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["page","p1","1"])
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["annotation","p0001-image"])
annotation.body.set_height(1800)
annotation.body.set_width(1200)
annotation.body.set_id("http://iiif.io/api/presentation/2.1/example/fixtures/resources/page1-full.png")
annotation.body.set_format("image/png")
annotation.body.set_type("Image")
if __name__ == "__main__":
    manifest.json_save("0001-mvm-image_manifest.json")