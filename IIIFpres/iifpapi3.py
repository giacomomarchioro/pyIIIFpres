
from . import plus
import json
global BASE_URL
BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1/"

class Required(object):
    """
    This is not an IIIF object but a class used by this software to identify required fields.
    This is equivalente to MUST statement in the guideline.
    """
    def __init__(self,description=None):
        self.problem_description = description
    def __repr__(self): 
        return 'Required attribute:%s' %self.problem_description

class Suggested(object):
    """
    This is not an IIIF object but a class used by this software to identify required fields.
    This is equivalente to SHOULD statement in the guideline.
    """
    def __init__(self,description=None):
        self.suggested = description
    def __repr__(self): 
        return 'Suggested attribute:%s' %self.suggested

# Let's group all the common arguments across the differnet types of collection

def unused(attr):
    """
    This function check if an attribute is not set (has no value in it).
    """
    if isinstance(attr, Required) or isinstance(attr, Suggested) or attr is None:
        return True
    else:
        return False

class CoreAttributes(object):
    """
    Core attributes are the attributes that are with all the major
    classes/container of IIIF namely: Collection, Manifest, Canvas, Range and
    Annotation Page, Annotation and Content and also in the minor classes such 
    as SeeAlso and partOf.

    ID an type attributes are required. The other might vary. 
    """
    def __init__(self):
        self.id = Required("A %s should have the ID property with at least one item." %self.__class__.__name__)
        self.type = self.__class__.__name__
        # These might be suggested or may be used if needed.
        self.label = None
    
    def set_id(self,objid=None,extendbase_url=None):
        """
        IIIF : The id property identifies this object with the URL at which it is available online.
        """
        if extendbase_url:
            if objid:
                ValueError("Set id using extendbase_url or objid not both.")
            if isinstance(extendbase_url,str):
                self.id = "/".join((BASE_URL,extendbase_url))
            if isinstance(extendbase_url,list):
                extendbase_url.insert(0,BASE_URL )
                self.id = "/".join(extendbase_url)
        elif objid is None:
            objid = BASE_URL
        else:
            self.id = objid
   
    def set_type(self):
        print("The type property must be kept %s." %self.__class__.__name__)
    
    def add_label(self,language,text):
        """
        IIIF : A human readable label, name or title. The label property is intended to be displayed 
        as a short, textual surrogate for the resource if a human needs to make a distinction 
        between it and similar resources, for example between objects, pages, or options for 
        a choice of images to display. The label property can be fully internationalized, and 
        each language can have multiple values.
        """
        if unused(self.label):
            self.label = {}
        self.label[language] = [text]

    def json_dumps(self):
        context = "http://iiif.io/api/presentation/3/context.json"
        def serializer(obj):
            return {k: v for k, v in obj.__dict__.items() if v is not None}
        res = json.dumps(self,default = serializer,indent=2)
        # little hack for fixing context first 3 chrs "{\n"
        res = "".join(('{\n "@context" : "%s", \n'%context,res[3:]))
        return res

    def json_save(self,filename):
        with open(filename,'w') as f:
            f.write(self.json_dumps())


class SeeAlso(CoreAttributes):
    """
    IIF: A machine-readable resource such as an XML or RDF description that is related to the
    current resource that has the seeAlso property. Properties of the resource should be given 
    to help the client select between multiple descriptions (if provided), and to make 
    appropriate use of the document. If the relationship between the resource and the document 
    needs to be more specific, then the document should include that relationship rather than 
    the IIIF resource. Other IIIF resources are also valid targets for seeAlso, for example to 
    link to a Manifest that describes a related object. The URI of the document must identify a
    single representation of the data in a particular format. For example, if the same data 
    exists in JSON and XML, then separate resources should be added for each representation, 
    with distinct id and format properties.
    """
    def __init__(self):
        super(SeeAlso, self).__init__()
        self.format = Suggested()
        self.profile = Suggested()

    def set_type(self,datatype):
        #TODO: add check
        self.type = datatype
    
    def set_profile(self,profile):
        #TODO: add check
        self.profile = profile
    
    def set_format(self,profile):
        #TODO: add check
        self.profile = format


