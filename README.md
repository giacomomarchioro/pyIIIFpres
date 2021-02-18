# pyIIIFpres
This is a Python module build for easing the construction of JSON manifests complaint with IIIF [API 3.0](https://iiif.io/api/presentation/3.0/) in production environment, similarly to [iiif-prezi](https://github.com/iiif-prezi/iiif-prezi) for earlier versions of the protocol.

**NOTE: this is NOT a a reference implementation, and is currently under development**

## Installation
The library uses only standard libraries and can be installed using `pip`:

   pip install git+https://github.com/giacomomarchioro/pyIIIFpres

## Basic usage
The module maps the api structure to Python classes. The user `set_` objects that can have only one value (e.g. `id`) and `add_` objects that can have multiple entity (e.g. `lablels`).
As an example we will execute the [Simple Manifest - Book recipe](https://iiif.io/api/cookbook/recipe/0009-book-1/) from the IIIF cookbook. More examples in the homonymous folder.

    ```python
    from IIIFpres import iiifpapi3
    iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1"
    manifest = iiifpapi3.Manifest()
    manifest.set_id(extendbase_url="manifest.json")
    manifest.add_label("en","Simple Manifest - Book")
    manifest.add_behavior("paged")

    data = (("Blank page",3204,4613,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f18","/full/max/0/default.jpg"),
            ("Frontispiece",3186,4612,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f19","/full/max/0/default.jpg"),
            ("Title page",3204,4613,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f20","/full/max/0/default.jpg"),
            ("Blank page",3174,4578,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f21","/full/max/0/default.jpg"),
            ("Bookplate",3198,4632,"https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f22","/full/max/0/default.jpg"),)

    for idx,d in enumerate(data):
        idx+=1 
        canvas = iiifpapi3.Canvas()
        canvas.set_id(extendbase_url=["canvas","p%s"%idx]) # in this case we use the base url
        canvas.set_height(d[2])
        canvas.set_width(d[1])
        canvas.add_label("en",d[0])
        annopage = iiifpapi3.AnnotationPage()
        annopage.set_id(extendbase_url=["page","p%s"%idx,"1"])
        annotation = iiifpapi3.Annotation(target=canvas.id)
        annotation.set_id(extendbase_url=["annotation","p%s-image"%str(idx).zfill(4)])
        annotation.set_motivation("painting")
        annotation.body.set_id("".join(d[3:]))
        annotation.body.set_type("Image")
        annotation.body.set_format("image/jpeg")
        annotation.body.set_width(d[1])
        annotation.body.set_height(d[2])
        s = iiifpapi3.service()
        s.set_id(d[3])
        s.set_type("ImageService3")
        s.set_profile("level1")
        annotation.body.add_service(s)
        # remember to add the item to their container!
        annopage.add_item(annotation)
        canvas.add_item(annopage)
        manifest.add_item(canvas)

    manifest.json_save("manifest.json")

