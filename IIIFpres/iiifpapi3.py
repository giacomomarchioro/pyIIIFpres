
from . import plus
from . import visualization_html
import json
global BASE_URL
BASE_URL = "https://"
logs = {"Required": 0, "Recommended": 0}


class Required(object):
    """
    This is not an IIIF object but a class used by this software to identify 
    required fields.
    This is equivalent to MUST statement in the guideline with the meaning
    of https://tools.ietf.org/html/rfc2119.
    """

    def __init__(self, description=None):
        self.Required = description

    def __repr__(self):
        logs["Required"] += 1
        return 'Required attribute:%s' % self.Required


class Recommended(object):
    """
    This is not an IIIF object but a class used by this software to identify 
    required fields.
    This is equivalent to SHOULD statement in the guideline with the meaning
    of https://tools.ietf.org/html/rfc2119.
    """

    def __init__(self, description=None):
        self.Recommended = description

    def __repr__(self):
        logs["Recommended"] += 1
        return 'Recommended attribute:%s' % self.Recommended


# Note: we use None for OPTIONAL with the meaning of
# https://tools.ietf.org/html/rfc2119

def unused(attr):
    """
    This function check if an attribute is not set (has no value in it).
    """
    if isinstance(attr, (Required, Recommended)) or attr is None:
        return True
    else:
        return False


def serializable(attr):
    """Check if attribute is Required and if so rise Value error.

    Args:
        attr : the value of the dictionary representing the attribute of the instance.
    """
    if isinstance(attr, Required):
        raise ValueError("Required attribute missing")
    if isinstance(attr, Recommended) or attr is None:
        return False
    else:
        return True


def checkitem(selfx, classx, obj):
    """Check if item is added to the right class:
    This function is used to check if the object is added to the right entity. 
    It returns a reference of the empty object if the object to be added is not
    specified.

    For instance, I want to add an Annotation object to a Manifest. It checks 
    if items is unused and if so create  list and append an object of the class
    provided.

    Args:
        selfx (class): Original class.
        classx (class): Class that is allowed.
        obj (class): Object to be added to the class items.

    Returns:
        class: an instance of the item that is add if obj is None.
    """
    #import pdb; pdb.set_trace()

    if unused(selfx.items):
        selfx.items = []
    if obj is None:
        obj = classx()
        selfx.items.append(obj)
        return obj
    else:
        if isinstance(obj, classx):
            selfx.items.append(obj)
        else:
            obj_name = obj.__class__.__name__
            class_name = selfx.__class__.__name__
            raise ValueError("%s object cannot be added to %s." %
                             (obj_name, class_name))


def checkstru(selfx, classx, obj):
    """Check if a structure is added to the right entity:
    This function is used to check if the object is added to the right entity. 
    It returns a reference of the empty object if the object to be added is not
    specified.

    For instance, I want to add an Annotation object to a Manifest. It checks if
    items is unused and if so create  list and append an object of the class 
    provided.

    Args:
        selfx (class): Original class.
        classx (class): Class that is allowed.
        obj (class): Object to be added to the class items.

    Returns:
        class: an instance of the item that is add if obj is None.
    """
    if unused(selfx.structures):
        selfx.structures = []
    if obj is None:
        obj = classx()
        selfx.structures.append(obj)
        return obj
    else:
        if isinstance(obj, classx):
            selfx.structures.append(obj)
        else:
            obj_name = obj.__class__.__name__
            class_name = selfx.__class__.__name__
            raise ValueError("%s object cannot be added to %s." %
                             (obj_name, class_name))

# Let's group all the common arguments across the differnet types of collection


class CoreAttributes(object):
    """
    Core attributes are the attributes in all the major
    classes/containers of IIIF namely: Collection, Manifest, Canvas, Range and
    Annotation Page, Annotation and Content and also in the minor classes such
    as SeeAlso and partOf.

    ID an type attributes are required. The other might vary.
    """

    def __init__(self):
        self.id = Required(
            "A %s should have the ID property with at least one item." %
            self.__class__.__name__)
        self.type = self.__class__.__name__
        # These might be suggested or may be used if needed.
        self.label = None

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
                self.id = "/".join((BASE_URL, extendbase_url))
            if isinstance(extendbase_url, list):
                extendbase_url.insert(0, BASE_URL)
                self.id = "/".join(extendbase_url)

        elif objid is None:
            self.id = BASE_URL
        else:
            assert objid.startswith("http"), "ID must start with http"
            self.id = objid

    def set_type(self):
        print("The type property must be kept %s." % self.__class__.__name__)

    def add_label(self, language, text):
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

        if unused(self.label):
            self.label = {}
        if language is None:
            language = "none"
        self.label[language] = [text]

    def json_dumps(
            self,
            dumps_errors=False,
            ensure_ascii=False,
            sort_keys=False):
        """Dumps the content of the object in JSON format.

        Args:
            dumps_errors (bool, optional): If set true it shows any problem 
            found directly on the JSON file with a Required or Recommended tag.
            Defaults to False.

        Returns:
            str: The object in JSON format.
        """
        context = "http://iiif.io/api/presentation/3/context.json"

        def serializerwitherrors(obj):
            return {k: v for k, v in obj.__dict__.items() if v is not None}

        def serializer(obj):
            return {k: v for k, v in obj.__dict__.items() if serializable(v)}
        if dumps_errors:
            res = json.dumps(
                self,
                default=serializerwitherrors,
                indent=2,
                ensure_ascii=ensure_ascii,
                sort_keys=sort_keys)
        else:
            res = json.dumps(
                self,
                default=serializer,
                indent=2,
                ensure_ascii=ensure_ascii,
                sort_keys=sort_keys)
        # little hack for fixing context first 3 chrs "{\n"
        res = "".join(('{\n  "@context": "%s",\n ' % context, res[3:]))
        return res

    def json_save(self, filename, save_errors=False, ensure_ascii=False):
        with open(filename, 'w') as f:
            f.write(self.json_dumps(
                dumps_errors=save_errors, ensure_ascii=ensure_ascii))

    def inspect(self):
        print(self.json_dumps(dumps_errors=True))
        print("Missing requirements field: %s." % logs["Required"])
        print("Missing recommended field: %s." % logs["Recommended"])
        logs["Required"] = 0
        logs["Recommended"] = 0
        return True
    
    def show_errors_in_browser(self):
        visualization_html.show_error_in_browser(self.json_dumps(dumps_errors=True))

    def __repr__(self) -> str:
        if unused(self.id):
            id_ = "Missing"
        else:
            id_ = self.id
        return " id:".join((self.type,id_))


