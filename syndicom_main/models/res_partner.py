from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    address_search_id = fields.Many2one(comodel_name='suisse.streets', string='Adresssuche')
    
    
    syndicom_statisical_entry = fields.Date(string='Statistisches Eintrittsdatum')
    syndicom_account_report_ids = fields.One2many('syndicom.account.report', 'partner_id', string='Kontoauszüge')
    syndicom_account_report_balance = fields.Float(string='Mitgliederkontostand')    
    syndicom_account_report_refreshed = fields.Datetime(string='Konto Report aktualisiert')
    
    work_location_ids = fields.Many2many(comodel_name='syndicom.work.locations', string='Betrieb / Standort')    
    work_sector = fields.Selection(string='Sektor', selection=[('1','Logistik'), ('2', 'ICT'),('3', 'Medien')])
    work_main_employeer = fields.Many2one(comodel_name='res.partner', string='Hauptarbeitgeber')
    work_main_personalnumber = fields.Char(string='Personalnummer')
    work_main_location = fields.Many2one(comodel_name='res.city', string='Arbeitsort')    
    work_main_building = fields.Char(string='Gebäude')
    work_main_region = fields.Char(string='Arbeitsregion gemäss AG')
    work_main_business_unit = fields.Char(string='Geschäftsbereich')
    work_main_function_id = fields.Many2one('member.hr.job', string='Funktion beim AG')
    work_main_cla_id = fields.Many2one('member.cla', string='GAV')

    work_is_freelance = fields.Boolean(string='Ist Freischaffend')
    work_is_self_employed = fields.Boolean(string='Ist selbstständig')
    work_is_temporary = fields.Boolean(string='Ist temporär')
    work_data_refreshed = fields.Datetime(string='Arbeitgeberdaten aktualisiert')
    
    member_is_confidant = fields.Boolean(string="Ist Vertrauensperson")
    member_young = fields.Boolean(string='Jugend')
    member_retired = fields.Boolean(string='Rentner')
    member_age = fields.Integer(string='Alter')
    member_entry_date = fields.Date(string='Exaktes Beitrittsdatum')
    member_data_refreshed = fields.Datetime(string='Mitgliederdaten aktualisiert')
    member_main_category = fields.Many2one(comodel_name='product.product', string='Mitgliederkategorie')
    
    partnership_discount = fields.Boolean(string='Partner Rabatt',help='Nur auf dem Mitglied aktivieren, welches vom Partnerrabatt profitiert')
    partnership_partner_id = fields.Many2one(comodel_name='res.partner', string='Partner des Mitglied',help='Partner des Mitglieds aufgrund der Verbindung der obige Rabatt zustande kommt')
    
    event_ids = fields.Many2many(comodel_name='event.event', string='Veranstaltungen',compute="_compute_partners_event_ids",store=True)
    

    # This adds all event_ids of all registrations from a partner
    # to the custom field events_ids
    # this was done for easy sending mass mailings as reminder or info mail
    @api.depends('registration_ids.event_id')
    def _compute_partners_event_ids(self):
        for rec in self:
            rec.event_ids = [(6, False, rec.registration_ids.event_id.ids)]

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


    """
    # TODO : felder aktivieren für Tracking

    customer_payment_method_subscription_id
    subscription_payment_interval
    payer_id

    # TODO : studio feld in richtiges Feld übernehmen => Achtung Datenmigration
    x_no_bill_till
    """