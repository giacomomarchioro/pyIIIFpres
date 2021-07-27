# https://iiif.io/api/cookbook/recipe/0117-add-image-thumbnail/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0117-add-image-thumbnail/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json ")
manifest.add_label("en","Playbill Cover with Manifest Thumbnail")
manifest.add_summary("en","Cover of playbill for \"Akiba gongen kaisen-banashi,\" \"Futatsu chōchō kuruwa nikki\" and \"Godairiki koi no fūjime\" performed at the Chikugo Theater in Osaka from the fifth month of Kaei 2 (May, 1849); main actors: Gadō Kataoka II, Ebizō Ichikawa VI, Kitō Sawamura II, Daigorō Mimasu IV and Karoku Nakamura I; on front cover: producer Mominosuke Ichikawa's crest.")
thum = manifest.add_thumbnail()
thum.set_id("https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_001/full/max/0/default.jpg")
thum.set_type("Image")
thum.set_format("image/jpeg")
thum.set_height(300)
thum.set_width(219)

# seems there is not much documentation about services
cplx_service = {
          "id": "https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_001",
          "type": "ImageService3",
          "profile": "level1",
          "extraFormats": [
            "jpg",
            "png"
          ],
          "extraQualities": [
            "default",
            "color",
            "gray"
          ],
          "protocol": "http://iiif.io/api/image",
          "tiles": [
            {
              "height": 512,
              "scaleFactors": [
                1,
                2,
                4,
                8
              ],
              "width": 512
          }]}
thum.add_service(cplx_service)
#tserv.set_id("https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_001")
#tserv.set_type("ImageService3")
#tserv.set_profile("level1")


canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas/p0")
canvas.add_label("en","front cover with color bar")
canvas.set_height(5312)
canvas.set_width(4520)
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url="page/p0/1")
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url="annotation/p0000-image")
annotation.body.set_height(5312)
annotation.body.set_width(4520)
annotation.body.set_id("https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_001_full/full/max/0/default.jpg")
annotation.body.set_format("image/jpeg")
annotation.body.set_type("Image")
srv = annotation.body.add_service()
srv.set_id("https://iiif.io/api/image/3.0/example/reference/4f92cceb12dd53b52433425ce44308c7-ucla_bib1987273_no001_rs_001_full")
srv.set_type("ImageService3")
srv.set_profile("level1")
if __name__ == "__main__":
    manifest.json_save("0117-add-image-thumbnail.json")