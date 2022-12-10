"""Implementation of IIIF Presentation API 3.0

This module maps IIIF Presentation API 3.0 resources to Python classes.
The user `set` resources with a single element, and `add` to the list of the
resources multiple objects.

Example:
    >>> from IIIFpres import iiifpapi3
    >>> iiifpapi3.BASE_URL = r"https://iiif.io/api/0001-mvm-image/"
    >>> manifest = iiifpapi3.Manifest()
    >>> manifest.set_id(extendbase_url="manifest.json")
    >>> manifest.add_label("en", "Image 1")
    >>> canvas = manifest.add_canvas_to_items()
    >>> canvas.set_id(extendbase_url="canvas/p1")
    >>> canvas.set_height(1800)
    >>> canvas.set_width(1200)
    >>> annopage = canvas.add_annotationpage_to_items()
    >>> annopage.set_id(extendbase_url="page/p1/1")
    >>> annotation = annopage.add_annotation_to_items(target=canvas.id)
    >>> annotation.set_motivation("painting")
    >>> annotation.set_id(extendbase_url="annotation/p0001-image")
    >>> annotation.body.set_height(1800)
    >>> annotation.body.set_width(1200)
    >>> annotation.body.set_id("http://resources/page1-full.png")
    >>> annotation.body.set_format("image/png")
    >>> annotation.body.set_type("Image")
    >>> manifest.to_json()

Attributes:
    BASE_URL (str): Module level variable containing the URL to be preappend
        to iiifpapi3._CoreAttributes.set_id extend_baseurl

    LANGUAGES (list[str]): Module level variable containing a list of accepted
        languages. This variable is used for checking accepted languages, using
        the `IANA sub tag registry`_

    CONTEXT (str,list): Module level variable containing the context of the
        JSONLD file. Can be set to a list in case of multiple contexts.

    INVALID_URI_CHARACTERS (str): A list of charachters that are not accepted
        in the URL.

    BEHAVIOURS (list[str]): A list of accepted behaviours.

Warning:
    only language subtags are checked not variants or composite strings.
    You can manually add a language if you need to use subtags:

Example:
    >>> from IIIFpres import iiifpapi3,BCP47lang
    >>> iiifpapi3.LANGUAGES.append("de-DE-u-co-phonebk")

Todo:
    * The motivation of the Annotations must not be painting, and the target of
      the Annotations must include this resource or part of it
    * Annotations that do not have the motivation value painting must not be in
      pages referenced in items, but instead in the annotations property.
    * You have to also use ``sphinx.ext.todo`` extension

.. _IANA sub tag registry:
    https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
"""
from . import visualization_html
from .BCP47_tags_list import lang_tags
from .dictmediatype import mediatypedict
import json
import warnings
import copy
import re
global BASE_URL
BASE_URL = "https://"
global LANGUAGES
LANGUAGES = lang_tags
global MEDIATYPES
MEDIATYPES = mediatypedict
global CONTEXT
CONTEXT = "http://iiif.io/api/presentation/3/context.json"
global INVALID_URI_CHARACTERS
# removed comma which is used by IIIF Image API and #
INVALID_URI_CHARACTERS = r"""!"$%&'()*+ :;<=>?@[\]^`{|}~ """
global BEHAVIOURS
BEHAVIOURS = ["auto-advance",
              "no-auto-advance",
              "repeat",
              "no-repeat",
              "unordered",
              "individuals",
              "continuous",
              "paged",
              "facing-pages",
              "non-paged",
              "multi-part",
              "together",
              "sequence",
              "thumbnail-nav",
              "no-nav",
              "hidden"]


class Required(object):
    """HELPER CLASS

    Note:
        This is not an IIIF object but a class used by this software to
        identify required fields. This is equivalent to MUST statement in the
        guideline with the meaning of https://tools.ietf.org/html/rfc2119 .
    """

    def __init__(self, description=None):
        self.Required = description

    def __eq__(self, o):
        return True if isinstance(o, self.__class__) else False

    def __repr__(self):
        return 'Required attribute:%s' % self.Required


class Recommended(object):
    """HELPER CLASS

    Note:
        This is not an IIIF object but a class used by this software to
        identify recommended fields. This is equivalent to SHOULD statement in
        the guideline with the meaning of https://tools.ietf.org/html/rfc2119.
    """

    def __init__(self, description=None):
        self.Recommended = description

    def __eq__(self, o):
        return True if isinstance(o, self.__class__) else False

    def __repr__(self):
        return 'Recommended attribute:%s' % self.Recommended


# Note: we use None for OPTIONAL with the meaning of
# https://tools.ietf.org/html/rfc2119

# The package is based on 4 main helper functions:

def unused(attr):
    """This function checks if an attribute is not set (has no value in it).
    """
    if isinstance(attr, (Required, Recommended)) or attr is None:
        return True
    else:
        return False


# For performance optimization we can reduce the instantiation of Classes
if not __debug__:
    def Recommended(msg=None):
        return None

    def Required(msg=None):
        return None

    def unused(attr):
        return True if attr is None else False


def serializable(attr):
    """Check if attribute is Required and if so rise Value error.

    Args:
        attr : the value of the dictionary of the attribute of the instance.
    """
    if isinstance(attr, Required):
        raise ValueError(attr)
    if isinstance(attr, Recommended) or attr is None:
        return False
    else:
        return True


def add_to(selfx, destination, classx, obj, acceptedclasses=None, target=None):
    """Helper function used for adding IIIF object to to IIIF lists.

    Args:
        selfx (object): The class it-self
        destination (str): The class list attribute where the object will be stored.
        classx (object): The IIIF class that will be used for instantiating the
        obejct.
        obj (object): An already instantiated IIIF object.
        acceptedclasses (objects, optional): Accepted classes for obj. Defaults to None.
        target (str, optional): The target of an Annotation. Defaults to None.

    Raises:
        ValueError: When users try to add the wrong object to a list.

    Returns:
        IIIF object: A reference to an instance of the IIIF object.
    """
    # if the argument is none we create a list.
    if unused(selfx.__dict__[destination]):
        selfx.__dict__[destination] = []
    # if we are not providing a IIIF Object we create one.
    if obj is None and target is None:
        obj = classx()
        selfx.__dict__[destination].append(obj)
        return obj
    elif obj is None:
        # used for annotation.
        obj = classx(target=target)
        selfx.__dict__[destination].append(obj)
        return obj
    # otherwise we check that the object that we provide has the right type.
    else:
        if acceptedclasses is None:
            acceptedclasses = classx
        if isinstance(obj, acceptedclasses):
            selfx.__dict__[destination].append(obj)
        else:
            obj_name = obj.__class__.__name__
            class_name = selfx.__class__.__name__
            raise ValueError("%s object cannot be added to %s." %
                             (obj_name, class_name))


def check_valid_URI(URI):
    """Check if it is a valid URI.

    Args:
        URI (str): The URI to check.

    Returns:
        Bool: True if it is valid.
    """
    isvalid = True
    URI = URI.replace("https:/", "", 1)
    URI = URI.replace("http:/", "", 1)
    for indx, carat in enumerate(URI):
        if carat in INVALID_URI_CHARACTERS:
            if carat == " ":
                carat = "a space"
            arrow = " "*(indx) + "^"
            isvalid = False
            print("I found: %s here. \n%s\n%s" % (carat, URI, arrow))
    return isvalid


def check_ID(self, extendbase_url, objid):
    """Function for creating and checking IDs.

    Args:
        extendbase_url (str): The baseURL to extend.
        objid (str): A valid ID.

    Raises:
        ValueError: When trying to use both args together.
    """
    if extendbase_url:
        if objid:
            raise ValueError(
                "Set id using extendbase_url or objid not both.")

        assert BASE_URL.endswith("/") or extendbase_url.startswith("/"), \
            "Add / to extandbase_url or BASE_URL"
        joined = "".join((BASE_URL, extendbase_url))
        assert check_valid_URI(joined), "Special characters must be encoded"
        return joined
    else:
        assert objid.startswith("http"), "ID must start with http or https"
        if self.type == 'Canvas':
            assert "#" not in (objid), "URI of the canvas must not contain a fragment: #"
        assert check_valid_URI(objid), "Special characters must be encoded"
        return objid


