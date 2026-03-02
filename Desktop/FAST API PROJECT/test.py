import requests


def decode_vin(vin):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
    response = requests.get(url)
    data = response.json()
    return data["Results"]


# Usage
results = decode_vin("1HGCM82633A004352")
for item in results:
    if item["Value"] and item["Value"] != "Not Applicable":
        print(f"{item['Variable']}: {item['Value']}")
```

---

# Other Useful Endpoints (same base URL)
```
# Get all makes
GET https: // vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format = json

# Get models for a make
GET https: // vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/toyota?format = json

# Get models for a make + year
GET https: // vpic.nhtsa.dot.gov/api/vehicles/getmodelsformakeyear/make/toyota/modelyear/2020?format = json

# Decode VIN with model year (more accurate)
GET https: // vpic.nhtsa.dot.gov/api/vehicles/decodevin/1HGCM82633A004352?format = json & modelyear = 2020
