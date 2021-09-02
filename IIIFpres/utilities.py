from . import  iiifpapi3 
import json

def modify_API3_json(path):
    """Modify an IIIF json file complaint with API 3.0
    This method parse only the frist level of the IIIF object. All the nested
    object are left as dict.

    It is faster compared to read read_API3_json.

    NOTE: the method assumes the IIIF object is complaint to API 3.0.

    Args:
        path (str): The path of the json file.
    """
    with open(path) as f: 
        t = json.load(f)
    t.pop('@context')
    entitydict = {'Manifest':iiifpapi3.Manifest(),
                  'Collection':iiifpapi3.Collection()}
    assert t['type'] in entitydict.keys(),"%s not a valid IIF object"%t['type']
    newobj = entitydict[t['type']]
    #TODO: find better solution .update will cause height and width to be set R.
    newobj.__dict__ = t
    return newobj 

def read_API3_json(path):
    """Read an IIIF json file complaint with API 3.0 and map the IIIF types to classes.

    This method parse the major IIIF types and map them to the iiifpapi3 classes.
    NOTE: the method assumes the IIIF object is complaint to API 3.0.

    Args:
        path (str): [description]
    """
    if type(path) == dict:
        t = path
    else:
        with open(path) as f: 
            t = json.load(f)    
    t.pop('@context')
   
    entitydict = {
     'Annotation':iiifpapi3.Annotation,
     'AnnotationPage':iiifpapi3.AnnotationPage,
     'Canvas':iiifpapi3.Canvas,
     'Collection':iiifpapi3.Collection,
     'FragmentSelector':iiifpapi3.FragmentSelector,
     'ImageApiSelector':iiifpapi3.ImageApiSelector,
     'Manifest':iiifpapi3.Manifest,
     'PointSelector':iiifpapi3.PointSelector,
     'Range':iiifpapi3.Range,
     'SpecificResource':iiifpapi3.SpecificResource,
     'Manifest':iiifpapi3.Manifest,
     'service':iiifpapi3.service,
     'thumbnail':iiifpapi3.thumbnail,
     'provider':iiifpapi3.provider,
     'homepage':iiifpapi3.homepage,
     'logo':iiifpapi3.logo,
     'rendering':iiifpapi3.rendering,
     'services':iiifpapi3.services,
     'start':iiifpapi3.start,
        }
    assert t['type'] in entitydict.keys(),"%s not a valid IIIF object"%t['type']
    def map_to_class(obj,iscollection=False):
        parent_is_collection = False
        if obj['type'] == 'Collection':
            parent_is_collection = True
        if 'items' in obj.keys():
            for n, item in enumerate(obj['items']):
                obj['items'][n] = map_to_class(item,iscollection=parent_is_collection)
        # we can map directly to each class using the object type except for
        # manifest References which as the same type of Manifest
        if iscollection and obj['type'] == "Manifest" and 'items' not in obj.items():
            newobj = iiifpapi3.refManifest()
        else:
            newobj = entitydict[obj['type']]()
        # TODO: find better solution .update will cause height and width to be set R.
        # newobj.__dict__ = newobj works apparently with no problem
        newobj.__dict__.update(obj)
        ## Specific cases
        if obj['type'] == 'Canvas':
            if newobj.duration != None:
                newobj.set_duration(newobj.duration)
        return newobj
    newobj = map_to_class(t)
    return newobj 


def delete_object_byID(obj,id):
    if hasattr(obj,"__dict__"):
        obj = obj.__dict__
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key == 'id' and value == id:
                return True
            delete_object_byID(value,id)
    if isinstance(obj,list):
        for item in obj:
            if delete_object_byID(item,id):
                obj.remove(item)
    else:
        pass

def remove_and_insert_new(obj,id,newobj):
    if hasattr(obj,"__dict__"):
        obj = obj.__dict__
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key == 'id' and value == id:
                return True
            remove_and_insert_new(value,id)
    if isinstance(obj,list):
        for item in obj:
            if remove_and_insert_new(item,id):
                obj.remove(item)
                obj.append(newobj)
    else:
        pass


                  
