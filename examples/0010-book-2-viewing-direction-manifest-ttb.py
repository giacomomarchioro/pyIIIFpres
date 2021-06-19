# https://iiif.io/api/cookbook/recipe/0010-book-2-viewing-direction
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = "https://iiif.io/api/cookbook/recipe/0010-book-2-viewing-direction"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest-ttb.json")
manifest.add_label("en","Diary with Top-to-Bottom Viewing Direction")
manifest.add_summary(language='en',text="William Lewis Sachtleben was an American long-distance cyclist who rode across Asia from Istanbul to Peking in 1891 to 1892 with Thomas Gaskell Allen Jr., his classmate from Washington University. This was part of a longer journey that began the day after they had graduated from college, when they travelled to New York and on to Liverpool; in all they travelled 15,044 miles by bicycle, 'the longest continuous land journey ever made around the world' as reported in their book <cite>Across Asia on a bicycle</cite> (1895). Sachtleben documented his travels with photographs and diaries, the latter of which he numbered sequentially. The diary of notebook 'No. 10' covers a portion of their journey through the Armenian area of Turkey from April 12 to May 9 (there is a 2-page reading list at the end). During this time they rode from Ankara (Angora in the diary) to Sivas, where they stayed for ten days while Allen had a bout of typhoid fever, and the first half of a ten-day excursion to Merzifon (Mersovan in the diary), taken by Sachtleben to give Allen additional time to recover.")
manifest.set_viewingDirection("top-to-bottom")
data = [('image 1',
  2251,
  3152,
  'https://iiif.io/api/image/3.0/example/reference/9ee11092dfd2782634f5e8e2c87c16d5-uclamss_1841_diary_07_02',
  '/full/max/0/default.jpg'),
 ('image 2',
  2268,
  3135,
  'https://iiif.io/api/image/3.0/example/reference/9ee11092dfd2782634f5e8e2c87c16d5-uclamss_1841_diary_07_03',
  '/full/max/0/default.jpg'),
 ('image 3',
  2274,
  3135,
  'https://iiif.io/api/image/3.0/example/reference/9ee11092dfd2782634f5e8e2c87c16d5-uclamss_1841_diary_07_04',
  '/full/max/0/default.jpg'),
 ('image 4',
  2268,
  3135,
  'https://iiif.io/api/image/3.0/example/reference/9ee11092dfd2782634f5e8e2c87c16d5-uclamss_1841_diary_07_05',
  '/full/max/0/default.jpg')]

for idx,d in enumerate(data):
    idx+=1 
    canvas = manifest.add_canvas_to_items()
    canvas.set_id(extendbase_url=["canvas","v%s"%idx]) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("en",d[0])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url=["page","v%s"%idx,"1"])
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url=["annotation","v%s-image"%str(idx).zfill(4)])
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
    manifest.json_save("0010-book-2-viewing-direction_manifest.json")