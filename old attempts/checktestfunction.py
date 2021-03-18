from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
