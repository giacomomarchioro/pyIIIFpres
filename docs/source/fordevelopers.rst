=============================
Documentation for developers
=============================


:py:class:`IIIFpres.iiifpapi3.Required`

Under The Hood Of iiifpapi3
---------------------------

`iiifpapi3`` is based on `multiple inheritance <https://en.wikipedia.org/wiki/Multiple_inheritance>`_. The attributes and the methods
common to multiple objects are grouped together and inherited by resources that used them.

The following figure shows the inheritance diagram of the classes:

.. inheritance-diagram:: IIIFpres.iiifpapi3
   :private-bases:

:ref:`APIref` gives you an overview of the public classes that are described in the
`IIIF presentation API 3.0 <https://iiif.io/api/presentation/3.0/>`_.

For following `RFC2119 <https://www.rfc-editor.org/rfc/rfc2119>`_ special classes are used for expressing if an attribute of the object
`MUST`, `SHOULD` or `MAY` be provided :

.. autoclass:: IIIFpres.iiifpapi3.Recommended
   :members:
   :no-inherited-members:

.. autoclass:: IIIFpres.iiifpapi3.Required
   :members:
   :no-inherited-members:

While attribute set to `None` must be interpreted as: "you `MAY` provide the
value".

However, some iiifpapi3 classes are private, their name start with an underscore because
they are actually abstractions for following the "Don't repeat your self" principle
and easing the conceptualization of IIIF Presentation API.

We can divide them in two groups:

Grouping classes
^^^^^^^^^^^^^^^^^^^^^^^
They group common IIIF resource structures.

.. autoclass:: IIIFpres.iiifpapi3._CoreAttributes
   :members:
   :no-inherited-members:

.. autoclass:: IIIFpres.iiifpapi3._CommonAttributes
   :members:
   :no-inherited-members:

.. autoclass:: IIIFpres.iiifpapi3._CMRCattributes
   :members:
   :no-inherited-members:

Helper method classes
^^^^^^^^^^^^^^^^^^^^^^^^
They allow to share a common method across multiple IIIF resource.
For instance adding an Annotation Page to the `annotations` list.

.. autoclass:: IIIFpres.iiifpapi3._Format
   :members:
   :no-inherited-members:

.. autoclass:: IIIFpres.iiifpapi3._HeightWidth
   :members:
   :no-inherited-members:

.. autoclass:: IIIFpres.iiifpapi3._Duration
   :members:
   :no-inherited-members:

.. autoclass:: IIIFpres.iiifpapi3._ViewingDirection
   :members:
   :no-inherited-members:

.. autoclass:: IIIFpres.iiifpapi3._MutableType
   :members:

.. autoclass:: IIIFpres.iiifpapi3._ImmutableType
   :members:

.. autoclass:: IIIFpres.iiifpapi3._SeeAlso
   :members:

.. autoclass:: IIIFpres.iiifpapi3._Service
   :members:

.. autoclass:: IIIFpres.iiifpapi3._Thumbnail
   :members:

.. autoclass:: IIIFpres.iiifpapi3._AddLanguage
   :members:

.. autoclass:: IIIFpres.iiifpapi3._Hompage
   :members:

.. autoclass:: IIIFpres.iiifpapi3._ServicesList
   :members:

.. autoclass:: IIIFpres.iiifpapi3._AnnotationsList
   :members:

.. autoclass:: IIIFpres.iiifpapi3._AddAnnoP2Items
   :members:

.. autoclass:: IIIFpres.iiifpapi3._Start
   :members:

