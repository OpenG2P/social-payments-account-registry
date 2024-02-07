#!/usr/bin/env python3

import csv
import sys
import traceback
import uuid
from datetime import datetime

import requests

# Change the following configurations depending on your spar instance
mapper_link_api_url = "https://spar.dev.openg2p.net/mapper/v1/mapper/sync/link"
csv_path = "sample_data.csv"
branch_code = "indigo"
bank_code = "dfsp2"
tokenize_national_id = True
tokenization_partner_id = "openg2p-auth-partner"

# Mappings
csv_file = None


def close():
    if csv_file:
        csv_file.close()
    input("Press Enter to exit...")
    sys.exit(1)


def convert_nationalid_to_token(national_id, partner_id):
    # The logic to token national id will need to be modified
    # according to national id provider.
    import base64

    from cryptography.hazmat.primitives import hashes

    hash_algo = hashes.SHA3_256()
    digest = hashes.Hash(hash_algo)
    digest.update(f"{national_id}{partner_id}".encode(encoding="utf-8"))
    token = base64.urlsafe_b64encode(digest.finalize()).decode().rstrip("=")
    return token


try:
    csv_file = open(csv_path)
except Exception:
    print(f"Could not open the file at the given path: {csv_path}")
    close()


def perform_mapping():
    csv_reader = csv.reader(csv_file)
    csv_content = list(csv_reader)
    header = csv_content[0]
    id_mapper_list = []

    datetime_now = datetime.now().isoformat()

    for line in csv_content[1:]:
        national_id = line[header.index("National ID")]
        account_no = line[header.index("Account number")]
        name = line[header.index("Name")]
        phone_num = line[header.index("Phone")]

        if tokenize_national_id:
            national_id = convert_nationalid_to_token(
                national_id, tokenization_partner_id
            )

        id_mapper_list.append(
            {
                "reference_id": str(uuid.uuid4()),
                "timestamp": datetime_now,
                "id": f"token:{national_id}@nationalId",
                "fa": f"account:{account_no}@{branch_code}.{bank_code}.bank_acc",
                "name": name if name else None,
                "phone_number": phone_num if phone_num else None,
                "additional_info": None,
                "locale": "eng",
            }
        )

    res = requests.post(
        mapper_link_api_url,
        json={
            "header": {
                "action": "link",
                "is_encrypted": False,
                "message_id": str(uuid.uuid4()),
                "message_ts": datetime_now,
                "receiver_id": "pymts.example.org",
                "sender_id": "registry.example.org",
                "sender_uri": "http://spar-social-payments-account-registry.spar/internal/callback/mapper",
                "total_count": len(id_mapper_list),
                "version": "0.1.0",
            },
            "message": {
                "link_request": id_mapper_list,
                "transaction_id": str(uuid.uuid4()),
            },
            "signature": 'Signature:  namespace="g2p", kidId="{sender_id}|{unique_key_id}|{algorithm}", algorithm="ed25519", created="1606970629", expires="1607030629", headers="(created) (expires) digest", signature="Base64(signing content)',
        },
    )
    print(res.text)
    try:
        res.raise_for_status()
    except Exception:
        traceback.print_exc()


perform_mapping()
close()