class partOf(CoreAttributes): 
    """
    A containing resource that includes the resource that has the partOf property. 
    When a client encounters the partOf property, it might retrieve the referenced 
    containing resource, if it is not embedded in the current representation, in order 
    to contribute to the processing of the contained resource. For example, the partOf 
    property on a Canvas can be used to reference an external Manifest in order to 
    enable the discovery of further relevant information. Similarly, a Manifest can 
    reference a containing Collection using partOf to aid in navigation.
    """
    def __init__(self):
        self.format = Suggested()
        self.profile = Suggested()     

class Supplementary(CoreAttributes):
    """
    A link from this Range to an Annotation Collection that includes the supplementing Annotations 
    of content resources for the Range. Clients might use this to present additional content to the 
    user from a different Canvas when interacting with the Range, or to jump to the next part of the 
    Range within the same Canvas. For example, the Range might represent a newspaper article that spans
    non-sequential pages, and then uses the supplementary property to reference an Annotation Collection
    that consists of the Annotations that record the text, split into Annotation Pages per newspaper page. 
    Alternatively, the Range might represent the parts of a manuscript that have been transcribed or 
    translated, when there are other parts that have yet to be worked on. The Annotation Collection would
    be the Annotations that transcribe or translate, respectively.
    """
    def __init__(self):
        super(Supplementary,self).__init__()
        self.type = "Supplementary"
    
    def set_type(self):
        print("type must be AnnotationCollection")


class body(CoreAttributes,plus.HeightWidthDuration):
    def __init__(self):
        super(body,self).__init__()
        self.type = Required("The type of the content resource must be included, and should be taken from the table listed under the definition of type.")
        self.format = Suggested("The format of the resource should be included and, if so, should be the media type that is returned when the resource is dereferenced.")
        self.profile = Suggested("The profile of the resource, if it has one, should also be included.")
        self.service = None
    
    def set_type(self,mytype):
        self.type = mytype
    
    def set_format(self,format):
        self.format = format
    
    def add_service(self,service):
        if unused(self.service):
            self.service = []
        self.service.append(service)

class CommonAttributes(CoreAttributes):
    """
    Common attributes are the attributes that are in common with all the major
    classes/container of IIIF namely: Collection, Manifest, Canvas, Range and
    Annotation Page, Annotation and Content.

    ID an type attributes are required. The other might vary. 
    """
    def __init__(self):
        super(CommonAttributes, self).__init__()
        self.metadata = None
        self.summary = None
        self.requiredStatement = None
        self.rights = None
        # https://iiif.io/api/presentation/3.0/#thumbnail
        self.thumbnail = None
        self.behavior = None
        self.seeAlso = None
        self.service = None
        self.hompage = None
        self.rendering = None
        self.partOf = None
    
    def add_metadata(self,label=None,value=None,language_l=None,
                     language_v=None,entry=None):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if unused(self.metadata):
            self.metadata = []
        arggr = [label,value,language_l,language_v]
        if any(elem is not None for elem in arggr ) and entry is not None:
            ValueError("Either use entry arguments or a combination of other arguments, NOT both.")
        if entry is None:
            entry = {"label":{language_l:[label]},
                    "value":{language_l:[value]}}
        self.metadata.append(entry)

    def add_summary(self,text,language):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if unused(self.summary):
            self.summary = {}
        self.summary[language] = [text]
    
    def add_requiredStatement(self,label,value,language):
        """
        IIIF: Text that must be displayed when the resource is displayed or used. 
        For example, the requiredStatement property could be used to present 
        copyright or ownership statements, an acknowledgement of the owning and/or
        publishing institution, or any other text that the publishing organization 
        deems critical to display to the user. Given the wide variation of potential 
        client user interfaces, it will not always be possible to display this 
        statement to the user in the client’s initial state. If initially hidden, 
        clients must make the method of revealing it as obvious as possible.
        """
        if unused(self.requiredStatement):
            self.requiredStatement = {}
        self.requiredStatement["label"] = {language:[label]}
        self.requiredStatement["value"] = {language:[value]}
    
    def set_rights(self,rights):
        """
        A string that identifies a license or rights statement that applies to the 
        content of the resource, such as the JSON of a Manifest or the pixels of an
        image. The value must be drawn from the set of Creative Commons license URIs,
        the RightsStatements.org rights statement URIs, or those added via the 
        extension mechanism. The inclusion of this property is informative, and for
        example could be used to display an icon representing the rights assertions.
        
        Not sure if it is suggested or mandatory.
        """
        #TODO: CHECK IF IT IS A VALID URL
        self.rights =  rights

    def add_thumbnail(self,obj):
        """
        #TODO:
        """
        if unused(self.thumbnail):
            self.thumbnail = {}

    def add_behavior(self,behavior):
        """
        """
        #TODO: CHECK IF ALLOWED
        if unused(self.behavior):
            self.behavior = []
        self.behavior.append(behavior)

    def add_seeAlso(self,t):
        pass
        

