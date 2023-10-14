from openg2p_common_g2pconnect_id_mapper.models.common import (
    MapperValue,
    RequestStatusEnum,
    TxnStatus,
)
from openg2p_common_g2pconnect_id_mapper.service.resolve import MapperResolveService
from openg2p_common_g2pconnect_id_mapper.service.update_link import (
    MapperUpdateOrLinkService,
)
from openg2p_fastapi_common.errors import BaseAppException
from social_payments_account_registry.models.selfservice import (
    GetTxnStatus,
    UpdateTxnStatus,
)
from social_payments_account_registry.services.id_mapper_service import IdMapperService


class G2PConnectIdMapperService(IdMapperService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapper_resolve_service = MapperResolveService.get_component()
        self.mapper_update_link_service = MapperUpdateOrLinkService.get_component()

    async def get_fa_request(self, id: str) -> GetTxnStatus:
        res = await self.mapper_resolve_service.resolve_request(
            [
                MapperValue(id=id),
            ]
        )
        res_status = res.status.value if res.status else ""
        return GetTxnStatus(txn_id=res.txn_id, status=res_status)

    async def get_fa_request_status(self, txn_id: str) -> GetTxnStatus:
        res: TxnStatus = self.mapper_resolve_service.transaction_queue.get(txn_id, None)
        if not res:
            raise BaseAppException(
                "G2P-SGI-300", "Resolve Transaction Id not found", http_status_code=400
            )
        if not res.refs:
            raise BaseAppException(
                "G2P-SGI-301",
                "Resolve Invalid Transaction without any requests found",
                http_status_code=500,
            )
        res_status = res.status.value if res.status else ""
        res_out = GetTxnStatus(txn_id=res.txn_id, status=res_status)
        # TODO: Not compatible with G2P Connect
        # if res.status == RequestStatusEnum.succ:
        if list(res.refs.values())[0].fa:
            res_out.fa = list(res.refs.values())[0].fa
            self.mapper_resolve_service.transaction_queue.pop(res.txn_id)
        return res_out

    async def update_fa_request(self, id: str, fa: str) -> UpdateTxnStatus:
        res = await self.mapper_update_link_service.update_or_link_request(
            [
                MapperValue(id=id, fa=fa),
            ]
        )
        res_status = res.status.value if res.status else ""
        return UpdateTxnStatus(txn_id=res.txn_id, status=res_status)

    async def update_fa_request_status(self, txn_id: str) -> UpdateTxnStatus:
        res: TxnStatus = self.mapper_update_link_service.transaction_queue.get(
            txn_id, None
        )
        if not res:
            raise BaseAppException(
                "G2P-SGI-310", "Update Transaction Id not found", http_status_code=400
            )
        if not res.refs:
            raise BaseAppException(
                "G2P-SGI-311",
                "Invalid Update Transaction without any requests found",
                http_status_code=500,
            )
        res_status = res.status.value if res.status else ""
        res_out = UpdateTxnStatus(txn_id=res.txn_id, status=res_status)
        if res.status == RequestStatusEnum.succ:
            self.mapper_resolve_service.transaction_queue.pop(res.txn_id)
        return res_out
