# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomInstitute(models.Model):
    _name = 'syndicom.course.institute'

    name = fields.Char('Name', required=True, translate=True)
    product_id = fields.Many2one(comodel_name='product.product', string='Produkt für Member Service')
    
