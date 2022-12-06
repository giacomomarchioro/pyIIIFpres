import unittest
import json
from IIIFpres import iiifpapi3
from IIIFpres.iiifpapi3 import Collection, Required,Recommended
# for print statements
import io
import unittest.mock

class TestEmptyManifest(unittest.TestCase):
    @classmethod
    def setUp(self):
        iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0004-canvas-size/"
        self.manifest = iiifpapi3.Manifest()
    
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
    
    def test_id_assertion(self):
        """ 
        Test ID should be in form.
        """
        with self.assertRaises(AssertionError):
            self.manifest.set_id("creativecommons.org/licenses/by-sa/3.0/")
        with self.assertRaises(AssertionError):
            self.manifest.set_id("//creativecommons.org/licenses/by/4.0/")
        
    def test_id_http(self):
        """ 
        http is valid URI.
        """
        url = "http://example.org/iiif/book1/canvas/p1"
        test = iiifpapi3.CoreAttributes()
        test.set_id(url)
        self.assertEqual(test.id,url)
    
    def test_id_https(self):
        """ 
        https is valid URI.
        """
        url = "https://example.org/iiif/book1/canvas/p1"
        test = iiifpapi3.CoreAttributes()
        test.set_id(url)
        self.assertEqual(test.id,url)

    def test_label(self):
        self.manifest.add_label("en","test")
        self.manifest.add_label("en",["test1","test2"])
        with self.assertRaises(AssertionError):
            # not valid because should be a list not dict
            self.manifest.add_label("en",{'a':1})
        with self.assertRaises(AssertionError):
            # not valid because can not be a list of dict
            self.manifest.add_label("en",[{12:'test'}])
        with self.assertRaises(AssertionError):
            # not valid because can not be a list of lists
            self.manifest.add_label("en",[[12]])
    
    def test_label_none(self):
        """If language set to None must be "none" in JSON.
        """
        self.manifest.add_label(None,['test3'])
        self.assertEqual(self.manifest.label['none'],['test3'])

    def test_adding_multiple_lables_not_overwrite(self):
        """If we add multiple label they should concatenate
        """
        self.manifest.add_label('it',['test1'])
        self.manifest.add_label('it','test2')
        self.assertEqual(self.manifest.label,{'it': ['test2', 'test1']})
         
    def test_raising_error_when_attribute_required(self):
        """This should rise a value error bevause ID is required and not set.
        """
        with self.assertRaises(ValueError):
            self.manifest.to_json()
    
    def test_raising_error_objid_and_extendbaseURL(self):
        """User try to set ID using both objid and extendbaseURL
        """
        with self.assertRaises(ValueError):
            self.manifest.set_id(objid=iiifpapi3.BASE_URL,extendbase_url=iiifpapi3.BASE_URL)
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdoutmanifest(self, n, expected_output, mock_stdout):
        self.manifest.set_type('Canvas')
        self.assertEqual(mock_stdout.getvalue(), expected_output)
    
    def test_only_numbers(self):
        correct = "The type property must be kept Manifest.\n"
        self.assert_stdoutmanifest("https:/test ", correct)

    def test_serialize_with_error(self):
        out =  self.manifest.to_json(dumps_errors=True) 
        e = {'Required': 'A Manifest should have the ID property with at least one item.'}
        self.assertEqual(out['id'],e)
       



class TestManifest(unittest.TestCase):
    @classmethod
    def setUp(self):
        iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0004-canvas-size/"
        self.manifest = iiifpapi3.Manifest()
        self.manifest.set_id(extendbase_url="manifest.json")
        self.canvas = self.manifest.add_canvas_to_items()
        self.canvas.set_id(extendbase_url="canvas/p1")
        self.canvas.set_height(1800)
        self.canvas.set_width(1200)
        annopage = self.canvas.add_annotationpage_to_items()
        annopage.set_id(extendbase_url="page/p1/1")
        annotation = annopage.add_annotation_to_items(target=self.canvas.id) 
        annotation.set_motivation("painting")
        annotation.set_id(extendbase_url="annotation/p0001-image")
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
    
    def test_fragment_in_ID(self):    
        with self.assertRaises(AssertionError):
            self.canvas.set_id("http://thishasafragment#xyx")