# Let's group all the common arguments across the different types of collection
class _CoreAttributes(object):
    """HELPER CLASS

    Core attributes are the attributes in all the major classes/containers of
    IIIF namely: Collection, Manifest, Canvas, Range and Annotation Page,
    Annotation and Content and also in the minor classes such as SeeAlso and
    partOf.

    The core attributes are: ID, Type, Label

    ID an type attributes are required. The other might vary.
    """

    def __init__(self):
        self.id = Required(
            "A %s must have the ID property." %
            self.__class__.__name__)
        self.type = self.__class__.__name__
        # These might be suggested or may be used if needed.
        self.label = None

    def set_id(self, objid=None, extendbase_url=None):
        """Set the ID of the object

        https://iiif.io/api/presentation/3.0/#id

        IIIF: The URI that identifies the resource. If the resource is only
        available embedded within another resource (see the terminology section
        for an explanation of “embedded”), such as a Range within a Manifest,
        then the URI may be the URI of the embedding resource with a unique
        fragment on the end. This is not true for Canvases, which must have
        their own URI without a fragment.

        Args:
            objid (str, optional): A string corresponding to the ID of the
                object.Defaults to None.
            extendbase_url (str , optional): A string containing the URL part
                to be joined with the iiifpapi3.BASE_URL . Defaults to None.
        """
        self.id = check_ID(self, extendbase_url, objid)

    def add_label(self, language, text):
        """Add a label to the object.

        Args:
            language (str): The language of the label.
            text (str or list of str): The content of the label.

        Example:
            >>> iiifobj.add_label("en", "A painting")
            >>> iiifobj.add_label("en", ["Canvas","Oil"])

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
        assert language in LANGUAGES or language == "none", \
            """Language must be a valid BCP47 language tag or none.
            Please read https://git.io/JoQty. Please read https://git.io/JoQty."""
        assert isinstance(text, (str, list)), "text can be a string or a list of strings"
        if isinstance(text, list):
            for i in text:
                assert isinstance(i, str), "list in labels can contain only strings"
        else:
            text = [text]
        if language not in self.label:
            self.label[language] = text
        else:
            # faster way to join lists
            self.label[language][0:0] = text

    def json_dumps(
            self,
            dumps_errors=False,
            ensure_ascii=False,
            sort_keys=False,
            context=None):
        """Dumps the content of the object in JSON format.

        Args:
            dumps_errors (bool, optional): If set true it shows any problem
                found directly on the JSON file with a Required or Recommended
                tag.Defaults to False.
            ensure_ascii (bool, optional): Ensure ASCI are used.
                Defaults to False.
            sort_keys (bool, optional): Sort the keys. Defaults to False.
            context (_type_, optional): Add additional context. Defaults to None.

        Returns:
            str: The JSON object as a string.
        """
        if context is None:
            context = CONTEXT

        if not __debug__:
            # in debug Required and Recommend are None hence we use a faster
            # serializer
            print("Debug False")
            dumps_errors = True

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
        res = "".join(('{\n  "@context": %s,\n ' % json.dumps(context), res[3:]))
        return res

    def orjson_dumps(
            self,
            dumps_errors=False,
            context=None):
        """Dumps the content of the object in JSON format using orJSON library.

        Args:
            dumps_errors (bool, optional): If set true it shows any problem
                found, directly on the JSON file with a Required or Recommended
                tag.Defaults to False.
            ensure_ascii (bool, optional): Ensure ASCI are used.
                Defaults to False.
            sort_keys (bool, optional): Sort the keys. Defaults to False.
            context (str,list, optional): Add additional context. Defaults to None.

        Returns:
            str: The JSON object as a string.
        """
        import orjson
        if context is None:
            context = CONTEXT

        if not __debug__:
            # in debug Required and Recommend are None hence we use a faster
            # serializer
            print("Debug False")
            dumps_errors = True

        def serializerwitherrors(obj):
            return {k: v for k, v in obj.__dict__.items() if v is not None}

        def serializer(obj):
            return {k: v for k, v in obj.__dict__.items() if serializable(v)}

        if dumps_errors:
            res = orjson.dumps(
                self,
                default=serializerwitherrors,
                option=orjson.OPT_INDENT_2)
        else:
            res = orjson.dumps(
                self,
                default=serializer,
                option=orjson.OPT_INDENT_2)
        # little hack for fixing context first 3 chrs "{\n"
        res = "".join(('{\n  "@context": %s,\n ' % json.dumps(context),
                      res[3:].decode("utf-8")))
        return res

    def to_json(
            self,
            dumps_errors=False,
            ensure_ascii=False,
            sort_keys=False,
            context=None):
        """Return the object with the JSON syntax.

        Args:
            filename (str): The filename.
            save_errors (bool, optional): If True also the errors will be
                dumped. Defaults to False.
            ensure_ascii (bool, optional): If True only ASCI character will be
                used. Defaults to False.
            context (str,list, optional): Add additional contexts to the JSON.
                Defaults to None.
        Return:
            dict: a JSON dump of the object as dict.
        """
        res = json.loads(self.json_dumps(
            dumps_errors=dumps_errors,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys,
            context=context))
        return res

    def json_save(self, filename, save_errors=False, ensure_ascii=False, context=None):
        """Save the JSON object to file.

        Args:
            filename (str): The filename.
            save_errors (bool, optional): If True also the errors will be
                dumped. Defaults to False.
            ensure_ascii (bool, optional): If True only ASCI character will be
                used. Defaults to False.
            context (str,list, optional): Add additional contexts to the JSON.
                Defaults to None.
        """
        with open(filename, 'w') as f:
            f.write(self.json_dumps(
                dumps_errors=save_errors, ensure_ascii=ensure_ascii, context=context))

    def orjson_save(self, filename, save_errors=False, context=None):
        """Save the JSON object to file.

        Args:
            filename (str): The filename.
            save_errors (bool, optional): If True also the errors will be
                dumped. Defaults to False.
            ensure_ascii (bool, optional): If True only ASCI character will be
                used. Defaults to False.
            context (str,list, optional): Add additional contexts to the JSON.
                Defaults to None.
        """
        with open(filename, 'w') as f:
            f.write(self.orjson_dumps(
                dumps_errors=save_errors, context=context))

    def inspect(self):
        """Print the object in the derminal and show the missing required
        and recomended fields.

        Returns:
            bool: True.
        """
        jdump = self.json_dumps(dumps_errors=True)
        print(jdump)
        print("Missing required field: %s." % jdump.count('"Required":'))
        print("Missing recommended field: %s." % jdump.count('"Recommended":'))
        return True

    def show_errors_in_browser(self, getHTML=False):
        """Opens a browser window showing the required and the reccomended
        attributes.

        Args:
            getHTML (bool, optional): Returns the HTML to a variable.
            Defaults to False.

        Returns:
            str: If getHTML is set to true returns the HTML as str.
        """
        jsonf = self.json_dumps(dumps_errors=True)
        HTML = visualization_html.show_error_in_browser(jsonf, getHTML=getHTML)
        return HTML

    def __repr__(self):
        if unused(self.id):
            id_ = "Missing"
        else:
            id_ = self.id
        if unused(self.type):
            type_ = "Type Missing"
        else:
            type_ = self.type
        return " id:".join((type_, id_))


# Common helpers methods that will be used for constructing the IIIF objects.
class _Format(object):
    """HELPER CLASS for setting the Format.
    """
    def set_format(self, format):
        """Set the format of the resource.

        https://iiif.io/api/presentation/3.0/#format

        IIIF: The specific media type (often called a MIME type) for a content
        resource, for example image/jpeg. This is important for distinguishing
        different formats of the same overall type of resource, such as
        distinguishing text in XML from plain text.

        Args:
            format (str): Usually  is the MIME e.g. image/jpeg.
        """

        assert "/" in format, "Format should be in the form type/format e.g. image/jpeg"
        assert format.split("/")[0].isalpha(), "Format should be in the form type/format e.g. image/jpeg"
        assert not format == 'image/jpg', "Correct media type for jpeg should be image/jpeg not image/jpg"
        assert not format == 'image/tif', "Correct media type  for tiff should be image/tiff"
        assert any(format in sl for sl in MEDIATYPES.values()), "Not a IANA valid media type."
        self.format = format


class _HeightWidth(object):
    """HELPER CLASS for setting Height and Width.
    """

    def _checkpositiveinteger(self, value):
        """Return the value if positive integer.

        Args:
            value (int,str): Value to check.

        Returns:
            inputvalue (int): the value coerced to int.
        """
        #  because we accept string and int it is easier to assume they are int
        assert str(value).isdigit(), "Must be a digit. It was %s" % value
        assert str(value).isnumeric(), "Must be a positive integer"
        assert int(value) > 0, "Must be a positive integer"
        return int(value)

    def set_width(self, width):
        """Set the width of the resource.

        https://iiif.io/api/presentation/3.0/#width

        Args:
            width (int,str): The width of the resource.
        """
        self.width = self._checkpositiveinteger(width)

    def set_height(self, height):
        """Set the height of the resource.

        https://iiif.io/api/presentation/3.0/#height

        Args:
            height (int,str): The height of the resource.
        """
        self.height = self._checkpositiveinteger(height)

    def set_hightwidth(self, height, width):
        """Set both the height and the width of the resource.

        https://iiif.io/api/presentation/3.0/#height
        https://iiif.io/api/presentation/3.0/#width

        Args:
            height (int, str): The height of the resource.
            width (int, str): The width of the resource.
        """
        self.set_width(width)
        self.set_height(height)


class _Duration(object):
    """HELPER CLASS for setting Duration.
    """
    def set_duration(self, duration):
        """Set the duration of the resource.

        https://iiif.io/api/presentation/3.0/#duration

        Args:
            duration (float): The duration of the resource in seconds.
        """
        if unused(self.height):
            self.height = None
        if unused(self.width):
            self.width = None
        self.duration = float(duration)


class _ViewingDirection(object):
    """HELPER CLASS for adding ViewingDirection obejcts.
    """
    def set_viewingDirection(self, viewingDirection):
        """Set the viewing direction of the object.

        The viewing direction can be one of these:
        left-to-right	The object is displayed from left to right.
                        The default if not specified.
        right-to-left	The object is displayed from right to left.
        top-to-bottom	The object is displayed from the top to the bottom.
        bottom-to-top	The object is displayed from the bottom to the top.

        https://iiif.io/api/presentation/3.0/#viewingdirection

        Args:
            viewingDirection (str): The viewing direction.
        """
        viewingDirections = ["left-to-right",
                             "right-to-left",
                             "bottom-to-top",
                             "top-to-bottom"]
        msg = "viewingDirection must be one of these values %s" % viewingDirections
        assert viewingDirection in viewingDirections, msg
        self.viewingDirection = viewingDirection


class _MutableType(object):
    """HELPER CLASS In some IIIF objects the type can be changed.
    """
    def set_type(self, mtype):
        """Set the type or class of the resource.

        https://iiif.io/api/presentation/3.0/#type

        IIIF: For content resources, the value of type is drawn from other
        specifications.

        Args:
            mtype (str): the type of the object e.g. Image or Dataset.
        """
        assert not mtype[0].isdigit(), "First letter should not be a digit"
        self.type = mtype


class _ImmutableType(object):
    """HELPER CLASS In some IIIF objects the type cannot be changed.
    """
    def set_type(self, mtype=None):
        """In case of IIIF objects with predefined type this function won't
        change the type but will rise an error if you try to change it.

        https://iiif.io/api/presentation/3.0/#type

        Args:
            mtype (str, optional): the type of the object.
                Defaults to None.

        Raises:
            ValueError: In case you are trying to set a type.
        """
        cnm = self.__class__.__name__
        cty = self.type
        if mtype == cty or mtype is None:
            m = "%s type is by default %s, this set will be ingored." % (cnm, cty)
            warnings.warn(m)
        else:
            e = "The %s type must be set to '%s' was: %s " % (cnm, cty, mtype)
            raise ValueError(e)


# IIIF Objects:

# Some object have an helper method for adding them.
class _SeeAlso(object):
    """HELPER CLASS for adding SeeAlso objects.
    """
    def add_seeAlso(self, seeAlsoobj=None):
        """Add a seeAlso object to the resource.

        IIIF: A machine-readable resource such as an XML or RDF description
        that is related to the current resource that has the seeAlso property.

        https://iiif.io/api/presentation/3.0/#seealso

        Args:
            seeAlsoobj (iiifpapi3.seeAlso, optional): a iiifpapi3.seeAlso
            object. Defaults to None.

        Returns:
            iiifpapi3.seeAlso: if seeAlsoobj is None a iiifpapi3.seeAlso
        """
        return add_to(self, 'seeAlso', seeAlso, seeAlsoobj)


class seeAlso(_MutableType, _CoreAttributes, _Format):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#seealso

    IIIF: A machine-readable resource such as an XML or RDF description that is
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
        self.type = Required("SeeAlso type is required, e.g. dataset, Image")
        self.label = Recommended("SeeAlso label is recommended.")
        self.format = Recommended("SeeAlso type is recommended e.g. text/xml")
        self.profile = Recommended("Resources referenced by the seeAlso or"
                                   "service properties should have the profile"
                                   "property.")

    def set_profile(self, profile):
        # TODO: add check
        self.profile = profile


