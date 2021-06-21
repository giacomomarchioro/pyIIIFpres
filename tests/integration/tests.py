# -*- coding: UTF-8 -*-.
from IIIFpres.iiifpapi3 import Manifest
from IIIFpres.utilities import read_API3_json
import unittest
import json
import os
from os.path import dirname 
import runpy
try:
    import dictdiffer
    def printdiff(dict_1,dict_2):
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

def get_files(examplename):
    """
    Return the dictionary of the reference example and the one produced 
    read it from json and writing it back.
    """
    with open(os.path.join(fixture_dir,'%s.json' %examplename)) as f: 
        ref = json.load(f) 
    example = runpy.run_path(os.path.join(prj_dir,'examples','%s.py'%examplename))
    json_manifest = json.loads(example['manifest'].json_dumps())
    return ref,json_manifest

def get_files2(examplename):
    """
    Return the dictionary of the reference example and the one produced by the script.
    Use the name of the example without extension.
    """
    example_path = os.path.join(fixture_dir,'%s.json' %examplename)
    with open(example_path) as f: 
        ref = json.load(f)
    mymanifest = read_API3_json(example_path)
    json_manifest = json.loads(mymanifest.json_dumps())
    return ref,json_manifest

class TestWithReferenceManifest(unittest.TestCase):
    
    # def test_Example_Manifest_Response(self):
    #     """
    #     Test Example_Manifest_Response https://iiif.io/api/presentation/3.0/#b-example-manifest-response
    #     """ 
    #     ref,json_manifest = get_files("Example_Manifest_Response")
    #     self.assertEqual(ordered(ref),ordered(json_manifest))


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
    
    
    def test_0117_add_image_thumbnail(self):
        """
        Test 0117-add-image-thumbnail
        """ 
        ref,json_manifest = get_files("0117-add-image-thumbnail")
        printdiff(ref,json_manifest)
        self.assertEqual(ordered(ref),ordered(json_manifest))
    
    # seems not a valid manifest https://github.com/IIIF/cookbook-recipes/issues/251
    # def test_0013_placeholderCanvas(self):
    #     """
    #     Test 0013-placeholderCanvas
    #     """ 
    #     ref,json_manifest = get_files("0013-placeholderCanvas")
    #     printdiff(ref,json_manifest)
    #     self.assertEqual(ordered(ref),ordered(json_manifest))

        

class Test_ReadAndWriteBack(unittest.TestCase):
    
    # def test_Example_Manifest_Response(self):
    #     """
    #     Test Example_Manifest_Response https://iiif.io/api/presentation/3.0/#b-example-manifest-response
    #     """ 
    #     ref,json_manifest = get_files("Example_Manifest_Response")
    #     self.assertEqual(ordered(ref),ordered(json_manifest))


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


# with open('org.json','w') as o, open('final.json','w') as f:
#     json.dump(ordered(ref),o,indent=2)
#     json.dump(ordered(json_manifest),f,indent=2)

if __name__ == '__main__':
    unittest.main()