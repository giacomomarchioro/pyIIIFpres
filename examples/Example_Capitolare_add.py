
from subprocess import check_output
import glob
import sys
import os 
from IIIFpres import iiifpapi3
from itertools import cycle
#folder = sys.argv[2]
folder = r"/Users/univr/Pictures/41"
romconv = {1: 'I',
 2: 'II',
 3: 'III',
 4: 'IV',
 5: 'V',
 6: 'VI',
 7: 'VII',
 8: 'VIII',
 9: 'IX',
 10: 'X',
 11: 'XI',
 12: 'XII',
 13: 'XIII',
 14: 'XIV',
 15: 'XV',
 16: 'XVI',
 17: 'XVII',
 18: 'XVIII',
 19: 'XIX'}

tsv_datasetpath = r"/Users/univr/Pictures/TEST IIF/lista manoscritti - Versione_con_aggiunte.tsv"
segnatura = 41
def search(segnatura):
    with open(tsv_datasetpath,'r') as f:
        header = True 
        for i in f:
            records = i.split("\t")
            if header:
                h = records
                header = False
            elif records[5]  == str(segnatura):
                return dict(zip(h,records))
record = search(segnatura)

iiifpapi3.BASE_URL = "http://lezioni.meneghetti.univr.it//manifests//%s" %segnatura
manifest = iiifpapi3.Manifest()
manifest.set_id()
segn = "%s (%s)" %(record["numero_del_codice"],record["numerazione_araba"])
manifest.add_label("it","Manoscritto: %s" %segn)

manifest.add_metadata(label="rilegatura_moderna",value=record["rilegatura_moderna"],language_l="it")
manifest.add_metadata(label="Collocazione:",value=record["Collocazione"],language_l="it")
manifest.add_metadata(label="Segnatura espressa come numero arabo:",value=record["roman_converted"],language_l="it")
manifest.add_metadata(label="Segnatura:",value=record["numero_del_codice"],language_l="it")
manifest.add_metadata(label="Antica segnatura con numero arabo:",value=record["numerazione_araba"],language_l="it")
manifest.add_metadata(label="Titolo secondo don Spagnolo:",value=record["titolo"],language_l="it")
manifest.add_metadata(label="Materiale",value=record["materiale"],language_l="it")
manifest.add_metadata(label="Numero di fogli",value=record["fogli"],language_l="it")

if "-" in record["Spagnolo"]:
    pagsp = "pagine %s" %record["Spagnolo"]
else: 
    pagsp = "pagina %s" %record["Spagnolo"]

manifest.add_metadata(label="Riferimento al catalogo di don Spagnolo",value=pagsp,language_l="it")
if record["datazione_f"] != "":
    if int(record["datazione_f"][:-2]) - 1 == int(record["datazione_i"][:-2]):
        datazione = "al %s secolo" %romconv[int(record["datazione_f"][:-2])]
    else:
        datazione = "tra i secoli %s e %s" %(romconv[int(record["datazione_f"][:-2])],romconv[int(record["datazione_f"][:-2])])
manifest.add_metadata(label="Databile",value=datazione,language_l="it",language_v="it")
manifest.add_metadata(label="lingua",value=record["lingua"],language_l="it")
if record["altezza"] != "" and record["ampiezza"] != "":
    dim = "%s x %s cm" %(record["altezza"],record["ampiezza"])

manifest.add_metadata(label="Dimensioni",value=dim,language_l="it")
manifest.add_metadata(label="Rilegatura:",value=record["rilegatura"],language_l="it")
manifest.add_metadata(label="Tipo di rilegatura",value=record["tipo_rilegatura"],language_l="it")
manifest.add_metadata(label="Materiale rilegatura",value=record["materiale_rilegatura"],language_l="it")
# more complex entry can be mapped directly to a dictionary and inserted using entry arguments
manifest.add_summary(f"Il manoscritto {segn} è databile {datazione} secondo le informazioni riportate nell catalogo di don Spagnolo ({pagsp}).  ",language="it")
thum = manifest.add_thumbnail()
manifest.set_viewingDirection("left-to-right")
manifest.add_behavior("paged")
manifest.set_navDate(f"{record['datazione_i']}-01-01T00:00:00Z")
manifest.set_rights("https://creativecommons.org/licenses/by/4.0/")
manifest.add_requiredStatement(label="Attribution",value="Provided by University of Verona",language_l="en",language_v="en")
prov = manifest.add_provider()
prov.add_label("it","Università di Verona")
prov.set_id("https://www.univr.it/it/")
homp = prov.add_homepage()
homp.set_id("https://sites.hss.univr.it/laboratori_integrati/laboratorio-lamedan/")
homp.set_type("Text")
homp.add_label("en","Laboratorio integrati - LAboratorio di Studi MEDioevale e DANteschi")
homp.set_format("text/html")
logo = prov.add_logo()
logo.set_id("https://cdn.univr.it/o/aol-theme/images/logo-univr-colori-80.png")
logo.set_type("Image")
logo.set_format("image/png")


