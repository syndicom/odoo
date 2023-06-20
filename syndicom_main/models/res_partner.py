from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    syndicom_account_report_ids = fields.One2many('syndicom.account.report', 'partner_id', string='Kontoauszüge')
    syndicom_account_report_balance = fields.Float(string='Mitgliederkontostand')    
    syndicom_account_report_refreshed = fields.Datetime(string='Konto Report aktualisiert')
    
    work_location_ids = fields.Many2many(comodel_name='syndicom.work.locations', string='Betrieb / Standort')    
    work_sector = fields.Selection(string='Sektor', selection=[('1','Logistik'), ('2', 'ICT'),('3', 'Medien')])
    work_main_employeer = fields.Many2one(comodel_name='res.partner', string='Hauptarbeitgeber')
    work_main_location = fields.Many2one(comodel_name='res.city', string='Arbeitsort')    
    work_main_building = fields.Char(string='Gebäude')
    work_is_freelance = fields.Boolean(string='Ist Freischaffend')
    work_is_self_employed = fields.Boolean(string='Ist selbstständig')
    work_data_refreshed = fields.Datetime(string='Arbeitgeberdaten aktualisiert')

    member_is_confidant = fields.Boolean(string="Ist Vertrauensperson")
    member_young = fields.Boolean(string='Jugend')
    member_retired = fields.Boolean(string='Rentner')
    member_age = fields.Integer(string='Alter')
    member_data_refreshed = fields.Datetime(string='Mitgliederdaten aktualisiert')
    


    """
    mobile = fields.Char(track_visibility='onchange')
    phone = fields.Char(track_visibility='onchange')
    street = fields.Char(track_visibility='onchange')
    street2 = fields.Char(track_visibility='onchange')
    zip = fields.Char(track_visibility='onchange')
    city = fields.Char(track_visibility='onchange')
    country_id = fields.Char(track_visibility='onchange')
    """

    """
    mediator_id = fields.Char(track_visibility='onchange')
    operating_unit_id = fields.Char(track_visibility='onchange')
    first_union_entry = fields.Char(track_visibility='onchange')
    anniversary_date = fields.Char(track_visibility='onchange')
    """


    