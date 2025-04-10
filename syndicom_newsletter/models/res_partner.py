from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_studio_purer_swisscom_rentner = fields.Boolean(
        string='Purer Swisscom Rentner',
        compute='_compute_purer_swisscom_rentner',
        store=True
    )

    @api.depends(
        'member_retired',
        'is_syndicom_member',
        'work_partner_relation_ids.other_partner_id.name',
        'work_partner_relation_ids.date_start',
        'work_partner_relation_ids.date_end'
    )
    def _compute_purer_swisscom_rentner(self):
        for partner in self:
            partner.x_studio_purer_swisscom_rentner = False

            if not (partner.member_retired and partner.is_syndicom_member):
                continue

            relations = partner.work_partner_relation_ids

            swisscom_or_cablex = relations.filtered(
                lambda r: r.other_partner_id and (
                    'swisscom' in (r.other_partner_id.name or '').lower() or
                    'cablex' in (r.other_partner_id.name or '').lower()
                )
            )
            unknown_employers = relations.filtered(
                lambda r: r.other_partner_id and r.other_partner_id.name == 'kein Arbeitgeber / Arbeitgeber unbekannt'
            )
            other_employers = relations.filtered(
                lambda r: r.other_partner_id and not any(
                    kw in (r.other_partner_id.name or '').lower()
                    for kw in ['swisscom', 'cablex', 'kein arbeitgeber / arbeitgeber unbekannt']
                )
            )

            if not swisscom_or_cablex:
                continue

            if other_employers:
                continue

            valid_unknown = False
            if unknown_employers:
                latest_unknown = max(
                    unknown_employers,
                    key=lambda r: r.date_start or fields.Date.today()
                )
                if not latest_unknown.date_end:
                    valid_unknown = True

            if not valid_unknown:
                continue

            partner.x_studio_purer_swisscom_rentner = True