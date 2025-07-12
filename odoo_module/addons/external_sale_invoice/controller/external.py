# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
import json
import logging

_logger = logging.getLogger(__name__)


class SaleOrderExternal(CustomerPortal):

    @http.route(["/external/sale-invoice"], type="http", auth="public", website=True)
    def external_sale_order(self, token=None, **kw):
        values = self._prepare_portal_layout_values()
        SaleOrder = request.env["sale.order"].sudo()
        domain = [("partner_id.x_external_token", "=", token)]
        sale_order_ids = SaleOrder.search(domain)

        values.update(
            {
                "sale_order_ids": sale_order_ids.sudo(),
                "page_name": "saleordertree",
                "default_url": "/external/sale-invoice?token={}".format(token),
            }
        )
        return request.render("external_sale_invoice.external_sale_list_views", values)

    @http.route(
        ["/external/sale-invoice/<int:id>"], type="http", auth="public", website=True
    )
    def external_sale_order_detail(self, id=None, token=None, message=None, **kw):
        SaleOrder = request.env["sale.order"].sudo()
        domain = [("id", "=", id), ("partner_id.x_external_token", "=", token)]
        sale_order_id = SaleOrder.sudo().search(domain)
        values = {
            "sale_order_id": sale_order_id,
            "page_name": "saleorderform",
            "message": message,
            "report_type": "html",
            "res_company": sale_order_id.company_id,
            "external_token": token,
        }
        return request.render("external_sale_invoice.sale_order_detail", values)

    @http.route("/external/sale_order/list-data", type="json", auth="public")
    def external_sale_order_list_data(self, token):
        SaleOrder = request.env["sale.order"].sudo()
        partner_id = (
            request.env["res.partner"].sudo().search([("x_external_token", "=", token)])
        )
        sale_orders = SaleOrder.search(
            [
                ("invoice_status", "in", ["to invoice", 'invoiced']),
                ("partner_id.x_external_token", "=", token),
            ],
            order="create_date desc",
        )
        if not (sale_orders or partner_id):
            return {
                "sale_orders": [],
                "partner_name": "",
                "partner_email": "",
                "partner_address": "",
            }

        return {
            "sale_orders": [
                {
                    "id": so.id,
                    "name": so.name,
                    "create_date": so.create_date.strftime("%Y-%m-%d %H:%M"),
                    "amount_total": so.amount_total,
                    "state": so.state,
                    "partner_name": so.partner_id.name,
                    "url": so.get_external_url(),
                }
                for so in sale_orders
            ],
            "partner_name": partner_id.name,
            "partner_email": partner_id.email or "",
            "partner_address": partner_id.contact_address or "",
        }

    @http.route("/external/invoice-request-state", type="json", auth="public")
    def invoice_request_state(self, id=None, token=None):
        InvoiceRequest = request.env["invoice.request"].sudo()
        invoice_request_id = InvoiceRequest.search(
            [("sale_id", "=", id), ("sale_id.partner_id.x_external_token", "=", token)],
            limit=1,
        )
        return {
            "inv_req_state": invoice_request_id.state or "",
            "inv_id": invoice_request_id.invoice_id.id,
        }

    @http.route("/external/invoice-request/create", type="json", auth="public")
    def invoice_request_create(self, id=None, token=None):
        InvoiceRequest = request.env["invoice.request"].sudo()
        invoice_request_id = InvoiceRequest.create({"sale_id": id})
        return {
            "inv_req_state": invoice_request_id.state,
            "inv_id": invoice_request_id.invoice_id.id,
        }

    @http.route("/external/invoice/pdf", type="http", auth="public")
    def external_invoice_pdf(self, id=None, token=None):
        invoice = (
            request.env["account.move"]
            .sudo()
            .search([("id", "=", id), ("partner_id.x_external_token", "=", token)])
        )
        if not invoice:
            return request.not_found()

        report = request.env["ir.actions.report"].sudo()
        pdf, _ = report._render_qweb_pdf("account.account_invoices", [invoice.id])
        pdfhttpheaders = [
            ("Content-Type", "application/pdf"),
            ("Content-Length", len(pdf)),
            ("Content-Disposition", 'attachment; filename="%s.pdf"' % (invoice.name)),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