class partOf(_MutableType, _CoreAttributes):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#partof

    IIIF: A containing resource that includes the resource that has the partOf
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
        self.type = Required("Each partOf item must have a type")
        self.label = Recommended("Each partOf item should have the label property.")


class supplementary(_ImmutableType, _CoreAttributes):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#supplementary

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
        self.label = Recommended("An Annotation Collection should have the"
                                 "label property with at least one entry.")


class _Service(object):
    """HELPER CLASS for adding services.
    """
    def add_service(self, serviceobj=None):
        """Add a service to the resource.

        https://iiif.io/api/presentation/3.0/#service

        IIIF: A service that the client might interact with directly and gain
        additional information or functionality for using the resource that
        has the service property, such as from an Image to the base URI of an
        associated IIIF Image API service.

        Args:
            serviceobj (serviceobj, optional): A `iiifpapi3.service` object or
            a dict representing the service in case of older service.
            Defaults to None.

        Returns:
            iiifpapi3.service: In case serviceobj is None a iiifpapi3.service.
        """
        return add_to(self, 'service', service, serviceobj, (service, dict))


class service(_CoreAttributes, _HeightWidth, _Service):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#service

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
        self.type = Required(
            "Each object must have a type property."
        )
        self.profile = Recommended(
            "Each object should have a profile property.")

        self.width = None
        self.height = None
        self.service = None
        self.sizes = None

    def set_type(self, mytype):
        """Set the type of the service.

        https://iiif.io/api/presentation/3.0/#service

        IIIF: For content resources, the value of type is drawn from other
        specifications. Please see the Service Registry document for the
        details of currently known service types.

        Args:
            mtype (str): the type of the object e.g. Image or Dataset.
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
        # throws error with ExampleExtensionService
        self.type = mytype

    def set_profile(self, profile):
        """Set the profile of the resource.

        https://iiif.io/api/presentation/3.0/#profile

        IIIF: The value must be a string, either taken from the profiles
        registry or a URI.

        Args:
            profile (str): A schema or named set of functionality available
            from the resource.
        """
        self.profile = profile

    def add_size(self, width, height):
        """Add size to the sizes list of the service.

        This methods does not return an handler.

        Args:
            width (int,str): The width of the resource.
            height (int,str): The height of the resource.
        """
        if unused(self.sizes):
            self.sizes = []
        self.sizes.append({"width": int(width), "height": int(height)})


class thumbnail(_MutableType, _CoreAttributes, _Format, _HeightWidth,
                _Duration, _Service):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#thumbnail
    https://iiif.io/api/cookbook/recipe/0065-opera-multiple-canvases/

    IIIF: A content resource, such as a small image or short audio clip, that
    represents the resource that has the thumbnail property. A resource may
    have multiple thumbnail resources that have the same or different type
    and format.

    The value must be an array of JSON objects, each of which must have the
    id and type properties, and should have the format property. Images and
    videos should have the width and height properties, and time-based
    media should have the duration property. It is recommended that a IIIF
    Image API service be available for images to enable manipulations such
    as resizing.

    Example:
        >>> tmb = canvas.add_thumbnail()
        >>> tmb.set_id("https://act1-thumbnail.png")
        >>> tmb.set_type("Image")
    """
    def __init__(self):
        super(thumbnail, self).__init__()
        self.service = None


class _Thumbnail(object):
    """HELPER CLASS for adding thumbnail.
    """
    def add_thumbnail(self, thumbnailobj=None):
        """Add a thumbnail object to the resource.

        https://iiif.io/api/presentation/3.0/#thumbnail

        IIIF: A content resource, such as a small image or short audio clip, that
        represents the resource that has the thumbnail property. A resource may
        have multiple thumbnail resources that have the same or different type
        and format.

        Args:
            thumbnailobj (iiifpapi3.thumbnail, optional): A iiifpapi3.thumbnail
             object. Defaults to None.

        Returns:
            iiifpapi3.thumbnail: a iiifpapi3.thumbnail object if thumnailobj is
            None.
        """
        return add_to(self, 'thumbnail', thumbnail, thumbnailobj)


class _AddLanguage(object):
    """HELPER CLASS for adding languages.
    """
    def add_language(self, language):
        """add a language to the language list of the resource.

        https://iiif.io/api/presentation/3.0/#language-of-property-values

        Example:
            >>> manifest.add_language('en')

        Note:
            pyIIIFpres accept only single tag, in case you need subtags you
            need to add them to iiifpapi3.LANGUAGES::

            >>> from IIIFpres import iiifpapi3,BCP47lang
            >>> iiifpapi3.LANGUAGES.append("de-DE-u-co-phonebk")

            Please read https://git.io/JoQty.

        Args:
            language (str): A BCP 47 language tag e.g. en, it, es.
        """
        if unused(self.language):
            self.language = []
        assert language in LANGUAGES or language == "none", \
            "Language must be a valid BCP47 language tag or none."\
            "Please read https://git.io/JoQty."
        self.language.append(language)


class homepage(_MutableType, _CoreAttributes, _Format, _AddLanguage):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#homepage
    https://iiif.io/api/cookbook/recipe/0234-provider/

    IIIF: A web page that is about the object represented by the resource that
    has the homepage property. The web page is usually published by the
    organization responsible for the object, and might be generated by a
    content management system or other cataloging system. The resource must be
    able to be displayed directly to the user. Resources that are related, but
    not home pages, must instead be added into the metadata property, with an
    appropriate label or value to describe the relationship.

    Example:
        >>> homp = provider.add_homepage()
        >>> homp.set_id("https://digital.library.ucla.edu/")
        >>> homp.set_type("Text")
        >>> homp.add_label("en","UCLA Library Digital Collections")
        >>> homp.set_format("text/html")
        >>> homp.set_language("en")
    """

    def __init__(self):
        super(homepage, self).__init__()
        self.language = None
        self.label = Required("Homepage must have a label")
        self.type = Required("Homepage must have a type.")
        self.format = Recommended(
            "Hompage should have a format property e.g. Text.")

    def set_language(self, language):
        """ Deprecated method use `add_language` instead."""
        warnings.warn('Please use `add_language` instead.', DeprecationWarning)
        self.add_language(language=language)


class _Hompage(object):
    """HELPER CLASS for adding homepages.
    """

    def add_homepage(self, homepageobj=None):
        """add an homepage object to the resource.

        https://iiif.io/api/presentation/3.0/#homepage
        https://iiif.io/api/cookbook/recipe/0234-provider/

        IIIF: A web page that is about the object represented by the resource that
        has the homepage property. The web page is usually published by the
        organization responsible for the object, and might be generated by a
        content management system or other cataloging system. The resource must be
        able to be displayed directly to the user. Resources that are related, but
        not home pages, must instead be added into the metadata property, with an
        appropriate label or value to describe the relationship.

        Example:
            >>> homp = provider.add_homepage()
            >>> homp.set_id("https://digital.library.ucla.edu/")
            >>> homp.set_type("Text")
            >>> homp.add_label("en","UCLA Library Digital Collections")
            >>> homp.set_format("text/html")
            >>> homp.set_language("en")

        Args:
            homepageobj (iiifpapi3.homepage, optional): a iiifpapi3.homepage
            object. Defaults to None.

        Returns:
            iiifpapi3.homepage: If homepage is None a iiifpapi3.homepage object
            handler.
        """
        return add_to(self, 'homepage', homepage, homepageobj)


class provider(_ImmutableType, _CoreAttributes, _Hompage, _SeeAlso):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#provider
    https://iiif.io/api/cookbook/recipe/0234-provider/

    IIIF: An organization or person that contributed to providing the content
    of the resource. Clients can then display this information to the user to
    acknowledge the provider’s contributions. This differs from the
    requiredStatement property, in that the data is structured, allowing the
    client to do more than just present text but instead have richer
    information about the people and organizations to use in different
    interfaces.

    Examples:
        >>> prov = manifest.add_provider()
        >>> prov.set_id("https://id.loc.gov/authorities/n79055331")
        >>> prov.add_label(language='en', text="UCLA Library")
        >>> homp = prov.add_homepage()
        >>> homp.set_id("https://digital.library.ucla.edu/")
    """

    def __init__(self):
        super(provider, self).__init__()
        self.context = None
        self.type = "Agent"
        self.label = Required(
            "Agents must have the label property, and its value must be a"
            "JSON object as described in the languages section.")
        self.homepage = Recommended(
            "Agents should have the homepage property, and its value must be"
            "an array of JSON objects as described in the homepage section.")
        self.logo = Recommended(
            "Agents should have the logo property, and its value must be an"
            "array of JSON objects as described in the logo section.")
        self.seeAlso = None

    def add_logo(self, logoobj=None):
        """add a logo object to the resource

        https://iiif.io/api/presentation/3.0/#logo
        https://iiif.io/api/cookbook/recipe/0234-provider/

        Examples:
            >>> logo = prov.add_logo()
            >>> logo.set_id("https://UCLA-Library-Logo/full/full/0/default.png")
            >>> serv = logo.add_service()
            >>> serv.set_id("https://UCLA-Library-Logo")

        Args:
            logoobj (iiifpapi3.logo, optional): If logoobj is None a i
                iiifpapi3.logo object handler. Defaults to None.

        Returns:
            iiifpapi3.logo: iiifpapi3.logo if logoobj is None.
        """
        return add_to(self, 'logo', logo, logoobj)


class logo(_ImmutableType, _CoreAttributes, _HeightWidth, _Format, _Service):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#logo
    https://iiif.io/api/cookbook/recipe/0234-provider/

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

    Examples:
        >>> logo = prov.add_logo()
        >>> logo.set_id("https://UCLA-Library-Logo/full/full/0/default.png")
        >>> serv = logo.add_service()
        >>> serv.set_id("https://UCLA-Library-Logo")
    """

    def __init__(self):
        super(logo, self).__init__()
        self.type = "Image"
        self.format = Recommended(
            "Logo should have a format attribute e.g. image/png")
        self.service = Recommended(
            "Logo should have service attribute,"
            "you can add using srv = mylogo.add_service()")

    def add_label(self, language, text):
        """Label not permitted in logo."""
        raise ValueError("Label not permitted in logo.")


class rendering(_MutableType, _CoreAttributes, _Format):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#rendering
    https://iiif.io/api/cookbook/recipe/0046-rendering/

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

    Example:
        >>> rendering = manifest.add_rendering()
        >>> rendering.set_id("https://fixtures.iiif.io/other/UCLA/kabuki.pdf")
        >>> rendering.set_type("Text")
        >>> rendering.add_label("en","PDF version")
        >>> rendering.set_format("application/pdf")
    """

    def __init__(self):
        super(rendering, self).__init__()
        self.format = Recommended(
            "Rendering should have a format property e.g. application/pdf.")
        self.label = Required("Rendering object must have a label.")
        self.type = Required("Rendering should have a type")


