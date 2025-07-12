from fastapi import APIRouter, Depends, Path
from app.core.security import verify_api_key
from app.core.odoo_rpc import XmlrpcClient
from app.schemas.sale_order import (
    SaleOrderCreateListRequest,
    SaleOrderCreateListResponse,
    SaleOrderSearchRequest,
    SaleOrderSearchResponse,
    SaleOrderDetailResponse,
    SaleOrderWriteRequest,
)
from app.core.enums import MODELS
from typing import List, Any, Dict

sale_routes = APIRouter(
    prefix="/sale_order",
    tags=["Sale Order"],
    dependencies=[Depends(verify_api_key)],
)


@sale_routes.post("", response_model=SaleOrderCreateListResponse)
def create_sale_order(
    body: SaleOrderCreateListRequest, _: str = Depends(verify_api_key)
):
    RPC = XmlrpcClient()
    res = RPC.create(model=MODELS.SALE_ORDER, data=body.to_odoo_payload())
    return SaleOrderCreateListResponse(ids=res)

@sale_routes.post("/search", response_model=SaleOrderSearchResponse)
def search_sale_order(body: SaleOrderSearchRequest, _: str = Depends(verify_api_key)):
    RPC = XmlrpcClient()
    res = RPC.search_read(
        model=MODELS.SALE_ORDER,
        domain=body.domain,
        fields=body.fields,
        limit=body.limit,
    )
    return res

@sale_routes.get("/{id}", response_model=SaleOrderDetailResponse)
def detail_sale_order(
        id: int = Path(..., title="Sale Order ID", description="The ID of the sale order to update", example=1),
        _: str = Depends(verify_api_key)
    ):
    RPC = XmlrpcClient()
    res = RPC.sale_order_search_read(id=id)
    return res

@sale_routes.put("/{id}", response_model=bool)
def write_sale_order(
    body: SaleOrderWriteRequest, 
    id: int = Path(..., title="Sale Order ID", description="The ID of the sale order to update", example=1),
    _: str = Depends(verify_api_key)
):
    RPC = XmlrpcClient()
    res = RPC.write(model=MODELS.SALE_ORDER, ids=[id],data=body.to_odoo_payload())
    return res

@sale_routes.post("/{id}/confirm", response_model=bool)
def confirm_sale_order(
    id: int = Path(..., title="Sale Order ID", description="The ID of the sale order to confirm", example=1),
    _: str = Depends(verify_api_key)
):
    RPC = XmlrpcClient()
    res = RPC.confirm_sale_order(id=id)
    return res

@sale_routes.post("/{id}/cancel", response_model=bool)
def cancel_sale_order(
    id: int = Path(..., title="Sale Order ID", description="The ID of the sale order to cancel", example=1),
    _: str = Depends(verify_api_key)
):
    RPC = XmlrpcClient()
    res = RPC.cancel_sale_order(id=id)
    return res

@sale_routes.post("/{id}/draft", response_model=bool)
def draft_sale_order(
    id: int = Path(..., title="Sale Order ID", description="The ID of the sale order to cancel", example=1),
    _: str = Depends(verify_api_key)
):
    RPC = XmlrpcClient()
    res = RPC.draft_sale_order(id=id)
    return res


