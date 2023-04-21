"""
The module maps the IIIF presentation API structure
(https://iiif.io/api/presentation/3.0/) to Python classes.
The user set_ objects that can have only one value (e.g. id) and add_ objects
that can have multiple entities (e.g. labels). As an example, we will execute
part of the Simple Manifest - Book recipe from the IIIF cookbook.


from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","Simple Manifest - Book")
manifest.add_behavior("paged")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas/p%s"%idx) # in this case we use the base url
...
manifest.json_save("manifest.json")

"""
__version__ = "4.0.1"
from .BCP47_tags import BCP47lang