class _ServicesList(object):
    """HELPER CLASS for adding service to service list.

    services is just a list grouping Service objects inside Manifest and
    Collection.

    """
    def add_service_to_services(self, serviceobj=None):
        """Add a service to the services list of the resource.

        https://iiif.io/api/presentation/3.0/#services

        IIIF: A list of one or more service definitions on the top-most
        resource of the document, that are typically shared by more than one
        subsequent resource. This allows for these shared services to be
        collected together in a single place, rather than either having their
        information duplicated potentially many times throughout the document,
        or requiring a consuming client to traverse the entire document
        structure to find the information.

        Args:
            serviceobj (iiifpapi3.service, optional): a iiifpapi3.service to be
            added. Defaults to None.

        Returns:
            iiifpapi3.service: If serviceobj is None a iiifpapi3.service object
            handler.
        """
        return add_to(self, 'services', service, serviceobj, (service, dict))


class languagemap(object):
    """HELPER CLASS
    This is not a IIIF type but is used for easing the construction of
    multilingual metadata and requiredstatements.

    Examples:
        >>> languagemap.add_label('Hosting','en')
        >>> languagemap.add_value('hosted by imagineRio','en')
    """

    def __init__(self):
        self.label = Required(
            "The metadata/requiredstatements must have at least a label")
        self.value = Required(
            "The metadata/requiredstatements must have at least a value")

    def add_value(self, value, language="none"):
        """Add the value of the language map.

        Args:
            value (str): The value of the language map e.g. Author:
            language (str, optional): The language of the value e.g. en.
            Defaults to "none".
        """
        if unused(self.value):
            self.value = {}
        if not isinstance(value, list):
            value = [value]

        # TODO: if html must begin with < and end with >
        # https://iiif.io/api/presentation/3.0/#45-html-markup-in-property-values
        # possible hack ignoring self-closing tags?
        # if any(['</' in i for i in value]):
        #    assert any([i.startswith('<') and i.endswith('>') for i in value]),\
        #        'if html must begin with < and end with >'
        assert language in LANGUAGES or language == "none", \
            "Language must be a valid BCP47 language tag or none."\
            "Please read https://git.io/JoQty."
        self.value[language] = value

    def add_label(self, label, language="none"):
        """Add the label of the language map.

        Example:
            >>> iiifobj.add_label("A painting","en")
            >>> iiifobj.add_label(["Canvas","Oil"],"en")

        Args:
            label (str): The value of the language map e.g. Dante Alighieri:
            language (str, optional): The language of the value e.g. it.
            Defaults to "none".

        """
        if unused(self.label):
            self.label = {}
        if not isinstance(label, list):
            label = [label]
        # TODO: check that is not html
        # https://iiif.io/api/presentation/3.0/#45-html-markup-in-property-values
        assert language in LANGUAGES or language == "none", \
            "Language must be a valid BCP47 language tag or none." \
            "Please read https://git.io/JoQty."
        self.label[language] = label


##
# COMMON ATTRIBUTES TO MAJOR CONTAINERS
##

class _CommonAttributes(_CoreAttributes, _Thumbnail, _Service, _Hompage,
                        _SeeAlso):
    """HELPER CLASS
    Common attributes are the attributes that are in common with all the major
    classes/container of IIIF namely: Collection, Manifest, Canvas, Range and
    Annotation Page, Annotation and Content.

    ID an type attributes are required. The other might vary.
    """

    def __init__(self):
        super(_CommonAttributes, self).__init__()
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
        self.provider = None

    def add_metadata(self, label=None, value=None, language_l="none",
                     language_v="none", entry=None):
        """Add a metadata object to the resource and returns a languge map.

        https://iiif.io/api/presentation/3.0/#metadata
        https://iiif.io/api/cookbook/recipe/0029-metadata-anywhere/

        IIIF: An ordered list of descriptions to be displayed to the user when
        they interact with the resource, given as pairs of human readable label
        and value entries. The content of these entries is intended for
        presentation only; descriptive semantics should not be inferred.
        An entry might be used to convey information about the creation of the
        object, a physical description, ownership information, or other purposes.

        Args:
            label (str, optional): The label e.g. `Author:`. Defaults to None.
            value (str, optional): The value e.g. `Herman Melville`.
                Defaults to None.
            language_l (str, optional): the language of the label e.g. `en`.
                Defaults to "none".
            language_v (str, optional): the langugage of the value e.g. `none`
                or `en`. Defaults to "none".
            entry (dict, optional): A metadata dict. Defaults to None.

        Examples:
            >>> iiifobj.add_metadata("Author:","Herman Melville","en","en")
            >>> md = canvas.add_metadata()
            >>> md.add_label("Author:","en")
            >>> md.add_value("Herman Meliville","en")

        Raises:
            ValueError: If an entry is provided toghether with other arguments.

        Returns:
            iiifpapi3.languagemap: If no arguments are passed a language map
            is return as handler so that the user can fill the fields.
        """
        if unused(self.metadata):
            self.metadata = []

        if label is None and value is None and entry is None:
            languagemapobj = languagemap()
            self.metadata.append(languagemapobj)
            return languagemapobj

        if (label is not None or value is not None) and entry is not None:
            raise ValueError(
                "Either use entry arguments or a combination "
                "of other arguments, NOT both.")

        if not isinstance(value, list):
            value = [value]
        assert language_l in LANGUAGES or language_l == "none", \
            "Language must be a valid BCP47 language tag or none." \
            "Please read https://git.io/JoQty."

        if entry is None:
            entry = {"label": {language_l: [label]},
                     "value": {language_v: value}}
        self.metadata.append(entry)

    def add_summary(self, language, text):
        """Add directly an entry in the summary dict without returning handler.

        https://iiif.io/api/presentation/3.0/#summary
        https://iiif.io/api/cookbook/recipe/0006-text-language

        IIIF: A short textual summary intended to be conveyed to the user when
        the metadata entries for the resource are not being displayed.
        This could be used as a brief description for item level search results,
        for small-screen environments, or as an alternative user interface when
        the metadata property is not currently being rendered.

        Args:
            language (str): The language of the summary.
            text (str): The text of the summary.
        """
        if unused(self.summary):
            self.summary = {}
        assert language in LANGUAGES or language == "none",\
            "Language must be a valid BCP47 language tag or none."\
            "Please read https://git.io/JoQty."
        self.summary[language] = [text]

    def set_requiredStatement(self, label=None, value=None, language_l=None,
                              language_v=None, entry=None):
        """Set/add a requiredStatement to the resource and returns a languge map.

        https://iiif.io/api/presentation/3.0/#requiredstatement
        https://iiif.io/api/cookbook/recipe/0006-text-language/

        IIIF: For example, the requiredStatement property could be used to
        present copyright or ownership statements, an acknowledgement of the
        owning and/or publishing institution, or any other text that the
        publishing organization deems critical to display to the user.

        Args:
            label (str, optional): The label e.g. `Attribution:`. Defaults to None.
            value (str, optional): The value e.g. `Provided courtesy of Example
            Institution`.
            Defaults to None.
            language_l (str, optional): the language of the label e.g. `en`.
            Defaults to "none".
            language_v (str, optional): the langugage of the value e.g. `none`
            or `en`. Defaults to "none".
            entry (dict, optional): A metadata dict. Defaults to None.

        Raises:
            ValueError: If an entry is provided toghether with other arguments.

        Returns:
            iiifpapi3.languagemap: If no arguments are passed a language map
            is returned as handler so that the user can fill the fields.

        Examples:
            >>> reqstat = manifest.set_requiredStatement()
            >>> reqstat.add_label(language="en", label="Held By")
            >>> reqstat.add_label(language="fr", label="Détenu par")
            >>> reqstat.add_value(value="Musée d'Orsay, Paris, France")
        """
        if label is None and value is None and entry is None:
            languagemapobj = languagemap()
            self.requiredStatement = languagemapobj
            return languagemapobj

        if unused(self.requiredStatement):
            self.requiredStatement = {}

        if (label is not None or value is not None) and entry is not None:
            raise ValueError(
                "Either use entry arguments or a combination of other"
                "arguments, NOT both.")
        if entry is None:
            if language_l is None:
                language_l = "none"
            if language_v is None:
                language_v = "none"
            assert language_l in LANGUAGES or language_l == "none",\
                "Language must be a valid BCP47 language tag or none. "\
                "Please read https://git.io/JoQty."
            assert language_v in LANGUAGES or language_v == "none",\
                "Language must be a valid BCP47 language tag or none. "\
                "Please read https://git.io/JoQty."
            entry = {"label": {language_l: [label]},
                     "value": {language_v: [value]}}
        self.requiredStatement = entry

    def set_rights(self, rights):
        """set the rights of the resources.

        https://iiif.io/api/presentation/3.0/#rights

        IIIF: A string that identifies a license or rights statement that
        applies to the content of the resource, such as the JSON of a Manifest
        or the pixels of an image. The value must be drawn from the set of
        Creative Commons license URIs, the RightsStatements.org rights
        statement URIs, or those added via the extension mechanism.
        The inclusion of this property is informative, and for example could be
        used to display an icon representing the rights assertions.

        Args:
            rights (str): an URL pointing to a licence.
        """
        licenceurls = ["http://creativecommons.org/licenses/",
                       "http://creativecommons.org/publicdomain/mark/",
                       "http://rightsstatements.org/vocab/"]
        assert any([rights.startswith(i) for i in licenceurls]
                   ), "Must start with:%s" % str(licenceurls)[1:-1]
        self.rights = rights

    def add_requiredStatement(self, label=None, value=None, language_l=None,
                              language_v=None, entry=None):
        warnings.warn('Please use set_requiredStatement instead.', DeprecationWarning)
        return self.set_requiredStatement(label, value, language_l, language_v, entry)

    def add_behavior(self, behavior):
        """add a one ore more behaviours to the resource without returning.

        https://iiif.io/api/presentation/3.0/#behavior
        https://iiif.io/api/cookbook/recipe/0009-book-1/

        IIIF: A set of user experience features that the publisher of the
        content would prefer the client to use when presenting the resource.
        This specification defines the values below. Others may be
        defined externally as an extension.

        `auto-advance`, `no-auto-advance`, `repeat`, `no-repeat`, `unordered`,
        `individuals`, `continuous`, `multi-part`, `facing-pages`, `non-paged`,
        `together`, `paged`, `sequence`, `thumbnail-nav`, `no-nav`, `hidden`,

        Examples:
            >>> iiifobj.add_behavior("thumbnail-nav")

        Warnings:
            This function does not test disjoints with inherited behaviours.

        Args:
            behavior (str): the behaviour to be added.
        """
        # TODO: should we assert if behaviour disjoint with others?
        assert behavior in BEHAVIOURS, f"{behavior} is not valid. See https://git.io/Jo7r9."
        # this might leave an empty list if user fail the assertion
        if unused(self.behavior):
            self.behavior = []
        if behavior == "auto-advance":
            assert self.type in ["Collection", "Manifest", "Canvas", "Range"],\
                f"{behavior} behavior is valid only for Collection, Manifest, Canvas, Range"
            if self.type == "Range":
                #  TODO: Ranges that include or are Canvases with at least the duration dimension.
                pass
            assert "no-auto-advance" not in self.behavior,\
                "Conflicts with no-auto-advance"

        elif behavior == "no-auto-advance":
            assert self.type in ["Collection", "Manifest", "Canvas", "Range"],\
                f"{behavior} behavior is valid only for Collection, Manifest, Canvas, Range"
            assert "auto-advance" not in self.behavior, "Conflicts with auto-advance"

        elif behavior == "repeat":
            assert self.type in ["Collection", "Manifest"],\
                f"{behavior} behavior is valid only for Collection and Manifest"
            # TODO: assert any([True for i in self.items if i.type == "Canvas" and i.duration is not None]), "This behaviour should be used when canvas has duration property. Add it after the canvas definition."
            assert "no-repeat" not in self.behavior, "Conflicts with no-repeat"

        elif behavior == "no-repeat":
            assert self.type in ["Collection", "Manifest"],\
                f"{behavior} behavior is valid only for Collection and Manifest"
            assert "repeat" not in self.behavior, "Conflicts with repeat"

        elif behavior == "unordered" or behavior == "individuals":
            assert self.type in ["Collection", "Manifest", "Range"],\
                f"{behavior} behavior is valid only for Collection, Manifest,Range"
            dsjntbhv = ("individuals", "continuous", "paged")
            assert not any(x in dsjntbhv for x in self.behavior),\
                f"Conflicts with one of: {dsjntbhv}"

        elif behavior == "continuous":
            assert self.type in ["Collection", "Manifest", "Range"],\
                f"{behavior} behavior is valid only for Collection, Manifest,Range"
