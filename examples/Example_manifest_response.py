#https://iiif.io/api/presentation/3.0/#b-example-manifest-response
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://example.org/iiif/book1/manifest"
manifest = iiifpapi3.Manifest()
manifest.set_id()
manifest.add_label("en","Book 1")
manifest.add_metadata(label="Author",value="Anne Author",language_l="en")
# more complex entry can be mapped directly to a dictionary and inserted using entry arguments
entry = {
        "label": { "en": [ "Published" ] },
        "value": {
        "en": [ "Paris, circa 1400" ],
        "fr": [ "Paris, environ 1400" ]
        }
        }
manifest.add_metadata(entry=entry)
manifest.add_metadata(label="Notes",value=["Text of note 1","Text of note 2"],language_l="en",language_v="en")
manifest.add_metadata(label="Source",value="<span>From: <a href=\"https://example.org/db/1.html\">Some Collection</a></span>",language_l="en")
manifest.add_summary("Book 1, written be Anne Author, published in Paris around 1400.",language="en")
thum = iiifpapi3.thumbnail()
thum.set_id("https://example.org/iiif/book1/page1/full/80,100/0/default.jpg")
thum.set_type("Image")
thum.set_format("Image/jpeg")
tserv = iiifpapi3.service()
tserv.set_id("https://example.org/iiif/book1/page1")
tserv.set_type("ImageService3")
tserv.set_profile("level1")
thum.add_service(tserv)
manifest.add_thumbnail(thum)
manifest.set_viewingDirection("right-to-left")
manifest.add_behavior("paged")
manifest.set_navDate("1856-01-01T00:00:00Z")
manifest.add_requiredStatement(label="Attribution",value="Provided by Example Organization",language_l="en",language_v="en")
prov = iiifpapi3.provider()
prov.add_label("en","Example Oranization")
homp = iiifpapi3.homepage()
homp.set_id()
homp.set_type("Text")
homp.set_type("Text")
homp.add_label("en","Example Organization Homepage")
homp.set_format("text/html")
logo = iiifpapi3.logo()
logo.set_id("https://example.org/service/inst1/full/max/0/default.png")
logo.set_type("Image")
logo.set_format("image/png")
serv1 = iiifpapi3.service()
serv1.set_id("https://example.org/service/inst1")
serv1.set_type("ImageService3")
serv1.set_profile("level2")
logo.add_service(serv1)
prov.add_logo(logo)
seeAl = iiifpapi3.seeAlso()
seeAl.set_id("https://data.example.org/about/us.jsonld")
seeAl.set_type("Dataset")
seeAl.set_format("application/ld+json")
seeAl.set_profile("https://schema.org/")
prov.add_seeAlso(seeAl)
homp2 =iiifpapi3.homepage()
homp2.set_id("https://example.org/info/book1/")
homp2.set_type("Text")
homp2.add_label("en","Home page for Book 1")
homp2.set_format("text/html")
manifest.add_homepage(homp2)
serv2 = iiifpapi3.service()
serv2.set_id("https://example.org/service/example")
serv2.set_type("ExampleExtensionService")
serv2.set_profile("https://example.org/docs/example-service.html")
sal2 = iiifpapi3.seeAlso()
sal2.set_id("https://example.org/library/catalog/book1.xml")
sal2.set_type("Dataset")
sal2.set_format("text/xml")
sal2.set_profile("https://example.org/profiles/bibliographic")
manifest.add_seeAlso(sal2)
ren = iiifpapi3.rendering()
ren.set_id("https://example.org/iiif/book1.pdf")
ren.set_type("Text")
ren.add_label("en","Download as PDF")
ren.set_format("application/pdf")
manifest.add_rendering(ren)
po = iiifpapi3.partOf()
po.set_id("https://example.org/collections/books/")
po.set_type("Collection")
manifest.add_partOf(po)
start = iiifpapi3.start()
start.set_id("https://example.org/iiif/book1/canvas/p2")
start.set_type("Canvas")
manifest.add_start(start)
mycomplexserv =  {
      "@id": "https://example.org/iiif/auth/login",
      "@type": "AuthCookieService1",
      "profile": "http://iiif.io/api/auth/1/login",
      "label": "Login to Example Institution",
      "service": [
        {
          "@id": "https://example.org/iiif/auth/token",
          "@type": "AuthTokenService1",
          "profile": "http://iiif.io/api/auth/1/token"          
        }
      ]
    }
manifest.add_services(mycomplexserv)



data = (("p. 1",750,1500, "https://example.org/iiif/book1/page1","/full/max/0/default.jpg","annotation"),
        ("p. 2",750,1000, "https://example.org/iiif/book1/page2","/full/max/0/default.jpg",False),
        )
for idx,d in enumerate(data):
    idx+=1 
    canvas = iiifpapi3.Canvas()
    canvas.set_id(extendbase_url=["canvas","p%s"%idx]) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label(None,d[0])
    annopage = iiifpapi3.AnnotationPage()
    annopage.set_id("https://example.org/iiif/book1/canvas/p%s" %idx)
    annotation = iiifpapi3.Annotation(target=canvas.id)
    annotation.set_id("https://example.org/iiif/book1/page/p%s/1" %idx)
    annotation.set_motivation("painting")
    annotation.body.set_id("".join(d[3:-1]))
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jpeg")
    annotation.body.set_width(1000)
    annotation.body.set_height(2000)
    s = iiifpapi3.service()
    s.set_id("https://example.org/iiif/book1/page1")
    s.set_type("ImageService3")
    s.set_profile("level2")
    subserv =  {
        "@id": "https://example.org/iiif/auth/login",
        "@type": "AuthCookieService1"
        }
    s.add_service(subserv)
    annotation.body.add_service(s)
    annopage.add_item(annotation)
    canvas.add_item(annopage)
    # if has annotation
    if d[5]:
        annopage2 = iiifpapi3.AnnotationPage()
        annopage2.set_id("https://example.org/iiif/book1/comments/p%s/1" %idx)
        canvas.add_annotation(annopage2)
    manifest.add_item(canvas)
rng = iiifpapi3.Range()
rng.add_label("en","Table of Contents")
rng2 = iiifpapi3.Range()
rng2.add_label("en","Introduction")
rng2.set_supplementary("https://example.org/iiif/book1/annocoll/introTexts")
rng2.add_canvas_to_items("https://example.org/iiif/book1/canvas/p1")
sr = iiifpapi3.SpecificResource()
sr.set_source("https://example.org/iiif/book1/canvas/p2")
fs = iiifpapi3.FragmentSelector()
fs.set_xywh(0,0,750,300)
sr.set_selector(fs)
annopage3 = iiifpapi3.AnnotationPage()
annopage3.set_id("https://example.org/iiif/book1/page/manifest/1")
anno = iiifpapi3.Annotation(manifest.id)
anno.set_id("https://example.org/iiif/book1/page/manifest/a1")
anno.set_motivation("commenting")
anno.body.set_language("en")
anno.body.set_value("I love this manifest!")
annopage3.add_item(anno)
annopage3.set_id("https://example.org/iiif/book1/page/manifest/1")        
manifest.add_annotation(annopage3)

manifest.json_save("manifes.json",save_errors=True)