class seeAlso(CoreAttributes):
    """
    IIF: A machine-readable resource such as an XML or RDF description that is 
    related to the current resource that has the seeAlso property. Properties 
    of the resource should be given to help the client select between multiple 
    descriptions (if provided), and to make appropriate use of the document. 
    If the relationship between the resource and the document needs to be more 
    specific, then the document should include that relationship rather than 
    the IIIF resource. Other IIIF resources are also valid targets for 
    seeAlso, for example to link to a Manifest that describes a related 
    object. The URI of the document must identify a single representation of 
    the data in a particular format. For example, if the same data exists in 
    JSON and XML, then separate resources should be added for each 
    representation, with distinct id and format properties.
    """

    def __init__(self):
        super(seeAlso, self).__init__()
        self.format = Recommended("Its should have a format")
        self.profile = Recommended("It should have a profile")

    def set_type(self, datatype):
        # TODO: add check
        self.type = datatype

    def set_profile(self, profile):
        # TODO: add check
        self.profile = profile

    def set_format(self, format):
        """Set the format of the IIIF type.
        IIIF: The specific media type (often called a MIME type) for a content 
        resource, for example image/jpeg. This is important for distinguishing 
        different formats of the same overall type of resource, such as 
        distinguishing text in XML from plain text. 

        Args: format (str): the format of the IIIF type, usually is the MIME e.g. 
        image/jpg """
        msg = "Format should be in the form type/format e.g. image/jpg"
        assert "/" in format, msg
        assert format.split("/")[0].isalpha(), msg
        self.format = format


class partOf(CoreAttributes):
    """
    A containing resource that includes the resource that has the partOf
    property. When a client encounters the partOf property, it might retrieve
    the referenced containing resource, if it is not embedded in the current
    representation, in order to contribute to the processing of the contained
    resource. For example, the partOf property on a Canvas can be used to
    reference an external Manifest in order to enable the discovery of further
    relevant information. Similarly, a Manifest can reference a containing
    Collection using partOf to aid in navigation.
    """

    def __init__(self):
        super(partOf, self).__init__()

    def set_type(self, type_):
        assert not type_[0].isdigit(), "First letter should not be a digit"
        self.type = type_

    def set_id(self, objid):
        self.id = objid


class supplementary(CoreAttributes):
    """
    IIIF: A link from this Range to an Annotation Collection that includes the 
    supplementing Annotations of content resources for the Range. Clients 
    might use this to present additional content to the user from a different 
    Canvas when interacting with the Range, or to jump to the next part of the 
    Range within the same Canvas. For example, the Range might represent a 
    newspaper article that spans non-sequential pages, and then uses the 
    supplementary property to reference an Annotation Collection that consists 
    of the Annotations that record the text, split into Annotation Pages per 
    newspaper page. Alternatively, the Range might represent the parts of a 
    manuscript that have been transcribed or translated, when there are other 
    parts that have yet to be worked on. The Annotation Collection would be 
    the Annotations that transcribe or translate, respectively.
    """

    def __init__(self):
        super(supplementary, self).__init__()
        self.type = "AnnotationCollection"

    def set_type(self):
        print("type must be AnnotationCollection")


class bodycommenting(object):
    def __init__(self):
        self.type = "TextualBody"
        self.value = None
        self.language = None

    def set_type(self, mtype):
        print("Commenting body should be TextualBody not %s" % mtype)

    def set_format(self, format):
        # TODO: what format are allowed?
        self.format = format

    def set_value(self, value):
        self.value = value

    def set_language(self, language):
        self.language = language


class bodypainting(CoreAttributes):
    def __init__(self):
        super(bodypainting, self).__init__()
        self.type = Required(
            "The type of the content resource must be included, and should be taken from the table listed under the definition of type.")
        self.format = Recommended(
            "The format of the resource should be included and, if so, should be the media type that is returned when the resource is dereferenced.")
        self.profile = Recommended(
            "The profile of the resource, if it has one, should also be included.")
        self.height = Required("Must have an height or a duration.")
        self.width = Required("Must have an width or a duration.")
        self.duration = None
        self.service = None

    def set_type(self, mytype):
        self.type = mytype

    def set_format(self, format):
        self.format = format

    def set_width(self, width: int):
        self.width = int(width)

    def set_height(self, height: int):
        self.height = int(height)

    def set_hightwidth(self, height: int, width: int):
        self.set_width(width)
        self.set_height(height)

    def set_duration(self, duration: float):
        if unused(self.height):
            self.height = None
        if unused(self.width):
            self.width = None
        self.duration = float(duration)

    def add_service(self, serviceobj=None):
        if unused(self.service):
            self.service = []
        if serviceobj is None:
            serviceobj = service()
            self.service.append(serviceobj)
            return serviceobj
        else:
            if isinstance(serviceobj, service) or isinstance(serviceobj, dict):
                self.service.append(serviceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)