# TODO: assert any([True for i in self.items if i.type == "Canvas" and i.height is not None]), "This behaviour should be used when canvas has duration property. Add it after the canvas definition."
            dsjntbhv = ("individuals", "unordered", "paged")
            assert not any(x in dsjntbhv for x in self.behavior),\
                f"Conflicts with one of: {dsjntbhv}"

        elif behavior == "paged":
            assert self.type in ["Collection", "Manifest", "Range"],\
                f"{behavior} behavior is valid only for Collection, Manifest,Range"
            dsjntbhv = ("individuals",
                        "continuous",
                        "facing-pages",
                        "unordered",
                        "non-paged")
            assert not any(x in dsjntbhv for x in self.behavior),\
                f"Conflicts with one of: {dsjntbhv}"

        elif behavior == "facing-pages" or behavior == "non-paged":
            assert self.type == "Canvas",\
                f"{behavior} behavior is valid only on on Canvases, where the "\
                "Canvas has at least height and width dimensions."
            assert self.height is not None,\
                f"with {behavior} behavior Canvas must have height property."
            assert self.width is not None,\
                f"with {behavior} behavior Canvas must have width property."
            if behavior == "facing-pages":
                dsjntbhv = ("paged", "non-paged")
            else:
                dsjntbhv = ("facing-pages", "paged")
            assert not any(x in dsjntbhv for x in self.behavior),\
                f"Conflicts with one of: {dsjntbhv}"

        elif behavior == "multi-part" or behavior == "together":
            assert self.type == "Collection",\
                f"{behavior} behavior is valid only on Collections."
            if behavior == "multi-part":
                dsjntbhv = "together"
            else:
                dsjntbhv = "multi-part"
            assert dsjntbhv not in self.behavior,\
                f"Conflicts with {dsjntbhv}"

        elif behavior in ["sequence", "thumbnail-nav", "no-nav"]:
            assert self.type == "Range",\
                f"{behavior} behavior is valid only on Ranges."
# TODO: Valid only on Ranges, where the Range is referenced in the structures property of a Manifest
            disjoint = ["sequence", "thumbnail-nav", "no-nav"]
            assert not any(x in disjoint.remove(behavior) for x in self.behavior),\
                f"Conflicts with one of: {disjoint}"

        elif behavior == "hidden":
            vc = ["Annotation",
                  "AnnotationCollection",
                  "AnnotationPage",
                  "SpecificResource",
                  "Choice"]
            assert self.type in vc, f"{behavior} behavior is valid only on {vc}."

        self.behavior.append(behavior)

    def add_partOf(self, partOfobj=None):
        """Add a partOf to the partOfs list of the resource.

        https://iiif.io/api/presentation/3.0/#partof

        IIIF: A containing resource that includes the resource that has the
        partOf property.

        Args:
            partOfobj (iiifpapi3.partOf, optional): a iiifpapi3.partOf to be
                added. Defaults to None.

        Returns:
            iifpapi3.partOf: If partOfobj is None a iiifpapi3.partOf object
                handler.
        """
        return add_to(self, 'partOf', partOf, partOfobj)

    def add_rendering(self, renderingobj=None):
        """Add a rendering to the renderings list of the resource.

        https://iiif.io/api/presentation/3.0/#rendering
        https://iiif.io/api/cookbook/recipe/0046-rendering/

        IIIF: A resource that is an alternative, non-IIIF representation of the
        resource that has the rendering property.

        Example:
            >>> rendering = manifest.add_rendering()
            >>> rendering.set_id("https://fixtures.iiif.io/other/UCLA/kab.pdf")
            >>> rendering.set_type("Text")
            >>> rendering.add_label("en", "PDF version")
            >>> rendering.set_format("application/pdf")

        Args:
            renderingobj (iiifpapi3.rendering, optional): a iiifpapi3.rendering
            to be added. Defaults to None.

        Returns:
            iiifpapi3.rendering: If renderingobj is None a iiifpapi3.rendering
            object handler.
        """
        return add_to(self, 'rendering', rendering, renderingobj)

    def add_provider(self, providerobj=None):
        """Add a provider to the provider list of the resource.

        https://iiif.io/api/presentation/3.0/#provider
        https://iiif.io/api/cookbook/recipe/0234-provider/

        IIIF: An organization or person that contributed to providing the
        content of the resource.

        Example:
            >>> prov = manifest.add_provider()
            >>> prov.set_id("https://id.loc.gov/authorities/n79055331")
            >>> prov.add_label(language='en', text="UCLA Library")
            >>> homp = prov.add_homepage()
            >>> homp.set_id("https://digital.library.ucla.edu/")

        Args:
            providerobj (iiifpapi3.provider, optional): a iiifpapi3.provider
            to beadded. Defaults to None.

        Returns:
            iiifpapi3.provider: If providerobj is None a iiifpapi3.provider
            object handler.
        """
        return add_to(self, 'provider', provider, providerobj)


class Annotation(_CommonAttributes):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#56-annotation

    Annotations follow the Web Annotation data model.

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

    def __init__(self, target=Required()):
        super(Annotation, self).__init__()
        self.motivation = None  # TODO: Check if this is required
        self.body = None  # TODO: Check if this is required
        self.target = target
        self.metadata = None

    def set_motivation(self, motivation):
        """set the motivation of the annotation.

        https://iiif.io/api/presentation/3.0/#values-for-motivation

        Args:
            motivation (str): the motivation of the annotation usually is
            `painting`, `supplementing`, `commenting`, `tagging`

        IIIF: this specification defines only motivations for Annotations that
        target Canvases. These motivations allow clients to determine how the
        Annotation should be rendered, by distinguishing between Annotations
        that provide the content of the Canvas, from ones with externally
        defined motivations which are typically comments about the Canvas.

        Additional motivations may be added to the Annotation to further
        clarify the intent, drawn from extensions or other sources. Other
        motivation values given in the Web Annotation specification should be
        used where appropriate, and examples are given in the Presentation API
        Cookbook.

        painting - Resources associated with a Canvas by an Annotation that has
        the motivation value painting must be presented to the user as the
        representation of the Canvas. The content can be thought of as being of
        the Canvas.

        supplementing - Resources associated with a Canvas by an Annotation
        that has the motivation value supplementing may be presented to the
        user as part of the representation of the Canvas, or may be presented
        in a different part of the user interface. The content can be thought
        of as being from the Canvas.

        """
        motivations = ["painting", "supplementing", "commenting", "tagging"]
        if motivation not in motivations:
            warnings.warn("Motivation not in %s" % motivations)
        if motivation == "painting":
            self.body = bodypainting()
        if motivation == "commenting" or motivation == "tagging":
            self.body = bodycommenting()
        self.motivation = motivation

    def set_target_specific_resource(self, specificresource=None):
        """Set a specific resource as the target of the annotation.

        This function will set the target of the specific resource as an
        object.

        Examples:
            https://iiif.io/api/cookbook/recipe/0261-non-rectangular-commenting/
            >>> annotation.set_target_specific_resource()
            >>> annotation.target.set_source(canvas.id)
            >>> svg ="<svg xmlns='http://www.w3.org/2000/svg' ... > ... </svg>"
            >>> annotation.target.set_selector_as_SvgSelector(value=svg)

        Args:
            specificresource (`iiifpapi3.sepcificreosurce`, optional): a
             `iiifpapi3.sepcificreosurce` object. Defaults to None.

        Raises:
            ValueError: if you add the wrong object.

        Returns:
            `iiifpapi3.sepcificreosurce` : A reference to the object.
        """
        if specificresource is None:
            specificresource = SpecificResource()
            self.target = specificresource
            return specificresource
        else:
            if isinstance(specificresource, SpecificResource):
                self.target = specificresource
            else:
                raise ValueError(
                    "Trying to add wrong object to target in %s" %
                    self.__class__.__name__)


class AnnotationPage(_CommonAttributes):
    """IIIF resource.

    https://iiif.io/api/presentation/3.0/#55-annotation-page

    IIIF: Annotations are collected together in Annotation Page resources,
    which are included in the items property from the Canvas. Each Annotation
    Page can be embedded in its entirety, if the Annotations should be
    processed as soon as possible when the user navigates to that Canvas, or a
    reference to an external page.

    """
    # TODO: AnnotationPage type MUST be AnnotationPage?
    def __init__(self):
        super(AnnotationPage, self).__init__()
        self.items = Recommended(
            "The annotation page should incude at least one item.")

    def add_item(self, item):
        """Add an item (Annotation) to the AnnotationPage.

        Same as `add_annotation_to_items` but doesn't return.

        An Annotation Page should have the items property with at least one
        item. Each item must be an Annotation.

        Args:
            item (Annotation): The Annotation
        """
        add_to(self, 'items', Annotation, item)

    def add_annotation_to_items(self, annotation=None, target=None):
        return add_to(self, 'items', Annotation, annotation, target=target)


