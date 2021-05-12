# pip install requests
import requests
iiifimageurl = "http://lezioni.meneghetti.univr.it//imageapi/m0171_0/m0171_0visn20_0001a21.jp2/info.json" 
imageinfo =  requests.get(iiifimageurl)
jsoninfo = imageinfo.json()
imgwidth = jsoninfo['width']
imgheight = jsoninfo['height']