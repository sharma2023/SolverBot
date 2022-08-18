# import requests

# requests.get("https://api.wolframalpha.com/v1/simple", 
#     params={"i": "int 5x dx",
#             "appid": "X2QW7H-AA3VJU6HJ4"}
# )


# import wolframalpha
# import json
    
# if __name__=="__main__":
#     # res = next(wolframalpha.Client("X2QW7H-AA3VJU6HJ4").query("int 5x dx").results).text
#     res = wolframalpha.Client("X2QW7H-AA3VJU6HJ4").query("int 5x dx")
#     retval = json.loads(json.dumps(res))["pod"][0]["subpod"]["img"]["@src"]
#     print(type(retval))
import requests
import os

# API_KEY = os.getenv("DEEPL_API_KEY")

# text = "Riemann Zeta function is a very important function in number theory."
# source_lang = 'EN'
# target_lang = 'JA'

# params = {
#             'auth_key' : API_KEY,
#             'text' : text,
#             'source_lang' : source_lang,
#             "target_lang": target_lang 
#         }

# request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
# result = request.json()

# print(result['translations'][0]['text'])

# https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=2b4f975c75727602&lat=35.685919835030944&lng=139.69470944396042

import json
from xml.etree import ElementTree
import xmltodict

request = requests.post("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=2b4f975c75727602&lat=35.685919835030944&lng=139.69470944396042")

dict_data = xmltodict.parse(request.content)

print(dict_data)
