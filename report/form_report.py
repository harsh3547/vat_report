import time
from openerp.report import report_sxw
from openerp.osv import osv

class form_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        self.id=[]
        self.id=[context.get('active_id',[])]
        super(form_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'today':time.strftime("%Y%m%d"),
                                  'len':self._len,
                                  'cr':cr,
                                  'uid': uid,
                                  'datas':self.data,
                                  'sum':self.sum1,
                                  })
        
    def _len(self,string):
        return len(string)
    
    def sum1(self):
        cr=self.cr
        uid=self.uid
        obj=self.pool.get('vat.report.wizard').browse(cr,uid,self.id[0])
        period_ids=obj.period_id.id
        id_list_tax=self.pool.get('account.tax.code').search(cr,uid,[])
        data=self._sum_period(cr,uid,id_list_tax,period_ids)
        print"===================================data",data
        value=[obj.set.field_27.id,obj.set.field_29.id,obj.set.field_30.id,obj.set.field_31.id,obj.set.field_32.id,obj.set.field_33.id,obj.set.field_34.id]
        print"========================================",value
        sum1=0
        for i in value:
            sum1=sum1 + data.get(i,0)
        print"=====================================sum1",sum1
        s=[obj.set.field_35.id]
        print"ssssssssssssssssssssssssssssssssss",s
        sum1=sum1-data.get(s[0],0)
        print"=================================sum2",sum1
        sum1=str(sum1)
        return sum1
                
           

    def data(self,id):
        print"ddddddddddddddddddddddddd",id
        cr=self.cr
        uid=self.uid
        if id==False:
            return ""
        period_ids=self.pool.get('vat.report.wizard').browse(cr,uid,self.id[0]).period_id.id
        id_list_tax=self.pool.get('account.tax.code').search(cr,uid,[])
        #print type(data['period_id'][0])
        data=self._sum_period(cr,uid,id_list_tax,period_ids)
        print"ddddddddddddddddddddddddd",id,data[id]
        return str(data[id])
    
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
        return res2

    def _sum_period(self, cr, uid, ids,period):
        #print '************************ ids ',ids
        move_state = ('posted', )
        period_id = period
        return self._sum(cr, uid, ids,
                         where=' AND line.period_id=%s AND move.state IN %s', where_params=(period_id, move_state))

        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
