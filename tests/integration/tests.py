# -*- coding: UTF-8 -*-.
from IIIFpres.iiifpapi3 import Canvas
from IIIFpres.utilities import read_API3_json,read_API3_json_file
from IIIFpres import utilities
import unittest
import json
import os
from os.path import dirname 
import runpy
try:
    import dictdiffer
    def printdiff(dict_1,dict_2):
        '''
        This is an utility for showing the difference line by line of two 
        dictionaries.
        '''
        for diff in list(dictdiffer.diff(dict_1, dict_2)):         
            print(diff)                                          
except ImportError:
    # pip install dictdiffer
    pass
#unittest.util._MAX_LENGTH=500000
# python -m unittest tests.py -v

prj_dir = os.getcwd()
fixture_dir = os.path.join(prj_dir,'tests','integration','fixtures')

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def get_files(examplename,resourcetype='manifest',context=None):
    """
    Return the dictionary of the reference example and the one produced 
    read it from json and writing it back.

    The object inside the example must be named as the resourcetype arg.
    """
    with open(os.path.join(fixture_dir,'%s.json' %examplename)) as f: 
        ref = json.load(f) 
    example = runpy.run_path(os.path.join(prj_dir,'examples','%s.py'%examplename))
    json_manifest = json.loads(example[resourcetype].json_dumps(context=context))
    return ref,json_manifest

def get_files2(examplename,context=None):
    """
    Return the dictionary of the reference example and the one produced by the script.
    Use the name of the example without extension.
    """
    example_path = os.path.join(fixture_dir,'%s.json' %examplename)
    with open(example_path) as f: 
        ref = json.load(f)
    mymanifest = read_API3_json(example_path)
    json_manifest = json.loads(mymanifest.json_dumps(context=context))
    return ref,json_manifest

r0001 = """
{
  "@context": "http://iiif.io/api/presentation/3/context.json",
  "id": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json",
  "type": "Manifest",
  "label": {
    "en": [
      "Image 1"
    ]
  },
  "items": [
    {
      "id": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/p1",
      "type": "Canvas",
      "height": 1800,
      "width": 1200,
      "items": [
        {
          "id": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/page/p1/1",
          "type": "AnnotationPage",
          "items": [
            {
              "id": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/annotation/p0001-image",
              "type": "Annotation",
              "motivation": "painting",
              "body": {
                "id": "http://iiif.io/api/presentation/2.1/example/fixtures/resources/page1-full.png",
                "type": "Image",
                "format": "image/png",
                "height": 1800,
                "width": 1200
              },
              "target": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/p1"
            }
          ]
        }
      ]
    }
  ]
}
"""

