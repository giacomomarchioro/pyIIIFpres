import json
context = "@context"
context_dec = "http://iiif.io/api/presentation/3/context.json"

class Required(object):
    """
    This is not an IIIF object but a class used by this sofware to identify required fields.
    This is equivalente to MUST setatement in the guideline.
    """
    def __init__(self,description=None):
        self.description = description
    def __repr__(self): 
        return 'Required attribute:%s' %self.description

class Recommended(object):
    """
    This is not an IIIF object but a class used by this sofware to identify required fields.
    This is equivalente to SHOULD setatement in the guideline.
    """
    def __init__(self,description=None):
        self.description = description
    def __repr__(self): 
        return 'Recommended attribute:%s' %self.description


class CommonsAtributes(object):
      def __init__(self):
        self.id = Required("You must provide this attribute")
        self.context = None
        self.type = "Manifest"
        self.label = Required("IIIF:A Manifest must have the label property with at least one entry.")
        self.items = []
        self.metadata = Recommended("A Manifest should have the metadata property with at least one item.")
        self.summary = Recommended("A Manifest should have the summary property with at least one entry.")
        self.requiredStatement = {}
        self.rights = None
        # https://iiif.io/api/presentation/3.0/#thumbnail
        self.thumbnail = Recommended("A Manifest should have the thumbnail property with at least one item.")
        self.navDate = None

    def set_ID(self,manifest_url):
        """
        IIIF : The id property identifies this manifest with the URL at which it is available online.
        """
        self.id = manifest_url

    def set_type(self):
        print("The type property must be kept Manifest.")

    def add_label(self,text,language):
        """
        IIIF : A human readable label, name or title. The label property is intended to be displayed 
        as a short, textual surrogate for the resource if a human needs to make a distinction 
        between it and similar resources, for example between objects, pages, or options for 
        a choice of images to display. The label property can be fully internationalized, and 
        each language can have multiple values.
        """
        if isinstance(self.label, Required):
            self.label = {}
        self.label[language] = [text]
    
    def add_metadata(self,label,value,language):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if isinstance(self.metadata, Recommended):
            self.metadata = []
        entry = {"label":{language:[label]},
                 "value":{language:[value]}}
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
        if isinstance(self.summary, Recommended):
            self.summary = {}
        self.summary[language] = text

    def add_requiredStatement(self,text,language):
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
        self.requiredStatement["label"] = {language:[text]}
        self.requiredStatement["value"] = {language:[text]}

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




class Provider(object):
    """"
    IIIF: An organization or person that contributed to providing the content of the resource. 
    Clients can then display this information to the user to acknowledge the provider’s contributions. 
    This differs from the requiredStatement property, in that the data is structured, allowing 
    the client to do more than just present text but instead have richer information about the 
    people and organizations to use in different interfaces.
    """"
    def __init__(self):
        self.id = Required("Agents must have the id property, and its value must be a string. The string must be a URI that identifies the agent.""")
        self.context = None
        self.type = "Agent"
        self.label = Required("IIIF:A Manifest must have the label property with at least one entry.")
        self.items = []
        self.metadata = Recommended("A Manifest should have the metadata property with at least one item.")
        self.summary = Recommended("A Manifest should have the summary property with at least one entry.")
        self.requiredStatement = {}
        self.rights = None
    
    def set_ID(self,manifest_url):
        """
        IIIF : The id property identifies this manifest with the URL at which it is available online.
        """
        self.id = manifest_url

    def set_type(self):
        print("The type property must be kept Manifest.")

    def add_label(self,text,language):
        """
        IIIF : A human readable label, name or title. The label property is intended to be displayed 
        as a short, textual surrogate for the resource if a human needs to make a distinction 
        between it and similar resources, for example between objects, pages, or options for 
        a choice of images to display. The label property can be fully internationalized, and 
        each language can have multiple values.
        """
        if isinstance(self.label, Required):
            self.label = {}
        self.label[language] = [text]
    
    def set_homepage(self,):
        pass

    def set_logo(self):
        pass

    def set_seeAlso(self):
        pass


class Image(object):
    """
    This is usually refered as content. 
    """
    def __init__(self):
        self.id = Required()
        self.type = "Image"
        self.format = Required()
        self.height = Required()
        self.width = Required()


