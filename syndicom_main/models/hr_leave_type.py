from odoo import models, fields, api


class HRLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    allowed_users_ids = fields.Many2many(comodel_name='res.users', string='Berechtigte Benutzer',help='Feld leerlassen, wenn alle Mitarbeiter:innen diesen Abwesenheitstyp verwenden dürfen')
    require_comment = fields.Boolean(string='Erfordert Bemerkung',help='Wenn diese Checkbox aktiviert ist, muss der Benutzer eine Beschreibung hinterlegen beim erfassen einer entsprechenden Abwesenheit')
    

class HrLeave(models.Model):
    _inherit = 'hr.leave'
    require_comment = fields.Boolean(related='holiday_status_id.require_comment',string='Erfordert Bemerkung')
    
    

