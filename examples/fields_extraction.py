from IIIFpres.utilities import read_API3_json
mymanifest = read_API3_json('tests/integration/fixtures/0024-book-4-toc.json')
fields = []
for i in mymanifest.items:
    imgurl = i.items[0].items[0].body['service'][0]['id']
    fields.append((i.label['en'][0],i.width,i.height,imgurl,"/full/max/0/default.jpg"))
print(fields)