# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools


class SyndicomCourseParticipant(models.Model):
    _name = 'syndicom.course.participant'
    _description = 'List of all syndicom cour participants'
    partner_id = fields.Many2one('res.partner', 'Kontakt')
    #member_service_id = fields.Many2one("member.service", string='Kontakt')
    course_id = fields.Many2one("syndicom.course", string="Kurs")
    date_registration = fields.Date(string="Anmeldedatum")
    status = fields.Selection(string='Status', selection=[('booked', 'Angemeldet'), ('canceld', 'Abgemeldet'),('waiting','Warteliste')],required=True)
    member_service_id = fields.Many2one(comodel_name='member.service', string='Link Member Service', store=True, compute="_compute_member_service")
    

    @api.model
    @api.depends('status','course_id')
    def _compute_member_service(self):
        for record in self:

            member_service = self.env['member.service'].search([('partner_id','=',record.partner_id.id),('course_id','=',record.course_id.id)], limit = 1)
            if record.status == 'booked' and len(member_service) == 0:
                # Create new entry in member.service
                product = self.env['syndicom.course.institute'].search([('id','=',record.course_id.institute_id.id)])

                member_service.create({
                    'partner_id': record.partner_id.id,
                    'course_id': record.course_id.id,
                    'product_id':  product.product_id.id,
                    'entry_date': record.course_id.date_from,
                    'leaving_date': record.course_id.date_to,
                })
            elif record.status in ['canceld','waiting'] and len(member_service) == 1:
                # Remove existing entry
                member_service.unlink()
    
   