class Range(object):
      def __init__(self):
        self.id = Required("You must provide this attribute")
        self.context = None
        self.type = "Manifest"
        self.label = Required("IIIF:A Manifest must have the label property with at least one entry.")
        self.items = []
        self.metadata = Recommended("A Manifest should have the metadata property with at least one item.")
        self.summary = Recommended("A Manifest should have the summary property with at least one entry.")
        self.requiredStatement = {}
        self.rights = None
        # https://iiif.io/api/presentation/3.0/#thumbnail
        self.thumbnail = Recommended("A Manifest should have the thumbnail property with at least one item.")
        self.navDate = None

    def set_ID(self,manifest_url):
        """
        IIIF : The id property identifies this manifest with the URL at which it is available online.
        """
        self.id = manifest_url

    def set_type(self):
        print("The type property must be kept Manifest.")

    def add_label(self,text,language):
        """
        IIIF : A human readable label, name or title. The label property is intended to be displayed 
        as a short, textual surrogate for the resource if a human needs to make a distinction 
        between it and similar resources, for example between objects, pages, or options for 
        a choice of images to display. The label property can be fully internationalized, and 
        each language can have multiple values.
        """
        if isinstance(self.label, Required):
            self.label = {}
        self.label[language] = [text]
    
    def add_metadata(self,label,value,language):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if isinstance(self.metadata, Recommended):
            self.metadata = []
        entry = {"label":{language:[label]},
                 "value":{language:[value]}}
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
        if isinstance(self.summary, Recommended):
            self.summary = {}
        self.summary[language] = text

    def add_requiredStatement(self,text,language):
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
        self.requiredStatement["label"] = {language:[text]}
        self.requiredStatement["value"] = {language:[text]}

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



class Canvas(object):
      def __init__(self):
        self.id = Required("You must provide this attribute")
        self.context = None
        self.type = "Manifest"
        self.label = Required("IIIF:A Manifest must have the label property with at least one entry.")
        self.items = []
        self.metadata = Recommended("A Manifest should have the metadata property with at least one item.")
        self.summary = Recommended("A Manifest should have the summary property with at least one entry.")
        self.requiredStatement = {}
        self.rights = None
        # https://iiif.io/api/presentation/3.0/#thumbnail
        self.thumbnail = Recommended("A Manifest should have the thumbnail property with at least one item.")
        self.navDate = None

    def set_ID(self,manifest_url):
        """
        IIIF : The id property identifies this manifest with the URL at which it is available online.
        """
        self.id = manifest_url

    def set_type(self):
        print("The type property must be kept Manifest.")

    def add_label(self,text,language):
        """
        IIIF : A human readable label, name or title. The label property is intended to be displayed 
        as a short, textual surrogate for the resource if a human needs to make a distinction 
        between it and similar resources, for example between objects, pages, or options for 
        a choice of images to display. The label property can be fully internationalized, and 
        each language can have multiple values.
        """
        if isinstance(self.label, Required):
            self.label = {}
        self.label[language] = [text]
    
    def add_metadata(self,label,value,language):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if isinstance(self.metadata, Recommended):
            self.metadata = []
        entry = {"label":{language:[label]},
                 "value":{language:[value]}}
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
        if isinstance(self.summary, Recommended):
            self.summary = {}
        self.summary[language] = text

    def add_requiredStatement(self,text,language):
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
        self.requiredStatement["label"] = {language:[text]}
        self.requiredStatement["value"] = {language:[text]}

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

class Manifest(object):
    def __init__(self):
        self.id = Required("You must provide this attribute")
        self.context = None
        self.type = "Manifest"
        self.label = Required("IIIF:A Manifest must have the label property with at least one entry.")
        self.items = []
        self.metadata = Recommended("A Manifest should have the metadata property with at least one item.")
        self.summary = Recommended("A Manifest should have the summary property with at least one entry.")
        self.requiredStatement = {}
        self.rights = None
        # https://iiif.io/api/presentation/3.0/#thumbnail
        self.thumbnail = Recommended("A Manifest should have the thumbnail property with at least one item.")
        self.navDate = None

    def set_ID(self,manifest_url):
        """
        IIIF : The id property identifies this manifest with the URL at which it is available online.
        """
        self.id = manifest_url

    def set_type(self):
        print("The type property must be kept Manifest.")

    def add_label(self,text,language):
        """
        IIIF : A human readable label, name or title. The label property is intended to be displayed 
        as a short, textual surrogate for the resource if a human needs to make a distinction 
        between it and similar resources, for example between objects, pages, or options for 
        a choice of images to display. The label property can be fully internationalized, and 
        each language can have multiple values.
        """
        if isinstance(self.label, Required):
            self.label = {}
        self.label[language] = [text]
    
    def add_metadata(self,label,value,language):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if isinstance(self.metadata, Recommended):
            self.metadata = []
        entry = {"label":{language:[label]},
                 "value":{language:[value]}}
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
        if isinstance(self.summary, Recommended):
            self.summary = {}
        self.summary[language] = text

    def add_requiredStatement(self,text,language):
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
        self.requiredStatement["label"] = {language:[text]}
        self.requiredStatement["value"] = {language:[text]}

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

    def validate(self):
        for i in g.__dict__.values():
            if isinstance(i, Required):
                print(i)


