from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    address_search_id = fields.Many2one(comodel_name='suisse.streets', string='Adresssuche')
    city_id = fields.Many2one(related='partner_id.city_id', readonly=False)

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
    