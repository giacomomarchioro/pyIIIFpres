pyIIIFpres
==========

|Build Status| |Coverage Status|

This is a Python module built for easing the construction of JSON
manifests compliant with IIIF `API
3.0 <https://iiif.io/api/presentation/3.0/>`__ in a production
environment, similarly to
`iiif-prezi <https://github.com/iiif-prezi/iiif-prezi>`__ for earlier
versions of the protocol.

.. note::
   This is NOT a reference implementation. Pull requests and issues
   are welcome!

Installation
------------

The library uses only standard libraries and can be installed using
``pip``.

Stable version:

::

   pip install pyIIIFpres

Development :

::

   pip install git+https://github.com/giacomomarchioro/pyIIIFpres

Basic usage
-----------

The module maps the API structure to Python classes. The user ``set_``
objects that can have only one value (e.g. ``id``) and ``add_`` objects
that can have multiple entities (e.g. ``labels``). As an example, we
will execute the `Simple Manifest - Book
recipe <https://iiif.io/api/cookbook/recipe/0009-book-1/>`__ from the
IIIF cookbook. More examples from the
`cookbook <https://iiif.io/api/cookbook/>`__ in the examples folder of
this repository.

.. code:: python

   from IIIFpres import iiifpapi3
   iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1/"
   manifest = iiifpapi3.Manifest()
   manifest.set_id(extendbase_url="manifest.json")
   manifest.add_label("en","Simple Manifest - Book")
   manifest.add_behavior("paged")

   #        label       width height id                                                                            service  
   data = (("Blank page",3204,4613,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f18","/full/max/0/default.jpg"),
           ("Frontispiece",3186,4612,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f19","/full/max/0/default.jpg"),
           ("Title page",3204,4613,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f20","/full/max/0/default.jpg"),
           ("Blank page",3174,4578,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f21","/full/max/0/default.jpg"),
           ("Bookplate",3198,4632,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f22","/full/max/0/default.jpg"),)

   for idx,d in enumerate(data):
       idx+=1
       canvas = manifest.add_canvas_to_items()
       canvas.set_id(extendbase_url="canvas/p%s"%idx) # in this case we use the base url
       canvas.set_height(d[2])
       canvas.set_width(d[1])
       canvas.add_label("en",d[0])
       annopage = canvas.add_annotationpage_to_items()
       annopage.set_id(extendbase_url="page/p%s/1" %idx)
       annotation = annopage.add_annotation_to_items(target=canvas.id)
       annotation.set_id(extendbase_url="annotation/p%s-image"%str(idx).zfill(4))
       annotation.set_motivation("painting")
       annotation.body.set_id("".join(d[3:]))
       annotation.body.set_type("Image")
       annotation.body.set_format("image/jpeg")
       annotation.body.set_width(d[1])
       annotation.body.set_height(d[2])
       s = annotation.body.add_service()
       s.set_id(d[3])
       s.set_type("ImageService3")
       s.set_profile("level1")

   manifest.json_save("manifest.json")

Debug the manifest
------------------

When you are populating a new IIIF type from scratch some helpful
function can be used for spotting errors.

:mod:`inspect <IIIFpres.iiifpapi3._CoreAttributes.inspect>` method returns a
JSON representation of the object where the recommended and required fields are
shown:

.. code:: python

   from IIIFpres import iiifpapi3
   manifest = iiifpapi3.Manifest()
   manifest.inspect()

``.show_errors_in_browser()`` method open a new browser tab highlighting
the required and recommended fields.

.. code:: python

   manifest.show_errors_in_browser()

Reading the manifest (experimental)
-----------------------------------

A json file compliant with presentation API3 can be read as follow:

.. code:: python

   from IIIFpres.utilities import read_API3_json
   mymanifest = read_API3_json('manifest.json')

This map Canvas, Annotation and the major IIIF types to iiifpapi3
classes, loading the rests as dicts.

Acknowledgements
----------------

Bisides contributors, I would like to thank
`dnoneill <https://github.com/dnoneill>`__ for suggestions , and IIIF
community and coordinators.

.. |Build Status| image:: https://travis-ci.com/giacomomarchioro/pyIIIFpres.svg?branch=main
   :target: https://travis-ci.com/giacomomarchioro/pyIIIFpres
.. |Coverage Status| image:: https://coveralls.io/repos/github/giacomomarchioro/pyIIIFpres/badge.svg?branch=main
   :target: https://coveralls.io/github/giacomomarchioro/pyIIIFpres?branch=main