images = sorted([image for image in glob.glob(folder+"/*.jp2")])
piatti_e_carte_di_guardia_ant = 4
fogli = 259
piatti_e_carte_di_guardia_post = 4
plabels = ['dorso','piatto anteriore','risguardia anteriore',]
sidesg1 = cycle(('recto','verso'))
for i in range(piatti_e_carte_di_guardia_ant):
    plabels.append("guardia anteriore %i %s" %(i,next(sidesg1)))
    plabels.append("guardia anteriore %i %s" %(i,next(sidesg1)))

sidesf = cycle(('recto','verso'))
for i in range(fogli):
    plabels.append("%i%s" %(i,next(sidesf)))
    plabels.append("%i%s" %(i,next(sidesf)))

sidesg2 = cycle(('recto','verso'))
for i in range(piatti_e_carte_di_guardia_post):
    plabels.append("guardia posteriore %i %s" %(i,next(sidesg2)))
    plabels.append("guardia posteriore %i %s" %(i,next(sidesg2)))

post_elements = ['risguardia posteriore', 'piatto posteriore']
for i in post_elements:
    plabels.append(i)
    
for idx,d in enumerate(images):
    idx+=1 
    image = os.path.join(folder,d)
    canvas = manifest.add_canvastoitems()
    canvas.set_id(extendbase_url=["canvas","p%s"%idx]) # in this case we use the base url
    out = check_output(["exiftool", image])
    Metadata = dict((e[:32].strip(),e[33:].strip()) for e in out.decode('utf8').split('\n'))
    width = Metadata['Image Width']
    height = Metadata['Image Height']
    canvas.set_height(width)
    canvas.set_width(height)
    canvas.add_label("it",plabels[idx])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url=["page","p%s"%idx,"1"])
    annotation = annopage.add_annotation_toitems(targetid=canvas.id)
    annotation.set_id(extendbase_url=["annotation","p%s-image"%str(idx).zfill(4)])
    annotation.set_motivation("painting")
    annotation.body.set_id(image)
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jp2")
    annotation.body.set_width(width)
    annotation.body.set_height(height)
    s = annotation.body.add_service()
    s.set_id(d[3])
    s.set_type("ImageService2")
    s.set_profile("level2")
    
    
rng = manifest.add_rangetostructures()
rng.set_id(extendbase_url=["range","r0"])
rng.add_label("en","Table of Contents")
rng2 = iiifpapi3.Range()
rng2.set_id(extendbase_url=["range","r1"])
rng2.add_label("en","Introduction")
rng2.set_supplementary("https://example.org/iiif/book1/annocoll/introTexts")
rng2.add_canvas_to_items("https://example.org/iiif/book1/canvas/p1")
sr = iiifpapi3.SpecificResource()
sr.set_source("https://example.org/iiif/book1/canvas/p2")
fs = iiifpapi3.FragmentSelector()
fs.set_xywh(0,0,750,300)
sr.set_selector(fs)
rng2.add_item(sr)
rng.add_item(rng2)
annopage3 = iiifpapi3.AnnotationPage()
annopage3.set_id("https://example.org/iiif/book1/page/manifest/1")
anno = iiifpapi3.Annotation(manifest.id)
anno.set_id("https://example.org/iiif/book1/page/manifest/a1")
anno.set_motivation("commenting")
anno.body.set_language("en")
anno.body.set_value("I love this manifest!")
annopage3.add_item(anno)
annopage3.set_id("https://example.org/iiif/book1/page/manifest/1")        
manifest.add_annotation(annopage3)

manifest.json_save("manifest.json")