class service(CoreAttributes):
    """https://iiif.io/api/presentation/3.0/#service
    IIIF:A service that the client might interact with directly and gain 
    additional information or functionality for using the resource that has 
    the service property, such as from an Image to the base URI of an 
    associated IIIF Image API service. The service resource should have 
    additional information associated with it in order to allow the client to 
    determine how to make appropriate use of it. Please see the Service 
    Registry document for the details of currently known service types. 

    The value must be an array of JSON objects. Each object will have 
    properties depending on the service’s definition, but must have either the 
    id or @id and type or @type properties. Each object should have a profile 
    property. 

    Any resource type may have the service property with at least one item. 
    Clients may process service on any resource type, and should process the 
    IIIF Image API service. 
    """

    def __init__(self):
        super(service, self).__init__()
        self.profile = Recommended(
            "Each object should have a profile property.")
        self.service = None

    def set_type(self, mytype):
        """
        The type of the service, for instance if the image is served
        using IIIF Image API 3.0 then use "ImageService3".
        """
        values = [
            "ImageService",
            "SearchService",
            "AutoCompleteService",
            "AuthCookieService",
            "AuthTokenService",
            "AuthLogoutService"]
        #assert any([mytype.startswith(i) for i in values]
        #           ), "Must start with:%s was: %s" % (str(values)[1:-1],mytype)
        # throw error with ExampleExtensionService
        self.type = mytype

    def set_profile(self, profile):
        self.profile = profile

    def add_service(self, serviceobj=None):
        if unused(self.service):
            self.service = []
        if serviceobj is None:
            serviceobj = service()
            self.service.append(serviceobj)
            return serviceobj
        else:
            if isinstance(serviceobj, service) or isinstance(serviceobj, dict):
                self.service.append(serviceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)


class thumbnail(CoreAttributes, plus.HeightWidthDuration):
    def __init__(self):
        super(thumbnail, self).__init__()
        self.service = None

    def set_type(self, mtype):
        self.type = mtype

    def set_format(self, format):
        """Set the format of the IIIF type.
        IIIF: The specific media type (often called a MIME type) for a content 
        resource,for example image/jpeg. This is important for distinguishing 
        different formats of the same overall type of resource, such as 
        distinguishing text in XML from plain text.

        Args:
            format (str): the format of the IIIF type, usually is the MIME 
            e.g. image/jpg
        """
        msg = "Format should be in the form type/format e.g. image/jpg"
        assert "/" in format, msg
        assert format.split("/")[0].isalpha(), msg
        self.format = format

    def add_service(self, serviceobj=None):
        if unused(self.service):
            self.service = []
        if serviceobj is None:
            serviceobj = service()
            self.service.append(serviceobj)
            return serviceobj
        else:
            if isinstance(serviceobj, service) or isinstance(serviceobj, dict):
                self.service.append(serviceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)


class provider(CoreAttributes):
    """
    IIIF: An organization or person that contributed to providing the content 
    of the resource. Clients can then display this information to the user to 
    acknowledge the provider’s contributions. This differs from the 
    requiredStatement property, in that the data is structured, allowing the 
    client to do more than just present text but instead have richer 
    information about the people and organizations to use in different 
    interfaces.

      "provider": [
    {
      "id": "https://example.org/about",
      "type": "Agent",
      "label": { "en": [ "Example Organization" ] },
      "homepage": [
        {
          "id": "https://example.org/",
          "type": "Text",
          "label": { "en": [ "Example Organization Homepage" ] },
          "format": "text/html"
        }
      ],
      "logo": [
        {
          "id": "https://example.org/images/logo.png",
          "type": "Image",
          "format": "image/png",
          "height": 100,
          "width": 120
        }
      ],
      "seeAlso": [
        {
          "id": "https://data.example.org/about/us.jsonld",
          "type": "Dataset",
          "format": "application/ld+json",
          "profile": "https://schema.org/"
        }
      ]
    }
    ]
    """

    def __init__(self):
        super(provider, self).__init__()
        self.context = None
        self.type = "Agent"
        self.homepage = Recommended(
            "Agents should have the homepage property, and its value must be an array of JSON objects as described in the homepage section.")
        self.logo = Recommended(
            "Agents should have the logo property, and its value must be an array of JSON objects as described in the logo section.")
        self.seeAlso = None

    def set_type(self):
        """The type property must be the string “Agent”.
        """
        print("The type property must be the default string “Agent”.")

    def add_logo(self, logoobj=None):
        if unused(self.logo):
            self.logo = []
        if logoobj is None:
            logoobj = logo()
            self.logo.append(logoobj)
            return logoobj
        else:
            if isinstance(logoobj, logo):
                self.logo.append(logoobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to logo in %s" %
                    self.__class__.__name__)

    def add_homepage(self, homepageobj=None):
        """
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.homepage):
            self.homepage = []
        if homepageobj is None:
            homepageobj = homepage()
            self.homepage.append(homepageobj)
            return homepageobj
        else:
            if isinstance(homepageobj, homepage):
                self.homepage.append(homepageobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to homepage in %s" %
                    self.__class__.__name__)

    def add_seeAlso(self, seeAlsoobj=None):
        """
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.seeAlso):
            self.seeAlso = []
        if seeAlsoobj is None:
            seeAlsoobj = seeAlso()
            self.seeAlso.append(seeAlsoobj)
            return seeAlsoobj
        else:
            if isinstance(seeAlsoobj, seeAlso):
                self.seeAlso.append(seeAlsoobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to seeAlso in %s" %
                    self.__class__.__name__)