class Test_required_recommended_and_optionals(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.seeAlso = iiifpapi3.seeAlso()
        self.partOf = iiifpapi3.partOf()
        self.supplementary = iiifpapi3.supplementary()
        self.bodycommenting = iiifpapi3.bodycommenting()
        self.bodypainting = iiifpapi3.bodypainting()
        self.service = iiifpapi3.service()
        self.thumbnail = iiifpapi3.thumbnail()
        self.provider = iiifpapi3.provider()
        self.homepage = iiifpapi3.homepage()
        self.logo = iiifpapi3.logo()
        self.rendering = iiifpapi3.rendering()
        self.services = iiifpapi3.services()
        #self.languagemap = iiifpapi3.languagemap()
        self.Annotation = iiifpapi3.Annotation()
        self.AnnotationPage = iiifpapi3.AnnotationPage()
        self.Canvas = iiifpapi3.Canvas()
        self.Manifest = iiifpapi3.Manifest()
        self.Collection = iiifpapi3.Collection()
        self.Range = iiifpapi3.Range()
        self.SpecificResource = iiifpapi3.SpecificResource()
        self.start = iiifpapi3.start()
        self.ImageApiSelector = iiifpapi3.ImageApiSelector()
        self.PointSelector = iiifpapi3.PointSelector()
        self.FragmentSelector = iiifpapi3.FragmentSelector()
        self.AnnotationCollection = iiifpapi3.AnnotationCollection()

    def test_label(self):
        self.assertEqual(self.Collection.label,Required('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(self.Manifest.label,Required('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(self.Range.label,Recommended('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(self.Canvas.label,Recommended('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(self.AnnotationCollection.label,Recommended('https://iiif.io/api/presentation/3.0/#label'))
        self.assertEqual(self.AnnotationPage.label,None)
        self.assertEqual(self.Annotation.label,None)
        

    def test_metadata(self):
        self.assertEqual(self.Collection.metadata,Recommended('https://iiif.io/api/presentation/3.0/#metadata'))
        self.assertEqual(self.Manifest.metadata,Recommended('https://iiif.io/api/presentation/3.0/#metadata'))
        self.assertEqual(self.Range.metadata,None)
        self.assertEqual(self.Canvas.metadata,None)
        self.assertEqual(self.AnnotationCollection.metadata,None)
        self.assertEqual(self.AnnotationPage.metadata,None)
        self.assertEqual(self.Annotation.metadata,None)

    def test_summary(self):
        self.assertEqual(self.Collection.summary,Recommended('https://iiif.io/api/presentation/3.0/#summary'))
        self.assertEqual(self.Manifest.summary,Recommended('https://iiif.io/api/presentation/3.0/#summary'))
        self.assertEqual(self.Range.summary,None)
        self.assertEqual(self.Canvas.summary,None)
        self.assertEqual(self.AnnotationCollection.summary,None)
        self.assertEqual(self.AnnotationPage.summary,None)
        self.assertEqual(self.Annotation.summary,None)

    def test_provider(self):
        self.assertEqual(self.Collection.provider,Recommended('https://iiif.io/api/presentation/3.0/#provider'))
        self.assertEqual(self.Manifest.provider,Recommended('https://iiif.io/api/presentation/3.0/#provider'))
        self.assertEqual(self.Range.provider,None)
        self.assertEqual(self.Canvas.provider,None)
        self.assertEqual(self.AnnotationCollection.provider,None)
        self.assertEqual(self.AnnotationPage.provider,None)
        self.assertEqual(self.Annotation.provider,None)

    def test_provider_args(self):
        self.assertEqual(self.provider.id,Required())
        self.assertEqual(self.provider.type,'Agent')
        self.assertEqual(self.provider.label,Required())
        self.assertEqual(self.provider.homepage,Recommended())
        self.assertEqual(self.provider.logo,Recommended())
        self.assertEqual(self.provider.seeAlso,None)

    def test_thumbnail(self):
        self.assertEqual(self.Collection.thumbnail,Recommended('https://iiif.io/api/presentation/3.0/#thumbnail'))
        self.assertEqual(self.Manifest.thumbnail,Recommended('https://iiif.io/api/presentation/3.0/#thumbnail'))
        self.assertEqual(self.Range.thumbnail,None)
        self.assertEqual(self.Canvas.thumbnail,None)
        self.assertEqual(self.AnnotationCollection.thumbnail,None)
        self.assertEqual(self.AnnotationPage.thumbnail,None)
        self.assertEqual(self.Annotation.thumbnail,None)
    
    def test_navDate(self):
        self.assertEqual(self.Collection.navDate,None)
        self.assertEqual(self.Manifest.navDate,None)
        self.assertEqual(self.Range.navDate,None)
        self.assertEqual(self.Canvas.navDate,None)
        self.assertFalse(hasattr(self.AnnotationCollection,"navDate"))
        self.assertFalse(hasattr(self.AnnotationPage,"navDate"))
        self.assertFalse(hasattr(self.Annotation,"navDate"))
    
    def test_placeholderCanvas(self):
        self.assertEqual(self.Collection.placeholderCanvas,None)
        self.assertEqual(self.Manifest.placeholderCanvas,None)
        self.assertEqual(self.Range.placeholderCanvas,None)
        self.assertEqual(self.Canvas.placeholderCanvas,None)
        self.assertFalse(hasattr(self.AnnotationCollection,"placeholderCanvas"))
        self.assertFalse(hasattr(self.AnnotationPage,"placeholderCanvas"))
        self.assertFalse(hasattr(self.Annotation,"placeholderCanvas"))
    
    def test_accompanyingCanvas(self):
        self.assertEqual(self.Collection.accompanyingCanvas,None)
        self.assertEqual(self.Manifest.accompanyingCanvas,None)
        self.assertEqual(self.Range.accompanyingCanvas,None)
        self.assertEqual(self.Canvas.accompanyingCanvas,None)
        self.assertFalse(hasattr(self.AnnotationCollection,"accompanyingCanvas"))
        self.assertFalse(hasattr(self.AnnotationPage,"accompanyingCanvas"))
        self.assertFalse(hasattr(self.Annotation,"accompanyingCanvas"))
    
    def test_type(self):
        self.assertEqual(self.Collection.type,'Collection')
        self.assertEqual(self.Manifest.type,'Manifest')
        self.assertEqual(self.Range.type,'Range')
        self.assertEqual(self.Canvas.type,'Canvas')
        self.assertEqual(self.AnnotationCollection.type,'AnnotationCollection')
        self.assertEqual(self.AnnotationPage.type,'AnnotationPage')
        self.assertEqual(self.Annotation.type,'Annotation')
    
    def test_height(self):
        self.assertFalse(hasattr(self.Collection,"height"))
        self.assertFalse(hasattr(self.Manifest,"height"))
        self.assertFalse(hasattr(self.Range,"height"))
        self.assertEqual(self.Canvas.height,Required())
        self.assertFalse(hasattr(self.AnnotationCollection,"height"))
        self.assertFalse(hasattr(self.AnnotationPage,"height"))
        self.assertFalse(hasattr(self.Annotation,"height"))
        mycnv = iiifpapi3.Canvas()
        mycnv.set_height(223)
        self.assertEqual(mycnv.width,Required())
    
    def test_width(self):
        self.assertFalse(hasattr(self.Collection,"width"))
        self.assertFalse(hasattr(self.Manifest,"width"))
        self.assertFalse(hasattr(self.Range,"width"))
        self.assertEqual(self.Canvas.width,Required())
        self.assertFalse(hasattr(self.AnnotationCollection,"width"))
        self.assertFalse(hasattr(self.AnnotationPage,"width"))
        self.assertFalse(hasattr(self.Annotation,"width"))
        mycnv = iiifpapi3.Canvas()
        mycnv.set_width(223)
        self.assertEqual(mycnv.height,Required())

    def test_duration(self):
        self.assertFalse(hasattr(self.Collection,"duration"))
        self.assertFalse(hasattr(self.Manifest,"duration"))
        self.assertFalse(hasattr(self.Range,"duration"))
        self.assertEqual(self.Canvas.duration,None)
        self.assertFalse(hasattr(self.AnnotationCollection,"duration"))
        self.assertFalse(hasattr(self.AnnotationPage,"duration"))
        self.assertFalse(hasattr(self.Annotation,"duration"))
        mycnv = iiifpapi3.Canvas()
        mycnv.set_duration(223.5)
        self.assertEqual(mycnv.height,None)
        self.assertEqual(mycnv.width,None)
    
    def test_viewingDirection(self):
        self.assertEqual(self.Collection.viewingDirection,None)
        self.assertEqual(self.Manifest.viewingDirection,None)
        self.assertEqual(self.Range.viewingDirection,None)
        self.assertFalse(hasattr(self.Canvas,"viewingDirection"))
        self.assertFalse(hasattr(self.AnnotationCollection,"viewingDirection"))
        self.assertFalse(hasattr(self.AnnotationPage,"viewingDirection"))
        self.assertFalse(hasattr(self.Annotation,"viewingDirection"))
    
    def test_behavior(self):
        self.assertEqual(self.Collection.behavior,None)
        self.assertEqual(self.Manifest.behavior,None)
        self.assertEqual(self.Range.behavior,None)
        self.assertEqual(self.Canvas.behavior,None)
        self.assertEqual(self.AnnotationCollection.behavior,None)
        self.assertEqual(self.AnnotationPage.behavior,None)
        self.assertEqual(self.Annotation.behavior,None)
    
    def test_homepage_args(self):
        self.assertEqual(self.homepage.id,Required())
        self.assertEqual(self.homepage.type,Required())
        self.assertEqual(self.homepage.label,Required())
        self.assertEqual(self.homepage.format,Recommended())
        self.assertEqual(self.homepage.language,None)
    
    def test_logo_args(self):
        self.assertEqual(self.logo.id,Required())
        self.assertEqual(self.logo.type,'Image')
        self.assertEqual(self.logo.format,Recommended())
    
    def test_rendering_args(self):
        self.assertEqual(self.rendering.id,Required())
        self.assertEqual(self.rendering.type,Required())
        self.assertEqual(self.rendering.label,Required())
        self.assertEqual(self.rendering.format,Recommended())
    
    def test_service(self):
        # Any resource type may have the service property with at least one item.
        self.assertEqual(self.Collection.service,None)
        self.assertEqual(self.Manifest.service,None)
        self.assertEqual(self.Range.service,None)
        self.assertEqual(self.Canvas.service,None)
        self.assertEqual(self.AnnotationCollection.service,None)
        self.assertEqual(self.AnnotationPage.service,None)
        self.assertEqual(self.Annotation.service,None)

        # The value must be an array of JSON objects.
        Col = self.Collection.add_service()
        Man = self.Manifest.add_service()
        Ran = self.Range.add_service()
        Can = self.Canvas.add_service()
        Ann = self.AnnotationCollection.add_service()
        Ann = self.AnnotationPage.add_service()
        Ann = self.Annotation.add_service()
        self.assertTrue(isinstance(self.Collection.service,list))
        self.assertTrue(isinstance(self.Manifest.service,list))
        self.assertTrue(isinstance(self.Range.service,list))
        self.assertTrue(isinstance(self.Canvas.service,list))
        self.assertTrue(isinstance(self.AnnotationCollection.service,list))
        self.assertTrue(isinstance(self.AnnotationPage.service,list))
        self.assertTrue(isinstance(self.Annotation.service,list))
        inst = [Col, Man, Ran, Can, Ann, Ann, Ann,]
        #  service’s definition, but must have either the id or @id and type or
        #  @type properties. Each object should have a profile property.
        for i in inst:
            self.assertEqual(i.id,Required())
            self.assertEqual(i.type,Required())
            self.assertEqual(i.profile,Recommended())

    def test_services(self):
        self.assertEqual(self.Collection.services,None)
        self.assertEqual(self.Manifest.services,None)
        self.assertFalse(hasattr(self.Canvas,"services"))
        self.assertFalse(hasattr(self.Range,"services"))
        self.assertFalse(hasattr(self.AnnotationCollection,"services"))
        self.assertFalse(hasattr(self.AnnotationPage,"services"))
        self.assertFalse(hasattr(self.Annotation,"services"))

    def test_seeAlso(self):
        self.assertEqual(self.Collection.seeAlso,None)
        self.assertEqual(self.Manifest.seeAlso,None)
        self.assertEqual(self.Range.seeAlso,None)
        self.assertEqual(self.Canvas.seeAlso,None)
        self.assertEqual(self.AnnotationCollection.seeAlso,None)
        self.assertEqual(self.AnnotationPage.seeAlso,None)
        self.assertEqual(self.Annotation.seeAlso,None)
    
    def test_seeAlso_args(self):
        self.assertEqual(self.seeAlso.id,Required())
        self.assertEqual(self.seeAlso.type,Required())
        self.assertEqual(self.seeAlso.label,Recommended())
        self.assertEqual(self.seeAlso.format,Recommended())
        self.assertEqual(self.seeAlso.profile,Recommended())
    
    def test_partOf(self):
        self.assertEqual(self.Collection.partOf,None)
        self.assertEqual(self.Manifest.partOf,None)
        self.assertEqual(self.Range.partOf,None)
        self.assertEqual(self.Canvas.partOf,None)
        self.assertEqual(self.AnnotationCollection.partOf,None)
        self.assertEqual(self.AnnotationPage.partOf,None)
        self.assertEqual(self.Annotation.partOf,None)
    
    def test_partOf_args(self):
        self.assertEqual(self.partOf.id,Required())
        self.assertEqual(self.partOf.type,Required())
        self.assertEqual(self.partOf.label,Recommended())
    
    def test_start(self):
        self.assertEqual(self.Range.start,None)
        self.assertEqual(self.Manifest.start,None)
        self.assertFalse(hasattr(self.Canvas,"start"))
        self.assertFalse(hasattr(self.Collection,"start"))
        self.assertFalse(hasattr(self.AnnotationCollection,"start"))
        self.assertFalse(hasattr(self.AnnotationPage,"start"))
        self.assertFalse(hasattr(self.Annotation,"start"))
    
    def test_start_args(self):
        self.assertEqual(self.start.id,Required())
        self.assertEqual(self.start.type,Required())
    
    def test_supplementary(self):
        self.assertEqual(self.Range.supplementary,None)
        self.assertFalse(hasattr(self.Manifest,"supplementary"))
        self.assertFalse(hasattr(self.Canvas,"supplementary"))
        self.assertFalse(hasattr(self.Collection,"supplementary"))
        self.assertFalse(hasattr(self.AnnotationCollection,"supplementary"))
        self.assertFalse(hasattr(self.AnnotationPage,"supplementary"))
        self.assertFalse(hasattr(self.Annotation,"supplementary"))
    
    def test_supplementary_args(self):
        self.assertEqual(self.supplementary.id,Required())
        self.assertEqual(self.supplementary.type,"AnnotationCollection")
    
    def test_items(self):
        self.assertEqual(self.Collection.items,Required())
        self.assertEqual(self.Manifest.items,Required())
        self.assertEqual(self.Range.items,Required())
        self.assertEqual(self.Canvas.items,Recommended())
        self.assertFalse(hasattr(self.AnnotationCollection,"items"))
        self.assertEqual(self.AnnotationPage.items,Recommended())
        self.assertFalse(hasattr(self.Annotation,"items"))
        # Test adding

        self.assertTrue(hasattr(self.Collection,"add_collection_to_items"))
        self.assertTrue(hasattr(self.Collection,"add_manifest_to_items"))
        self.assertFalse(hasattr(self.Collection,"add_canvas_to_items"))
        self.assertFalse(hasattr(self.Collection,"add_annotationpage_to_items"))
        self.assertFalse(hasattr(self.Collection,"add_annotation_to_items"))
        self.assertFalse(hasattr(self.Collection,"add_range_to_items"))

        self.assertFalse(hasattr(self.Manifest,"add_collection_to_items"))
        self.assertFalse(hasattr(self.Manifest,"add_manifest_to_items"))
        self.assertTrue(hasattr(self.Manifest,"add_canvas_to_items"))
        self.assertFalse(hasattr(self.Manifest,"add_annotationpage_to_items"))
        self.assertFalse(hasattr(self.Manifest,"add_annotation_to_items"))
        self.assertFalse(hasattr(self.Manifest,"add_range_to_items"))

        self.assertFalse(hasattr(self.Canvas,"add_collection_to_items"))
        self.assertFalse(hasattr(self.Canvas,"add_manifest_to_items"))
        self.assertFalse(hasattr(self.Canvas,"add_canvas_to_items"))
        self.assertTrue(hasattr(self.Canvas,"add_annotationpage_to_items"))
        self.assertFalse(hasattr(self.Canvas,"add_annotation_to_items"))
        self.assertFalse(hasattr(self.Canvas,"add_range_to_items"))

        self.assertFalse(hasattr(self.AnnotationPage,"add_collection_to_items"))
        self.assertFalse(hasattr(self.AnnotationPage,"add_manifest_to_items"))
        self.assertFalse(hasattr(self.AnnotationPage,"add_canvas_to_items"))
        self.assertFalse(hasattr(self.AnnotationPage,"add_annotationpage_to_items"))
        self.assertTrue(hasattr(self.AnnotationPage,"add_annotation_to_items"))
        self.assertFalse(hasattr(self.AnnotationPage,"add_range_to_items"))

        # TODO: a Canvas or a Specific Resource where the source is a Canvas.
        self.assertFalse(hasattr(self.Range,"add_collection_to_items"))
        self.assertFalse(hasattr(self.Range,"add_manifest_to_items"))
        self.assertTrue(hasattr(self.Range,"add_canvas_to_items"))
        self.assertFalse(hasattr(self.Range,"add_annotationpage_to_items"))
        self.assertFalse(hasattr(self.Range,"add_annotation_to_items"))
        self.assertTrue(hasattr(self.Range,"add_range_to_items"))

    def test_add_to_items_return(self):
        self.assertTrue(isinstance(self.Collection.add_collection_to_items(),iiifpapi3.Collection))
        self.assertTrue(isinstance(self.Collection.add_manifest_to_items(),iiifpapi3.refManifest))
        self.assertTrue(isinstance(self.Manifest.add_canvas_to_items(),iiifpapi3.Canvas))
        self.assertTrue(isinstance(self.Canvas.add_annotationpage_to_items(),iiifpapi3.AnnotationPage))
        self.assertTrue(isinstance(self.AnnotationPage.add_annotation_to_items(),iiifpapi3.Annotation))
        # for range is just a dictionary that must have type Canvas
        self.Range.add_canvas_to_items(canvas_id="http")
        self.assertTrue(self.Range.items[0]['type'] == 'Canvas')
        self.assertTrue(isinstance(self.Range.add_range_to_items(),iiifpapi3.Range))
    
    def test_structures(self):
        self.assertEqual(self.Manifest.structures,None)
        self.assertFalse(hasattr(self.Range,"structures"))
        self.assertFalse(hasattr(self.Canvas,"structures"))
        self.assertFalse(hasattr(self.Collection,"structures"))
        self.assertFalse(hasattr(self.AnnotationCollection,"structures"))
        self.assertFalse(hasattr(self.AnnotationPage,"structures"))
        self.assertFalse(hasattr(self.Annotation,"structures"))
        self.assertTrue(hasattr(self.Manifest,"add_range_to_structures"))
        self.Range.add_canvas_to_items(canvas_id="http")
        self.assertTrue(self.Range.items[0]['type'] == 'Canvas')
        self.assertTrue(isinstance(self.Range.add_range_to_items(),iiifpapi3.Range))

    def test_annotations(self):
        self.assertEqual(self.Collection.annotations,None)
        self.assertEqual(self.Manifest.annotations,None)
        self.assertEqual(self.Range.annotations,None)
        self.assertEqual(self.Canvas.annotations,None)
        # and content resource
        self.assertFalse(hasattr(self.AnnotationCollection,"annotations"))
        self.assertFalse(hasattr(self.AnnotationPage,"annotations"))
        self.assertFalse(hasattr(self.Annotation,"annotations"))
        # TODO: The motivation of the Annotations must not be painting
    
    def test_collection(self):
        colMan = self.Collection.add_manifest_to_items()
        # check that manifest is referenced not embedded
        self.assertFalse(hasattr(colMan,"items"))
        self.Collection.add_manifest_to_items(self.Manifest)
        lastadd = self.Collection.items[-1]
        self.assertFalse(hasattr(lastadd,"items"))

    def test_manifest(self):
        # check that manifest is referenced not embedded
        self.assertEqual(self.Manifest.id,Required())
        self.assertEqual(self.Manifest.items,Required())
        self.assertEqual(self.Manifest.structures,None)
        # These will typically be comment style Annotations, and must not have 
        # painting as their motivation.
        self.assertEqual(self.Manifest.annotations,None)
        # TODO: These will typically be comment style Annotations, and must not have
        # painting as their motivation
    
    def test_canvas(self):
        # check that manifest is referenced not embedded
        self.assertEqual(self.Manifest.id,Required())
        self.assertEqual(self.Manifest.items,Required())
        self.assertEqual(self.Manifest.structures,None)
        # These will typically be comment style Annotations, and must not have 
        # painting as their motivation.
        self.assertEqual(self.Manifest.annotations,None)
        # TODO: These will typically be comment style Annotations, and must not have
        # painting as their motivation
        # TODO: Content must not be associated with space or time outside of 
        # the Canvas’s dimensions

    def test_ranges(self):
        self.assertEqual(self.Range.id,Required())
        self.assertEqual(self.Range.type,'Range')
        # TODO:Ranges that have the behavior value sequence must be directly within 
        # the structures property of the Manifest, 
        # and must not be embedded or referenced within other Ranges. 
    
    def test_annotationpage(self):
        self.assertEqual(self.AnnotationPage.id,Required())
        self.assertEqual(self.AnnotationPage.type,'AnnotationPage')
    
    def test_annotation(self):
        self.assertEqual(self.Annotation.id,Required())
        self.assertEqual(self.Annotation.type,'Annotation')
        self.assertEqual(self.Annotation.target,Required())
        # TODO: the URI of the Canvas must be repeated in the target
        with self.assertRaises(AssertionError):
            self.Annotation.set_id("www.example.com")

    # Content resource are inside body
    def test_bodypainting(self):
        self.assertEqual(self.bodypainting.id,Required())
        self.assertEqual(self.bodypainting.type,Required())
        self.assertEqual(self.bodypainting.format,Recommended())
        self.assertEqual(self.bodypainting.profile,Recommended())
        self.assertEqual(self.bodypainting.language,None)
        #self.assertEqual(self.bodypainting.height,Required()) # or may
        #self.assertEqual(self.bodypainting.width,Required()) # or may
        self.assertEqual(self.bodypainting.duration,None)
    
    def test_annotationcollection(self):
        self.assertEqual(self.AnnotationCollection.id,Required())
        self.assertEqual(self.AnnotationCollection.label,Recommended())
        self.AnnotationCollection.set_id("non http")


class Test_repr_and_print(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.Required = iiifpapi3.seeAlso()
        self.partOf = iiifpapi3.partOf()
        self.supplementary = iiifpapi3.supplementary()
        self.bodycommenting = iiifpapi3.bodycommenting()
        self.bodypainting = iiifpapi3.bodypainting()
        self.service = iiifpapi3.service()
        self.thumbnail = iiifpapi3.thumbnail()

    
    def test_recommended(self):
        t = "teststring12312=)123123'''òò"
        g = iiifpapi3.Recommended(t)
        self.assertEqual(g.__repr__(),"Recommended attribute:%s"%t)
    
    def test_required(self):
        t = "teststring12312=)123123'''òò"
        g = iiifpapi3.Required(t)
        self.assertEqual(g.__repr__(),"Required attribute:%s"%t)

    def test_check_invalid_URI(self):
        """Check that a space is detected.
        """
        self.assertFalse(iiifpapi3.check_valid_URI("https:/test "))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, n, expected_output, mock_stdout):
        iiifpapi3.check_valid_URI(n)
        self.assertEqual(mock_stdout.getvalue(), expected_output)
    
    def test_only_numbers(self):
        correct = "I found: a space here. \ntest \n    ^\n"
        self.assert_stdout("https:/test ", correct)









        

if __name__ == '__main__':
    unittest.main()