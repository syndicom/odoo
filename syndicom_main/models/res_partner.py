from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    address_search_id = fields.Many2one(comodel_name='suisse.streets', string='Adresssuche')
    
    

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
    work_is_temporary = fields.Boolean(string='Ist temporär')
    work_data_refreshed = fields.Datetime(string='Arbeitgeberdaten aktualisiert')

    member_is_confidant = fields.Boolean(string="Ist Vertrauensperson")
    member_young = fields.Boolean(string='Jugend')
    member_retired = fields.Boolean(string='Rentner')
    member_age = fields.Integer(string='Alter')
    member_data_refreshed = fields.Datetime(string='Mitgliederdaten aktualisiert')
    member_main_category = fields.Many2one(comodel_name='product.product', string='Mitgliederkategorie')
    
    @api.onchange('address_search_id')
    def _onchange_partner_adress(self):
        if self.address_search_id:

            if self.address_search_id.city_id:
                self.city_id = self.address_search_id.city_id
            
            if self.address_search_id.country_id:
                self.country_id = self.address_search_id.country_id

            if self.address_search_id.state_id:
                self.state_id = self.address_search_id.state_id
            
            self.street = self.address_search_id.street
            self.zip = self.address_search_id.zip
            self.city = self.address_search_id.city

            self.address_search_id = False

    mobile = fields.Char(tracking=True)   
    phone = fields.Char(tracking=True)
    street = fields.Char(tracking=True)
    street2 = fields.Char(tracking=True)
    zip = fields.Char(tracking=True)
    city = fields.Char(tracking=True)
    country_id = fields.Many2one(tracking=True)
    mediator_id = fields.Many2one(tracking=True)
    operating_unit_id = fields.Many2one(tracking=True)
    first_union_entry = fields.Date(tracking=True)
    anniversary_date = fields.Date(tracking=True)



