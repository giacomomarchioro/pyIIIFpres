from IIIFpres import iiifpapi3
import urllib.parse
iiifpapi3.BASE_URL = "https://example.org/iiif/book1/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Special characters in URL")
manifest.add_behavior("paged")

data = (("Colon in URL",2060,1553,"https://www.nb.no/services/image/resolver/URN%3ANBN%3Ano-nb_digibok_2009070210001_0618/info.json","/full/max/0/default.jpg"),
        ("Exclamation mark in URL",3186,4612,"https://iiif.library.ethz.ch/iiif/2/e-periodica!zui!1938_014!zui-001_1938_014_0634.jpg/info.json","/full/max/0/default.jpg"),)

for idx,d in enumerate(data):
    idx+=1 
    canvas = iiifpapi3.Canvas()
    canvas.set_id(extendbase_url="canvas/p%s"%idx) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("en",d[0])
    annopage = iiifpapi3.AnnotationPage()
    annopage.set_id(extendbase_url="page/p%s/1" %idx)
    annotation = iiifpapi3.Annotation(target=canvas.id)
    annotation.set_id(extendbase_url="annotation/p%s-image"%str(idx).zfill(4))
    annotation.set_motivation("painting")
    url = "".join(urllib.parse.quote(str(d[3]),safe='/')).replace('%3A', ':', 1)
    annotation.body.set_id("".join(url))
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jpeg")
    annotation.body.set_width(d[1])
    annotation.body.set_height(d[2])
    s = iiifpapi3.service()
    s.set_id(url)
    s.set_type("ImageService3")
    s.set_profile("level1")
    annotation.body.add_service(s)
    annopage.add_item(annotation)
    canvas.add_item(annopage)
    manifest.add_item(canvas)

manifest.json_save("manifest.json")