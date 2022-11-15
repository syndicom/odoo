# -*- coding: utf-8 -*-

from odoo import models,fields

class ParticipationPartner(models.Model):
   _inherit = "res.partner"
   syn_petition_participation_ids = fields.One2many(
       "syndicom.petition.participation",
       "partner_id",
       string="Petitionsteilnehmer"  )