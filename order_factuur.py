import json
with open("Project-2-\\2000-096.json") as order:
    order_data = json.load(order)

for product in order_data["order"]["producten"]:
    aantal = product["aantal"]
    prijs_per_stuk = product["prijs_per_stuk_excl_btw"]
    btw = product["btw_percentage"]

subtotaal = round(aantal * prijs_per_stuk, 2)
btw_bedrag = round((subtotaal/100)* btw, 2)

order_data["Bedrijfsgegevens"] = {"Bedrijfsnaam": "NovaTech Solutions B.V",
    "Bedrijfsadres": "Innovatieplein 12",
    "Postcode & Plaats": "1012 AB Amsterdam",
    "KVK nummer": "KVK87654321",
    "BTW nummer": "NL003456789B01",
    "IBAN": "NL91ABNA0417164300",
    "Telefoonnummer": "+31 20 123 4567",
    "E-mail": "info@novatechsolutions.nl",
    "Website": "www.novatechsolutions.nl"}

order_data["order"]["subtotaal"] = subtotaal
order_data["order"][f"btw({btw}%)"] = btw_bedrag
order_data["order"]["totaalbedrag"] = subtotaal + btw_bedrag

with open("Project-2-\\2000-096_factuur.json", "w") as factuur:
    json.dump(order_data, factuur, indent = 4)