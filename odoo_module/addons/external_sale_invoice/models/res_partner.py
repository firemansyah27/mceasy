# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import hashlib


class ResPartner(models.Model):
    _inherit= 'res.partner'
    
    x_external_token = fields.Char('External Token')
    
    def generate_external_token(self):
        for partner in self:
            raw_string = f"{partner.id}-{partner.name or ''}-{partner.email or ''}"
            token = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
            partner.x_external_token = token