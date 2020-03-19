# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _

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
    approved_by = fields.Many2many('res.users', string='Approved By', readonly=True)

    def send_confirmation(self, mailing_users):

        employee = self.env['hr.employee']
        for order in self:
            line_str = ""
            for line in order.order_line:
                line_str += "{} x {}<br>".format(line.name, line.product_qty)

            for user in mailing_users:
                body = """Dear {}, 
                <p>You have <a href='http://admin.asctherapeutics.com/web#id={}&amp;model=purchase.order&amp;view_type=form'>{}</a> waiting to be approved</p>
                <strong>Ordered items:</strong>
                <p>{}</p>
                <p><strong>Total: ${}</strong></p>
                <p>Best Regards,</p>
                """.format(user.name, order.id, order.name, line_str, order.amount_total)
                template_obj = self.env['mail.mail']
                template_data = {
                    'subject': 'Purchase Order Approval Request: ' + order.name,
                    'body_html': body,
                    'email_from': "IT@asctherapeutics.com",
                    'email_to': user.email_formatted
                    }
                template_id = template_obj.create(template_data)
                template_obj.send(template_id)

    def button_approve(self, force=False):
        employee = self.env['hr.employee']
        acc_manager = employee.search([('job_id','like','Accounting Manager')]).user_id
        ceo = employee.search([('job_id','like','CEO')]).user_id

        for order in self:
            department_head = employee.search(['&', ('category_ids','like','Department Head'), ('department_id', '=', order.user_id.employee_ids.department_id.name)]).user_id
            if order.amount_total <= 5000:
                self.write({'approved_by': [(4, self.env.user.id)]})
                self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
                self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
            elif order.amount_total > 5000 and order.amount_total <= 10000:
                self.write({'approved_by': [(4, self.env.user.id)]})
                if acc_manager in order.approved_by and department_head in order.approved_by:
                    self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
                    self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
            elif order.amount_total > 10000:
                self.write({'approved_by': [(4, self.env.user.id)]})
                if acc_manager in order.approved_by and department_head in order.approved_by and ceo not in order.approved_by:
                    self.send_confirmation([ceo])
                elif acc_manager in order.approved_by and department_head in order.approved_by and ceo in order.approved_by:
                    self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
                    self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        return {}

    def button_confirm(self):
        employee = self.env['hr.employee']
        acc_manager = employee.search([('job_id','like','Accounting Manager')]).user_id
        ceo = employee.search([('job_id','like','CEO')]).user_id

        for order in self:
            department_head = employee.search(['&', ('category_ids','like','Department Head'), ('department_id', '=', order.user_id.employee_ids.department_id.name)]).user_id
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            if order.amount_total <= 5000:
                if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.company_id.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve()
                else:
                    mailing_users = [department_head]
                    self.send_confirmation(mailing_users)
                    order.write({'state': 'to approve'})
            elif order.amount_total > 5000 and order.amount_total <= 10000:
                mailing_users = [acc_manager, department_head]
                self.send_confirmation(mailing_users)
                order.write({'state': 'to approve'})
            elif order.amount_total > 10000:
                mailing_users = [acc_manager, department_head]
                self.send_confirmation(mailing_users)
                order.write({'state': 'to approve'})
        return True

        
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