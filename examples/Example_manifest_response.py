from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://example.org/iiif/book1/manifest"
manifest = iiifpapi3.Manifest()
manifest.set_id()
manifest.add_label("en","Book 1")
manifest.add_metadata(label="Author",value="Anne Author",language_l="en")
# more complex entry
entry = {
        "label": { "en": [ "Published" ] },
        "value": {
        "en": [ "Paris, circa 1400" ],
        "fr": [ "Paris, environ 1400" ]
        }
        }
manifest.add_metadata(entry=entry)
manifest.add_metadata(label="Notes",value=["Text of note 1","Text of note 2"],language_l="en",language_v="en")
manifest.add_metadata(label="Source",value="<span>From: <a href=\"https://example.org/db/1.html\">Some Collection</a></span>",language_v="en")
manifest.add_summary("Book 1, written be Anne Author, published in Paris around 1400.",language="en")
manifest.add_behavior("paged")

data = (("Blank page",3204,4613,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f18","/full/max/0/default.jpg"),
        ("Frontispiece",3186,4612,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f19","/full/max/0/default.jpg"),
        ("Title page",3204,4613,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f20","/full/max/0/default.jpg"),
        ("Blank page",3174,4578,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f21","/full/max/0/default.jpg"),
        ("Bookplate",3198,4632,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f22","/full/max/0/default.jpg"),)

for idx,d in enumerate(data):
    idx+=1 
    canvas = iiifpapi3.Canvas()
    canvas.set_id(extendbase_url=["canvas","p%s"%idx]) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("en",d[0])
    annopage = iiifpapi3.AnnotationPage()
    annopage.set_id(extendbase_url=["page","p%s"%idx,"1"])
    annotation = iiifpapi3.Annotation(target=canvas.id)
    annotation.set_id(extendbase_url=["annotation","p%s-image"%str(idx).zfill(4)])
    annotation.set_motivation("painting")
    annotation.body.set_id("".join(d[3:]))
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jpeg")
    annotation.body.set_width(d[1])
    annotation.body.set_height(d[2])
    s = iiifpapi3.service()
    s.set_id(d[3])
    s.set_type("ImageService3")
    s.set_profile("level1")
    annotation.body.add_service(s)
    annopage.add_item(annotation)
    canvas.add_item(annopage)
    manifest.add_item(canvas)

manifest.json_save("manifes.json",save_errors=True)