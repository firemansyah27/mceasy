/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

export class ButtonInvoice extends Component {

    setup() {
        this.state = useState({
            invReqState: '',
            invId: 0,
            token: new URLSearchParams(window.location.search).get("token"),
        });
        const id = this.props.saleOrderId; 
        const token = this.state.token
        onWillStart(async () => {
            const res = await jsonrpc("/external/invoice-request-state", { id, token});
            this.state.invReqState = res.inv_req_state;
            this.state.invId = res.inv_id;
        });
    }


    async requestInvoice() {
        const id = this.props.saleOrderId;
        const token = this.state.token;
        this.state.loading = true;
        try {
            if (this.state.invReqState === '') {
                const res = await jsonrpc("/external/invoice-request/create", { id, token});
                console.log(res)
                if (res){
                    this.state.invReqState = res.inv_req_state
                    this.state.indId = res.inv_id
                }
            }
        } catch (e) {
            console.error("Error:", e);
        } finally {
            this.state.loading = false;
        }
    }

    async downloadInvoice(){
        const invoiceId = this.state.invId;
        const token = this.state.token;
    
        if (!invoiceId) {
            return;
        }
        const downloadUrl = `/external/invoice/pdf?id=${invoiceId}&token=${token}`;
        window.open(downloadUrl, '_blank');
    }
}

ButtonInvoice.template = "external_sale_invoice.ButtonInvoice";
registry.category("public_components").add("external_sale_invoice.ButtonInvoice", ButtonInvoice);
