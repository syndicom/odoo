from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    address_search_id = fields.Many2one(comodel_name='suisse.streets', string='Adresssuche')
    city_id = fields.Many2one(related='partner_id.city_id', readonly=False)

    @api.onchange('address_search_id')
    def _onchange_partner_adress(self):
        for rec in self:
            if rec.address_search_id:
                if rec.address_search_id.city_id:
                    rec.city_id = rec.address_search_id.city_id
                
                if rec.address_search_id.country_id:
                    rec.country_id = rec.address_search_id.country_id

                if rec.address_search_id.state_id:
                    rec.state_id = rec.address_search_id.state_id
                
                rec.street = rec.address_search_id.street
                rec.zip = rec.address_search_id.zip
                rec.city = rec.address_search_id.city

            rec.address_search_id = False


    