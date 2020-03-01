# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class asc_therapeutics_customize(models.Model):
#     _name = 'asc_therapeutics_customize.asc_therapeutics_customize'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

#Extending the purchase order model, uses Catalog Number by default
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        if (self.product_id.x_catalog_number):
            self.name += " Catalog No.: " + self.product_id.x_catalog_number


# General Override Zoom Emailing
class CalendarEvent(models.Model):
    _inherit = 'calendar.event'
    
    def read(self, fields=None, load='_classic_read'):
        res = super(CalendarEvent, self).read(fields=fields, load=load)
        
        for i in self:
            print (i.name)    
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        return res

    @api.model
    def create(self, values):
        res = super(CalendarEvent, self).create(values)
        
        print(res)
    
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        return res
    
    
    def write(self, values):
        res = super(CalendarEvent, self).write(values)
        
        print(values)
    
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
        return res