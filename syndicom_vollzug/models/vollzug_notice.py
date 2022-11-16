# -*- coding: utf-8 -*-
from odoo import models, fields



class SyndicomVollzugNotice(models.Model):
    _name = 'syndicom.vollzug.notice'
    _description = 'Vollzug Meldungen'
    _inherit = ['mail.thread','mail.activity.mixin']
    name = fields.Char('Name')
    enterprise_id = fields.Many2one('res.partner', 'Betrieb')
    notice_number = fields.Char(string='Meldungsnummer')
    notice_date = fields.Date(string='Meldungsdatum')
#    commissioner = fields.Char(string='Auftraggeber CH')
    state_id = fields.Many2one('res.country.state', 'Kanton')
    person_ids = fields.One2many('syndicom.vollzug.declaration.person','notice_id', string='Personen')
    place_ids = fields.One2many('syndicom.vollzug.notice.place','notice_id', string='Einsatzgebiete')
    task_id = fields.Many2one('project.task', 'Kontrolle')
     
    def button_create_new_task(self):
        new_task = self.env['project.task'].create({   'project_id':3,
                                            'partner_id': self.enterprise_id.id,
                                            'name': 'neu erstellt'
                                           })
        
        self.env.cr.commit()

        self.task_id = new_task.id