class AnnotationCollection(_CommonAttributes):
    """IIIF resource.

    https://iiif.io/api/presentation/3.0/#58-annotation-collection

    Annotation Collections represent groupings of Annotation Pages that should
    be managed as a single whole, regardless of which Canvas or resource they
    target. This allows, for example, all of the Annotations that make up a
    particular translation of the text of a book to be collected together. A
    client might then present a user interface that allows all of the
    Annotations in an Annotation Collection to be displayed or hidden according
    to the user’s preference.

    """
    def __init__(self):
        super(AnnotationCollection, self).__init__()
        self.label = Recommended("An Annotation Collection should have the"
                                 "label property with at least one entry.")

    def set_id(self, objid, extendbase_url=None):
        """Set the ID of the object

        https://iiif.io/api/presentation/3.0/#id
        https://iiif.io/api/presentation/3.0/#58-annotation-collection

        IIIF: Annotation Collections must have a URI, and it should be an
        HTTP(S) URI.

        Note:
            Usually ID must be HTTP(S) in this case it seems not.

        Args:
            objid (str, optional): A string corresponding to the ID of the
            object.
            Defaults to None.
            extendbase_url (str , optional): A string containing the URL part
            to be joined with the iiifpapi3.BASE_URL . Defaults to None.
        """
        try:
            return super().set_id(objid=objid, extendbase_url=extendbase_url)
        except AssertionError:
            warnings.warn("%s is not an http, AnnotationCollections should use HTTP(S) URI")
            self.id = objid


class _AnnotationsList(object):
    """HELPER CLASS
    Some IIIF obejcts have a list of annotations. This list can contain
    only AnnotationPages.
    """
    def add_annotationpage_to_annotations(self, annopageobj=None):
        """Add an AnnotationPage to the annotations list.

        https://iiif.io/api/presentation/3.0/#55-annotation-page

        IIIF: Annotations are collected together in Annotation Page resources,
        which are included in the items property from the Canvas. Each
        Annotation Page can be embedded in its entirety, if the Annotations
        should be processed as soon as possible when the user navigates to that
        Canvas, or a reference to an external page.

        https://iiif.io/api/presentation/3.0/#annotations

        IIIF: An ordered list of Annotation Pages that contain commentary or
        other Annotations about this resource, separate from the Annotations
        that are used to paint content on to a Canvas.

        Args:
            annopageobj (AnnnotationPage, optional): An `AnnotationPage`
            object. Defaults to None.

        Returns:
            AnnotationPage: An `AnnotationPage` if `annopageobj` is `None`.
        """
        return add_to(self, 'annotations', AnnotationPage, annopageobj)


class _AddAnnoP2Items(object):
    """HELPER CLASS for adding annotationpage to items.
    """

    def add_annotationpage_to_items(self, annotationpageobj=None, target=None):
        """Add an annotation page to the items list of the object.

        Args:
            annotationpageobj (`iiifpapi3.AnnotationPage, optional): An object
            instance of `iiifpapi3.AnnotationPage`. Defaults to None.
            target (str, optional): The `target`of the annotation.
            Defaults to None.

        Returns:
            iiifpapi3.AnnotationPage(): if `annotationpageobj` is None.
        """
        return add_to(self,
                      'items',
                      AnnotationPage,
                      annotationpageobj,
                      target=target)


class contentresources(_MutableType, _CommonAttributes, _HeightWidth,
                       _Duration, _AnnotationsList, _Format, _AddAnnoP2Items):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#57-content-resources

    IIIF: Content resources are external web resources that are referenced
    from within the Manifest or Collection.
    This includes images, video, audio, data, web pages or any other format.
    """
    def __init__(self):
        super(_CommonAttributes, self).__init__()
        self.annotations = None
        self.type = Required("The type of the content resource must be "
                             "included,and should be taken from the table"
                             "listed under the definition of type.")
        self.format = Recommended("The format of the resource should be"
                                  "included and, if so, should be the media"
                                  "type that is returned when the resource is"
                                  "dereferenced.")
        self.profile = Recommended("The profile of the resource, if it has one,"
                                   "should also be included")

    def add_annotation(self, annotation=None):
        """Please use `add_annotationpage_to_annotations` instead."""
        warnings.warn('Please use `add_annotationpage_to_annotations` instead.',
                      DeprecationWarning)
        return add_to(self, 'annotations', Annotation, annotation, target=self.id)


class bodycommenting(_ImmutableType):
    def __init__(self):
        self.type = "TextualBody"
        self.value = None
        self.language = None

    def set_format(self, format):
        """Set the format of the resource.

        https://iiif.io/api/presentation/3.0/#format

        IIIF: The specific media type (often called a MIME type) for a content
        resource, for example image/jpeg. This is important for distinguishing
        different formats of the same overall type of resource, such as
        distinguishing text in XML from plain text.

        Note:
            pyIIIFpres will check that the format is in `MEDIATYPES['text']`
            If you are confident with the format you are using set the format
            using `obj.format = ...` or run the script with -O flag.
            or append your format to the MEDIATYPES:
            >>> MEDIATYPES['text'].append('myformat')

        Args:
            format (str): Usually  is the MIME e.g. text/plain.
        """
        assert format in MEDIATYPES['text'], "Not a valid MEDIATYPE for text"
        self.format = format

    def set_value(self, value):
        """Set the value of the TextualBody e.g. `"Comment text"`

        Args:
            value (str): The value of the TextualBody
        """
        self.value = str(value)

    def set_language(self, language):
        """Set the language of the TextualBody value.

        Args:
            language (str): The language of the TextualBody value e.g. "en"
        """
        assert language in LANGUAGES or language == "none",\
            "Language must be a valid BCP47 language tag or none."\
            "Please read https://git.io/JoQty."
        self.language = language


class bodypainting(contentresources, _Service, _AddLanguage):
    """Pseudo-IIIF resource

    IIIF: the content associated with a Canvas (and therefore the content of a
    Manifest) is provided by the body property of Annotations with the painting
    motivation.
    """
    def __init__(self):
        super(bodypainting, self).__init__()
        self.height = None
        self.width = None
        self.duration = None
        self.service = None
        self.language = None
        self.items = None

    def add_choice(self, choiceobj=None):
        """Add a Choice to the body of the annotation.

        https://preview.iiif.io/cookbook/3333-choice/recipe/0033-choice/

        Args:
            choiceobj (dict, optional): A dictionary representing the Choice.
            Defaults to None.

        Raises:
            ValueError: if you try to add the wrong object type.

        Returns:
            iiifpapi3.bodypainting(): A `bodypainting` instance.
        """
        assert isinstance(self.type, Required) or self.type == "Choice",\
            "Body type must be Choice"
        if unused(self.items):
            self.items = []
        if choiceobj is None:
            self.id = None
            self.format = None
            self.height = None
            self.width = None
            # TODO: myabe assert these properties are not defined
            choice = bodypainting()
            self.type = "Choice"
            self.items.append(choice)
            # TODO: remove items from the new bodypainting?
            return choice
        else:
            if isinstance(choiceobj, bodypainting) or isinstance(choiceobj, dict):
                self.items.append(choiceobj)
            else:
                raise ValueError(
                    "Trying to add wrong object to service in %s" %
                    self.__class__.__name__)


class _CMRCattributes(_CommonAttributes, _AnnotationsList, _ImmutableType):
    """HELPER CLASS
    This is another class for grouping the attributes in common with
    Canvas, Manifest, Range and Collection.

    Namely: `placeholderCanvas`, `accompanyingCanvas`, `NavDate`

    All these values are optional.
    """
    def __init__(self):
        super(_CMRCattributes, self).__init__()
        self.placeholderCanvas = None
        self.accompanyingCanvas = None
        self.navDate = None

    def _apcanvas(self, canvastype, canvas):
        """An helper method for setting placeholder and accompany Canvas.

        Args:
            canvastype (str): The canvas type.
            canvas (iiifpapi3.Canvas): A canvas object.

        Returns:
            iiifpapi3.Canvas: A modified Canvas to be used as  Canvas.
        """
        if hasattr(self, canvastype):
            if canvas is None:
                phcnv = Canvas()
            else:
                assert isinstance(canvas, Canvas), "Use a valid iiifpapi3.Canvas"
                phcnv = copy.copy(canvas)
            delattr(phcnv, 'placeholderCanvas')
            delattr(phcnv, 'accompanyingCanvas')
            self.placeholderCanvas = phcnv
            return phcnv
        else:
            raise AttributeError("A %s can not have a %s" % (canvastype, canvastype))

    def set_placeholderCanvas(self, canvas=None):
        """set a placeholderCanvas to the object.

        https://iiif.io/api/presentation/3.0/#placeholdercanvas

        IIIF: A single Canvas that provides additional content for use before
        the main content of the resource that has the placeholderCanvas
        property is rendered, or as an advertisement or stand-in for that
        content.

        Args:
            phcnv (iiifpapi3.Canvas, optional): A Canvas to be used as
            placeholderCanvas.

        Raises:
            AttributeError: if you are tyring to ad a placeholder Canvas to a
            placeholder Canvas.

        Returns:
            iiifpapi3.Canvas: A modified Canvas to be used as placeholder
            Canvas.
        """
        return self._apcanvas('placeholderCanvas', canvas=canvas)

    def set_accompanyingCanvas(self, canvas=None):
        """set a accompanyingCanvas to the object.

        https://iiif.io/api/presentation/3.0/#accompanyingcanvas

        IIIF: A single Canvas that provides additional content for use while
        rendering the resource that has the accompanyingCanvas property.

        Args:
            phcnv (iiifpapi3.Canvas, optional): A Canvas to be used as
            accompanyingCanvas.

        Raises:
            AttributeError: if you are tyring to ad a accompanying Canvas to a
            accompanying Canvas.

        Returns:
            iiifpapi3.Canvas: A modified Canvas to be used as accompanying
            Canvas.
        """
        return self._apcanvas('accompanyingCanvas', canvas=canvas)

    def set_navDate(self, navDate):
        """set the navDate of the object.

        https://iiif.io/api/presentation/3.0/#navdate
        https://iiif.io/api/cookbook/recipe/0230-navdate/

        IIIF: A date that clients may use for navigation purposes when
        presenting the resource to the user in a date-based user interface,
        such as a calendar or timeline. More descriptive date ranges, intended
        for display directly to the user, should be included in the metadata
        property for human consumption.

        Args:
            navDate (str): A date in UTC in the format "2010-01-01T00:00:00Z"
        """
        # check using a modified regex from www.w3.org
        # https://www.w3.org/TR/xmlschema11-2/#dateTime
        r = (r"-?([1-9][0-9]{3,}|0[0-9]{3})"
             r"-(0[1-9]|1[0-2])"
             r"-(0[1-9]|[12][0-9]|3[01])"
             r"T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))"
             r"(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))")
        assert re.match(r, navDate), "The value must be an XSD dateTime"\
            "literal with a timezone. It was: %s" % navDate
        if navDate[-1] != "Z":
            warnings.warn(f"The value should be given in UTC with the Z was {navDate}")
        self.navDate = navDate


class Canvas(_CMRCattributes, _HeightWidth, _Duration, _AddAnnoP2Items):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#53-canvas

    The Canvas represents an individual page or view and acts as a central
    point for assembling the different content resources that make up the
    display. Canvases must be identified by a URI and it must be an HTTP(S)
    URI.
    """

    def __init__(self):
        super(Canvas, self).__init__()
        self.label = Recommended("A Canvas should have the label property with at least one entry.")
        self.height = Required("Must have an height or a duration.")
        self.width = Required("Must have an width or a duration.")
        self.duration = None
        self.items = Recommended(
            "The canvas should contain at least one item.")
        self.annotations = None
        self.placeholderCanvas = None
        self.accompanyingCanvas = None

    def add_item(self, item):
        """Add an item (AnnotationPage) to the Canvas.

        Same as add_annotationpage_to_items but doesn't return.

        A Canvas should have the items property with at least one item.
        Each item must be an Annotation Page.

        Args:
            item (AnnotationPage): The AnnotationPage object.
        """
        add_to(self, 'items', AnnotationPage, item)

    def add_annotation(self, annotation=None):
        """
        Danger:
            From 0.4 use iiifpapi3.Canvas.add_annotationpage_to_annotations
        """
        warnings.warn('Please use `add_annotationpage_to_annotations` instead.', DeprecationWarning)
        return add_to(self, 'annotations', Annotation, annotation, target=self.id)


