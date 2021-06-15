import unittest
import json
from IIIFpres import iiifpapi3


class TestManifest(unittest.TestCase):
    @classmethod
    def setUp(self):
        iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0004-canvas-size"
        self.manifest = iiifpapi3.Manifest()
        self.manifest.set_id(extendbase_url="manifest.json")
        canvas = self.manifest.add_canvastoitems()
        canvas.set_id(extendbase_url=["canvas","p1"])
        canvas.set_height(1800)
        canvas.set_width(1200)
        annopage = canvas.add_annotationpage_to_items()
        annopage.set_id(extendbase_url=["page","p1","1"])
        annotation = annopage.add_annotation_toitems(target=canvas.id) 
        annotation.set_motivation("painting")
        annotation.set_id(extendbase_url=["annotation","p0001-image"])
        annotation.body.set_height(1800)
        annotation.body.set_width(1200)
        annotation.body.set_id("http://iiif.io/api/presentation/2.1/example/fixtures/resources/page1-full.png")
        annotation.body.set_format("image/png")
        annotation.body.set_type("Image")
    
    def test_unicodeiswrittentojson(self):
        """
        Test unicode is written correctly.
        """ 
        unicodestring = "Picture of Göttingen "
        self.manifest.add_label("en",unicodestring)
        reloaded = json.loads(self.manifest.json_dumps())
        self.assertEqual(reloaded['label']['en'][0] ,unicodestring)

    def test_rightsassertion(self):
        """ 
        Test if rights throwassertion throw right assertion
        """
        with self.assertRaises(AssertionError):
            self.manifest.set_rights("creativecommons.org/licenses/by-sa/3.0/")

if __name__ == '__main__':
    unittest.main()