from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pure_swisscom_rentner = fields.Boolean(
        string='Pure Swisscom Rentner',
        compute='_compute_pure_rentner',
        store=True
    )
    pure_post_rentner = fields.Boolean(
        string='Pure Post Rentner',
        compute='_compute_pure_rentner',
        store=True
    )

    @api.depends(
        'member_retired',
        'is_syndicom_member',
        'work_partner_relation_ids.other_partner_id.name',
        'work_partner_relation_ids.other_partner_id.category_id.name',
        'work_partner_relation_ids.date_start',
        'work_partner_relation_ids.date_end'
    )
    def _compute_pure_rentner(self):
        for partner in self:
            partner.pure_swisscom_rentner = False
            partner.pure_post_rentner = False

            if not (partner.member_retired and partner.is_syndicom_member):
                continue

            relations = partner.work_partner_relation_ids

            # Helper function to check if a partner is an employer
            def is_employer(rel):
                return any(
                    'arbeitgeber' in (cat.name or '').lower()
                    for cat in rel.other_partner_id.category_id
                )

            # Swisscom / Cablex employers
            swisscom_or_cablex = relations.filtered(
                lambda r: r.other_partner_id and is_employer(r) and (
                    'swisscom' in (r.other_partner_id.name or '').lower() or
                    'cablex' in (r.other_partner_id.name or '').lower()
                )
            )

            # Post employers
            post = relations.filtered(
                lambda r: r.other_partner_id and is_employer(r) and (
                    'post' in (r.other_partner_id.name or '').lower()
                )
            )

            # Unknown employers
            unknown_employers = relations.filtered(
                lambda r: r.other_partner_id and r.other_partner_id.name == 'kein Arbeitgeber / Arbeitgeber unbekannt'
            )

            # Other employers not allowed
            other_employers = relations.filtered(
                lambda r: r.other_partner_id and is_employer(r) and not any(
                    kw in (r.other_partner_id.name or '').lower()
                    for kw in ['swisscom', 'cablex', 'post', 'kein arbeitgeber / arbeitgeber unbekannt']
                )
            )

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

            if swisscom_or_cablex:
                partner.pure_swisscom_rentner = True

            if post:
                partner.pure_post_rentner = True
