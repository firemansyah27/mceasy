# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InvoiceRequest(models.Model):
    _name= 'invoice.request'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    
    sale_id = fields.Many2one('sale.order', string="Sale Order")
    partner_id = fields.Many2one(related='sale_id.partner_id', string="Customer")
    invoice_id = fields.Many2one('account.move')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', string='Status', readonly=True)
    
    def button_reject(self):
        for rec in self:
            rec.state = 'rejected'
            
    def button_approve(self):
        for rec in self:
            if rec.sale_id:
                invoice_ids = rec.sale_id.invoice_ids
                if invoice_ids:
                    rec.invoice_id = invoice_ids[0].id
                else:
                    invoice = rec.sale_id._create_invoices()
                    invoice.action_post()
                    rec.invoice_id = invoice.id
            rec.state = 'approved'
            