class TestUtilites(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.ref = json.loads(r0001)
    
    def test_read_API3_json_file(self):
        example_path = os.path.join(fixture_dir,'0001-mvm-image.json')
        json_manifest = read_API3_json_file(example_path)
        self.assertEqual(ordered(self.ref),ordered(json_manifest.to_json()))

    def test_remove_id(self):
        idr = "https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/p1"
        utilities.delete_object_byID(self.ref,idr)
        self.assertEqual(len(self.ref['items']),0)
    
    def test_remove_annoid(self):
        idr = "https://iiif.io/api/cookbook/recipe/0001-mvm-image/page/p1/1"
        utilities.delete_object_byID(self.ref,idr)
        self.assertEqual(len(self.ref['items'][0]['items']),0)

    def test_remove_and_insert(self):
        idr = "https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/p1"
        newcnv = Canvas()
        newid = "https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/new"
        newcnv.set_id(newid)
        utilities.remove_and_insert_new(self.ref,idr,newcnv)
        self.assertEqual(self.ref['items'][0].id,newid)

    def test_modify(self):
        example_path = os.path.join(fixture_dir,'0001-mvm-image.json')
        obj = utilities.modify_API3_json(example_path)
        self.assertEqual(ordered(self.ref),ordered(obj.to_json()))

    def test_remove_annoid(self):
        idr = "https://iiif.io/api/cookbook/recipe/0001-mvm-image/page/p1/1"
        example_path = os.path.join(fixture_dir,'0001-mvm-image.json')
        obj = utilities.modify_API3_json(example_path)
        utilities.delete_object_byID(obj,idr)
        # note modify transform only the first layer the rest are dicts
        # items[0].items wont' work.
        self.assertEqual(len(obj.items[0]['items'] ),0)

    def test_remove_and_insert(self):
        idr = "https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/p1"
        newcnv = Canvas()
        newid = "https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/new"
        newcnv.set_id(newid)
        example_path = os.path.join(fixture_dir,'0001-mvm-image.json')
        obj = utilities.modify_API3_json(example_path)
        utilities.remove_and_insert_new(obj,idr,newcnv)
        self.assertEqual(obj.items[0].id,newid)



class TestWithReferenceManifest(unittest.TestCase):
    
    # not a valid manifest https in rights statement
    def test_Example_manifest_response(self):
        """
        Test Example_manifest_response https://iiif.io/api/presentation/3.0/#b-example-manifest-response
        """ 
        ref,json_manifest = get_files("Example_manifest_response")
        self.assertEqual(ordered(ref),ordered(json_manifest))


    def test_0001_mvm_image(self):
        """
        Test 0001-mvm-image
        """ 
        ref,json_manifest = get_files("0001-mvm-image")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0002_mvm_audio(self):
        """
        Test 0002-mvm-audio
        """ 
        ref,json_manifest = get_files("0002-mvm-audio")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0003_mvm_video(self):
        """
        Test 0003-mvm-video
        """ 
        ref,json_manifest = get_files("0003-mvm-video")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0004_canvas_size(self):
        """
        Test 0004-canvas-size
        """ 
        ref,json_manifest = get_files("0004-canvas-size")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0005_image_service(self):
        """
        Test 0005-image-service
        """ 
        ref,json_manifest = get_files("0005-image-service")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0006_text_language(self):
        """
        Test 0006-text-language
        """ 
        ref,json_manifest = get_files("0006-text-language")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0007_text_language(self):
        """
        Test 0007-string-formats
        """ 
        ref,json_manifest = get_files("0007-string-formats")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0008_rights(self):
        """
        Test 0008-rights
        """ 
        ref,json_manifest = get_files("0008-rights")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0009_book_1(self):
        """
        Test 0009-book-1
        """ 
        ref,json_manifest = get_files("0009-book-1")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0011_book_3_behaviour_manifest_continuous(self):
        """
        Test 0011-book-3-behaviour-manifest-continuous
        """ 
        ref,json_manifest = get_files("0011-book-3-behaviour-manifest-continuous")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0011_book_3_behavior_manifest_individuals(self):
        """
        Test 0011-book-3-behavior-manifest-individuals
        """ 
        ref,json_manifest = get_files("0011-book-3-behavior-manifest-individuals")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0010_book_2_viewing_direction_manifest_rtl(self):
        """
        Test 0010-book-2-viewing-direction-manifest-rtl
        """ 
        ref,json_manifest = get_files("0010-book-2-viewing-direction-manifest-rtl")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0033_choice(self):
        """
        0033-choice
        """
        ref,json_manifest = get_files("0033-choice")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0046_rendering(self):
        """
        0046-rendering
        """
        ref,json_manifest = get_files("0046-rendering")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0117_add_image_thumbnail(self):
        """
        Test 0117-add-image-thumbnail
        """ 
        ref,json_manifest = get_files("0117-add-image-thumbnail")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    # seems not a valid manifest https://github.com/IIIF/cookbook-recipes/issues/251
    def test_0013_placeholderCanvas(self):
        """
        Test 0013-placeholderCanvas
        """ 
        ref,json_manifest = get_files("0013-placeholderCanvas")
        printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0230_navdate_navdate_map_2(self):
        """
        test_0230_navdate_navdate_map_
        """ 
        ref,json_manifest = get_files("0230-navdate-navdate_map_2-manifest")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0230_navdate_navdate_map_1(self):
        """
        test_0230_navdate_navdate_map_1
        """ 
        ref,json_manifest = get_files("0230-navdate-navdate_map_1-manifest")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0230_navdate_navdate_collection(self):
        """
        test_0230_navdate_navdate_collection
        """ 
        ref,json_manifest = get_files("0230-navdate-navdate_collection",'collection')
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0202_start_canvas(self):
        """
        test_0202-start-canvas
        """ 
        ref,json_manifest = get_files("0202-start-canvas")
        self.assertEqual(ordered(ref),ordered(json_manifest))
        
    def test_0024_book_4_toc(self):
        """
        0024-book-4-toc
        """ 
        ref,json_manifest = get_files("0024-book-4-toc")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0234_provider(self):
        """
        0234_provider
        """ 
        ref,json_manifest = get_files("0234-provider")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    
    def test_0053_seeAlso(self):
        """
        0053-seeAlso
        """ 
        ref,json_manifest = get_files("0053-seeAlso")
        #printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0065_opera_multiple_canvases(self):
        """
        0065-opera-multiple-canvases
        """ 
        ref,json_manifest = get_files("0065-opera-multiple-canvases")
        #printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0026_toc_opera(self):
        """
        0026-toc-opera
        """ 
        ref,json_manifest = get_files("0026-toc-opera")
        #printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0154_geo_extension(self):
        """
        0154-geo-extension
        """ 
        context = [
            "http://iiif.io/api/extension/navPlace-context/context.json",
            "http://iiif.io/api/presentation/3/context.json"
        ]
        ref,json_manifest = get_files("0154-geo-extension",context=context)
        printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0266_full_canvas_annotation(self):
        """
        0266-full-canvas-annotation
        """ 
        ref,json_manifest = get_files("0266-full-canvas-annotation")
        printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0021_tagging(self):
        """
        0021-tagging
        """ 
        ref,json_manifest = get_files("0021-tagging")
        printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0261_non_rectangular_commenting(self):
        """
        0261-non-rectangular-commenting
        """ 
        ref,json_manifest = get_files("0261-non-rectangular-commenting")
        printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0269_embedded_or_referenced_annotations(self):
        """
        0269-embedded-or-referenced-annotations
        """ 
        ref,json_manifest = get_files("0269-embedded-or-referenced-annotations")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    # def test_0326_annotating_image_layer(self):
    #     """
    #     0326-annotating-image-layer
    #     """ 
    #     ref,json_manifest = get_files("0326-annotating-image-layer")
    #     self.assertEqual(ordered(ref),ordered(json_manifest))
    

#
#
#       TEST READ AND WRITE BACK
# 
#          

class Test_ReadAndWriteBack(unittest.TestCase):
    
    # sees not a valid manifest, we use an edited version
    def test_Example_manifest_response(self):
         """
         Test Example_Manifest_Response https://iiif.io/api/presentation/3.0/#b-example-manifest-response
         """ 
         ref,json_manifest = get_files("Example_manifest_response")
         self.assertEqual(ordered(ref),ordered(json_manifest))


    def test_0001_mvm_image(self):
        """
        Test 0001-mvm-image
        """ 
        ref,json_manifest = get_files2("0001-mvm-image")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0002_mvm_audio(self):
        """
        Test 0002-mvm-audio
        """ 
        ref,json_manifest = get_files2("0002-mvm-audio")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0003_mvm_video(self):
        """
        Test 0003-mvm-video
        """ 
        ref,json_manifest = get_files2("0003-mvm-video")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0004_canvas_size(self):
        """
        Test 0004-canvas-size
        !!Warning seems it uses a strange media type image/jpg
        """ 
        ref,json_manifest = get_files2("0004-canvas-size")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0005_image_service(self):
        """
        Test 0005-image-service
        """ 
        ref,json_manifest = get_files2("0005-image-service")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0006_text_language(self):
        """
        Test 0006-text-language
        """ 
        ref,json_manifest = get_files2("0006-text-language")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0007_text_language(self):
        """
        Test 0007-string-formats
        """ 
        ref,json_manifest = get_files2("0007-string-formats")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0008_rights(self):
        """
        Test 0008-rights
        """ 
        ref,json_manifest = get_files2("0008-rights")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0009_book_1(self):
        """
        Test 0009-book-1
        """ 
        ref,json_manifest = get_files2("0009-book-1")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0011_book_3_behaviour_manifest_continuous(self):
        """
        Test 0011-book-3-behaviour-manifest-continuous
        """ 
        ref,json_manifest = get_files2("0011-book-3-behaviour-manifest-continuous")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0011_book_3_behavior_manifest_individuals(self):
        """
        Test 0011-book-3-behavior-manifest-individuals
        """ 
        ref,json_manifest = get_files2("0011-book-3-behavior-manifest-individuals")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0010_book_2_viewing_direction_manifest_rtl(self):
        """
        Test 0010-book-2-viewing-direction-manifest-rtl
        """ 
        ref,json_manifest = get_files2("0010-book-2-viewing-direction-manifest-rtl")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0117_add_image_thumbnail(self):
        """
        Test 0117-add-image-thumbnail
        """ 
        ref,json_manifest = get_files2("0117-add-image-thumbnail")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    
    def test_0013_placeholderCanvas(self):
        """
        Test 0013-placeholderCanvas
        """ 
        ref,json_manifest = get_files2("0013-placeholderCanvas")
        printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0230_navdate_navdate_map_2(self):
        """
        test_0230_navdate_navdate_map_
        """ 
        ref,json_manifest = get_files2("0230-navdate-navdate_map_2-manifest")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0230_navdate_navdate_map_1(self):
        """
        test_0230_navdate_navdate_map_1
        """ 
        ref,json_manifest = get_files2("0230-navdate-navdate_map_1-manifest")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0230_navdate_navdate_collection(self):
        """
        test_0230_navdate_navdate_collection
        """ 
        ref,json_manifest = get_files2("0230-navdate-navdate_collection")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0202_start_canvas(self):
        """
        test_0202-start-canvas
        """ 
        ref,json_manifest = get_files2("0202-start-canvas")
        self.assertEqual(ordered(ref),ordered(json_manifest))
        
    def test_0024_book_4_toc(self):
        """
        0024-book-4-toc
        """ 
        ref,json_manifest = get_files2("0024-book-4-toc")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0234_provider(self):
        """
        0234_provider
        """ 
        ref,json_manifest = get_files2("0234-provider")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0053_seeAlso(self):
        """
        0053-seeAlso
        """ 
        ref,json_manifest = get_files2("0053-seeAlso")
        #printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0065_opera_multiple_canvases(self):
        """
        0065-opera-multiple-canvases
        """ 
        ref,json_manifest = get_files2("0065-opera-multiple-canvases")
        #printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0026_toc_opera(self):
        """
        0026-toc-opera
        """ 
        ref,json_manifest = get_files2("0026-toc-opera")
        #printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0266_full_canvas_annotation(self):
        """
        0266-full-canvas-annotation
        """ 
        ref,json_manifest = get_files2("0266-full-canvas-annotation")
        self.assertEqual(ordered(ref),ordered(json_manifest))

    def test_0021_tagging(self):
        """
        0021-tagging
        """ 
        ref,json_manifest = get_files2("0021-tagging")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0261_non_rectangular_commenting(self):
        """
        0261-non-rectangular-commenting
        """ 
        ref,json_manifest = get_files2("0261-non-rectangular-commenting")
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    def test_0269_embedded_or_referenced_annotations(self):
        """
        0269-embedded-or-referenced-annotations
        """ 
        ref,json_manifest = get_files2("0269-embedded-or-referenced-annotations")
        self.assertEqual(ordered(ref),ordered(json_manifest))

# with open('org.json','w') as o, open('final.json','w') as f:
#     json.dump(ordered(ref),o,indent=2)
#     json.dump(ordered(json_manifest),f,indent=2)

if __name__ == '__main__':
    unittest.main()