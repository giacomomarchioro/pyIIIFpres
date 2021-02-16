from IIIFpres import iifpapi3
iifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1"
m = iifpapi3.Manifest()
m.set_id(extendbase_url="manifest.json")
m.add_label("en","Simple Manifest - Book")
m.add_behavior("paged")
m.set_viewingDirection("right-to-left")

s = iifpapi3.service()

data = (("Blank page",4613,3204,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f18","/full/max/0/default.jpg"),
        ("Frontispiece",3186,4612,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f19","/full/max/0/default.jpg"),
        ("Title page",3204,4613,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f20","/full/max/0/default.jpg"),
        ("Blank page",3174,4578,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f21","/full/max/0/default.jpg"),
        ("Blankplate",3198,4632,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f22","/full/max/0/default.jpg"),)

for idx,d in enumerate(data):
    idx+=1 
    c = iifpapi3.Canvas()
    c.set_id(extendbase_url=["canvas","p%s"%idx]) # in this case we use the base url
    c.set_height(d[1])
    c.set_width(d[2])
    c.add_label("en",d[0])
    ap = iifpapi3.AnnotationPage()
    ap.set_id(extendbase_url=["page","p%s"%idx,str(idx)])
    a = iifpapi3.Annotation(target=c.id)
    a.set_id(extendbase_url=["annotation","p%s-image"%str(idx).zfill(4)])
    a.set_motivation("painting")
    a.body.set_id("".join(d[3:]))
    a.body.set_type("Image")
    a.body.set_format("image/jpeg")
    a.body.set_width(3204)
    a.body.set_height(4613)
    a.body.profile = None # we mute the suggested warning
    s = iifpapi3.service()
    s.set_id(d[3])
    s.set_type("ImageService3")
    s.set_profile("level1")
    a.body.add_service(s)
    ap.add_item(a)
    c.add_item(ap)
    m.add_item(c)
