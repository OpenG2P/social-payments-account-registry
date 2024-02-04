#!/usr/bin/env python3

# ruff: noqa: I001

from spar_g2pconnect_id_mapper.app import Initializer as MapperInitializer
from openg2p_fastapi_common.ping import PingInitializer

main_init = MapperInitializer()
PingInitializer()

main_init.main()
