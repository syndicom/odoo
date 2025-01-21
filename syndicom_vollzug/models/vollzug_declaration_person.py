# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import date, datetime, timedelta

from dateutil import rrule

from odoo import api, fields, models, tools


class SyndicomvollzugDeclarationPerson(models.Model):
    _name = 'syndicom.vollzug.declaration.person'
    _description = 'Vollzug deklarierte Personen'
    name = fields.Char('Name')
    declaration_id = fields.Many2one('syndicom.vollzug.declaration', 'Deklaration', index=True)
    notice_id = fields.Many2one('syndicom.vollzug.notice', 'Meldung')
    place_id = fields.Many2one('syndicom.vollzug.notice.place', 'Einsatzgebiete')
    task_id = fields.Many2one('project.task', 'Personen')
    currency_id = fields.Many2one('res.currency', 'Währung')
    country_id = fields.Many2one('res.country', 'Land')
    firstname = fields.Char('Vorname')
    description = fields.Text(string='Beschreibung')
    contact_id = fields.Many2one('res.partner', 'Verbundener Kontakt') #, stored=True, compute="_compute_search_partner")
    contact_match = fields.Selection(string='Gefunden durch', selection=[('ahv', 'AHV Nummer'), ('birthday1', 'Geburtsd./Vor- Nachname'),('adresse', 'Vor-/Nachname / Adresse'),('birthday2', 'Geburtsd. / Vorname'),('birthday3', 'Geburtsd. / Teil-Vorname'),('birthday4', 'Geburtsd. / Str / PLZ'),])
    
    employeer_id = fields.Many2one('res.partner', 'Verbundener Betrieb')
    date_entry = fields.Date(string='Eintrittsdatum')
    date_leave = fields.Date(string='Austrittsdatum')
    personal_nr = fields.Char(string='Personalnummer')
    employment_rate = fields.Float(string='Beschäftigungsgrad')
    duration = fields.Integer(string='Anz. Monate', store=True, compute="_compute_duration_in_month")

    duration_association = fields.Integer(string='Verband (mt.)')
    duration_ev = fields.Integer(string='EV (mt.)')
    duration_none = fields.Integer(string='Nicht-Verband (mt.)')

    total_an = fields.Monetary(string='AN Beitrag') #,compute="_compute_total_an")
    total_ag = fields.Monetary(string='AG Beitrag') #,compute="_compute_total_ag")
    total_ag_nicht_verband = fields.Monetary(compute='_compute_duration_in_month')
    total_ag_verband = fields.Monetary(compute='_compute_duration_in_month')
    total_ag_per_month = fields.Serialized(compute='_compute_duration_in_month')
    salutation = fields.Char(string='Anrede')
    street = fields.Char(string='Adresse')
    zip = fields.Char(string='PLZ')
    city = fields.Char(string='Ort')
    birthday = fields.Date(string='Geburtstag')
    apprentice = fields.Char(string='Lehrling')
    is_apprentice = fields.Boolean(string='Ist Lehrling', store=True, compute='_compute_apprentice')
    ssn = fields.Char(string='AHV-Nummer')
    gender = fields.Selection([('m','Männlich'),('w','Weiblich'),('n','Neutral')], compute='_compute_gender')
    salary = fields.Float(string='Bruttolohn')
    zemis = fields.Char(string='Zemis')
    qualification = fields.Char(string='Qualifikation')
    field = fields.Char(string='Einsatzgebiet')
    job = fields.Char(string='Tätigkeit')
    cla_partner = fields.Many2one(string='GAV Partner',related='declaration_id.cla_partner')
    duration_correction = fields.Integer(string='Korrektur')
    duration_consolidated = fields.Integer(string='Konsolidierte Anz. Monate', store=True, compute='_compute_duration_consolidated')
    
    discount_ag = fields.Float(string='Rabatt AG')

    @api.depends('date_entry','date_leave','employment_rate','is_apprentice', 'duration_correction')
    def _compute_duration_in_month(self):
        for record in self:
            record.total_ag_per_month = {}
            if record.declaration_id:
                record._compute_apprentice()
                # Getting settings records
                association_imputed = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.association_imputed', '0')
                ev_imputed = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.ev_imputed', '0')
                # Sanitize entry and leave date of the person according to the declaration data
                date_entry = max(record.date_entry or record.declaration_id.date_from, record.declaration_id.date_from)
                date_leave = min(record.date_leave or record.declaration_id.date_to, record.declaration_id.date_to)
                # Declaration
                m = 0
                m_total = 0
                duration_asso = 0
                duration_ev = 0
                duration_none = 0
                total_ag = 0
                total_ag_verband = 0
                total_ag_nicht_verband = 0
                total_an = 0
                discount_ag = 0

                # Check Employment Rate
                if record.employment_rate:
                    if record.employment_rate <= 1 and record.employment_rate > 0:
                        record.employment_rate = record.employment_rate * 100
                else:
                    record.employment_rate = 0

                # Iterate all possible months, to check the membership of the linked enterprise for every single month
                # Count

                dt_start = date(date_entry.year,date_entry.month,1)
                dt_end = date(date_leave.year,date_leave.month,28)
                dt_end = dt_end.replace(day=28) + timedelta(days=4)
                dt_end = dt_end - timedelta(days=dt_end.day)

                for dt in rrule.rrule(rrule.MONTHLY,dtstart=dt_start, until=dt_end):
                  
                    m_total = m_total + 1

                # Check every month
                for dt in rrule.rrule(rrule.MONTHLY,dtstart=dt_start, until=dt_end):

                    m = m+1
                    actual_month = dt
                    delta_days = 31

                    end_month = actual_month.replace(day=28) + timedelta(days=4)
                    end_month = end_month - timedelta(days=end_month.day)
                    first_month = date(dt.year,dt.month,1)

                    # First Month (only counted if at least 15 days) multiple months
                    if(m==1 and m != m_total ):
                        if(date_leave < end_month.date()):
                            end_month = datetime.combine(date_leave, datetime.min.time())
                        delta_day = end_month.date() - date_entry
                        delta_days = delta_day.days
                       

                    # only one month
                    elif(m==1 and m == m_total):
                        delta_day = date_leave - date_entry
                        delta_days = delta_day.days

                    # all others
                    else:
                        delta_day = date_leave - date(dt.year,dt.month,1)
                        delta_days = delta_day.days


                    # Enough Days, check witch kind of calculation logic
                    if(delta_days >= 14 ):
                        
                        # check the relation table to see if the enterprise is in a association, a ev or none of them
                        is_association_this_month = record._get_is_association_this_month(association_imputed, dt)

                        logic = 'nicht'

                        if(len(is_association_this_month) == 1):
                            if(is_association_this_month.other_partner_id.id == int(ev_imputed) ):
                                duration_ev = duration_ev + 1
                                logic = 'ev'
                            else:
                                duration_asso = duration_asso + 1
                                logic = 'verband'
                        else:
                            duration_none = duration_none + 1

                        # now we know the type of relation, so lets check for the price in the pricelist
                        pricelist = self.env['syndicom.vollzug.pricelist'].search(
                        ["&","&","&","&",("gav_id","=",record.declaration_id.cla_partner.id),("date_from","<=",first_month),("category","=",logic),"|",("date_to","=",False),("date_to",">=",end_month),"|",("active","=",True),("active","=",False)]
                        , limit = 1)

                        total_ag_this_month = 0

                        if(len(pricelist) == 1):
                            if(pricelist.logic == 'absolut'):
                                if(record.is_apprentice == True):
                                    total_ag = total_ag + pricelist.amount_ag_lernend
                                    total_ag_this_month = pricelist.amount_ag_lernend
                                    total_an = total_an + pricelist.amount_lernend
                                elif(record.employment_rate < 50):
                                    total_ag = total_ag + pricelist.amount_ag_tz
                                    total_ag_this_month = pricelist.amount_ag_tz
                                    total_an = total_an + pricelist.amount_tz
                                else:
                                    total_ag = total_ag + pricelist.amount_ag_vz
                                    total_ag_this_month = pricelist.amount_ag_vz
                                    total_an = total_an + pricelist.amount_vz
                            elif(pricelist.logic == 'prozent'):
                                if(record.is_apprentice == True):
                                    total_ag = total_ag + (record.salary / 100 * pricelist.amount_ag_lernend)
                                    total_ag_this_month = (record.salary / 100 * pricelist.amount_ag_lernend)
                                    total_an = total_an + (record.salary / 100 * pricelist.amount_lernend)
                                elif(record.employment_rate < 50):
                                    total_ag = total_ag + (record.salary / 100 * pricelist.amount_ag_tz)
                                    total_ag_this_month = (record.salary / 100 * pricelist.amount_ag_tz)
                                    total_an = total_an + (record.salary / 100 * pricelist.amount_tz)
                                else:
                                    total_ag = total_ag + (record.salary / 100 * pricelist.amount_ag_vz)
                                    total_ag_this_month = (record.salary / 100 * pricelist.amount_ag_vz)
                                    total_an = total_an + (record.salary / 100 * pricelist.amount_vz)
                            discount_ag = discount_ag + (total_ag_this_month / 100 * pricelist.discount)
                            if pricelist.category == 'verband':
                                total_ag_verband += total_ag_this_month
                            else:
                                total_ag_nicht_verband += total_ag_this_month
                        total_ag_per_month = record.total_ag_per_month
                        total_ag_per_month[f'{dt.month}.{dt.year}'] = total_ag_this_month
                        record.total_ag_per_month = total_ag_per_month

                if record.duration_correction != 0 and m > 0:
                    if (m == record.duration_association) or (m == duration_ev) or (m == duration_none):
                        total_an = total_an / m * (m + record.duration_correction)
                        total_ag = total_ag / m * (m + record.duration_correction)
                        total_ag_nicht_verband = total_ag_nicht_verband / m * (m + record.duration_correction)
                        total_ag_verband = total_ag_verband / m * (m + record.duration_correction)
                        discount_ag = discount_ag / m * (m + record.duration_correction)

                record.duration_association = max(0, duration_asso)
                record.duration_ev = max(0,duration_ev)
                record.duration_none = max(0,duration_none)
                record.duration = max(0,record.duration_association + record.duration_ev + record.duration_none + record.duration_correction)
                record.total_an = max(0,total_an)
                record.total_ag = max(0,total_ag)
                record.total_ag_nicht_verband = max(0,total_ag_nicht_verband)
                record.total_ag_verband = max(0,total_ag_verband)
                record.discount_ag = max(0,discount_ag)

            else:
                record.duration_association = 0
                record.duration_ev = 0
                record.duration_none = 0
                record.duration = 0
                record.total_an = 0
                record.total_ag = 0
                record.total_ag_nicht_verband = 0
                record.total_ag_verband = 0
                record.discount_ag = 0

    @api.model
    @tools.ormcache('association_imputed', 'dt', 'enterprise_id')
    def _get_is_association_this_month_cached(self, association_imputed, dt, enterprise_id):
        """Cached search """
        return self.env['res.partner.relation.all'].search([
            "&", "&", "&", "|",
             ("active", "=", True),
             ("active", "=", False),
             ("is_inverse", "=", False),
             ("this_partner_id", "=", enterprise_id),
             ("type_id", "=", int(association_imputed)),
             "|",
             ("date_start", "<=", dt),
             "&",
             ("date_end", "=", False),
             ("date_end", ">=", dt),
        ]).ids

    def _get_is_association_this_month(self, association_imputed, dt):
        self.ensure_one()
        return self.env['res.partner.relation.all'].browse(
            self._get_is_association_this_month_cached(
                association_imputed, dt, self.declaration_id.enterprise_id.id
            )
        )

    @api.depends('birthday','ssn','zip')
    def _compute_search_partner(self):

        for rec in self:
            
            if rec.contact_id == False:
                #gefunden durch?
                match = False
                plz_list = []

                # Finde Kontakt mit AHV
                mitglied =  self.env['res.partner'].search([('ahv_number','=',rec.ssn)] , order="is_syndicom_member desc", limit = 1)
                if len(mitglied) > 0:
                    match = 'ahv'
                
                # Keine AHV übereinstimmung
                # Prüfe Geburtsdatum, Vor und Nachnamen
                if len(mitglied) == 0:
                    
                    mitglied =  self.env['res.partner'].search([('contact_birthday','=',rec.birthday),('firstname','=',rec.firstname),('lastname','=',rec.name)], order="is_syndicom_member desc", limit = 1)
                    if len(mitglied) > 0:      
                        match = 'birthday1'
                
                # Prüfe komplette Adresse: Vor- / Nachname, strasse, plz ort
                if len(mitglied) == 0:
                    
                    plz_list = rec.city.split(" ")
                    mitglied =  self.env['res.partner'].search([('street','=',rec.street),('firstname','=',rec.firstname),('lastname','=',rec.name),('zip','in',plz_list)], order="is_syndicom_member desc", limit = 1)
                    if len(mitglied) > 0:
                        match = 'adresse'
                
                # Prüfe Geburtsdatum, Vorname
                if len(mitglied) == 0:
                    
                    mitglied = self.env['res.partner'].search([('contact_birthday','=',rec.birthday),('firstname','=',rec.firstname)], order="is_syndicom_member desc", limit = 1)
                    if len(mitglied) > 0:
                        match = 'birthday2'
                    
                # Prüfe Geburtsdatum, Teil- Vorname
                if len(mitglied) == 0:
                    
                    mitglied = self.env['res.partner'].search([('contact_birthday','=',rec.birthday),('firstname','=',rec.firstname)], order="is_syndicom_member desc", limit = 1)
                    if len(mitglied) > 0:
                        match = 'birthday3'
                
                # Prüfe Geburtsdatum, Str / Plz 
                if len(mitglied) == 0:
                    
                    mitglied = self.env['res.partner'].search([('contact_birthday','=',rec.birthday),('street','=',rec.street),('lastname','=',rec.name)], order="is_syndicom_member desc", limit = 1)
                    if len(mitglied) > 0:
                        match = 'birthday4'

                rec.contact_id = mitglied
                rec.contact_match = match
            else:
                rec.contact_id = rec.contact_id


    @api.depends('duration','duration_correction')
    def _compute_duration_consolidated(self):
        for record in self:
            consolidated = record.duration + record.duration_correction
            if consolidated < 0: 
                consolidated = 0
            if consolidated > record.declaration_id.duration_declaration:
                consolidated = record.declaration_id.duration_declaration
            record.duration_consolidated = consolidated

    @api.depends('apprentice')
    def _compute_apprentice(self):
        for record in self:
            if str(record.apprentice).lower() in ['lehrling','apprentice','ja','si','oui','1','true','yes','apprenti','apprendi','apprendista','lernender','azubi','auszubildender']:
                record.is_apprentice = True
            else:
                record.is_apprentice = False

    @api.depends('salutation')
    def _compute_gender(self):
        for record in self:
            record.gender = 'n'
            if record.salutation:
                if record.salutation.lower() in ['herr','monsieur','mister','m','male','signor','mänlich','mrs','mrs.','m.','homme']:
                    record.gender = 'm'
                elif record.salutation.lower() in ['frau','madame','md','weiblich','f','w','female','signora','miss','ms','ms.','mme','femme']:
                    record.gender = 'w'

    def _get_sum_total_ag_per_month(self):
        """Aggregate all declaration person total_agg per month and year."""
        total_ag_per_month = defaultdict(int)
        for person in self:
            if person.total_ag_per_month:
                for monthyear, value in person.total_ag_per_month.items():
                    total_ag_per_month[monthyear] += value
        return total_ag_per_month