class homepage(CoreAttributes):
    """https://iiif.io/api/presentation/3.0/#homepage
    IIIF: A web page that is about the object represented by the resource that 
    has the homepage property. The web page is usually published by the 
    organization responsible for the object, and might be generated by a 
    content management system or other cataloging system. The resource must be 
    able to be displayed directly to the user. Resources that are related, but 
    not home pages, must instead be added into the metadata property, with an 
    appropriate label or value to describe the relationship.
    """

    def __init__(self):
        super(homepage, self).__init__()
        self.language = None
        self.format = Recommended(
            "Hompage should have a format property e.g. Text.")

    def set_language(self, language):
        if unused(self.language):
            self.language = []
        self.language.append(language)

    def set_format(self, format):
        """Set the format of the IIIF type.
        IIIF: The specific media type (often called a MIME type) for a content 
        resource, for example image/jpeg. This is important for distinguishing 
        different formats of the same overall type of resource, such as 
        distinguishing text in XML from plain text.

        Args:
            format (str): the format of the IIIF type, usually is the MIME e.g. image/jpg
        """
        msg = "Format should be in the form type/format e.g. image/jpg"
        assert "/" in format, msg
        assert format.split("/")[0].isalpha(), msg
        self.format = format

    def set_type(self, mtype):
        self.type = mtype


class logo(CoreAttributes, plus.HeightWidthDuration):
    """
    A small image resource that represents the Agent resource it is associated 
    with. The logo must be clearly rendered when the resource is displayed or 
    used, without cropping, rotating or otherwise distorting the image. It is 
    recommended that a IIIF Image API service be available for this image for 
    other manipulations such as resizing.

    When more than one logo is present, the client should pick only one of them,
    based on the information in the logo properties. For example, the client 
    could select a logo of appropriate aspect ratio based on the height and 
    width properties of the available logos. The client may decide on the logo
    by inspecting properties defined as extensions.

    "logo": [
    {
      "id": "https://example.org/img/logo.jpg",
      "type": "Image",
      "format": "image/jpeg",
      "height": 100,
      "width": 120
    }
    ]
    #TODO Duration should not be included
    """

    def __init__(self):
        super(logo, self).__init__()
        self.format = Recommended(
            "Logo should have a format attribute e.g. image/png")
        self.service = Recommended(
            "Logo should have service attribute, you can add using srv = mylogo.add_service()")

    def set_format(self, format):
        """Set the format of the IIIF type.
        IIIF: The specific media type (often called a MIME type) for a content 
        resource, for example image/jpeg. This is important for distinguishing 
        different formats of the same overall type of resource, such as 
        distinguishing text in XML from plain text.

        Args:
            format (str): the format of the IIIF type, usually is the MIME e.g. image/jpg
        """
        msg = "Format should be in the form type/format e.g. image/jpeg"
        assert "/" in format, msg
        assert format.split("/")[0].isalpha(), msg
        self.format = format

    def set_type(self, mtype):
        self.type = mtype

    def set_label(self, label):
        raise ValueError("Label not permitted in logo.")

    def add_service(self, serviceobj=None):
        if unused(self.service):
            self.service = []
        if serviceobj is None:
            serviceobj = service()
            self.service.append(serviceobj)
            return serviceobj
        else:
            if isinstance(serviceobj, service) or isinstance(serviceobj, dict):
                self.service.append(serviceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)


class rendering(CoreAttributes):
    """https://iiif.io/api/presentation/3.0/#rendering 
    A resource that is an alternative, non-IIIF representation of the resource
    that has the rendering property. Such representations typically cannot be
    painted onto a single Canvas, as they either include too many views, have
    incompatible dimensions, or are compound resources requiring additional
    rendering functionality. The rendering resource must be able to be
    displayed directly to a human user, although the presentation may be
    outside of the IIIF client. The resource must not have a splash page or
    other interstitial resource that mediates access to it. If access control
    is required, then the IIIF Authentication API is recommended. Examples
    include a rendering of a book as a PDF or EPUB, a slide deck with images of
    a building, or a 3D model of a statue.

    "rendering": [
    {
      "id": "https://example.org/1.pdf",
      "type": "Text",
      "label": { "en": [ "PDF Rendering of Book" ] },
      "format": "application/pdf"
    }
    ]
    """

    def __init__(self):
        super(rendering, self).__init__()
        self.format = Recommended(
            "Rendering should have a format property e.g. application/pdf.")

    def set_format(self, format):
        """Set the format of the IIIF type.
        IIIF: The specific media type (often called a MIME type) for a content resource,
        for example image/jpeg. This is important for distinguishing different formats
        of the same overall type of resource, such as distinguishing text in XML from
        plain text.

        Args:
            format (str): the format of the IIIF type, usually is the MIME e.g. image/jpg
        """
        msg = "Format should be in the form type/format e.g. image/jpg"
        assert "/" in format, msg
        assert format.split("/")[0].isalpha(), msg
        self.format = format

    def set_type(self, type):
        self.type = type


class services(CoreAttributes):
    """
    A list of one or more service definitions on the top-most resource of the
    document, that are typically shared by more than one subsequent resource.
    This allows for these shared services to be collected together in a single
    place, rather than either having their information duplicated potentially
    many times throughout the document, or requiring a consuming client to
    traverse the entire document structure to find the information. The
    resource that the service applies to must still have the service property,
    as described above, where the service resources have at least the id and
    type or @id and @type properties. This allows the client to know that the
    service applies to that resource. Usage of the services property is at the
    discretion of the publishing system.
    """

    def __init__(self):
        super(services, self).__init__()
        self.profile = Recommended(
            "services should have a profile property e.g. https://example.org/docs/service.")
        self.service = Required(
            "Services must have at least one service, use add_service() method to add one.")

    def set_profile(self, profile):
        self.profile = profile

    def add_service(self, serviceobj=None):
        if unused(self.service):
            self.service = []
        if serviceobj is None:
            serviceobj = service()
            self.service.append(serviceobj)
            return serviceobj
        else:
            if isinstance(serviceobj, service) or isinstance(serviceobj, dict):
                self.service.append(serviceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)


