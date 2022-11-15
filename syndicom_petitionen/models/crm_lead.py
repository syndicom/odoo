# -*- coding: utf-8 -*-

from odoo import models,fields

class LeadPartner(models.Model):
   _inherit = "crm.lead"
   syn_petition_participation_ids = fields.One2many(
       "syndicom.petition.participation",
       "partner_id",
       string="Petitionsteilnehmer"  )