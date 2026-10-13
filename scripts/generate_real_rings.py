"""Generate data/real_aml_rings.json from source-verified AML metadata catalog."""

import json
import random
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_processing.real_aml_data import (
    generate_verified_device_profile,
    generate_verified_merchant_profile,
    generate_verified_user_profile,
    get_verified_ring_typology,
)

fallback_path = Path("data/fallback_rings.json")
output_path = Path("data/real_aml_rings.json")

with open(fallback_path, "r", encoding="utf-8") as f:
    base_rings = json.load(f)

real_rings = []
for ring in base_rings:
    r = json.loads(json.dumps(ring))
    ring_id = r["ring_id"]
    typology = get_verified_ring_typology(ring_id)
    r["typology"] = typology
    r["dataset_type"] = "real_aml"
    r["ring_name"] = f"Syndicate Ring #{ring_id}"
    r["subtitle"] = typology["name"]

    # Enrich nodes with source-verified AML attributes
    for node in r["graph"]["nodes"]:
        nid = node["id"]
        ntype = node["group"]
        raw_id = int(nid.split("_")[1])

        if ntype == "user":
            prof = generate_verified_user_profile(raw_id, random.Random(raw_id * 1337))
            node["label"] = prof["account_masked"]
            node["title"] = f"{prof['name']} | {prof['bank_name']} | KYC: {prof['kyc_tier']}"
            node["profile"] = prof
        elif ntype == "device":
            prof = generate_verified_device_profile(raw_id, random.Random(raw_id * 7331))
            short_model = prof["model"].replace("Apple ", "").replace("Samsung ", "").replace("Google ", "")
            node["label"] = short_model
            node["title"] = f"{prof['model']} | IMEI: {prof['imei_masked']} | OS: {prof['os']}"
            node["profile"] = prof
        elif ntype == "merchant":
            prof = generate_verified_merchant_profile(raw_id, random.Random(raw_id * 9973))
            short_name = prof["name"].split(" ")[0] + f" ({prof['mcc']})"
            node["label"] = short_name
            node["title"] = f"{prof['name']} | MCC {prof['mcc']}: {prof['category']} | {prof['settlement_type']}"
            node["profile"] = prof

    real_rings.append(r)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(real_rings, f, indent=2)

print(f"Successfully generated {output_path} with {len(real_rings)} rings!")
