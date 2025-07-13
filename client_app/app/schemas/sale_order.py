from pydantic import BaseModel, Field, RootModel
from typing import List, Any, Optional, Dict


class SaleOrderLineCreateRequest(BaseModel):
    id: Optional[int] = None
    product_id: int
    name: str
    product_uom_qty: float = 1.0
    price_unit: float


class SaleOrderCreateRequest(BaseModel):
    id: Optional[int] = None
    partner_id: int
    order_line: List[SaleOrderLineCreateRequest] = Field(alias="order_line")


class SaleOrderCreateListRequest(RootModel[List[SaleOrderCreateRequest]]):
    def to_odoo_payload(self) -> List[dict]:
        """Convert request to list of dicts with order_line in One2many format"""
        result = []
        for order in self.root:
            order_dict = order.model_dump(exclude={"id"})
            order_dict["order_line"] = [
                (0, 0, line.model_dump(exclude={"id"})) for line in order.order_line
            ]
            result.append(order_dict)
        return result

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "partner_id": 1,
                    "order_line": [
                        {
                            "price_unit": 290,
                            "name": "[FURN_6666] Acoustic Bloc Screens",
                            "product_id": 31,
                            "product_uom_qty": 1,
                        },
                        {
                            "price_unit": 140,
                            "name": "[E-COM11] Cabinet with Doors",
                            "product_id": 21,
                            "product_uom_qty": 1,
                        },
                    ],
                }
            ]
        }
    }


class SaleOrderWriteRequest(RootModel[Dict[str, Any]]):

    def to_odoo_payload(self) -> List[dict]:
        order_dict = self.root
        order_line = []
        for line in order_dict.get("order_line", []):
            if "id" not in line:
                raise ValueError("Missing 'id' in order_line item")
            line_id = line.pop("id")
            order_line.append((1, line_id, line))
        order_dict["order_line"] = order_line
        return order_dict

    model_config = {
        "json_schema_extra": {
            "example": {
                "partner_id": 1,
                "order_line": [
                    {
                        "id": 1,
                        "product_id": 23,
                        "product_uom_qty": 2,
                        "price_unit": 50000,
                    },
                    {
                        "id": 2,
                        "product_id": 23,
                        "product_uom_qty": 1,
                        "price_unit": 75000,
                    },
                ],
            }
        }
    }


class SaleOrderCreateListResponse(BaseModel):
    ids: List[int] = Field(..., example=[1, 2, 3])


class SaleOrderSearchRequest(BaseModel):
    domain: List[Any] = Field(default_factory=list, example=[["state", "=", "sale"]])
    fields: List[str] = Field(
        default_factory=lambda: ["id", "name"],
        example=["id", "name", "partner_id", "amount_total"],
    )
    limit: Optional[int] = Field(default=None, example=10)


class SaleOrderSearchResponse(RootModel[List[Dict[str, Any]]]):
    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "id": 16,
                    "name": "S00016",
                    "partner_id": "Decco Addict",
                    "amount_total": 1364.48,
                }
            ]
        }
    }


class SaleOrderDetailResponse(RootModel[List[Dict[str, Any]]]):
    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "id": 16,
                    "name": "S00016",
                    "partner_id": "Decco Addict",
                    "amount_total": 1364.48,
                    "order_line": [
                        {
                            "product_id": 31,
                            "product_name": "Acoustic Bloc Screens",
                            "product_uom_qty": 3.0,
                            "price_unit": 275.0,
                            "subtotal": 825.0,
                        },
                        {
                            "product_id": 25,
                            "product_name": "Office Chair Black",
                            "product_uom_qty": 3.0,
                            "price_unit": 120.5,
                            "subtotal": 361.5,
                        },
                    ],
                }
            ]
        }
    }
