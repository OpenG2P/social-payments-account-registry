#!/usr/bin/env python3

import csv
import sys
import uuid

import requests

mapper_link_api_url = "https://spar.explore.openg2p.org/mapper/v1/mapper/link"


with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_content = list(csv_reader)
    header = csv_content[0]
    dfsp_list = []
    id_mapper_list = []
    for line in csv_content[1:]:
        national_id = line[header.index("nationalid")]
        id_value = line[header.index("account_no")]
        id_mapper_list.append(
            {
                "reference_id": str(uuid.uuid4()),
                "timestamp": "2022-12-04T17:20:07-04:00",
                "id": f"token:{national_id}@nationalId",
                "fa": f"account:{id_value}@indigo.dfsp1.bank_acc",
                "name": None,
                "phone_number": None,
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
                "message_ts": "2022-12-04T18:01:07+00:00",
                "receiver_id": "pymts.example.org",
                "sender_id": "registry.example.org",
                "sender_uri": "http://spar-social-payments-account-registry.spar/internal/callback/mapper",
                "total_count": 0,
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
    res.raise_for_status()
