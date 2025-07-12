/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

export class ExternalSaleOrderList extends Component {
    setup() {
        this.state = useState({
            saleOrders: [],
            loading: true,
        });

        onWillStart(async () => {
            const token = new URLSearchParams(window.location.search).get("token");
            const res = await jsonrpc("/external/sale_order/list-data", { token });
            this.state.saleOrders = res.sale_orders;
            this.state.loading = false;
            this.partnerName = res.partner_name;
            this.partnerEmail = res.partner_email;
            this.partnerAddress = res.partner_address;
        });
    }

    getStatusClass(state) {
        return {
            draft: "bg-info",
            sent: "bg-primary",
            sale: "bg-success",
            cancel: "bg-danger",
        }[state] + " rounded-pill py-1 px-3 text-white";
    }
}

ExternalSaleOrderList.template = "external_sale_invoice.ExternalSaleOrderList";
registry.category("public_components").add("external_sale_invoice.ExternalSaleOrderList", ExternalSaleOrderList);
