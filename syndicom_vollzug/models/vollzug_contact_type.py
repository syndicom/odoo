# -*- coding: utf-8 -*-
from odoo import models, fields



class SyndicomVollzugContactType(models.Model):
    _name = 'syndicom.vollzug.contact.type'
    _description = 'Vollzug Contact Type'
    name = fields.Char('Typ')
    
     