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

with open("example_manifest_response.json") as instance, open("iiif_3_0.json") as schema:
    jsonschema.validate(instance=json.load(instance),schema=json.load(schema))

