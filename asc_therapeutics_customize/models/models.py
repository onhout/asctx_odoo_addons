# -*- coding: utf-8 -*-

from odoo import models, fields, api

#Extending the purchase order model, uses Catalog Number by default
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    @api.onchange('product_id')
    def product_id_change(self):
        if (self.product_id.x_catalog_number):
            self.name += " Catalog No.: " + self.product_id.x_catalog_number

#Add Received Status to Purchase Orders
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('received', 'Received')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')

#Add interaction for setting received status after the transfer is set to done
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def read(self, fields=None, load='_classic_read'):
        res = super(StockPicking, self).read(fields=fields, load=load)
        
        for i in res:
            for po in self:
                if po.id == i['id'] and 'state' in i and i['state'] == 'done':
                    po.purchase_id.write({'state': 'received'})

        return res


# General Override Zoom Emailing
# class CalendarEvent(models.Model):
#     _inherit = 'calendar.event'
    
#     def read(self, fields=None, load='_classic_read'):
#         res = super(CalendarEvent, self).read(fields=fields, load=load)
        
#         for i in self:
#             print (i.name)    
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         return res

#     @api.model
#     def create(self, values):
#         res = super(CalendarEvent, self).create(values)
        
#         print(res)
    
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         return res
    
    
#     def write(self, values):
#         res = super(CalendarEvent, self).write(values)
        
#         print(values)
    
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         print("AIOSJDOAISJDIOAJSDIOJASODJAOISDJOAISJDIOAJSDIOJASD")
#         return res