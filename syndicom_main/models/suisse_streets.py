# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SuisseStreets(models.Model):
    _name = 'suisse.streets'
    _description = 'Schweizer Strassenverzeichnis'
    
    active = fields.Boolean(string='Aktiv',default=True)    

    name = fields.Char(string='Adresssuche', compute='_compute_search_term', store=True)

    street = fields.Char(string='Strasse')
    number = fields.Char(string='Hausnummer')
    zip = fields.Integer(string='PLZ')
    city = fields.Char(string='Stadt')

    city_id = fields.Many2one(comodel_name='res.city', string='Verbundene Stadt')
    lang_id = fields.Many2one(comodel_name='res.lang', string='Hauptsprache')
    country_id = fields.Many2one(comodel_name='res.country', string='Verbundenes Land')
    state_id = fields.Many2one(comodel_name='res.country.state', string='Verbundener Kanton')

    @api.depends('street','number','city','zip')
    def _compute_search_term(self):
        for rec in self:
            if rec.zip and rec.street and rec.city:
                rec.name = str(rec.zip) + ' ' + rec.street + ' (' + rec.city + ')'
            elif rec.zip and rec.street:
                rec.name = str(rec.zip) + ' ' + rec.street
            else:
                rec.name = 'unbekannt'
    
    
    
