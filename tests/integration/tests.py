# -*- coding: UTF-8 -*-.
from IIIFpres.iiifpapi3 import Manifest
import unittest
import json
import os
from os.path import dirname 
import runpy
#unittest.util._MAX_LENGTH=2000
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
    Return the dictionary of the reference example and the one produced by the script.
    Use the name of the example without extension.
    """
    with open(os.path.join(fixture_dir,'%s.json' %examplename)) as f: 
        ref = json.load(f) 
    example = runpy.run_path(os.path.join(prj_dir,'examples','%s.py'%examplename))
    json_manifest = json.loads(example['manifest'].json_dumps())
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



if __name__ == '__main__':
    unittest.main()