class languagemap(object):
    """This is not a IIIF type but is used for easing the construction of
    multilingual metadata and requiredstatements.
    """

    def __init__(self):
        self.label = Required(
            "The metadata/requiredstatements must have at least a label")
        self.value = Required(
            "The metadata/requiredstatements must have at least a value")

    def add_value(self, value, language="none"):
        if unused(self.value):
            self.value = {}
        if not isinstance(value, list):
            value = [value]
        # TODO: if html must begin with < and ends with >
        # https://iiif.io/api/presentation/3.0/#45-html-markup-in-property-values
        self.value[language] = value

    def add_label(self, label, language="none"):
        if unused(self.label):
            self.label = {}
        if not isinstance(label, list):
            label = [label]
        # TODO: check that is not html
        # https://iiif.io/api/presentation/3.0/#45-html-markup-in-property-values
        self.label[language] = label


##
# COMMON ATTRIBUTES TO MAJOR CONTAINERS
##

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
        self.homepage = None
        self.rendering = None
        self.partOf = None

    def add_metadata(self, label=None, value=None, language_l="none",
                     language_v="none", entry=None):
        """
        An ordered list of descriptions to be displayed to the user when they
        interact with the resource, given as pairs of human readable label and
        value entries. The content of these entries is intended for
        presentation only; descriptive semantics should not be inferred. An
        entry might be used to convey information about the creation of the
        object, a physical description, ownership information, or other
        purposes.
        """
        if unused(self.metadata):
            self.metadata = []

        if label is None and value is None and entry is None:
            languagemapobj = languagemap()
            self.metadata.append(languagemapobj)
            return languagemapobj

        if (label is not None or value is not None) and entry is not None:
            raise ValueError(
                "Either use entry arguments or a combination of other arguments, NOT both.")

        if not isinstance(value, list):
            value = [value]

        if entry is None:
            entry = {"label": {language_l: [label]},
                     "value": {language_v: value}}
        self.metadata.append(entry)

    def add_summary(self, language, text):
        """
        An ordered list of descriptions to be displayed to the user when they
        interact with the resource, given as pairs of human readable label and
        value entries. The content of these entries is intended for
        presentation only; descriptive semantics should not be inferred. An
        entry might be used to convey information about the creation of the
        object, a physical description, ownership information, or other
        purposes.
        """
        if unused(self.summary):
            self.summary = {}
        self.summary[language] = [text]

    def add_requiredStatement(self, label=None, value=None, language_l=None,
                              language_v=None, entry=None):
        """
        IIIF: Text that must be displayed when the resource is displayed or
        used. For example, the requiredStatement property could be used to
        present copyright or ownership statements, an acknowledgement of the
        owning and/or publishing institution, or any other text that the
        publishing organization deems critical to display to the user. Given
        the wide variation of potential client user interfaces, it will not
        always be possible to display this statement to the user in the
        client’s initial state. If initially hidden, clients must make the
        method of revealing it as obvious as possible.
        """
        if label is None and value is None and entry is None:
            languagemapobj = languagemap()
            self.requiredStatement = languagemapobj
            return languagemapobj

        if unused(self.requiredStatement):
            self.requiredStatement = {}

        if (label is not None or value is not None) and entry is not None:
            raise ValueError(
                "Either use entry arguments or a combination of other arguments, NOT both.")
        if entry is None:
            entry = {"label": {language_l: [label]},
                     "value": {language_v: [value]}}
        self.requiredStatement = entry

    def set_rights(self, rights):
        """
        A string that identifies a license or rights statement that applies to
        the content of the resource, such as the JSON of a Manifest or the
        pixels of an image. The value must be drawn from the set of Creative
        Commons license URIs, the RightsStatements.org rights statement URIs,
        or those added via the extension mechanism. The inclusion of this
        property is informative, and for example could be used to display an
        icon representing the rights assertions.

        Not sure if it is suggested or mandatory.
        """
        # TODO: CHECK IF IT IS A VALID URL
        licenceurls = ["http://creativecommons.org/licenses/",
                       "http://creativecommons.org/publicdomain/mark/",
                       "http://rightsstatements.org/vocab/",
                       "https://creativecommons.org/licenses/",
                       "https://creativecommons.org/publicdomain/mark/",
                       "https://rightsstatements.org/vocab/"]
        assert any([rights.startswith(i) for i in licenceurls]
                   ), "Must start with:%s" % str(licenceurls)[1:-1]
        self.rights = rights

    def add_thumbnail(self, thumbnailobj=None):
        """
        https://iiif.io/api/presentation/3.0/#thumbnail A content resource,
        such as a small image or short audio clip, that represents the resource
        that has the thumbnail property. A resource may have multiple thumbnail
        resources that have the same or different type and format.

        The value must be an array of JSON objects, each of which must have the
        id and type properties, and should have the format property. Images and
        videos should have the width and height properties, and time-based
        media should have the duration property. It is recommended that a IIIF
        Image API service be available for images to enable manipulations such
        as resizing.
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.thumbnail):
            self.thumbnail = []
        if thumbnailobj is None:
            thumbnailobj = thumbnail()
            self.thumbnail.append(thumbnailobj)
            return thumbnailobj
        else:
            if isinstance(thumbnailobj, thumbnail):
                self.thumbnail.append(thumbnailobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to thumbnail in %s" %
                    self.__class__.__name__)

    def add_behavior(self, behavior):
        """
        A set of user experience features that the publisher of the content
        would prefer the client to use when presenting the resource. This
        specification defines the values in the table below. Others may be
        defined externally as an extension.
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.behavior):
            self.behavior = []
        self.behavior.append(behavior)

    def add_homepage(self, homepageobj=None):
        """
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.homepage):
            self.homepage = []
        if homepageobj is None:
            homepageobj = homepage()
            self.homepage.append(homepageobj)
            return homepageobj
        else:
            if isinstance(homepageobj, homepage):
                self.homepage.append(homepageobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to homepage in %s" %
                    self.__class__.__name__)

    def add_seeAlso(self, seeAlsoobj=None):
        """
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.seeAlso):
            self.seeAlso = []
        if seeAlsoobj is None:
            seeAlsoobj = seeAlso()
            self.seeAlso.append(seeAlsoobj)
            return seeAlsoobj
        else:
            if isinstance(seeAlsoobj, seeAlso):
                self.seeAlso.append(seeAlsoobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to seeAlso in %s" %
                    self.__class__.__name__)

    def add_partOf(self, partOfobj=None):
        """
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.partOf):
            self.partOf = []
        if partOfobj is None:
            partOfobj = partOf()
            self.partOf.append(partOfobj)
            return partOfobj
        else:
            if isinstance(partOfobj, seeAlso):
                self.partOf.append(partOfobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to partOf in %s" %
                    self.__class__.__name__)

    def add_rendering(self, renderingobj=None):
        """
        """
        # TODO: CHECK IF ALLOWED
        if unused(self.rendering):
            self.rendering = []
        if renderingobj is None:
            renderingobj = rendering()
            self.rendering.append(renderingobj)
            return renderingobj
        else:
            if isinstance(renderingobj, rendering):
                self.rendering.append(renderingobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to renderging in %s" %
                    self.__class__.__name__)


class Annotation(CommonAttributes):
    """

    https://iiif.io/api/presentation/3.0/#56-annotation Annotations follow the
    Web Annotation data model. The description provided here is a summary plus
    any IIIF specific requirements. The W3C standard is the official
    documentation.

    Annotations must have their own HTTP(S) URIs, conveyed in the id property.
    The JSON-LD description of the Annotation should be returned if the URI is
    dereferenced, according to the Web Annotation Protocol.

    When Annotations are used to associate content resources with a Canvas, the
    content resource is linked in the body of the Annotation. The URI of the
    Canvas must be repeated in the target property of the Annotation, or the
    source property of a Specific Resource used in the target property.

    Note that the Web Annotation data model defines different patterns for the
    value property, when used within an Annotation. The value of a Textual Body
    or a Fragment Selector, for example, are strings rather than JSON objects
    with languages and values. Care must be taken to use the correct string
    form in these cases.

    Additional features of the Web Annotation data model may also be used, such
    as selecting a segment of the Canvas or content resource, or embedding the
    comment or transcription within the Annotation. The use of these advanced
    features sometimes results in situations where the target is not a content
    resource, but instead a SpecificResource, a Choice, or other non-content
    object. Implementations should check the type of the resource and not
    assume that it is always content to be rendered.
    """
    # https://iiif.io/api/presentation/3.0/#56-annotation

    def __init__(self, target):
        super(CommonAttributes, self).__init__()
        self.motivation = None
        self.body = None
        self.target = target
        self.metadata = None

    def set_motivation(self, motivation):
        """
        https://iiif.io/api/presentation/3.0/#values-for-motivation Values for
        motivation This specification defines two values for the Web Annotation
        property of motivation, or purpose when used on a Specific Resource or
        Textual Body.

        While any resource may be the target of an Annotation, this
        specification defines only motivations for Annotations that target
        Canvases. These motivations allow clients to determine how the
        Annotation should be rendered, by distinguishing between Annotations
        that provide the content of the Canvas, from ones with externally
        defined motivations which are typically comments about the Canvas.

        Additional motivations may be added to the Annotation to further
        clarify the intent, drawn from extensions or other sources. Clients
        must ignore motivation values that they do not understand. Other
        motivation values given in the Web Annotation specification should be
        used where appropriate, and examples are given in the Presentation API
        Cookbook.

        Value   Description painting    Resources associated with a Canvas by
        an Annotation that has the motivation value painting must be presented
        to the user as the representation of the Canvas. The content can be
        thought of as being of the Canvas. The use of this motivation with
        target resources other than Canvases is undefined. For example, an
        Annotation that has the motivation value painting, a body of an Image
        and the target of the Canvas is an instruction to present that Image as
        (part of) the visual representation of the Canvas. Similarly, a textual
        body is to be presented as (part of) the visual representation of the
        Canvas and not positioned in some other part of the user interface.

        supplementing   Resources associated with a Canvas by an Annotation
        that has the motivation value supplementing may be presented to the
        user as part of the representation of t he Canvas, or may be presented
        in a different part of the user interface. The content can be thought
        of as being from the Canvas. The use of this motivation with target
        resources other than Canvases is undefined. For example, an Annotation
        that has the motivation value supplementing, a body of an Image and the
        target of part of the Canvas is an instruction to present that Image to
        the user either in the Canvas’s rendering area or somewhere associated
        with it, and could be used to present an easier to read representation
        of a diagram. Similarly, a textual body is to be presented either in
        the targeted region of the Canvas or otherwise associated with it, and
        might be OCR, a manual transcription or a translation of handwritten
        text, or captions for what is
        """

        motivations = ["painting", "supplementing"]
        if motivation not in motivations:
            pass  # TODO:warning
        if motivation == "painting":
            self.body = bodypainting()
        if motivation == "commenting":
            self.body = bodycommenting()
        self.motivation = motivation


class AnnotationPage(CommonAttributes):
    """

    """

    def __init__(self):
        super(AnnotationPage, self).__init__()
        self.items = Recommended(
            "The annotation page must incude at least one item.")
        self.annotations = None

    def add_item(self, item):
        if unused(self.items):
            self.items = []
        self.items.append(item)

    def add_annotation_toitems(self, annotation=None, target=None):
        if unused(self.items):
            self.items = []
        if annotation is None:
            if unused(target):
                raise ValueError("Passing an empty ID!")
            annotation = Annotation(target=target)
            self.items.append(annotation)
            return annotation
        else:
            self.items.append(annotation)


class Canvas(CommonAttributes):
    """https://iiif.io/api/presentation/3.0/#53-canvas 
    The Canvas represents an individual page or view and acts as a central
    point for assembling the different content resources that make up the
    display. Canvases must be identified by a URI and it must be an HTTP(S)
    URI.
    """

    def __init__(self):
        super(Canvas, self).__init__()
        self.height = Required("Must have an height or a duration.")
        self.width = Required("Must have an width or a duration.")
        self.duration = None
        self.items = Recommended(
            "The canvas should contain at least one item.")
        self.annotations = None

    def set_width(self, width: int):
        self.width = int(width)

    def set_height(self, height: int):
        self.height = int(height)

    def set_hightwidth(self, height: int, width: int):
        self.set_width(width)
        self.set_height(height)

    def set_duration(self, duration: float):
        if unused(self.height):
            self.height = None
        if unused(self.width):
            self.width = None
        self.duration = float(duration)

    def add_item(self, item):
        if unused(self.items):
            self.items = []
        self.items.append(item)

    def add_annotation(self, annotation=None):
        if unused(self.annotations):
            self.annotations = []
        if annotation is None:
            annotation = Annotation(target=self.id)
            self.annotations.append(annotation)
            return annotation
        else:
            self.annotations.append(annotation)

    def add_annotationpage_to_items(self, annotationpageobj=None):
        # return self.check(self.items,AnnotationPage,annotationpageobj)
        if unused(self.items):
            self.items = []
        if annotationpageobj is None:
            annotationp = AnnotationPage()
            self.items.append(annotationp)
            return annotationp
        else:
            self.items.append(annotationpageobj)

    def add_annotationpage_to_annotations(self, annotationpageobj=None):
        # return self.check(self.items,AnnotationPage,annotationpageobj)
        if unused(self.annotations):
            self.annotations = []
        if annotationpageobj is None:
            annotationp = AnnotationPage()
            self.annotations.append(annotationp)
            return annotationp
        else:
            self.annotations.append(annotationpageobj)


class Manifest(CommonAttributes, plus.ViewingDirection, plus.navDate):
    """
    The Manifest resource typically represents a single object and any
    intellectual work or works embodied within that object. In particular it
    includes descriptive, rights and linking information for the object. The
    Manifest embeds the Canvases that should be rendered as views of the object
    and contains sufficient information for the client to initialize itself and
    begin to display something quickly to the user.

    The identifier in id must be able to be dereferenced to retrieve the JSON
    description of the Manifest, and thus must use the HTTP(S) URI scheme.

    The Manifest must have an items property, which is an array of JSON-LD
    objects. Each object is a Canvas, with requirements as described in the
    next section. The Manifest may also have a structures property listing one
    or more Ranges which describe additional structure of the content, such as
    might be rendered as a table of contents. The Manifest may have an
    annotations property, which includes Annotation Page resources where the
    Annotations have the Manifest as their target. These will typically be
    comment style Annotations, and must not have painting as their motivation.
    """

    def __init__(self):
        super(Manifest, self).__init__()
        self.start = None
        self.viewingDirection = None
        self.navDate = None
        self.services = None
        self.service = None
        self.items = Required("The Manifest must have an items property")
        self.annotations = None
        self.provider = None
        self.structures = None

    def add_item(self, item):
        if unused(self.items):
            self.items = []
        self.items.append(item)

    def set_start(self, start):
        self.start = start

    def add_services(self, services=None):
        if unused(self.services):
            self.services = []
        self.services.append(services)

    def add_annotation(self, annotation=None):
        if unused(self.annotations):
            self.annotations = []
        if annotation is None:
            annotation = Annotation(target=self.id)
            self.annotations.append(annotation)
            return annotation
        else:
            self.annotations.append(annotation)

    def add_service(self, serviceobj=None):
        if unused(self.service):
            self.service = []
        if serviceobj is None:
            serviceobj = service()
            self.service.append(serviceobj)
            return serviceobj
        else:
            if isinstance(serviceobj, service) or isinstance(serviceobj, dict):
                self.service.append(serviceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)

    def add_provider(self, providerobj=None):
        if unused(self.provider):
            self.provider = []
        if providerobj is None:
            providerobj = provider()
            self.provider.append(providerobj)
            return providerobj
        else:
            if isinstance(providerobj, provider):
                self.provider.append(providerobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to provider in %s" %
                    self.__class__.__name__)

    def add_canvastoitems(self, canvasobj=None):
        if unused(self.items):
            self.items = []
        if canvasobj is None:
            canvasobj = Canvas()
            self.items.append(canvasobj)
            return canvasobj
        else:
            if isinstance(canvasobj, Canvas):
                self.items.append(canvasobj)
            else:
                raise ValueError(
                    "Trying to add wrong object as canvas to items in %s" %
                    self.__class__.__name__)

    def add_structure(self, structure):
        if unused(self.structures):
            self.structures = []
        self.structures.append(structure)

    def add_rangetostructures(self, rangeobj=None):
        return checkstru(self, Range, rangeobj)


class Collection(CommonAttributes):
    def __init__(self):
        super(Collection, self).__init__()
        self.services = None
        self.annotations = None
        self.items = Required(
            "A collection object must have at least one item!")

    def add_service(self, serviceobj=None):
        if unused(self.service):
            self.service = []
        if serviceobj is None:
            serviceobj = service()
            self.service.append(serviceobj)
            return serviceobj
        else:
            if isinstance(serviceobj, service) or isinstance(serviceobj, dict):
                self.service.append(serviceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)

    def add_annotation(self, annotation):
        if unused(self.annotation):
            self.annotation = []
        self.annotation.append(annotation)

    def add_item(self, item):
        if unused(self.items):
            self.items = []
        self.items.append(item)


class Range(CommonAttributes):
    def __init__(self):
        super(Range, self).__init__()
        self.annotations = None
        self.items = Required("A range object must have at least one item!")
        self.supplementary = None

    def add_annotation(self, annotation):
        if unused(self.annotation):
            self.annotation = []
        self.annotation.append(annotation)

    def add_item(self, item):
        if unused(self.items):
            self.items = []
        self.items.append(item)

    def add_range_to_items(self):
        if unused(self.items):self.items = []
        newrange = Range()
        self.items.append(newrange)
        return newrange
    
    def add_SpecificResource_to_items(self):
        if unused(self.items):self.items = []
        sr = SpecificResource()
        self.items.append(sr )
        return sr 

    def set_start(self, start):
        # TODO: use addmethod
        self.start = start

    def set_supplementary(self, objid=None, extendbase_url=None):
        self.supplementary = supplementary()
        self.supplementary.set_id(objid, extendbase_url)

    def add_canvas_to_items(self, canvas_id):
        """Add a canvas to items by id of the canvas
        """
        if unused(self.items):
            self.items = []
        entry = {"id": canvas_id,
                 "type": "Canvas"}
        self.items.append(entry)


class SpecificResource(CommonAttributes):
    def __init__(self):
        super(SpecificResource, self).__init__()
        self.id = Recommended("An ID is recommended.")
        self.source = None

    def set_source(self, source):
        self.source = source

    def set_selector(self, selector):
        self.selector = selector

    def set_selector_as_PointSelector(self):
        ps = PointSelector()
        self.selector = ps
        return ps


class start(CommonAttributes):

    def __init__(self):
        super(start, self).__init__()
        self.profile = Recommended("Start object should have a profile.")
        self.source = None
        self.selector = None

    def set_type(self, mtype):
        if mtype != "Canvas":
            self.source = Required(
                "If you are not pointing to a Canvas please specify a source.")
            self.selector = Required(
                "If you are not pointing to a Canvas please specify a selector")
        self.type = mtype

    def set_source(self, source):
        self.source = source

    def set_selector(self, selector):
        self.selector = selector


class ImageApiSelector(object):
    def __init__(self) -> None:
        self.type = None
        self.region = None
        self.size = None
        self.rotation = None
        self.quality = None
        self.fromat = None

    def set_type(self, type):
        self.type = type

    def set_region(self, region):
        self.region = region

    def set_rotation(self, rotation):
        self.rotation = rotation

    def set_quality(self, quality):
        self.quality = quality

    def set_format(self, format):
        """Set the format of the IIIF type. IIIF: The specific media type
        (often called a MIME type) for a content resource, for example
        image/jpeg. This is important for distinguishing different formats of
        the same overall type of resource, such as distinguishing text in XML
        from plain text.

        Args: format (str): the format of the IIIF type, usually is the MIME
            e.g. image/jpg
        """
        msg = "Format should be in the form type/format e.g. image/jpg"
        assert "/" in format, msg
        assert format.split("/")[0].isalpha(), msg
        self.format = format


class PointSelector(object):
    """
    There are common use cases in which a point, rather than a range or area,
    is the target of the Annotation. For example, putting a pin in a map should
    result in an exact point, not a very small rectangle. Points in time are
    not very short durations, and user interfaces should also treat these
    differently. This is particularly important when zooming in (either
    spatially or temporally) beyond the scale of the frame of reference. Even
    if the point takes up a 10 by 10 pixel square at the user’s current
    resolution, it is not a rectangle bounding an area.

    It is not possible to select a point using URI Fragments with the Media
    Fragment specification, as zero-sized fragments are not allowed. In order
    to fulfill the use cases, this specification defines a new Selector class
    called PointSelector.

    Property	Description
    type	Required. Must be the value “PointSelector”.
    x	Optional. An integer giving the x coordinate of the point, relative to 
        the dimensions of the target resource.
    y	Optional. An integer giving the y coordinate of the point, relative to 
        the dimensions of the target resource.
    t	Optional. A floating point number giving the time of the point in seconds,
        relative to the duration of the target resource
    """

    def __init__(self) -> None:
        self.type = None
        self.x = None
        self.y = None
        self.t = None

    def set_type(self, type):
        self.type = type

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_t(self, t):
        self.t = t


class FragmentSelector(object):
    def __init__(self) -> None:
        self.type = "FragmentSelector"
        self.value = Required("A fragment selector must have a value!")

    def set_type(self, type):
        print("Type should be kept FragmentSelector")

    def set_value(self, value):
        self.value = value

    def set_xywh(self, x, y, w, h):
        self.value = "xywh=%i,%i,%i,%i" % (x, y, w, h)

 #json.dumps(g, default=lambda x:x.__dict__)
