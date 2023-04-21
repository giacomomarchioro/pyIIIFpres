from IIIFpres import iiifpapi3
import geojson

iiifpapi3.BASE_URL = (
    r"https://iiif.io/api/cookbook/recipe/0139-geolocate-canvas-fragment/"
)

manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en", "Recipe Manifest for #139")
manifest.add_summary(
    "en",
    "A IIIF Presentation API 3.0 Manifest containing a GeoJSON-LD Web Annotation which targets a Canvas fragment.",
)
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas.json")
canvas.add_label("en", "Chesapeake and Ohio Canal Pamphlet")
canvas.set_height(7072)
canvas.set_width(5212)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url="contentPage.json")
annotation = annopage.add_annotation_to_items(target=canvas.id)
annotation.set_motivation("painting")
annotation.add_label("en","Pamphlet Cover")
annotation.set_id(extendbase_url="content.json")
annotation.body.set_id(
    "https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-88695674/full/max/0/default.jpg"
)
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
annotation.body.set_height(7072)
annotation.body.set_width(5212)
srv = annotation.body.add_service()
srv.set_id(
    "https://iiif.io/api/image/3.0/example/reference/43153e2ec7531f14dd1c9b2fc401678a-88695674"
)
srv.set_profile("level1")
srv.set_type("ImageService3")
canvasannopage = canvas.add_annotationpage_to_annotations()
canvasannopage.set_id(extendbase_url="supplementingPage.json")
annotation2 = canvasannopage.add_annotation_to_items(
    target=canvas.id + "#xywh=920,3600,1510,3000"
)
annotation2.set_motivation("tagging")
annotation2.add_label(
    "en",
    "Annotation containing GeoJSON-LD coordinates that place the map depiction onto a Leaflet web map.",
)
annotation2.set_id(extendbase_url="geoAnno.json")
# For creating the body we use geojson package
pol = geojson.Polygon(
    [
    [
        [-77.097847, 38.901359],
        [-77.02694, 38.901359],
        [-77.02694, 39.03404],
        [-77.097847, 39.03404],
    ]
    ]
)
properties = {"label": {"en": ["Targeted Map from Chesapeake and Ohio Canal Pamphlet"]}}
geojsonbody = geojson.Feature(geometry=pol, properties=properties)
geojsonbody.id = iiifpapi3.BASE_URL + "geo.json"
annotation2.body = geojsonbody
contexts = [
    "http://iiif.io/api/presentation/3/context.json",
    "http://geojson.org/geojson-ld/geojson-context.jsonld",
]
if __name__ == "__main__":
    manifest.json_save("0139-geolocate-canvas-fragment.json", context=contexts)

