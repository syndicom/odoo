from odoo import models, fields

class FilterPartnersWizard(models.TransientModel):
    _name = 'wizard.filter.partners'
    _description = 'Filter Partners by Petition Participation'

    petition_id = fields.Many2one('syndicom.petition', string='Petition to Exclude', required=True)

    def apply_filter(self):
        participations = self.env['syndicom.petition.participation'].search([
            ('petition_id', '=', self.petition_id.id)
        ])
        bad_partner_ids = participations.mapped('partner_id').ids

        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Partners',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'domain': [
                ('is_syndicom_member', '=', True),
                ('work_main_employeer', 'ilike', 'swisscom'),
                ('id', 'not in', bad_partner_ids),
            ],
        }
