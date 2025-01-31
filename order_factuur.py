import json
import os
import shutil

order_dir = "Project-2-\\JSON_ORDER"
factuur_dir = "Project-2-\\JSON_INVOICE"
processed_dir = "Project-2-\\JSON_PROCESSED"

os.makedirs(factuur_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

for filename in os.listdir(order_dir):
    if filename.endswith(".json"):
        order_folder = os.path.join(order_dir, filename)
        with open(order_folder) as order:
            order_data = json.load(order)
        
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
            json.dump(order_data, factuur, indent=4)

        shutil.move(order_folder, os.path.join(processed_dir, filename))

