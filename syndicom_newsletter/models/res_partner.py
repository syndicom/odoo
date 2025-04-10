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

    is_swisscom_company = fields.Boolean(
        string='Is Swisscom Company',
        help='Indicates if this partner is a Swisscom employer',
    )
    is_post_company = fields.Boolean(
        string='Is Post Company',
        help='Indicates if this partner is a Post employer',
    )

    @api.depends(
        'member_retired',
        'is_syndicom_member',
        'work_partner_relation_ids.other_partner_id.is_swisscom_company',
        'work_partner_relation_ids.other_partner_id.is_post_company',
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

            # Swisscom employers
            swisscom_employers = relations.filtered(
                lambda r: r.other_partner_id and r.other_partner_id.is_swisscom_company
            )

            # Post employers
            post_employers = relations.filtered(
                lambda r: r.other_partner_id and r.other_partner_id.is_post_company
            )

            # Unknown employers
            unknown_employers = relations.filtered(
                lambda r: r.other_partner_id and r.other_partner_id.name == 'kein Arbeitgeber / Arbeitgeber unbekannt'
            )

            # Other employers not allowed
            other_employers = relations.filtered(
                lambda r: r.other_partner_id and not (
                    r.other_partner_id.is_swisscom_company or
                    r.other_partner_id.is_post_company or
                    r.other_partner_id.name == 'kein Arbeitgeber / Arbeitgeber unbekannt'
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

            if swisscom_employers:
                partner.pure_swisscom_rentner = True

            if post_employers:
                partner.pure_post_rentner = True
