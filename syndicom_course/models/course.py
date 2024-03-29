# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomCourse(models.Model):
    _name = 'syndicom.course'

    name = fields.Char('Name', required=True, translate=True)

    active = fields.Boolean(string='Aktiv',default=True)
    stage = fields.Selection(string='Stufe', selection=[('new', 'Neu'), 
                                                        ('coming', 'Geplant'),
                                                        ('ok','Garantiert'),
                                                        ('full','Ausgebucht'),
                                                        ('done','Abgeschlossen')])
    
    lang_id = fields.Many2one('res.lang', string='Kurssprache')
    participant_ids = fields.One2many('syndicom.course.participant', 'course_id', string='Teilnehmer')
    
    sync_time = fields.Datetime(string='Zeitpunkt der letzten Synchronisation mit www')
    

    course_number = fields.Char(string='Kursnummer')
    date_from = fields.Date(string='Von')
    date_to = fields.Date(string='Bis')
    date_string = fields.Char(string='Datum Text', help='Wenn zusätzliche Informationen zu den einzelnen Kurstagen angegeben werden sollen')
    date_dateline = fields.Date(string='Anmeldefrist')
    seats = fields.Integer(string='Plätze')
    seats_min = fields.Integer(string='Min. Teilnehmer')
    seats_free = fields.Integer(string='Freie Plätze')
    topic = fields.Char(string='Thema')
    location = fields.Char(string='Ort Alternative')
    location_id = fields.Many2one(comodel_name='res.partner', string='Ort')
    speaker_ids = fields.Many2many(comodel_name='syndicom.course.speaker', string='Referent')
    level_ids = fields.Many2many(comodel_name='syndicom.course.level', string='Kurslevel')
    document_ids = fields.Many2many(comodel_name='syndicom.course.document', string='Dokumente')
    
    
    
    description_content = fields.Char(string='Kursinhalt')
    description_benefit = fields.Char(string='Nutzen')
    description_target = fields.Char(string='Zielpublikum')
    description_references = fields.Char(string='Referenten')
    description = fields.Char(string='Beschrieb')
    description_note = fields.Char(string='Hinweis')
    description_price = fields.Char(string='Preis')
    description_requirements = fields.Char(string='Voraussetzungen')
    description_devices = fields.Char(string='Kursgeräte')
    
    price_member = fields.Float(string='Preis für Mitglieder')
    price_others = fields.Float(string='Preis für Nicht-Mitglieder')
    price_catering = fields.Float(string='Preis Verpflegung Mitglieder')
    price_catering_others = fields.Float(string='Preis Verpflegung Nicht-Mitglieder')
    price_overnight = fields.Float(string='Preis Übernachtung Mitglieder')
    price_overnight_others = fields.Float(string='Preis Übernachtung Nicht-Mitglieder')

    for_members = fields.Boolean(string='Für Mitglieder')
    for_confidants = fields.Boolean(string='Für Vertrauensleute')
    for_employees = fields.Boolean(string='Für Mitarbeiter')
    
    link_member = fields.Char(string='Link Mitglieder')
    link_confidants = fields.Char(string='Link Vertrauensleute')
    link_employees = fields.Char(string='Link Mitarbeiter')
    
    institute_id = fields.Many2one(comodel_name='syndicom.course.institute', string='')
    
    duration = fields.Char(string='Dauer')

    has_hotel = fields.Boolean(string='Hotelzimmer')
    
    om_id = fields.Integer(string='OM ID')


    


