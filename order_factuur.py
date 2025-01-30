import json

with open("2000-096.json") as order:
    order_data = json.load(order)

for product in order_data["order"]["producten"]:
    aantal = product["aantal"]
    prijs_per_stuk = product["prijs_per_stuk_excl_btw"]
    btw = product["btw_percentage"]

subtotaal = round(aantal * prijs_per_stuk, 2)
btw_bedrag = round((subtotaal/100)* btw, 2)

order_data["order"]["subtotaal"] = subtotaal
order_data["order"][f"btw({btw}%)"] = btw_bedrag
order_data["order"]["totaalbedrag"] = subtotaal + btw_bedrag

with open("2000-096_factuur.json", "w") as factuur:
    json.dump(order_data, factuur, indent = 4)





