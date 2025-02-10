import json
import tools
from opencage.geocoder import OpenCageGeocode

key = "f0f52f5d8ceb458c996128b6ae5c4b5b"

geocoder = OpenCageGeocode(key)

with open("../datas/villes_france.json") as file:
    datas = json.load(file)
query = datas[0]["Nom_commune"]

result = geocoder.geocode(query)

print(u"%f;%f;%s;%s" % (
result[0]["geometry"]["lat"],
result[0]["geometry"]["lng"],
result[0]["components"]["country_code"],
 result[0]["annotations"]["timezone"]["name"]))
