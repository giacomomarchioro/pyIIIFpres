from .iiifpapi3 import CoreAttributes, Manifest
from .iiifpapi3 import check_valid_URI,unused
from .iiifpapi3 import Recommended,Required
from .iiifpapi3 import BASE_URL,LANGUAGES,MEDIATYPES
from .iiifpapi3 import config

#from shapely.geometry import mapping, shape

class Feature(object):
    def __init__(self):
        self.id = Required()
        self.type  = "Feature"
        self.geometry = Recommended()
        self.properties = Recommended()
        
    def set_id(self, objid=None, extendbase_url=None):
        """Set the ID of the object 
        Args:
            objid (str, optional): A string corresponding to the ID of the object.
            Defaults to None.
            extendbase_url (str or list, optional): A string or a list of strings
            to be joined with the iiifpapi3.BASE_URL . Defaults to None.
        """

        if extendbase_url:
            if objid:
                raise ValueError(
                    "Set id using extendbase_url or objid not both.")
            
            if isinstance(extendbase_url, str):
                joined = "".join((BASE_URL, extendbase_url))
                assert check_valid_URI(joined),"Special characters must be encoded"
                self.id = joined
            if isinstance(extendbase_url, list):
                extendbase_url.insert(0, BASE_URL)
                joined = "".join(extendbase_url)
                assert check_valid_URI(joined),"Special characters must be encoded"
                self.id = joined

        elif objid is None:
            self.id = config.base_url
        else:
            assert objid.startswith("http"), "ID must start with http or https"
            if self.type == 'Canvas':
                assert "#" not in (objid), "URI of the canvas must not contain a fragment: \#"
            assert check_valid_URI(objid),"Special characters must be encoded"
            self.id = objid

    def set_label(self, language, text):
        """Add a label to the object

        Args:
            language (str): The language of the label.
            text (str): The content of the label.

        IIIF : A human readable label, name or title. The label property is 
        intended to be displayed as a short, textual surrogate for the resource
        if a human needs to make a distinction between it and similar resources,
        for example between objects, pages, or options for a choice of images 
        to display. The label property can be fully internationalized, and each
        language can have multiple values.
        """

        if unused(self.properties):
            self.properties = {}
        if language is None:
            language = "none"
        assert language in LANGUAGES or language == "none","Language must be a valid BCP47 language tag or none"
        self.properties['label'] = {language : [text]}
    
    def set_summary(self, language, text):
        """
        An ordered list of descriptions to be displayed to the user when they
        interact with the resource, given as pairs of human readable label and
        value entries. The content of these entries is intended for
        presentation only; descriptive semantics should not be inferred. An
        entry might be used to convey information about the creation of the
        object, a physical description, ownership information, or other
        purposes.
        """
        if unused(self.properties):
            self.summary = {}
        assert language in LANGUAGES or language == "none","Language must be a valid BCP47 language tag or none"
        self.properties['summary'] = {language : [text]}

    def set_geometry_as_point(self,longitude, latitude):
        """Set geometry attribute as point providing the longitude and the latitude

        Args:
            longitude (float): longitude of the location.
            latitude (float): latitude of the location.
        """
        self.geometry = {
              "type": "Point",
              "coordinates": [
                longitude,
                latitude
              ]
            }



class navPlace(object):
    def __init__(self):
        self.type  = "FeatureCollection"
        self.features = Required("A NavPlace must have a list one feature")

    def add_feature(self,feature=None):
        if unused(self.features):
            self.features = []
        if feature is None:
            feature = Feature()
        self.features.append(feature)
        return feature
