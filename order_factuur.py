import json
import os
import shutil

order_dir = r"C:\school\code\projecten\Project-2-\\JSON_ORDER"
factuur_dir = r"C:\school\code\projecten\Project-2-\\JSON_INVOICE"
processed_dir = r"C:\school\code\projecten\Project-2-\\JSON_PROCESSED"
error_dir = r"C:\school\code\projecten\Project-2-\\JSON_ORDER_ERROR"

os.makedirs(factuur_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(error_dir, exist_ok=True)

for filename in os.listdir(order_dir):
    if filename.endswith(".json"):
        order_folder = os.path.join(order_dir, filename)
        try:
            with open(order_folder) as order:
                order_data = json.load(order)

            totale_subtotaal = 0
            totale_btw = 0

            for product in order_data["order"]["producten"]:
                aantal = product["aantal"]
                prijs_per_stuk = product["prijs_per_stuk_excl_btw"]
                btw = product["btw_percentage"]

                subtotaal = round(aantal * prijs_per_stuk ,2)
                btw_bedrag = round((subtotaal/100)* btw, 2) 
               
                totale_btw += btw_bedrag
                totale_subtotaal += subtotaal
                
            order_data["order"]["subtotaal"] = round(totale_subtotaal,2)
            order_data["order"][f"btw({btw}%)"] = round(totale_btw,2)
            order_data["order"]["totaalbedrag"] = round(totale_subtotaal +  totale_btw, 2)
                
            order_data["Bedrijfsgegevens"] = {"Bedrijfsnaam": "NovaTech Solutions B.V",
                "Bedrijfsadres": "Innovatieplein 12",
                "Postcode & Plaats": "1012 AB Amsterdam",
                "KVK nummer": "KVK87654321",
                "BTW nummer": "NL003456789B01",
                "IBAN": "NL91ABNA0417164300",
                "Telefoonnummer": "+31 20 123 4567",
                "E-mail": "info@novatechsolutions.nl",
                "Website": "www.novatechsolutions.nl"}
            
            factuur = filename.replace(".json", "_factuur.json")
            with open(os.path.join(factuur_dir, factuur), "w") as factuur:
                json.dump(order_data, factuur, indent= 4)

            shutil.move(order_folder, os.path.join(processed_dir, filename))
        except (KeyError, ValueError) as e:
            shutil.move(order_folder, os.path.join(error_dir, filename))



