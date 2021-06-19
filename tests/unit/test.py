import unittest
import json
from IIIFpres import iiifpapi3
from IIIFpres.iiifpapi3 import Required,Recommended

a_seeAlso = iiifpapi3.seeAlso()
a_partOf = iiifpapi3.partOf()
a_supplementary = iiifpapi3.supplementary()
a_bodycommenting = iiifpapi3.bodycommenting()
a_bodypainting = iiifpapi3.bodypainting()
a_service = iiifpapi3.service()
a_thumbnail = iiifpapi3.thumbnail()
a_provider = iiifpapi3.provider()
a_homepage = iiifpapi3.homepage()
a_logo = iiifpapi3.logo()
a_rendering = iiifpapi3.rendering()
a_services = iiifpapi3.services()
#a_languagemap = iiifpapi3.languagemap()
a_Annotation = iiifpapi3.Annotation()
a_AnnotationPage = iiifpapi3.AnnotationPage()
a_Canvas = iiifpapi3.Canvas()
a_Manifest = iiifpapi3.Manifest()
a_Collection = iiifpapi3.Collection()
a_Range = iiifpapi3.Range()
a_SpecificResource = iiifpapi3.SpecificResource()
a_start = iiifpapi3.start()
a_ImageApiSelector = iiifpapi3.ImageApiSelector()
a_PointSelector = iiifpapi3.PointSelector()
a_FragmentSelector = iiifpapi3.FragmentSelector()
a_AnnotationCollection = iiifpapi3.AnnotationCollection()



class TestManifest(unittest.TestCase):
    @classmethod
    def setUp(self):
        iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0004-canvas-size"
        self.manifest = iiifpapi3.Manifest()
        self.manifest.set_id(extendbase_url="manifest.json")
        canvas = self.manifest.add_canvas_to_items()
        canvas.set_id(extendbase_url=["canvas","p1"])
        canvas.set_height(1800)
        canvas.set_width(1200)
        annopage = canvas.add_annotationpage_to_items()
        annopage.set_id(extendbase_url=["page","p1","1"])
        annotation = annopage.add_annotation_to_items(target=canvas.id) 
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

    def test_rights_assertion(self):
        """ 
        Test if rights throw assertion.
        """
        with self.assertRaises(AssertionError):
            self.manifest.set_rights("creativecommons.org/licenses/by-sa/3.0/")
        with self.assertRaises(AssertionError):
            self.manifest.set_rights("https://creativecommons.org/licenses/by/4.0/")
    
    def test_accompanyingCanvas(self):
        """ 
        Test if an accompanyingCanvas rise attribute error when try
        to set a nested accompanyingCanvas
        """
        ac = self.manifest.set_accompanyingCanvas()
        with self.assertRaises(AttributeError):
            ac.set_accompanyingCanvas()


class Test_required_recommended_and_optionals(unittest.TestCase):
    def test_label(self):
        self.assertEqual(a_Collection.label,Required('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(a_Manifest.label,Required('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(a_Range.label,Recommended('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(a_Canvas.label,Recommended('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(a_AnnotationCollection.label,Recommended('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(a_AnnotationPage.label,None)
        self.assertEqual(a_Annotation.label,None)
        

    def test_metadata(self):
        self.assertEqual(a_Collection.metadata,Recommended('https://iiif.io/api/presentation/3.0/#metadata'))
        self.assertEqual(a_Manifest.metadata,Recommended('https://iiif.io/api/presentation/3.0/#metadata'))
        self.assertEqual(a_Range.metadata,None)
        self.assertEqual(a_Canvas.metadata,None)
        self.assertEqual(a_AnnotationCollection.metadata,None)
        self.assertEqual(a_AnnotationPage.metadata,None)
        self.assertEqual(a_Annotation.metadata,None)

    def test_summary(self):
        self.assertEqual(a_Collection.summary,Recommended('https://iiif.io/api/presentation/3.0/#summary'))
        self.assertEqual(a_Manifest.summary,Recommended('https://iiif.io/api/presentation/3.0/#summary'))
        self.assertEqual(a_Range.summary,None)
        self.assertEqual(a_Canvas.summary,None)
        self.assertEqual(a_AnnotationCollection.summary,None)
        self.assertEqual(a_AnnotationPage.summary,None)
        self.assertEqual(a_Annotation.summary,None)

    def test_provider(self):
        self.assertEqual(a_Collection.provider,Recommended('https://iiif.io/api/presentation/3.0/#provider'))
        self.assertEqual(a_Manifest.provider,Recommended('https://iiif.io/api/presentation/3.0/#provider'))
        self.assertEqual(a_Range.provider,None)
        self.assertEqual(a_Canvas.provider,None)
        self.assertEqual(a_AnnotationCollection.provider,None)
        self.assertEqual(a_AnnotationPage.provider,None)
        self.assertEqual(a_Annotation.provider,None)

    def test_provider_args(self):
        self.assertEqual(a_provider.id,Required())
        self.assertEqual(a_provider.type,'Agent')
        self.assertEqual(a_provider.label,Required())
        self.assertEqual(a_provider.homepage,Recommended())
        self.assertEqual(a_provider.logo,Recommended())
        self.assertEqual(a_provider.seeAlso,None)
        

if __name__ == '__main__':
    unittest.main()