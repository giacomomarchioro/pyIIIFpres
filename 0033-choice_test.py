# https://preview.iiif.io/cookbook/3333-choice/recipe/0033-choice/manifest.json
# experimental 
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://preview.iiif.io/cookbook/3333-choice/recipe/0033-choice/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Choice Example")
#manifest.add_behavior("paged")
for i in range(2):
    canvas = manifest.add_canvas_to_items()
    canvas.set_id(extendbase_url="canvas/p1") # in this case we use the base url
    canvas.set_height(11011)
    canvas.set_width(6810)
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url="page/p1/1")
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url="annotation/p0001-image")
    annotation.set_motivation("painting")
    choice1 = annotation.body.add_choice()
    choice1.set_id(r"http://lezioni.meneghetti.univr.it//imageapi/test_choice/0_VIS.jp2/full/full/0/default.jpg")
    choice1.set_type("Image")
    choice1.set_format("image/jpeg")
    choice1.set_width(11011)
    choice1.set_height(6810)
    choice1.add_label("en","Natural Light")
    s1 = choice1.add_service()
    s1.set_id(r"http://lezioni.meneghetti.univr.it//imageapi/test_choice/0_VIS.jp2")
    s1.set_type("ImageService3")
    s1.set_profile("level1")

    choice2 = annotation.body.add_choice()
    choice2.set_id(r"http://lezioni.meneghetti.univr.it//imageapi/test_choice/1_IR_760nm.jp2/full/full/0/default.jpg")
    choice2.set_type("Image")
    choice2.set_format("image/jpeg")
    choice2.set_width(11011)
    choice2.set_height(6810)
    choice2.add_label("en","IR 760 nm")
    s2 = choice2.add_service()
    s2.set_id(r"http://lezioni.meneghetti.univr.it//imageapi/test_choice/1_IR_760nm.jp2")
    s2.set_type("ImageService3")
    s2.set_profile("level1")


    choice3 = annotation.body.add_choice()
    choice3.set_id(r"http://lezioni.meneghetti.univr.it//imageapi/test_choice/2_IR_Apollo_downscaled.jp2/full/full/0/default.jpg")
    choice3.set_type("Image")
    choice3.set_format("image/jpeg")
    choice3.set_width(11011)
    choice3.set_height(6810)
    choice3.add_label("en","Apollo")
    s3 = choice3.add_service()
    s3.set_id(r"http://lezioni.meneghetti.univr.it//imageapi/test_choice/2_IR_Apollo_downscaled.jp2")
    s3.set_type("ImageService3")
    s3.set_profile("level1")


if __name__ == "__main__":
    manifest.json_save("0033-choice_manifest_multi.json")