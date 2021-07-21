# we can use the ort of Nakatani Shuyo's language-detection library 
# (version from 03/03/2014) to Python by Michal Danilk.
# pip install langdetect
import IIIFpres
from langdetect import detect,LangDetectException
from IIIFpres import iiifpapi3


def check_languages(IIIFObj):
    
    def check(tobetested,expected):
        """Method for interfacing the language detector and checking the language.

        Args:
            tobetested (str): The text to be tested.
            expected (str): The expected language of the text, as in the IIIF file.
        """
        try:
            if detect(tobetested) != expected:
                print("❌  %s seems not to be: %s" %(tobetested,expected))
            else:
                print("✅  %s is : %s" %(tobetested,expected))
        except LangDetectException:
            print("⚠️  Could not detect language for %s but is set to: %s" %(tobetested,expected))
    
    def check_languagemap(obj):
        """Check languagemap objects.

        Args:
            obj (dict): Language map dict
        """
        if isinstance(obj,iiifpapi3.languagemap):
            obj = obj.__dict__

        for lang in obj['label']:
            for value in obj['label'][lang]:
                        check(value,lang)

        for lang in obj['value']:
            for value in obj['value'][lang]:
                check(value,lang)
        

    if hasattr(IIIFObj,"label"):
        if not iiifpapi3.unused(IIIFObj.label):
            for lang in IIIFObj.label:
                for value in IIIFObj.label[lang]:
                    check(value,lang)

    if hasattr(IIIFObj,"summary"):
        if not iiifpapi3.unused(IIIFObj.summary):
            for lang in IIIFObj.summary:
                for value in IIIFObj.summary[lang]:
                    check(value,lang)

    if hasattr(IIIFObj,"metadata"):
        if not iiifpapi3.unused(IIIFObj.metadata):
            for metadata in IIIFObj.metadata:
                check_languagemap(metadata)
    
    if hasattr(IIIFObj,"requiredStatement"):
        if not iiifpapi3.unused(IIIFObj.requiredStatement):
            check_languagemap(IIIFObj.requiredStatement)
    
    if hasattr(IIIFObj,"body"):
        if not iiifpapi3.unused(IIIFObj.body):
            if hasattr(IIIFObj.body,"text"):
                check(IIIFObj.body.text,IIIFObj.body.language)
    
    if hasattr(IIIFObj,"items"):
        if not iiifpapi3.unused(IIIFObj.items) and not isinstance(IIIFObj,dict):
            for item in IIIFObj.items:
                check_languages(item)
    
    if hasattr(IIIFObj,"structures"):
        if not iiifpapi3.unused(IIIFObj.structures):
            for structure in IIIFObj.structures:
                check_languages(structure)
    
    if hasattr(IIIFObj,"homepage"):
        if not iiifpapi3.unused(IIIFObj.homepage):
            for structure in IIIFObj.homepage:
                check_languages(structure)
    
    if hasattr(IIIFObj,"rendering"):
        if not iiifpapi3.unused(IIIFObj.rendering):
            for rendering in IIIFObj.rendering:
                check_languages(rendering)

    if hasattr(IIIFObj,"provider"):
        if not iiifpapi3.unused(IIIFObj.provider):
            for provider in IIIFObj.provider:
                check_languages(provider)


    
    

        