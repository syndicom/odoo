
from odoo import fields,models
class Partner(models.Model):
    _inherit = 'res.partner'
    type = fields.Selection(selection_add=[('declaration','Deklarationen'),('declaration_cc','Dekla. CC'),])                 
    syn_declaration_frees_till = fields.Date(string="Beitragsbefreit")
    syn_declaration_no_mail = fields.Boolean(string='Nicht per E-Mail')
    syn_contact_type_ids = fields.One2many('syndicom.vollzug.contact.type', 'partner_id',
                                            'VZ Kontaktart'
                                            
                                            )
    
    

 
