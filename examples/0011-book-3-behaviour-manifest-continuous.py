# https://iiif.io/api/cookbook/recipe/0009-book-1/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0011-book-3-behavior/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest-continuous.json")
manifest.add_label("gez","Ms. 21 Māzemurā Dāwit, Asmat [መዝሙረ ዳዊት]")
manifest.add_behavior("continuous")

data = (("Section 1 [Recto]",11368,1592,"https://iiif.io/api/image/3.0/example/reference/8c169124171e6b2253b698a22a938f07-21198-zz001hbmd9_1300412_master","/full/max/0/default.jpg"),
        ("Section 2 [Recto]",11608,1536,"https://iiif.io/api/image/3.0/example/reference/8c169124171e6b2253b698a22a938f07-21198-zz001hbmft_1300418_master","/full/max/0/default.jpg"),
        ("Section 3 [Recto]",10576,1504,"https://iiif.io/api/image/3.0/example/reference/8c169124171e6b2253b698a22a938f07-21198-zz001hbmgb_1300426_master","/full/max/0/default.jpg"),
        ("Section 4 [Recto]",2488,1464,"https://iiif.io/api/image/3.0/example/reference/8c169124171e6b2253b698a22a938f07-21198-zz001hbmhv_1300436_master","/full/max/0/default.jpg"),
)

for idx,d in enumerate(data):
    idx+=1 
    canvas = manifest.add_canvas_to_items()
    canvas.set_id(extendbase_url="canvas/s%s"%idx) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("en",d[0])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url="page/s%s/1"%idx)
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url="annotation/s%s-image"%str(idx).zfill(4))
    annotation.set_motivation("painting")
    annotation.body.set_id("".join(d[3:]))
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jpeg")
    annotation.body.set_width(d[1])
    annotation.body.set_height(d[2])
    s = annotation.body.add_service()
    s.set_id(d[3])
    s.set_type("ImageService3")
    s.set_profile("level1")

if __name__ == "__main__":
    manifest.json_save("manifest.json")