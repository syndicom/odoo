from odoo import fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class CountWidget(fields.Field):
    type = 'count'

    def render(self, values):
        query = self._domain_to_sql(values.get('domain', []))
        count = self.env[self.model_name].search_count(query)
        return '<div class="count-widget"><span class="count">%s</span><a class="show-results" href="#">Ergebnisse anzeigen</a></div>' % count

    def value_to_html(self, value):
        return value

    @staticmethod
    def _domain_to_sql(cls, domain):
        return expression.AND(domain).to_sql(cls.model_name, cls.env.cr)

    def _get_domain(self, values):
        return values.get('domain', [])

    def _get_records(self, values):
        domain = self._get_domain(values)
        if not domain:
            raise UserError(_('Domain is empty'))
        return self.env[self.model_name].search(domain)

    def _show_results(self, values):
        records = self._get_records(values)
        action = self.env.ref('base.action_res_partner_form').read()[0]
        action['domain'] = [('id', 'in', records.ids)]
        action['views'] = [(self.env.ref('base.view_partner_form').id, 'form')]
        return action

    def on_change(self, values):
        action = {}
        if 'show_results' in values:
            action = self._show_results(values)
        return {'action': action}
