#!/usr/bin/env python3

# ruff: noqa: I001

from social_payments_account_registry.app import Initializer as SparInitializer
from spar_connector_g2pconnect.app import (
    Initializer as SparConnectorG2pConnectInitializer,
)
from spar_mojaloop_als_oracle.app import Initializer as MojaloopApiInitializer
from openg2p_common_g2pconnect_id_mapper.app import (
    Initializer as G2pConnectMapperInitializer,
)
from openg2p_fastapi_auth.app import Initializer as AuthInitializer
from openg2p_fastapi_common.ping import PingInitializer

main_init = SparInitializer()
AuthInitializer()
G2pConnectMapperInitializer()
SparConnectorG2pConnectInitializer()
MojaloopApiInitializer()
PingInitializer()

main_init.main()
