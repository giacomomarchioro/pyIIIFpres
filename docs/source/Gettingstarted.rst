=================
Getting started
=================


The philosophy of this package
================================

The philosophy of this package is to try to create an isomorphic class
structure based on IIIF presentation API, knowing the IIIF standard and
Python and autocomplete ideally should be the only requirements to get
started. Doing so you don't need to learn IIIF Presentation API and pyIIIFpres
data models because they should be `isomorphic <https://en.wikipedia.org/wiki/Isomorphism>`_
so learning one of the two should automatically reinforce the knowledge of the other.

Workaround for the common errors
================================

One of the aims of this package is to prevent any possible error in the
production and consumption of the manifest. The choice of this
philosophy arises from years of finding poor metadata around the web.

At the same time, pyIIIFpres should offer always an easy workaround in
case the threat is actually under control.

These global variables are lists or strings that you can modify to allow
your specific case they are built from possible threads and
recommendations from RFC and IANA and IIIF but in some cases, they can
prevent correct choices:

::

   from IIIFpres import iiifpapi3
   iiifpapi3.INVALID_URI_CHARACTERS
   iiifpapi3.LANGUAGES
   iiifpapi3.BEHAVIOURS
   iiifpapi3.MEDIATYPES

See the documentation on how to modify them.

There are more drastic approaches to modifying these variables like
setting the value of a property without the ``set_`` method for instance
``homepage.set_format("myinvalid/format")`` can be set directly like
this ``homepage.format = "myinvalid/format"``.

Eventually, all the checks can be disabled running your script using the
optimization flag::

   $ python -O myscirpt.py

Creating a IIIF type and populating it
======================================

The best method to get started is to have a look at
`Cookbook <https://iiif.io/api/cookbook/>`__ and find the relative
example in the `example folder of pyIIIFpres
project <https://github.com/giacomomarchioro/pyIIIFpres/tree/main/examples>`__.
It is easy to modify the provided example and design interactively a
manifest that suits your need.

Change the base URL (in the newer version the final slash is required).

.. code:: python

   from IIIFpres import iiifpapi3
   iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1/"
   manifest = iiifpapi3.Manifest()

When setting the ID use the ``extendbase_url`` for appending the
``BASE_URL``:

.. code:: python

   annotation.set_id(extendbase_url="canvas/page/annotation")

The ID will be:
``https://iiif.io/api/cookbook/recipe/0009-book-1/canvas/page/annotation``

The :mod:`inspect() <IIIFpres.iiifpapi3._CoreAttributes.inspect>` method can 
give you a quick view of the ``Required`` and ``Suggested`` fields.

.. code:: python

   manifest.inspect()

Most of the ``add_`` methods return a handler that can be used for
modifying the object.

.. code:: python

   cnv = manifest.add_canvastoitems()
   cnv.inspect()

Using :mod:`inspect() <IIIFpres.iiifpapi3._CoreAttributes.inspect>` on the
handler will return only the hints for
populating it. Inspecting nested objects in the terminal could be
painful. :mod:`.show_errors_in_browser() <IIIFpres.iiifpapi3._CoreAttributes.inspect>`
opens a browser tab, showing the required and recommended fields.

Don’t forget that each class has also the method ``.__dict__``. For
instance ``manifest.__dict__`` returns a compact representation of the
manifest showing only the types of the items and the ID of the items.

.. code:: python

   manifest.__dict__

Save a IIIF object
==================

Use :meth:`.json_save() <IIIFpres.iiifpapi3._CoreAttributes.json_save>`
on the root element to save the JSON file.

.. code:: python

   manifest.json_save()

Or :meth:`.json_dumps() <IIIFpres.iiifpapi3._CoreAttributes.json_dumps>` for dumping
it as string.

.. code:: python

   manifest.json_dumps()

Debugging the Code
==================

It should be quite clear where the error happens during the insertion of
an invalid value through the iiifpapi module. However, missing
``Required`` statements need some tools to spot them because they are
checked when the manifest/collection is written in the JSON file hence
the module does not show exactly when the error occurred.

The suggested approach is the following:
1. Open ``ipython`` console
2. run your script using ``%run myscript.py``
3. activate the debug tool using ``%debug``
4. press ``u`` and enter until you see the frame where
the manifest/collection is defined
e.g. ``mymanifest.json_save("SFMAG_manifest30.json")``
5. now use ``.show_errors_in_browser()`` function on the istance of your
manifest/collection e.g. ``mymanifest.show_errors_in_browser()``
6. A new tab in the browser should open (try to execute the command again if
it does not).
7. You can use your browser built-in search tool for searching the\
``❌Required`` string this will bring you exactly where the error occurred
8. Now you can modify your script for correcting the error easily.

