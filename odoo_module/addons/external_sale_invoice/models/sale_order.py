# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit= 'sale.order'
    
    @api.model
    def sale_order_detail(self, id):
        fields = ['id', 'name', 'partner_id', 'amount_total']
        records = self.browse([id])

        result = []
        for order in records:
            order_data = order.read(fields)[0]
            order_data['order_line'] = [
                line.read(['product_id', 'product_id','product_uom_qty', 'price_unit', 'price_subtotal'])
                for line in order.order_line
            ]
            result.append(order_data)
        return result
    
    def get_external_url(self):
        external_url = "/external/sale-invoice/{}?token={}".format(self.id,self.partner_id.x_external_token)
        return external_url