import asyncio
import logging
from datetime import datetime

import httpx
from openg2p_common_g2pconnect_id_mapper.models.common import RequestStatusEnum
from openg2p_common_g2pconnect_id_mapper.models.link import (
    LinkCallbackHttpRequest,
    LinkCallbackRequest,
    LinkHttpRequest,
    LinkRequestStatusReasonCode,
    SingleLinkCallbackRequest,
)
from openg2p_common_g2pconnect_id_mapper.models.message import (
    MsgCallbackHeader,
    MsgHeaderStatusReasonCodeEnum,
)
from openg2p_common_g2pconnect_id_mapper.models.resolve import ResolveHttpRequest
from openg2p_common_g2pconnect_id_mapper.models.update import (
    SingleUpdateCallbackRequest,
    UpdateCallbackHttpRequest,
    UpdateCallbackRequest,
    UpdateHttpRequest,
)
from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.service import BaseService
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..config import Settings
from ..models.orm.id_fa_mapping import IdFaMapping

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class MapperService(BaseService):
    async def link(self, correlation_id: str, request: LinkHttpRequest):
        total_request_count = len(request.message.link_request)
        total_count = 0
        failure_count = 0

        response = LinkCallbackHttpRequest(
            # TODO: dummy signature
            signature=request.signature,
            header=MsgCallbackHeader(
                message_id=request.header.message_id,
                message_ts=datetime.utcnow(),
                action="link",
                status=RequestStatusEnum.succ,
                total_count=total_request_count,
                sender_id=_config.callback_sender_id,
                receiver_id=request.header.sender_id,
                is_msg_encrypted=False,
            ),
            message=LinkCallbackRequest(
                transaction_id=request.message.transaction_id,
                correlation_id=correlation_id,
                link_response=[],
            ),
        )

        session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        async with session_maker() as session:
            for each_req in request.message.link_request:
                single_response = SingleLinkCallbackRequest(
                    reference_id=each_req.reference_id,
                    fa=each_req.fa,
                    timestamp=datetime.utcnow(),
                    status=RequestStatusEnum.succ,
                    additional_info=each_req.additional_info,
                    locale=each_req.locale,
                )
                try:
                    session.add(
                        IdFaMapping(
                            id_value=each_req.id,
                            fa_value=each_req.fa,
                            name=each_req.name,
                            phone=each_req.phone_number,
                            additional_info=[
                                info.model_dump() for info in each_req.additional_info
                            ],
                            active=True,
                            created_at=single_response.timestamp,
                        )
                    )
                    await session.commit()
                except IntegrityError as e:
                    if "Unique" in str(e):
                        single_response.status = RequestStatusEnum.rjct
                        single_response.status_reason_code = (
                            LinkRequestStatusReasonCode.rjct_id_invalid
                        )
                        single_response.status_reason_message = (
                            "Duplicate ID exists. Use 'update' instead."
                        )
                        failure_count += 1
                    else:
                        raise

                total_count += 1
                response.message.link_response.append(single_response)
        response.header.completed_count = total_count
        if total_count == failure_count:
            response.header.status = RequestStatusEnum.rjct
            response.header.status_reason_code = (
                MsgHeaderStatusReasonCodeEnum.rjct_errors_too_many
            )
            response.header.status_reason_message = (
                "All requests in transaction failed."
            )
        self.make_callback(
            response, url=request.header.sender_uri, url_suffix="/on-link"
        )

    async def update(self, correlation_id: str, request: UpdateHttpRequest):
        total_request_count = len(request.message.update_request)
        total_count = 0
        failure_count = 0

        response = UpdateCallbackHttpRequest(
            # TODO: dummy signature
            signature=request.signature,
            header=MsgCallbackHeader(
                message_id=request.header.message_id,
                message_ts=datetime.utcnow(),
                action="update",
                status=RequestStatusEnum.succ,
                total_count=total_request_count,
                sender_id=_config.callback_sender_id,
                receiver_id=request.header.sender_id,
                is_msg_encrypted=False,
            ),
            message=UpdateCallbackRequest(
                transaction_id=request.message.transaction_id,
                correlation_id=correlation_id,
                update_response=[],
            ),
        )
        session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        async with session_maker() as session:
            for each_req in request.message.update_request:
                single_response = SingleUpdateCallbackRequest(
                    reference_id=each_req.reference_id,
                    timestamp=datetime.utcnow(),
                    id=each_req.id,
                    status=RequestStatusEnum.succ,
                    additional_info=each_req.additional_info,
                    locale=each_req.locale,
                )

                query = select(IdFaMapping).where(IdFaMapping.id_value == each_req.id)
                result = await session.execute(query)
                result = result.scalar()
                if result:
                    if each_req.fa:
                        result.fa_value = each_req.fa
                    if each_req.name:
                        result.name = each_req.name
                    if each_req.phone_number:
                        result.phone = each_req.phone_number
                    if each_req.additional_info:
                        addl_info_copy = result.additional_info.copy()
                        addl_info_keys = [info["name"] for info in addl_info_copy]
                        for info in each_req.additional_info:
                            if info.name in addl_info_keys:
                                addl_info_copy[
                                    addl_info_keys.index(info.name)
                                ] = info.model_dump()
                            else:
                                addl_info_copy.append(info.model_dump())
                    result.additional_info = addl_info_copy

                    await session.commit()
                else:
                    single_response.status = RequestStatusEnum.rjct
                    single_response.status_reason_code = (
                        LinkRequestStatusReasonCode.rjct_id_invalid
                    )
                    single_response.status_reason_message = (
                        "Mapping doesnt exist against given ID. Use 'link' instead."
                    )
                    failure_count += 1

                total_count += 1
                response.message.update_response.append(single_response)
        response.header.completed_count = total_count
        if total_count == failure_count:
            response.header.status = RequestStatusEnum.rjct
            response.header.status_reason_code = (
                MsgHeaderStatusReasonCodeEnum.rjct_errors_too_many
            )
            response.header.status_reason_message = (
                "All requests in transaction failed."
            )
        self.make_callback(
            response, url=request.header.sender_uri, url_suffix="/on-update"
        )

    async def resolve(self, correlation_id: str, request: ResolveHttpRequest):
        # session_maker = async_sessionmaker(dbengine.get(), expire_on_commit=False)
        # async with session_maker() as session:
        #     for _each_req in request.message.link_request:
        pass

    def make_callback(self, response, url=None, url_suffix=None):
        _logger.info("Make Callback Response json: %s", response.model_dump_json())
        if not (url or _config.default_callback_url):
            return
        elif not url:
            url = _config.default_callback_url

        asyncio.create_task(self._callback(response, url=url, url_suffix=url_suffix))

    async def _callback(self, response: BaseModel, url, url_suffix=None):
        res = httpx.post(f"{url.rstrip('/')}{url_suffix}", json=response.model_dump())
        _logger.debug("Mapper callback Response:  %s", res.content)
        res.raise_for_status()