Getting the format right
========================

`pyIIIFpres
checks <https://github.com/giacomomarchioro/pyIIIFpres/blob/623eb788e90ca0d15b84906b088d16ac049cd34b/IIIFpres/iiifpapi3.py#L419>`__
the format MIME type based on `IANA media types
page <https://www.iana.org/assignments/media-types/media-types.xhtml>`__,
building the missing templates from the registry and the format for
instance ``image/jpeg``,\ ``image/gif`` etc. etc.

The full list of media types used by pyIIIFpres can be accessed using:

.. code:: python

   from IIIFpres import iiifpapi3
   iiifpapi3.MEDIATYPES

An additional helper class gives you the possibility to access the
mediatypes using the dot notation:

.. code:: python

   from IIIFpres import MediaTypes

.. code:: python

   In [1]: MediaTypes.audio.mp4
   Out[1]: 'audio/mp4'

   In [2]: MediaTypes.image.jp2
   Out[2]: 'image/jp2'

   In [3]: MediaTypes.application.json_seq
   Out[3]: 'application/json-seq'

Getting the language right
==========================

`pyIIIFpres
checks <https://github.com/giacomomarchioro/pyIIIFpres/blob/623eb788e90ca0d15b84906b088d16ac049cd34b/IIIFpres/iiifpapi3.py#L250>`__
the language subtags of labels, summaries and other text content against
the `language subtag
registry <https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry>`__.

.. warning::
   only language subtags are checked not variants or composite strings.

In this registry, there are more than 190 two-letters subtags and 8022
three-letters subtags, hence you have 28% chance that inserting a random
two-letter string will result in a valid subtag and 45% chance that
inserting a random three-letters string will result in a valid
three-letter tag.

You might want to limit the check to a subset of languages you know are
in your document to avoid these errors. This can be achieved by
reassigning the :mod:`LANGUAGES <IIIFpres.iiifpapi3.LANGUAGES>` global variable:

.. code:: python

   from IIIFpres import iiifpapi3,BCP47lang
   iiifpapi3.LANGUAGES = [BCP47lang.english,BCP47lang.spanish]
   # all the rest of your script

Add subtags with variants and composite strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(Or how to solve AssertionError: Language must be a valid BCP47 language tag or none)
-------------------------------------------------------------------------------------

pyIIIFpres allows only language subtags. If you think that a single
sub-tag is not enough for describing the language of the document you
can add your custom language string in this way:

.. code:: python

   from IIIFpres import iiifpapi3,BCP47lang
   iiifpapi3.LANGUAGES.append("de-DE-u-co-phonebk")
   # all the rest of your script

But keep in mind the golden `W3C golden
rule <https://www.w3.org/International/questions/qa-choosing-language-tags#langsubtag>`__:

.. epigraph::
   Always bear in mind that the golden rule is to keep your language tag
   as short as possible. Only add further subtags to your language tag if
   they are needed to distinguish the language from something else in the
   context where your content is used.

