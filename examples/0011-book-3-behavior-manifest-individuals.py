# https://iiif.io/api/cookbook/recipe/0009-book-1/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0011-book-3-behavior/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest-individuals.json")
manifest.add_label("ca","[Conoximent de las orines] Ihesus, Ihesus. En nom de Deu et dela beneyeta sa mare e de tots los angels i archangels e de tots los sants e santes de paradis yo micer Johannes comense aquest libre de reseptes en l’ayn Mi 466.")
manifest.add_behavior("individuals")

data = [('inside cover; 1r',
  3375,
  2250,
  'https://iiif.io/api/image/3.0/example/reference/85a96c630f077e6ac6cb984f1b752bbf-0-21198-zz00022840-1-master',
  '/full/max/0/default.jpg'),
 ('2v, 3r',
  3375,
  2250,
  'https://iiif.io/api/image/3.0/example/reference/85a96c630f077e6ac6cb984f1b752bbf-1-21198-zz00022882-1-master',
  '/full/max/0/default.jpg'),
 ('3v, 4r',
  3375,
  2250,
  'https://iiif.io/api/image/3.0/example/reference/85a96c630f077e6ac6cb984f1b752bbf-2-21198-zz000228b3-1-master',
  '/full/max/0/default.jpg'),
 ('4v, 5r',
  3375,
  2250,
  'https://iiif.io/api/image/3.0/example/reference/85a96c630f077e6ac6cb984f1b752bbf-3-21198-zz000228d4-1-master',
  '/full/max/0/default.jpg')]

for idx,d in enumerate(data):
    idx+=1 
    canvas = manifest.add_canvas_to_items()
    canvas.set_id(extendbase_url="canvas/v%s"%idx) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("en",d[0])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url="page/v%s/1" %idx)
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url="annotation/v%s-image" %str(idx).zfill(4))
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

if __name__ == "__main__":
    manifest.json_save("manifest.json")