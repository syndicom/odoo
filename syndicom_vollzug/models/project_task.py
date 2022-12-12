
from odoo import fields,models
class ProjectTask(models.Model):
    _inherit = 'project.task'
    control_number = fields.Char(string='Kontrollnummer')
    syn_personen_ids = fields.One2many(
       "syndicom.vollzug.declaration.person",
       "task_id",
       string="Personen"  )
     
    

 