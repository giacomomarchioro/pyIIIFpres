# implementation of Image and Canvas with Differing Dimensions https://iiif.io/api/cookbook/recipe/0118_multivalue/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://example.org/iiif/text-language/manifest" # do not place final /
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest")
manifest.add_label("fr","Arrangement en gris et noir no 1")
metaentry = manifest.add_metadata()
metaentry.add_label(language="en",label="Alternative titles")
metaentry.add_value(language="en",value=["Whistler's Mother","Arrangement in Grey and Black No. 1"])
metaentry.add_value(language="fr",value=["Portrait de la mère de l'artiste","La Mère de Whistler"])
manifest.add_summary(text="A painting in oil on canvas created by the American-born painter James McNeill Whistler, in 1871.",
                    language="en")
manifest.add_summary(text="Arrangement en gris et noir n°1, also called Portrait de la mère de l'artiste.",
                    language="fr")
canvas = manifest.add_canvastoitems()
canvas.set_id(extendbase_url=["canvas1"])
canvas.set_height(991)
canvas.set_width(1114)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["canvas1","page1"])
annotation = annopage.add_annotation_toitems(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["canvas1","page1","annotation1"])
annotation.body.set_id("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Whistlers_Mother_high_res.jpg/1114px-Whistlers_Mother_high_res.jpg")
annotation.body.set_format("image/jpg")
annotation.body.set_type("Image")
if __name__ == "__main__":
    manifest.json_save("0118_multivalue.json")