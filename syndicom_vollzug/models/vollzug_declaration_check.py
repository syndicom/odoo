# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools


class SyndicomVollzugDeclarationCheck(models.Model):
    _name = 'syndicom.vollzug.declaration.check'
    _auto = False
    _description = 'Computed List to check all declaration enterprises'
    name = fields.Char('Name')
    gav = fields.Char(string='GAV')    
    zip = fields.Char(string='PLZ')
    city = fields.Char('Stadt')
    name_an = fields.Char(string='Hauptempfänger')
    email = fields.Char(string='An')
    email_cc = fields.Char(string='CCs')
    count_an = fields.Integer(string='Anz. AN')
    count_cc = fields.Integer(string='Anz. CCs')    
    date_start = fields.Date(string='GAV Unterstellt seit')
    date_end = fields.Date(string='GAV Unterstellt bis')
    partner_id = fields.Integer(string='Kontakt im Betrieb')
    gav_id = fields.Integer(string="GAV ID")
    lang = fields.Char(string='Sprache')
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query())
        )

    def _query(self, with_clause="", fields={}, groupby="", from_clause=""):

        return """

            SELECT 
            distinct
                        p.id,
                        c.id gav_id,
                        p.name,
                        c.name gav,
                        p.zip,
                        p.city,
                        


                        

                        (select count(*) from res_partner can 
                        inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                        where can.parent_id = p.id and can.active = True) count_an,
                        
                        (select count(*) from res_partner can 
                        inner join  syndicom_vollzug_contact_type typ_cc on typ_cc.partner_id = can.id and typ_cc.name = 'declaration' and typ_cc.is_copy = True
                        where can.parent_id = p.id and can.active = True) count_cc,
                        
                        case 
                            when (select count(*) from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '' ) = 0 then p.email
                            else (select can.email from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '' limit 1) end as email,
                            
                        case 
                            when (select count(*) from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '' ) = 0 then p.id
                            else (select can.id from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '' limit 1) end as partner_id,
                            

                        case 
                            when (select count(*) from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '') = 0 then ''
                            else (select can.name from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '' limit 1) end as name_an,

                        case 
                            when (select count(*) from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '') = 0 then p.lang
                            else (select can.lang from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_an on typ_an.partner_id = can.id and typ_an.name = 'declaration' and typ_an.is_main = True
                                    where can.parent_id = p.id and can.active = True and can.email != '' limit 1) end as lang,
                            
                        case 
                            when (select count(*) from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_cc on typ_cc.partner_id = can.id and typ_cc.name = 'declaration' and typ_cc.is_copy = True
                                    where can.parent_id = p.id and can.active = True and can.email != '') = 0 then ''
                            else (select string_agg(email::text, ',') from res_partner can 
                                    inner join  syndicom_vollzug_contact_type typ_cc on typ_cc.partner_id = can.id and typ_cc.name = 'declaration' and typ_cc.is_copy = True
                                    where can.parent_id = p.id and can.active = True and can.email != '') end as email_cc,





                        con.date_start,
                        con.date_end
                            
            FROM 
                        res_partner p
                        inner join 	res_partner_relation_all con on con.is_inverse = False and con.this_partner_id = p.id
                        inner join  res_partner_relation_type rel_type on rel_type.id = con.type_id and rel_type.cla_imputed_ok = True
                        inner join 	res_partner c on c.id = con.other_partner_id
                        
           
            WHERE
                    p.active = True
                and p.is_company = True
                
            """