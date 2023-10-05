#!/usr/bin/env python3

from social_payments_account_registry.app import Initializer as SparInitializer
from spar_mapper_g2p_connect.app import Initializer as SparG2PConnectMapperInitializer

main_init = SparInitializer()
SparG2PConnectMapperInitializer()

main_init.main()