class start(_CoreAttributes):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#start
    https://iiif.io/api/cookbook/recipe/0009-book-1/

    A Canvas, or part of a Canvas, which the client should show on
    initialization for the resource that has the start property.
    This property allows the client to begin with the first Canvas that
    contains interesting content rather than requiring the user to manually
    navigate to find it.

    Examples:
        >>> manifest.set_start()
        >>> manifest.start.set_type("Canvas")
        >>> manifest.start.set_id("0202-start-canvas/canvas/p2")
    """
    def __init__(self):
        super(start, self).__init__()
        self.type = Required("Start object must have a type.")
        self.profile = Recommended("Start object should have a profile.")
        self.source = None
        self.selector = None

    def set_type(self, mtype):
        """Set the type of the resource: Canvas or SpecificResource.

        Args:
            mtype (str): The type of the resource that must be Canvas or
            SpecificResource.
        """
        if mtype != "Canvas" and self.source is None:
            self.source = Required(
                    "If you are not pointing to a Canvas please specify a source.")
        if mtype != "Canvas" and self.selector is None:
            self.selector = Required(
                    "If you are not pointing to a Canvas please specify a selector")
        self.type = mtype

    def set_source(self, source):
        self.source = source

    def set_selector(self, selector):
        self.selector = selector


class _Start(object):
    def set_start(self, startobj=None):
        """This method set a start obejct at self.start.
        IIIF: A Canvas, or part of a Canvas, which the client should show on
        initialization for the resource that has the start property.
        The reference to part of a Canvas is handled in the same way that
        Ranges reference parts of Canvases. This property allows the client to
        begin with the first Canvas that contains interesting content rather
        than requiring the user to manually navigate to find it.

        Notes:
            `set_start` self assign start attribute to a iiifpapi3.start
            handler see example below on how to use it.

        Examples:
            manifest.set_start()
            manifest.start.set_type('Canvas')
            manifest.start.set_id("https://example.org/iiif/1/canvas/1")

        Returns:
            start object: a reference to the start object to be used
        """
        if startobj is None:
            self.start = start()
        else:
            self.start = startobj
        return self.start


class Manifest(_CMRCattributes, _ViewingDirection, _Start, _ServicesList):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#52-manifest
    https://iiif.io/api/cookbook/recipe/0009-book-1/

    IIIF: The Manifest resource typically represents a single object and any
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

    Example:
        >>> manifest = iiifpapi3.Manifest()
        >>> manifest.set_id(extendbase_url="manifest.json")
        >>> manifest.add_label("en", "Image 1")
        >>> canvas = manifest.add_canvas_to_items()
    """

    def __init__(self):
        super(Manifest, self).__init__()
        self.start = None
        self.label = Required("A Manifest must have the label property with at least one entry.")
        self.viewingDirection = None
        self.services = None
        self.service = None
        self.thumbnail = Recommended("A Manifest should have the thumbnail property with at least one item.")
        self.summary = Recommended("A Manifest should have the summary property with at least one entry.")
        self.metadata = Recommended("A Manifest should have the metadata property with at least one item.")
        self.items = Required("The Manifest must have an items property with at least one item")
        self.annotations = None
        self.provider = Recommended("A Manifest should have the provider property with at least one item.")
        self.structures = None
        self.placeholderCanvas = None

    def add_item(self, item):
        """Add an item (Canvas) to the Manifest.

        Same as iiifpapi3.Manifest.add_canvas_to_items but doesn't return.

        A Manifest must have the items property with at least one item.
        Each item must be a Canvas.
        Clients must process items on a Manifest.

        Example:
            >>> manifest = iiifpapi3.Manifest()
            >>> manifest.set_id(extendbase_url="manifest.json")
            >>> manifest.add_label("en", "Image 1")
            >>> canvas = iiifpapi3.Canvas()
            >>> manifest.add_item(canvas)

        Args:
            item (Canvas): The canvas
        """
        add_to(self, 'items', Canvas, item)

    def add_services(self, services=None):
        warnings.warn('Please use `add_service_to_services` instead.', DeprecationWarning)
        add_to(self, 'services', service, services, (service, dict))

    def add_annotation(self, annotation=None):
        warnings.warn('Please use `add_annotationpage_to_annotations` instead.', DeprecationWarning)
        return add_to(self, 'annotations', AnnotationPage, annotation)

    def add_canvas_to_items(self, canvasobj=None):
        """Add a Canvas object to the items list.

        https://iiif.io/api/presentation/3.0/#canvas
        https://iiif.io/api/cookbook/recipe/0009-book-1/

        Args:
            canvasobj (iiifpapi3.Canvas, optional): A iiifpapi3.Canvas to be
                added to the Manifest.items list. Defaults to None.

        Example:
            >>> canvas = manifest.add_canvas_to_items()
            >>> canvas.set_height(1800)
            >>> canvas.set_width(1200)

        Returns:
            iiifpapi3.Canvas: if canvasobj is None an empty iiifpapi3.
            Canvas obj
        """
        return add_to(self, 'items', Canvas, canvasobj)

    def add_structure(self, structure):
        """Add an already instatiated Range to structres without return.

        Note:
            This is equivalent to iiifpapi3.Manifest.add_range_to_structures
            but does not return.

        Example:
            >>> manifest = iiifpapi3.Manifest()
            >>> manifest.set_id(extendbase_url="manifest.json")
            >>> manifest.add_label("en", "Image 1")
            >>> range = iiifpapi3.Range()
            >>> range.set_id('https//test')
            >>> manifest.add_item(range)

        Args:
            structure (Range): A Range object.
        """
        add_to(self, 'structures', Range, structure)

    def add_range_to_structures(self, rangeobj=None):
        """Add a Range object to the structures list.

        https://iiif.io/api/presentation/3.0/#range
        https://iiif.io/api/cookbook/recipe/0024-book-4-toc

        Args:
            rangeobj (iiifpapi3.Range, optional): A iiifpapi3.Range to be
                added to the Manifest.structures list. Defaults to None.

        Example:
            >>> rng = manifest.add_range_to_structures()
            >>> rng.set_id(extendbase_url="range/r0")
            >>> rng.add_label('en',"Table of Contents")
            >>> r1  = rng.add_range_to_items()
            >>> r1.set_id(extendbase_url="range/r1")

        Returns:
            iiifpapi3.Range: if rangeobj is None an empty iiifpapi3.Range obj
        """
        return add_to(self, 'structures', Range, rangeobj)


class refManifest(_CoreAttributes, _Thumbnail):
    """pseudo-IIIF resource

    https://iiif.io/api/presentation/3.0/#51-collection

    This class is used for creating references to Manifest:

    IIIF: Collections or Manifests referenced in the items property must have
    the id, type and label properties. They should have the thumbnail property.

    """
    def __init__(self):
        super(refManifest, self).__init__()
        self.thumbnail = Recommended("A Manifest reference should have the thumbnail property with at least one item.")
        self.type = "Manifest"
        self.navDate = None


