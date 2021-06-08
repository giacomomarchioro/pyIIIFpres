# pip install requests
import requests
# when you use a proxy you might have to use the original link e.g. "http://localhost:1080/iipsrv/iipsrv.fcgi?iiif=/imageapi//m0171_0/m0171_0visn20_0001a21.jp2/info.json"
iiifimageurl = "http://lezioni.meneghetti.univr.it//imageapi/m0171_0/m0171_0visn20_0001a21.jp2/info.json" 
imageinfo =  requests.get(iiifimageurl)
jsoninfo = imageinfo.json()
imgwidth = jsoninfo['width']
imgheight = jsoninfo['height']