(before inserting you could check it using, for instance,
https://schneegans.de/lv/)

Language map object
===================

Remember that :mod:`add_metadata <IIIFpres.iiifpapi3._CommonAttributes.add_metadata>`
:mod:`set_requiredStatement <IIIFpres.iiifpapi3._CommonAttributes.set_requiredStatement>`
if left empty return a  :mod:`languagemap <IIIFpres.iiifpapi3.languagemap>`
object that can help building multi language support.

::

   reqst = manifest.set_requiredStatement()
   reqst.add_label('Provided by','en')
   reqst.add_value('Univeristy of Verona','en')
   reqst.add_label('Contenuto fornito da','it')
   reqst.add_value('Università di Verona','it')

Using a language detector
^^^^^^^^^^^^^^^^^^^^^^^^^

Another possible approach could be to use a language detector. There are
many different alternatives to accomplish this task, this `StackOverflow
answer <https://stackoverflow.com/a/47106810/2132157>`__ gives a good
overview of the panorama.

This
`example <https://github.com/giacomomarchioro/pyIIIFpres/blob/main/examples/using_languagedetection.py>`__
shows a basic implementation using ``langdetect``.

The output of using the language detector on the manifest iiifpapi3
object of `0065-opera-multiple-canvases
recipe <https://github.com/giacomomarchioro/pyIIIFpres/blob/main/examples/0065-opera-multiple-canvases.py>`__
is the following:

::

   In [3]: check_languages(manifest)                                               
   ❌  L'Elisir D'Amore seems not to be: it
   ✅  The Elixir of Love is : en
   ✅  Date Issued is : en
   ⚠️  Could not detect language for 2019 but is set to: en
   ✅  Publisher is : en
   ✅  Indiana University Jacobs School of Music is : en
   ❌  Atto Primo seems not to be: en
   ❌  Atto Secondo seems not to be: en
   ✅  Gaetano Donizetti, L'Elisir D'Amore is : it
   ❌  Atto Primo seems not to be: en
   ✅  Preludio e Coro d'introduzione – Bel conforto al mietitore is : it
   ✅  Remainder of Atto Primo is : en
   ❌  Atto Secondo seems not to be: en


Behaviours and strange behaviours
===================================
To learn more about IIIF behaviours visit:
https://iiif.io/api/presentation/3.0/#behavior

IIIFpres firstly checks that the behaviour is inside :mod:`BEHAVIOURS(<IIIFpres.iiifpapi3.BEHAVIOURS>`
global variable:

.. code:: python

   from IIIFpres import iiifpapi3
   iiifpapi3.BEHAVIOURS

So if you want to use non-standard behaviour you have to append to this
list first to bypass the check:

.. code:: python

   iiifpapi3.BEHAVIOURS.append("mystrangebehaviour")

Then checks if the behaviour is applied to the right IIIF object.

.. warning::
   At the moment pyIIIFpres does not check if the objects referenced by Range
   and Collection have the right attributes e.g. Canvas must have a ``duration``
   for ``auto-advance`` behaviour.



Getting the Image size automatically
====================================
pyIIIFpres do not provide built-in methods for inferring information
about the images. Depending on your need you might find useful different
solutions. This for keeping the footprint of the library low and avoiding
requirements.

============== ====================
\              Format not supported
============== ====================
Using ImageAPI None
Pillow         None.
Exiftools      None
OpenCV         jpg 2000
Matplotlib     jpg 2000
============== ====================

Using ImageAPI
^^^^^^^^^^^^^^

.. code:: python

   import requests
   # when you use a proxy you might have to use the original link e.g. "http://localhost:1080/iipsrv/iipsrv.fcgi?iiif=/imageapi//m0171_0/m0171_0visn20_0001a21.jp2/info.json"
   iiifimageurl = "http://lezioni.meneghetti.univr.it//imageapi/m0171_0/m0171_0visn20_0001a21.jp2/info.json" 
   imageinfo =  requests.get(iiifimageurl)
   jsoninfo = imageinfo.json()
   imgwidth = jsoninfo['width']
   imgheight = jsoninfo['height']

Exiftool
^^^^^^^^

Once installed `Exiftool <https://exiftool.org/>`__ it can be called as
a subprocess:

.. code:: python

   from subprocess import check_output
   out = check_output(["exiftool", imagepath])
   Metadata = dict((e[:32].strip(),e[33:].strip()) for e in out.decode('utf8').split('\n'))
   width = Metadata['Image Width']
   height = Metadata['Image Height']

Using Pillow
^^^^^^^^^^^^^

``pip install Pillow``

.. code:: python

   from PIL import Image
   image = PIL.Image.open("image.png")
   width, height = image.size

Using OpenCV
^^^^^^^^^^^^^

``pip install opencv-python``

.. code:: python

   import cv2
   img = cv2.imread('image.jpg')
   width, height, channelsN = img.shape


Reading and modifying JSON compliant with API-3.0
=================================================

pyIIIFpres offers some support for reading and modifying JSON files
compliant with API 3.

.. important::
   pyIIIFpres assumes that the JSON file is compliant with API 3,
   ``inspect()`` and ``show_errors_in_browser()`` will highlight only
   errors in the new addition of the user to the file.

:mod:`read_API3_json() <IIIFpres.utilities.read_API3_json>` maps most of the
IIIF type to ``IIFpapi3`` classes, you can access and modify the elements using
the normal ``set_`` methods:

.. code:: python

   from IIIFpres.utilities import read_API3_json
   mymanifest = read_API3_json('tests/integration/fixtures/0001-mvm-image.json')
   mymanifest.items[0].items[0].items[0]
   # Out: Annotation id:https://iiif.io/api/cookbook/recipe/0001-mvm-image/annotation/p0001-image
   mymanifest.items[0].items[0].items[0].set_id('http:mynewid.com')
   mymanifest.items[0].items[0].items[0]
   # Out: Annotation id:http:mynewid.com
   mymanifest.json_save("revised_manifest.json")

If performance is critical :mod:`modify_API3_json() <IIIFpres.utilities.modify_API3_json>`
map only the first IIIF type encountered to ``IIFpapi3`` classes leaving all
the rest as ``dicts``.

.. code:: python

   from IIIFpres.utilities import modify_API3_json
   mymanifest = modify_API3_json('tests/integration/fixtures/0001-mvm-image.json')
   canvas = mymanifest.add_canvas_to_items()
   canvas.set_id(extendbase_url=["canvas","p1"])
   canvas.add_label("en","Forgotten painting")
   canvas.set_height(1271)
   canvas.set_width(2000)
   mymanifest.json_save("revised_manifest.json")

The deletion of an IIIF type instance can be done using
``read_API3_json`` or ``modify_API3_json`` and removing the entity from
the structure manually:

.. code:: python

   mymanifest.items.pop(0)

or using the :mod:`delete_object_byID() <IIIFpres.utilities.delete_object_byID>`
if the instance has an ID:

.. code:: python

   from IIIFpres.utilities import delete_object_byID
   mymanifest = modify_API3_json('tests/integration/fixtures/0001-mvm-image.json')
   mymanifest.__dict__
   delete_object_byID(mymanifest,id='https://iiif.io/api/cookbook/recipe/0001-mvm-image/page/p1/1')
   mymanifest.__dict__

.. note::
   any nested object will be deleted when deleting the parent
   object!

.. tip::
   If you need supports for reading annotations of both IIIF API 2.1 and
   3.0 an excellent package to use could be :
   `python-iiif-annotation-tool <https://github.com/robcast/python-iiif-annotation-tool>`__

Validating the JSON manifest using the official schema
======================================================
pyIIIFpres does its best to prevent any error but it is wise to check if
the resulting .json is valid using the official IIIF API 3.0 schema
provided by Glen Robson and IIIF Consortium that can be found
`here <https://github.com/IIIF/presentation-validator/blob/master/schema/iiif_3_0.json>`__.

A possible solution could take advantage of ``jsonschema`` python
package:

.. code:: python

   # json schema is availabe here https://github.com/IIIF/presentation-validator/blob/master/schema/iiif_3_0.json
   # we can use jsonschema module for vallidating
   # to install it you can use pip install jsonschema
   import os
   import jsonschema
   import json
   if not os.path.exists('iiif_3_0.json'):
       import urllib.request
       jsonchemadownloadurl = r"https://raw.githubusercontent.com/IIIF/presentation-validator/master/schema/iiif_3_0.json"
       with urllib.request.urlopen(jsonchemadownloadurl) as response, open("iiif_3_0.json", 'wb') as out_file:
           data = response.read()
           out_file.write(data)

   to_be_tested = "example_manifest_response.json"
   with open(to_be_tested) as instance, open("iiif_3_0.json") as schema:
       jsonschema.validate(instance=json.load(instance),schema=json.load(schema))

Improve performance of writing and serving JSON IIIF-objects
============================================================

If you are saving the JSON files in your server there is usually no need
to improve the performance. However, if you are planning to create the
JSON IIIF objects (manifests, collection…) “on-the-fly” each time the
user requests them or caching the results temporarily you might want to
improve the writing speed of the manifest.

`tests/performance/performance_test.py <https://github.com/giacomomarchioro/pyIIIFpres/blob/main/tests/performance/performance_test.py>`__

offers a way to test the performance of your server in serving a
manifest with 2000 canvas and 2000 annotations, and one of 4000 canvas
and 40000 annotations. Feel free to do a pull request with the results
of the test which are appended to the csv files in the same folder.

If the speed is not enough for your needs, you can try one of the
following actions or both:
1. Install orjson: ``pip install orjson`` and use
:mod:`myIIIFobject.orjson_save() <IIIFpres.iiifpapi3._CoreAttributes.orjson_save()>`
or :mod:`myIIIFobject.orjson_dumps() <IIIFpres.iiifpapi3._CoreAttributes.orjson_dumps()>`
` instead of ``myIIIFobject.json_save()`` or ``.json_dumps()``
2. ⚠️Check the IIIF
JSON object once and then run optimized Python code using the ``-O``
flag e.g. ``python -O 0001-mvm-image.py``\ ⚠️

``orjson`` is a much faster parser compared to the standard ``json``
module.

.. important::
   The ``-O`` **flag ⚠️removes all the assertions and most
   of the helper classes**\ ⚠️. Hence you should use it with caution. One
   strategy could be to check (without the flag) if the IIIF Object is valid
   when you insert it in your digital library or you modify it  and then
   use the optimized version to serve it, without the need of using other
   tools.

An Intel(R) Core(TM) i7-4770HQ CPU @ 2.20GHz using ``pyIIIFpres`` can
produce 4000 canvas and 40000 annotations in 2.26 seconds, using orjson
in 1.19 seconds and with the optimization in 0.48 seconds.