class service(CommonAttributes):
    """https://iiif.io/api/presentation/3.0/#service
    A service that the client might interact with directly and 
    gain additional information or functionality for using the 
    resource that has the service property, such as from an 
    Image to the base URI of an associated IIIF Image API 
    service. The service resource should have additional 
    information associated with it in order to allow the 
    client to determine how to make appropriate use of it. 
    Please see the Service Registry document for the details 
    of currently known service types.

    The value must be an array of JSON objects. Each object 
    will have properties depending on the service’s definition,
     but must have either the id or @id and type or @type 
     properties. Each object should have a profile property.

    Any resource type may have the service property with at 
    least one item.
    Clients may process service on any resource type, and 
    should process the IIIF Image API service.

    """
    def __init__(self):
        super(service,self).__init__()
        self.profile = Suggested("Each object should have a profile property.")



    def set_type(self,mytype):
        values = [
            "ImageService",
            "SearchService",
            "AutoCompleteService",
            "AuthCookieService",
            "AuthTokenService",
            "AuthLogoutService"]
        if mytype in values:
            self.type = mytype
        else:
            ValueError("mytype not right must be one of these value %s" %",".join(values))
    
    def set_type(self,mtype):
        self.type = mtype
        
    def set_profile(self,profile):
        self.profile = profile

class Annotation(CommonAttributes):
    """

    https://iiif.io/api/presentation/3.0/#56-annotation 
    Annotations follow the Web Annotation data model. The description provided here is a summary 
    plus any IIIF specific requirements. The W3C standard is the official documentation.

    Annotations must have their own HTTP(S) URIs, conveyed in the id property. The JSON-LD 
    description of the Annotation should be returned if the URI is dereferenced, according to 
    the Web Annotation Protocol.

    When Annotations are used to associate content resources with a Canvas, the content resource
    is linked in the body of the Annotation. The URI of the Canvas must be repeated in the target
    property of the Annotation, or the source property of a Specific Resource used in the target 
    property.

    Note that the Web Annotation data model defines different patterns for the value property, 
    when used within an Annotation. The value of a Textual Body or a Fragment Selector, for example,
    are strings rather than JSON objects with languages and values. Care must be taken to use the 
    correct string form in these cases.

    Additional features of the Web Annotation data model may also be used, such as selecting a 
    segment of the Canvas or content resource, or embedding the comment or transcription within 
    the Annotation. The use of these advanced features sometimes results in situations where the 
    target is not a content resource, but instead a SpecificResource, a Choice, or other 
    non-content object. Implementations should check the type of the resource and not assume that 
    it is always content to be rendered.
    """
    #https://iiif.io/api/presentation/3.0/#56-annotation 
    def __init__(self,target):
        super(CommonAttributes, self).__init__()
        self.motivation = None
        self.body = body()
        self.target = target
          
    def set_motivation(self,motivation):
        """
        https://iiif.io/api/presentation/3.0/#values-for-motivation
        Values for motivation
        This specification defines two values for the Web Annotation property of 
        motivation, or purpose when used on a Specific Resource or Textual 
        Body.

        While any resource may be the target of an Annotation, this 
        specification defines only motivations for Annotations that 
        target Canvases. These motivations allow clients to determine 
        how the Annotation should be rendered, by distinguishing between 
        Annotations that provide the content of the Canvas, from ones with
        externally defined motivations which are typically comments about
        the Canvas.

        Additional motivations may be added to the Annotation to further 
        clarify the intent, drawn from extensions or other sources. 
        Clients must ignore motivation values that they do not understand.
        Other motivation values given in the Web Annotation specification 
        should be used where appropriate, and examples are given in the 
        Presentation API Cookbook.

        Value	Description
        painting	Resources associated with a Canvas by an Annotation
        that has the motivation value painting must be presented to the 
        user as the representation of the Canvas. The content can be 
        thought of as being of the Canvas. The use of this motivation 
        with target resources other than Canvases is undefined. 
        For example, an Annotation that has the motivation value
        painting, a body of an Image and the target of the Canvas is
        an instruction to present that Image as (part of) the visual
        representation of the Canvas. Similarly, a textual body is 
        to be presented as (part of) the visual representation of 
        the Canvas and not positioned in some other part of the 
        user interface.

        supplementing	Resources associated with a Canvas by an 
        Annotation that has the motivation value supplementing may 
        be presented to the user as part of the representation of t
        he Canvas, or may be presented in a different part of the 
        user interface. The content can be thought of as being from 
        the Canvas. The use of this motivation with target resources 
        other than Canvases is undefined. For example, an Annotation 
        that has the motivation value supplementing, a body of an 
        Image and the target of part of the Canvas is an instruction
        to present that Image to the user either in the Canvas’s 
        rendering area or somewhere associated with it, and could be
        used to present an easier to read representation of a diagram.
        Similarly, a textual body is to be presented either in the
        targeted region of the Canvas or otherwise associated with it,
        and might be OCR, a manual transcription or a translation of
        handwritten text, or captions for what is
        """

        motivations = ["painting","supplementing"]
        if motivation not in motivations:
            pass #TODO:warning
        self.motivation = motivation


