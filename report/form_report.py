import time
from openerp.report import report_sxw
from osv import osv

class form_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        self.id=[]
        self.id=[context.get('active_id',[])]
        super(form_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'time':time,
                                  'cr':cr,
                                  'uid': uid,
                                  'datas':self._data,
                                  })

    def _data(self):
        cr=self.cr
        uid=self.uid
        period_ids=self.pool.get('vat.report.wizard').browse(cr,uid,self.id[0]).period_id.id
        id_list_tax=self.pool.get('account.tax.code').search(cr,uid,[])
        #print type(data['period_id'][0])
        data=self._sum_period(cr,uid,id_list_tax,period_ids)
        return data
    
    def _sum(self, cr, uid, ids, where ='', where_params=()):
        parent_ids = tuple(self.pool.get('account.tax.code').search(cr, uid, [('parent_id', 'child_of', ids)]))
        cr.execute('SELECT line.tax_code_id, sum(line.tax_amount) \
                    FROM account_move_line AS line, \
                    account_move AS move \
                    WHERE line.tax_code_id IN %s '+where+' \
                    AND move.id = line.move_id \
                    GROUP BY line.tax_code_id',
                       (parent_ids,) + where_params)
        res=dict(cr.fetchall())
        obj_precision = self.pool.get('decimal.precision')
        res2 = {}
        for record in self.pool.get('account.tax.code').browse(cr, uid, ids):
            def _rec_get(record):
                amount = res.get(record.id, 0)
                for rec in record.child_ids:
                    amount += _rec_get(rec) * rec.sign
                return amount
            res2[record.id] = int(round(_rec_get(record),0))
        print '*************************** res 2 _sum ', res2
        return res2

    def _sum_period(self, cr, uid, ids,period):
        #print '************************ ids ',ids
        move_state = ('posted', )
        period_id = period
        return self._sum(cr, uid, ids,
                         where=' AND line.period_id=%s AND move.state IN %s', where_params=(period_id, move_state))

        
report_sxw.report_sxw('report.vat_form_report','vat.report.wizard','addons/vat_report/report/form_report.mako',
    parser=form_report)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
