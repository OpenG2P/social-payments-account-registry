import orjson
import redis.asyncio as redis_asyncio
from openg2p_common_g2pconnect_id_mapper.context import queue_redis_async_pool
from openg2p_common_g2pconnect_id_mapper.models.common import (
    MapperValue,
    RequestStatusEnum,
    SingleTxnRefStatus,
    TxnStatus,
)
from openg2p_common_g2pconnect_id_mapper.service.link import MapperLinkService
from openg2p_common_g2pconnect_id_mapper.service.resolve import MapperResolveService
from openg2p_common_g2pconnect_id_mapper.service.update import MapperUpdateService
from openg2p_fastapi_common.errors import BaseAppException
from social_payments_account_registry.models.selfservice import (
    GetTxnStatus,
    UpdateTxnStatus,
)
from social_payments_account_registry.services.id_mapper_service import IdMapperService

from ..config import Settings

_config = Settings.get_config()


class G2PConnectIdMapperService(IdMapperService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapper_resolve_service = MapperResolveService.get_component()
        self.mapper_link_service = MapperLinkService.get_component()
        self.mapper_update_service = MapperUpdateService.get_component()

    async def get_fa_request(self, id: str) -> GetTxnStatus:
        res = await self.mapper_resolve_service.resolve_request(
            [
                MapperValue(id=id),
            ],
            wait_for_response=False,
        )
        res_status = res.status.value if res.status else ""
        return GetTxnStatus(txn_id=res.txn_id, status=res_status)

    async def get_fa_request_status(self, txn_id: str) -> GetTxnStatus:
        queue = redis_asyncio.Redis(connection_pool=queue_redis_async_pool.get())
        if not await queue.exists(f"{_config.queue_resolve_name}{txn_id}"):
            await queue.aclose()
            raise BaseAppException(
                "G2P-SGI-300", "Resolve Transaction Id not found", http_status_code=400
            )
        res = TxnStatus.model_validate(
            orjson.loads(await queue.get(f"{_config.queue_resolve_name}{txn_id}"))
        )
        await queue.aclose()
        txn_id = res.txn_id
        if not res.refs:
            raise BaseAppException(
                "G2P-SGI-301",
                "Resolve Invalid Transaction without any requests found",
                http_status_code=400,
            )
        single_res: SingleTxnRefStatus = list(res.refs.values())[0]
        single_res_status = single_res.status.value if single_res.status else ""
        single_res_out = GetTxnStatus(txn_id=txn_id, status=single_res_status)
        if single_res.status == RequestStatusEnum.succ:
            single_res_out.fa = single_res.fa
        return single_res_out

    async def update_fa_request(
        self, id: str, fa: str, link: bool = False
    ) -> UpdateTxnStatus:
        if link:
            res = await self.mapper_link_service.link_request(
                [
                    MapperValue(id=id, fa=fa),
                ],
                wait_for_response=False,
            )
        else:
            res = await self.mapper_update_service.update_request(
                [
                    MapperValue(id=id, fa=fa),
                ],
                wait_for_response=False,
            )
        res_status = res.status.value if res.status else ""
        return UpdateTxnStatus(txn_id=res.txn_id, status=res_status)

    async def update_fa_request_status(
        self, txn_id: str, link: bool = False
    ) -> UpdateTxnStatus:
        queue = redis_asyncio.Redis(connection_pool=queue_redis_async_pool.get())
        channel_name = ""
        if link:
            channel_name = _config.queue_link_name
        else:
            channel_name = _config.queue_update_name
        if not await queue.exists(f"{channel_name}{txn_id}"):
            await queue.aclose()
            raise BaseAppException(
                "G2P-SGI-310",
                "Update/Link Transaction Id not found",
                http_status_code=400,
            )
        res = TxnStatus.model_validate(
            orjson.loads(await queue.get(f"{channel_name}{txn_id}"))
        )
        await queue.aclose()
        if not res.refs:
            raise BaseAppException(
                "G2P-SGI-311",
                "Invalid Update Transaction without any requests found",
                http_status_code=400,
            )
        single_res: SingleTxnRefStatus = list(res.refs.values())[0]
        single_res_status = single_res.status.value if single_res.status else ""
        single_res_out = UpdateTxnStatus(txn_id=txn_id, status=single_res_status)
        return single_res_out
