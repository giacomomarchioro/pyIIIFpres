# a revised version of https://iiif.io/api/presentation/3.0/#b-example-manifest-response
# it creates 2000 canvas each with annotation and subservices.
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://example.org/iiif/book1/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest")
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
manifest.add_metadata(label="Source",value="<span>From: <a href=\"https://example.org/db/1.html\">Some Collection</a></span>",language_l="en", language_v="none")
manifest.add_summary(language="en",text="Book 1, written be Anne Author, published in Paris around 1400.")
thum = manifest.add_thumbnail()
thum.set_id("https://example.org/iiif/book1/page1/full/80,100/0/default.jpg")
thum.set_type("Image")
thum.set_format("image/jpeg")
tserv = thum.add_service()
tserv.set_id("https://example.org/iiif/book1/page1")
tserv.set_type("ImageService3")
tserv.set_profile("level1")
manifest.set_viewingDirection("right-to-left")
manifest.add_behavior("paged")
manifest.set_navDate("1856-01-01T00:00:00Z")
manifest.set_rights("http://creativecommons.org/licenses/by/4.0/")
manifest.set_requiredStatement(label="Attribution",value="Provided by Example Organization",language_l="en",language_v="en")
prov = manifest.add_provider()
prov.add_label("en","Example Organization")
prov.set_id("https://example.org/about")
homp = prov.add_homepage()
homp.set_id("https://example.org/")
homp.set_type("Text")
homp.add_label("en","Example Organization Homepage")
homp.set_format("text/html")
logo = prov.add_logo()
logo.set_id("https://example.org/service/inst1/full/max/0/default.png")
#logo.set_type("Image")
logo.set_format("image/png")
serv1 = logo.add_service()
serv1.set_id("https://example.org/service/inst1")
serv1.set_type("ImageService3")
serv1.set_profile("level2")
seeAl = prov.add_seeAlso()
seeAl.set_id("https://data.example.org/about/us.jsonld")
seeAl.set_type("Dataset")
seeAl.set_format("application/ld+json")
seeAl.set_profile("https://schema.org/")
homp2 = manifest.add_homepage()
homp2.set_id("https://example.org/info/book1/")
homp2.set_type("Text")
homp2.add_label("en","Home page for Book 1")
homp2.set_format("text/html")
serv2 = manifest.add_service()
serv2.set_id("https://example.org/service/example")
serv2.set_type("ExampleExtensionService")
serv2.set_profile("https://example.org/docs/example-service.html")
sal2 = manifest.add_seeAlso()
sal2.set_id("https://example.org/library/catalog/book1.xml")
sal2.set_type("Dataset")
sal2.set_format("text/xml")
sal2.set_profile("https://example.org/profiles/bibliographic")
ren = manifest.add_rendering()
ren.set_id("https://example.org/iiif/book1.pdf")
ren.set_type("Text")
ren.add_label("en","Download as PDF")
ren.set_format("application/pdf")
po = manifest.add_partOf()
po.set_id("https://example.org/collections/books/")
po.set_type("Collection")
start = manifest.set_start()
start.set_id("https://example.org/iiif/book1/canvas/p2")
start.set_type("Canvas")
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


#        label,width,height,id,
d = ("p. 1",750,1000, "https://example.org/iiif/book1/page1","/full/max/0/default.jpg","annotation",True)

for idx in range(2000):
    idx+=1 
    canvas = manifest.add_canvas_to_items()
    canvas.set_id(extendbase_url="canvas/p%s"%idx) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("none",d[0])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url="page/p%s/1" %idx)
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url="annotation/p%s-image"%str(idx).zfill(4))
    annotation.set_motivation("painting")
    annotation.body.set_id("".join(d[3:-2]))
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jpeg")
    annotation.body.set_width(1500)
    annotation.body.set_height(2000)
    s = annotation.body.add_service()
    s.set_id(d[3])
    s.set_type("ImageService3")
    s.set_profile("level2")
    if d[6]:
        subserv =  {
                "@id": "https://example.org/iiif/auth/login",
                "@type": "AuthCookieService1"
                }
        s.add_service(subserv)
    # if has annotation
    if d[5]:
        annopage2 = canvas.add_annotationpage_to_annotations()
        annopage2.set_id("https://example.org/iiif/book1/comments/p%s/1" %idx)
    
rng = manifest.add_range_to_structures()
rng.set_id(extendbase_url="range/r0")
rng.add_label("en","Table of Contents")
rng2 = iiifpapi3.Range()
rng2.set_id(extendbase_url="range/r1")
rng2.add_label("en","Introduction")
rng2.set_supplementary("https://example.org/iiif/book1/annocoll/introTexts")
rng2.add_canvas_to_items("https://example.org/iiif/book1/canvas/p1")
sr = iiifpapi3.SpecificResource()
sr.set_source("https://example.org/iiif/book1/canvas/p2")
fs = iiifpapi3.FragmentSelector()
fs.set_xywh(0,0,750,300)
sr.set_selector(fs)
rng2.add_item(sr)
rng.add_item(rng2)
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
if __name__ == "__main__":
        manifest.orjson_dumps("manifest.json")