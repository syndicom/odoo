# -*- coding: utf-8 -*-

from odoo import fields,models

class BaseUserRole(models.Model):
   _inherit = "res.users.role"
   for_newsletter = fields.Boolean(string='Auch für Newsletter berechtigungen')
   