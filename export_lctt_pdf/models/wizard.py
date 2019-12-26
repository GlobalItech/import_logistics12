from odoo import models, fields, api


class StockReport(models.TransientModel):
    _name = "wizard.lctt.history"
    _description = "Current Stock History"

    date_to= fields.Date("Date To")
    date_from= fields.Date("Date From")

    @api.multi
    def print_report_attendance(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'report.model',
            'form': self.read()[0]
        }
        return self.env.ref('export_lctt_pdf.lctt_xlsx').report_action(self, data=datas)


class ReportCarpetPurchase(models.AbstractModel):
    _name='report.export_lctt_pdf.lctt_report'




    @api.model
    def get_report_values(self, docids, data=None):

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']

        lines = []
        purchase_obj_ids = self.env['purchase.order.line'].search([('order_id.date_order', '>=', date_from),
                                                              ('order_id.date_order', '<=', date_to),
                                                              ('order_id.s_for', '=', 'import')])

        if purchase_obj_ids:

            for purchase_obj in purchase_obj_ids:

                sum_unit_pricefc = 0.000
                for l in purchase_obj.order_id.order_line:
                    sum_unit_pricefc += l.sub_total_lp
                lc_amount = 0.0
                for lc_ob in purchase_obj.order_id.lc_ids:
                    lc_amount += lc_ob.amount

                #                 unit_price_fc =[l.unit_pricefc for l in purchase_obj.order_line]
                #                 sub_total_lp = [l.sub_total_lp for l in purchase_obj.order_line],
                Insurance = purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Insurance').amount or 0.0,
                Bank_Charges = purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Bank Charges').amount or 0.0,
                Govt_Tax_Duties = purchase_obj.order_id.lc_ids.filtered(
                    lambda x: x.name.name == 'Govt Tax/Duties').amount or 0.0,
                Demerage = purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Demerage').amount or 0.0,
                Detensions = purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Detensions').amount or 0.0,
                Clearing = purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Clearing').amount or 0.0,
                Freight = purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Freight').amount or 0.0,
                #                 'Cost':0.0

                if sum_unit_pricefc != 0:
                    vals = ({
                        'po_name': purchase_obj.order_id.name,
                        'ref-no': purchase_obj.order_id.lc_ref,
                        'name': purchase_obj.order_id.partner_id.name,
                        'bank_name': purchase_obj.order_id.bank_name.name,
                        'lc_ref_no': purchase_obj.order_id.lc_ref_no,
                        'condition': purchase_obj.order_id.condition.name,
                        'date': purchase_obj.order_id.date_order,
                        #                     'date':datetime.strftime(purchase_obj.date_order, "%Y-%m-%d"),
                        'particular': purchase_obj.product_id.name,
                        'qty': purchase_obj.product_qty,
                        'rate': purchase_obj.unit_pricefc,
                        'value': purchase_obj.sub_total_fc,
                        'fx_rate': purchase_obj.order_id.fx_rate,
                        #                     p.amount = subtotal
                        'sub_total_lp':purchase_obj.sub_total_lp,

                        'Insurance': (Insurance[0] / sum_unit_pricefc) or 0.0,
                        'Bank Charges': (Bank_Charges[0] / sum_unit_pricefc) or 0.0,
                        'Govt Tax/Duties': (Govt_Tax_Duties[0] / sum_unit_pricefc) or 0.0,
                        'Demerage': (Demerage[0] / sum_unit_pricefc) or 0.0,
                        'Detensions': (Detensions[0] / sum_unit_pricefc) or 0.0,
                        'Clearing': (Clearing[0] / sum_unit_pricefc) or 0.0,
                        'Freight': (Freight[0] / sum_unit_pricefc) or 0.0,
                        'Cost': 0.0
                    })
                    lines.append(vals)

                else:
                    vals = ({
                        'po_name': purchase_obj.order_id.name,
                        'ref-no': purchase_obj.order_id.lc_ref,
                        'name': purchase_obj.order_id.partner_id.name,
                        'bank_name': purchase_obj.order_id.bank_name.name,
                        'lc_ref_no': purchase_obj.order_id.lc_ref_no,
                        'condition': purchase_obj.order_id.condition.name,
                        'date': purchase_obj.order_id.date_order,
                        #                     'date':datetime.strftime(purchase_obj.date_order, "%Y-%m-%d"),
                        'particular':purchase_obj.product_id.name,
                        'qty': purchase_obj.product_qty,
                        'rate': purchase_obj.unit_pricefc,
                        'value': purchase_obj.sub_total_fc,
                        'fx_rate': purchase_obj.order_id.fx_rate,
                        #                     p.amount = subtotal
                        'sub_total_lp': purchase_obj.sub_total_lp,

                        'Insurance': purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Insurance').amount or 0.0,
                        'Bank Charges': purchase_obj.order_id.lc_ids.filtered(
                            lambda x: x.name.name == 'Bank Charges').amount or 0.0,
                        'Govt Tax/Duties': purchase_obj.order_id.lc_ids.filtered(
                            lambda x: x.name.name == 'Govt Tax/Duties').amount or 0.0,
                        'Demerage': purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Demerage').amount or 0.0,
                        'Detensions': purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Detensions').amount or 0.0,
                        'Clearing': purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Clearing').amount or 0.0,
                        'Freight': purchase_obj.order_id.lc_ids.filtered(lambda x: x.name.name == 'Freight').amount or 0.0,
                        'Cost': 0.0
                    })
                    lines.append(vals)

            return {

                'datacr': lines,
                'date_order': data['form']['date_to'],
                'date_order2': data['form']['date_from']
            }
