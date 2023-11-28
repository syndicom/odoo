from odoo import fields, models
from odoo.exceptions import UserError


class ResAccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    correction_account_id = fields.Many2one(comodel_name='account.account', string='Korrigiere Konto')
    correction_analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Korrigiere Kst')
    
    correction_ids = fields.One2many(comodel_name='account.move.line.correction', inverse_name='line_id', string='Korrekturen')

    def create_correction(self):
        for rec in self:

            if rec.correction_account_id.id == False and rec.correction_analytic_account_id.id == False:
                raise UserError("Weder eine neues Konto noch eine neue KST wurden ausgewählt - was soll schon korrigiert werden?")
            elif rec.correction_account_id.id == False:
                correction_account = rec.account_id.id
                correction_analytic = rec.correction_analytic_account_id.id
            elif rec.correction_analytic_account_id.id == False:
                correction_account = rec.correction_account_id.id
                correction_analytic = rec.analytic_account_id.id
            else:
                correction_account = rec.correction_account_id.id
                correction_analytic = rec.correction_analytic_account_id.id

            old_account = rec.account_id.id
            old_analytic_account = rec.analytic_account_id.id

            self.env['account.move.line.correction'].create({
                'line_id': rec.id,
                'old_account_id': old_account,
                'old_analytic_account_id': old_analytic_account,
                'new_account_id': correction_account,
                'new_analytic_account_id': correction_analytic,
            })

            rec.write({
                'account_id': correction_account,
                'analytic_account_id': correction_analytic,
                'correction_account_id' :False,
                'correction_analytic_account_id' :False,
            })


       
    


class ResAccountMoveLineCorrection(models.Model):
    _name = 'account.move.line.correction'
    _description = 'Korrekturen für Buchungszeilen'
    line_id = fields.Integer(string='Line ID')    
    old_account_id = fields.Many2one(comodel_name='account.account', string='Konto vor Änderung')
    old_analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Kst vor Änderung')
    new_account_id = fields.Many2one(comodel_name='account.account', string='Neues Konto')
    new_analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Neue Kst')

    

   