class AnnotationPage(CommonAttributes):
    """
 
    """
    def __init__(self):
        super(AnnotationPage, self).__init__()
        self.items = Suggested()
        self.annotations = None

    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)

class Canvas(CommonAttributes):
    """
    https://iiif.io/api/presentation/3.0/#53-canvas
    The Canvas represents an individual page or view and acts as a central point for assembling the
    different content resources that make up the display. Canvases must be identified by a URI and it 
    must be an HTTP(S) URI.
    """
    def __init__(self):
        super(Canvas, self).__init__()
        self.height = Required()
        self.width = Required()
        self.items = Suggested()
        self.annotations = None
    
    def set_width(self,width:int):
        self.width = width
    
    def set_height(self,height:int):
        self.height = height
    
    def set_hightwidth(self,height:int,width:int):
        self.set_width = width
        self.set_height = height

    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)

class Manifest(CommonAttributes,plus.ViewingDirection):
    """
    The Manifest resource typically represents a single object 
    and any intellectual work or works embodied within that 
    object. In particular it includes descriptive, rights and 
    linking information for the object. The Manifest embeds 
    the Canvases that should be rendered as views of the object 
    and contains sufficient information for the client to 
    initialize itself and begin to display something quickly to
     the user.

    The identifier in id must be able to be dereferenced to 
    retrieve the JSON description of the Manifest, and thus 
    must use the HTTP(S) URI scheme.

    The Manifest must have an items property, which is an array
    of JSON-LD objects. Each object is a Canvas, with 
    requirements as described in the next section.
    The Manifest may also have a structures property listing 
    one or more Ranges which describe additional structure of 
    the content, such as might be rendered as a table of
    contents. The Manifest may have an annotations property, 
    which includes Annotation Page resources where the 
    Annotations have the Manifest as their target. 
    These will typically be comment style Annotations,
    and must not have painting as their motivation.
    """
    def __init__(self):
        super(Manifest, self).__init__()
        self.items = []

    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)
        

class Collection(CommonAttributes):
    def __init__(self):
        super(Collection, self).__init__()
        self.other  = None
        self.seeAlso = SeeAlso()


    def set_seeAlso(self):
        pass

    def  set_Pass(self):
        pass


        


 #json.dumps(g, default=lambda x:x.__dict__)