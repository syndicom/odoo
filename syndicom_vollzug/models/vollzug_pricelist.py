# -*- coding: utf-8 -*-
from odoo import models, fields
from datetime import date


class SyndicomVollzugPricelist(models.Model):
    _name = 'syndicom.vollzug.pricelist'
    _description = 'Vollzug Preisliste'

    # TODO: compute aktiv aufgrund von date_from und date_to
    active = fields.Boolean(string='Aktiv',compute="_compute_is_active", store=True)

    gav_id = fields.Many2one(comodel_name='res.partner', string='GAV Partner')
    category = fields.Selection(string='Beitrag für', selection=[('verband', 'Verbandsmitglieder'), ('ev', 'Einzelverbandsmitglieder'), ('nicht', 'Nicht-Verband')])
    logic = fields.Selection(string='Berechnungslogik', selection=[('absolut', 'Absolute Beträge'), ('prozent', 'Prozentual'),])
    
    amount_tz = fields.Float(string='Teilzeit')
    amount_vz = fields.Float(string='Vollzeit')
    amount_lernend = fields.Float(string='Lernende')
    
    amount_ag_tz = fields.Float(string='AG-Beitrag Teilzeit')
    amount_ag_vz = fields.Float(string='AG-Beitrag Vollzeit')
    amount_ag_lernend = fields.Float(string='AG-Beitrag Lernende')
    
    
    discount_max = fields.Float(string='Rabatt Max.', digits=(4, 13))
    discount = fields.Float(string='Rabatt in %')
    
    date_from = fields.Date(string='Gültig ab')
    date_to = fields.Date(string='Gültig bis')

    def _compute_is_active(self):
        for rec in self:
            date_start = rec.date_from
            date_end = rec.date_to

            if date_start == False:
                date_start = date.today()
            
            if date_start <= date.today() and (date_end == False or date_end >= date.today()):
                rec.active = True
            else:
                rec.active = False

    def _get_by_date(self, filter_date):
        """Return the first valid pricelist for a given date from a recordset."""
        for pricelist in self:
            if (pricelist.date_from or filter_date).replace(day=1) <= filter_date <= (pricelist.date_to or filter_date):
                return pricelist
        return self.env['syndicom.vollzug.pricelist']