class Collection(_CMRCattributes, _ViewingDirection, _ServicesList):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#51-collection
    https://iiif.io/api/cookbook/recipe/0230-navdate/navdate-collection.json

    IIIF: Collections are used to list the Manifests available for viewing.
    Collections may include both other Collections and Manifests, in order to
    form a tree-structured hierarchy. Collections might align with the curated
    management of cultural heritage resources in sets, also called
    “collections”, but may have absolutely no such similarity.

    Example:
        >>> collection = iiifpapi3.Collection()
        >>> collection.set_id("0230-navdate/navdate-collection.json")
        >>> collection.add_label(language='en',text="Chesapeake and Ohio")
        >>> tbn = collection.add_thumbnail()
        >>> collection.add_manifest_to_items(manifest_2)
        >>> collection.add_manifest_to_items(manifest_1)

    """
    def __init__(self):
        super(Collection, self).__init__()
        self.services = None
        self.annotations = None
        self.thumbnail = Recommended("A Collection should have the thumbnail property with at least one item.")
        self.summary = Recommended("A Collection should have the summary"
                                   "property with at least one entry. Clients "
                                   "should render summary on a Collection.")
        self.provider = Recommended("A Collection should have the provider property with at least one item.")
        self.label = Required("A Collection must have the label property with at least one entry.")
        self.items = Required(
            "A collection object must have at least one item!")
        self.metadata = Recommended("A Collection should have the metadata property with at least one item.")
        self.viewingDirection = None

    def add_annotation(self, annotationobj):
        warnings.warn('Please use `add_annotationpage_to_annotations` instead.', DeprecationWarning)
        return add_to(self, 'annotations', AnnotationPage, annotationobj)

    def add_item(self, item):
        """Add an item (Collection or Manifest) to the Manifest without returning.

        A Collection must have the items property.
        Each item must be either a Collection or a Manifest.

        Args:
            item (Collection or Manifest): The item to be added.
        """
        add_to(self, 'items', Canvas, item, (Collection, Manifest))

    def add_collection_to_items(self, collectionobj=None):
        """Add a Collection object to the items list.

        https://iiif.io/api/presentation/3.0/#51-collection
        https://iiif.io/api/cookbook/recipe/0009-book-1/

        Args:
            collectionobj (iiifpapi3.Canvas, optional): A iiifpapi3.Canvas to be
                added to the Manifest.items list. Defaults to None.

        Example:
            >>> subcollection = collection.add_collection_to_items()

        Returns:
            iiifpapi3.Collection: if collectionobj is None an empty
            iiifpapi3.Collection obj
        """
        return add_to(self, 'items', Collection, collectionobj)

    def add_manifest_to_items(self, manifestobj=None):
        """Add a Manifest object to the items list.

        https://iiif.io/api/presentation/3.0/#51-collection
        https://iiif.io/api/cookbook/recipe/0009-book-1/

        Args:
            manifestobj (iiifpapi3.Manifest, optional): A iiifpapi3.Manifest to
                be added to the Collection.items list. Defaults to None.

        Example:
            >>> subcollection = collection.add_collection_to_items()

        Returns:
            iiifpapi3.Manifest: if manifestobj is None an empty
            iiifpapi3.Manifest obj
        """
        if isinstance(manifestobj, Manifest):
            # Adding a Manifest only the references and thumbnail are passed
            newobj = copy.copy(manifestobj)
            delattr(newobj, 'items')
            manifestobj = newobj
        return add_to(self, 'items', refManifest, manifestobj, (Manifest, refManifest))


class Range(_CMRCattributes, _ViewingDirection, _Start):
    """IIIF resource

    https://iiif.io/api/presentation/3.0/#54-range
    https://iiif.io/api/cookbook/recipe/0024-book-4-toc

    IIIF: Ranges are used to represent structure within an object beyond the
    default order of the Canvases in the items property of the Manifest, such
    as newspaper sections or articles, chapters within a book, or movements
    within a piece of music. Ranges can include Canvases, parts of Canvases,
    or other Ranges, creating a tree structure like a table of contents.

    Example:
        >>> rng = manifest.add_range_to_structures()
        >>> rng.set_id(extendbase_url="range/r0")
        >>> rng.add_label('en',"Table of Contents")
        >>> r1  = rng.add_range_to_items()
        >>> r1.set_id(extendbase_url="range/r1")
        >>> r1.add_label('gez',"Tabiba Tabiban [ጠቢበ ጠቢባን]")

    """
    def __init__(self):
        super(Range, self).__init__()
        self.annotations = None
        self.items = Required("A range object must have at least one item!")
        self.supplementary = None
        self.label = Recommended("A Range should have the label property with at least one entry")
        self.viewingDirection = None
        self.start = None

    def add_annotation(self, annotationobj=None):
        warnings.warn('Please use `add_annotationpage_to_annotations` instead.', DeprecationWarning)
        return add_to(self, 'annotations', AnnotationPage, annotationobj)

    def add_item(self, item):
        """Add an item (Range,Canvas,Specific Resource where the source is a
        Canvas) to the Range.

        This function does not return. Use::

            iiifpapi3.Range.add_range_to_items
            iiifpapi3.Range.add_specificresource_to_items


        A Range must have the items property with at least one item.
        Each item must be a Range, a Canvas or a Specific Resource where the
        source is a Canvas.

        Args:
            item (Range,Canvas,SpecRes): The IIIF Object.
        """
        add_to(self, 'items', Canvas, item, (Range, SpecificResource, Canvas))

    def add_range_to_items(self, rangeobj=None):
        """Add a Range object to the items list.

        https://iiif.io/api/presentation/3.0/#54-range
        https://iiif.io/api/cookbook/recipe/0024-book-4-toc

        Args:
            rangeobj (iiifpapi3.Range, optional): A iiifpapi3.Range to
                be added to the Range.items list. Defaults to None.

        Example:
            >>> subrange  = range.add_range_to_items()
            >>> subrange.set_id(extendbase_url="range/r1")
            >>> subrange.add_label('gez',"Tabiba Tabiban [ጠቢበ ጠቢባን]")

        Returns:
            iiifpapi3.Range: if rangeobj is None an empty
            iiifpapi3.Range obj
        """
        return add_to(self, 'items', Range, rangeobj)

    def add_specificresource_to_items(self, specificresourceobj=None):
        """Add a SpecificResource object to the items list.

        https://iiif.io/api/presentation/3.0/#54-range
        https://iiif.io/api/cookbook/recipe/0024-book-4-toc

        Args:
            rangeobj (iiifpapi3.SpecificResource, optional): A
                iiifpapi3.SpecificResource to be added to the Range.items list.
                Defaults to None.

        Example:
            >>> subrange  = range.add_range_to_items()
            >>> subrange.set_id(extendbase_url="range/r1")
            >>> subrange.add_label('gez',"Tabiba Tabiban [ጠቢበ ጠቢባን]")

        Returns:
            iiifpapi3.SpecificResource: if rangeobj is None an empty
            iiifpapi3.SpecificResource obj
        """
        return add_to(self, 'items', SpecificResource, specificresourceobj)

    def set_supplementary(self, objid=None, extendbase_url=None):
        """Set a supplementary resource to the range

        A link from this Range to an Annotation Collection that includes the
        supplementing Annotations of content resources for the Range.

        https://iiif.io/api/presentation/3.0/#supplementary

        Args:
            objid (str, optional): The ID of the supplementary resource.
                Defaults to None.
            extendbase_url (str, optional): part of the URL to be appended at
                the IIIFpapi3.BASE_URL global variable to create the ID.
                Defaults to None.
        """
        self.supplementary = supplementary()
        self.supplementary.set_id(objid, extendbase_url)

    def add_canvas_to_items(self, canvas_id):
        """Ad a reference to a Canvas to the items.

        To do:
            Might be useful to add canvasobj removing attributes.

        Args:
            canvas_id (str): The ID of the Canvas.
        """
        if unused(self.items):
            self.items = []
        entry = {"id": canvas_id,
                 "type": "Canvas"}
        self.items.append(entry)


class SpecificResource(_CommonAttributes):
    """IIIF Web Annotation Data Model resource

    https://www.w3.org/TR/annotation-model/#specific-resources
    """
    def __init__(self):
        super(SpecificResource, self).__init__()
        self.id = Recommended("An ID is recommended.")
        self.source = None

    def set_source(self, source, extendbase_url=None):
        """Set the source of the SpecificResource

        Args:
            source (str): The source is usually an URL.
            extendbase_url (str, optional): For extending the BASE_URL and
            using it as a source. Defaults to None.
        """
        self.source = check_ID(self, extendbase_url=extendbase_url, objid=source)

    def set_selector(self, selector):
        """Set the selector of the specifc resource.

        Args:
            selector (any): The selector of the specific resource.
        """
        self.selector = selector

    def set_selector_as_PointSelector(self):
        """Set the selectof of the SpecificReource as a PointSelector.

        Returns:
            iiifpapi3.PointSelector: A reference to an empty
                iiifpapi3.PointSelector
        """
        ps = PointSelector()
        self.selector = ps
        return ps

    def set_selector_as_SvgSelector(self, value=None):
        """Set the selector to an SvgSelector or to a SVG string.

        Args:
            value (str, optional): An SVG as a string. Defaults to None.

        Returns:
            iiifpapi3.SvgSelector: An instance of iiifpapi3.SvgSelector
        """
        ss = SvgSelector()
        if value is not None:
            ss.set_value(value)
        self.selector = ss
        return ss


class ImageApiSelector(_Format, _ImmutableType):
    """IIIF Resource

    https://iiif.io/api/annex/openannotation/#iiif-image-api-selector

    IIIF: The Image API Selector is used to describe the operations available
    via the Image API in order to retrieve a particular image representation.
    In this case the resource is the abstract image as identified by the IIIF
    Image API base URI plus identifier, and the retrieval process involves
    adding the correct parameters after that base URI. For example, the top
    left hand quadrant of an image has the region parameter of pct:0,0,50,50
    which must be put into the requested URI to obtain the appropriate
    representation.
    """
    def __init__(self):
        self.type = "ImageApiSelector"
        self.region = None
        self.size = None
        self.rotation = None
        self.quality = None
        self.fromat = None

    def set_region(self, region):
        """Set the region of the image API selector.

        Args:
            region (str): The region of the ImageAPI selector.
        """
        self.region = region

    def set_rotation(self, rotation):
        """Set the rotation of the image API selector.

        Args:
            rotation (str,int): The rotation to be applied to the image.
        """
        self.rotation = rotation

    def set_quality(self, quality):
        """Set the quality to to the ImageAPI  selector.

        Args:
            quality (str): e.g. default
        """
        self.quality = quality

    def set_size(self, size):
        """Set the size parameter of the ImageAPI selector.

        Args:
            size (str): The requested size of the image.
        """
        self.size = size


class PointSelector(_ImmutableType):
    """

    https://iiif.io/api/annex/openannotation/#point-selector

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

    def __init__(self):
        self.type = "PointSelector"
        self.x = None
        self.y = None
        self.t = None

    def set_x(self, x):
        """Set the x coordinate.

        Args:
            x (int): The x coordinate.
        """
        self.x = x

    def set_y(self, y):
        """Set the y coordiante.

        Args:
            y (int): The y coordinate.
        """
        self.y = y

    def set_t(self, t):
        """Set the time time of the point in seconds.

        Args:
            t (float): The time of the point in seconds relative to the duration.
        """
        self.t = t


class FragmentSelector(_ImmutableType):
    """
    W3C: As the most well understood mechanism for selecting a Segment is to
    use the fragment part of an IRI defined by the representation's media type,
    it is useful to allow this as a description mechanism via a Selector.

    https://www.w3.org/TR/annotation-model/#fragment-selector

    """
    def __init__(self):
        self.type = "FragmentSelector"
        self.value = Required("A fragment selector must have a value!")

    def set_value(self, value):
        """Set the value of the FragmentSelector

        Args:
            value (int): The
        """
        self.value = value

    def set_xywh(self, x, y, w, h):
        """Set the starting x and y point and the widht and height.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.
            w (int): The width coordinate.
            h (int): The hieght coordinate.
        """
        self.value = "xywh=%i,%i,%i,%i" % (x, y, w, h)


class SvgSelector(_ImmutableType):
    """The SvgSelector is used to select a non rectangualar region of an image.
    https://www.w3.org/TR/annotation-model/#svg-selector
    """
    def __init__(self):
        self.type = "SvgSelector"
        self.value = None

    def set_value(self, value):
        """Set the value of the SVG Selector

        Args:
            value (str): A string containing the SVG element.
        """
        self.value = value