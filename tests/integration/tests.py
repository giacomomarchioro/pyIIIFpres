from IIIFpres.iiifpapi3 import Manifest
import unittest
import json
import os
from os.path import dirname 
import runpy

prj_dir = dirname(dirname(os.getcwd()))

class TestWithReferenceManifest(unittest.TestCase):
    
    def test_0002_mvm_audio(self):
        """
        Test 0002-mvm-audio
        """ 
        example = runpy.run_path(os.path.join(prj_dir,'examples','0002-mvm-audio.py'))
        with open(os.path.join('fixtures','0002-mvm-audio.json')) as f: 
            ref = json.load(f) 
        json_manifest = json.loads(example['manifest'].json_dumps(sort_keys=True))
        self.assertEqual(ref,json_manifest)
    
    def test_0003_mvm_video(self):
        """
        Test 0003-mvm-video
        """ 
        example = runpy.run_path(os.path.join(prj_dir,'examples','0003-mvm-video.py'))
        with open(os.path.join('fixtures','0003-mvm-video.json')) as f: 
            ref = dict(json.load(f))
        json_manifest = dict(json.loads(example['manifest'].json_dumps()))
        self.assertEqual(ref,json_manifest)
    
    def test_0004_canvas_size(self):
        """
        Test 0004-canvas-size
        """ 
        example = runpy.run_path(os.path.join(prj_dir,'examples','0004-canvas-size.py'))
        with open(os.path.join('fixtures','0004-canvas-size.json')) as f: 
            ref = dict(json.load(f))
        json_manifest = dict(json.loads(example['manifest'].json_dumps()))
        self.assertEqual(ref,json_manifest)

    def test_0006_text_language(self):
        """
        Test 0006-text-language
        """ 
        example = runpy.run_path(os.path.join(prj_dir,'examples','0006-text-language.py'))
        with open(os.path.join('fixtures','0006-text-language.json')) as f: 
            ref = json.load(f).dumps(sort_keys=True) 
        json_manifest = example['manifest'].json_dumps(sort_keys=True)
        self.assertEqual(ref,json_manifest)
    
    def test_0007_text_language(self):
        """
        Test 0007-string-formats
        """ 
        example = runpy.run_path(os.path.join(prj_dir,'examples','0007-string-formats.py'))
        with open(os.path.join('fixtures','0007-string-formats.json')) as f: 
            ref = dict(json.load(f)) 
        json_manifest = dict(json.loads(example['manifest'].json_dumps()))
        self.assertEqual(ref,json_manifest)

    def test_dictinary(self):
        """
        Test 0007-string-formats
        """ 
        ref = {
            "a": "b",
            "c": "d"
        }
        json_manifest = {
            "c": "d",
            "a": "b"
        }
        self.assertEqual(ref,json_manifest)


if __name__ == '__main__':
    unittest.main()