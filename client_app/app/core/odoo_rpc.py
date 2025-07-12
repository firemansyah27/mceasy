import xmlrpc.client
import os
from typing import List, Dict, Any
import logging
from fastapi import HTTPException
from app.core.enums import MODELS

_logger = logging.getLogger(__name__)


class XmlrpcClient:
    def __init__(self):
        self.url = os.getenv("ODOO_URL")
        self.db = os.getenv("ODOO_DB")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PASSWORD")

        if not all([self.url, self.db, self.username, self.password]):
            raise EnvironmentError("Missing Odoo environment variables.")

        self.uid = self._authenticate()
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")

    def _authenticate(self):
        common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        uid = common.authenticate(self.db, self.username, self.password, {})
        if not uid:
            raise ConnectionError("Authentication with Odoo XML-RPC failed.")
        return uid

    def _execute_kw(
        self,
        model: str,
        method: str,
        args: List[Any] = None,
        kwargs: Dict[str, Any] = None,
    ):
        args = args or []
        kwargs = kwargs or {}

        try:
            return self.models.execute_kw(
                self.db, self.uid, self.password, model, method, args, kwargs
            )
        except xmlrpc.client.Fault as fault:
            _logger.error(f"Odoo RPC Fault: {fault.faultString}")
            raise HTTPException(status_code=400, detail=self._parse_fault(fault))

    def _parse_fault(self, fault: xmlrpc.client.Fault) -> str:
        try:
            lines = fault.faultString.strip().split("\n")
            for line in reversed(lines):
                if line.strip() and not line.strip().startswith("File"):
                    return line.strip()
            return "Unknown error from Odoo"
        except Exception:
            return "Malformed fault string from Odoo"

    def create(self, model: str, data: List[Dict]):
        return self._execute_kw(model=model, method="create", args=[data])

    def write(self, model: str, ids: List[int], data: Dict) -> bool:
        return self._execute_kw(model=model, method="write", args=[ids, data])

    def search_read(
        self,
        model: str,
        domain: List = None,
        fields: List[str] = None,
        limit: int = None,
    ):
        domain = domain or []
        fields = fields or ["id", "name"]
        kwargs = {"fields": fields}
        if limit:
            kwargs["limit"] = limit

        return self._execute_kw(
            model=model, method="search_read", args=[domain], kwargs=kwargs
        )

    def sale_order_search_read(self, id: int):
        return self._execute_kw(
            model=MODELS.SALE_ORDER,
            method="sale_order_detail",
            args=[id],
        )
        
    def confirm_sale_order(self, id: int):
        return self._execute_kw(
            model=MODELS.SALE_ORDER,
            method="action_confirm",
            args=[id],
        )
        
    def cancel_sale_order(self, id: int):
        result = self._execute_kw(
            model=MODELS.SALE_ORDER,
            method="action_cancel",
            args=[id],
        )
        if isinstance(result, dict) and result.get("type") == "ir.actions.act_window":
            context = result.get("context", {})
            context["default_order_id"] = id
            wizard_id = self._execute_kw(
                model="sale.order.cancel",
                method="create",
                args=[{}],
                kwargs={"context": context},
            )
            cancel_result = self._execute_kw(
                model="sale.order.cancel",
                method="action_cancel",
                args=[[wizard_id]],
            )
            return cancel_result
        return result
        
    def draft_sale_order(self, id: int):
        return self._execute_kw(
            model=MODELS.SALE_ORDER,
            method="action_draft",
            args=[id],
        )
