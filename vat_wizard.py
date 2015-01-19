# coding=utf-8
from openerp.osv import fields,osv,orm

class vat_report_wizard(osv.osv):
    _name = "vat.report.wizard"
    _columns = {
              'name':fields.char('Name'),
              'field_81':fields.boolean('Pirminė'),
              'field_82':fields.boolean('Patikslinta'),
              'field_91':fields.boolean('Mokestinio laikotarpio '),
              'field_92':fields.boolean('Išregistruojamo iš PVM mokėtojų ar likviduojamo asmens paskutinio mokestinio laikotarpio'),
              'period_id': fields.many2one('account.period','Period(month)'),
              'partner_1':fields.many2one('res.partner','Vadovas(asmuo)'),
              'partner_2':fields.many2one('res.partner','Vyr. buhalteris(buhalteris) '),
              'set':fields.many2one('vat.report.form','settings browse object for report'),
              'company_id':fields.many2one('res.company'),
       
              }
    
    def _get_period(self, cr, uid, context=None):
        """Return default period value"""
        ctx = dict(context or {}, account_period_prefer_normal=True)
        period_ids = self.pool.get('account.period').find(cr, uid, context=ctx)
        return period_ids and period_ids[0] or False
    
    def _partner_1(self,cr,uid,id,context=None):
        id=[]
        id=self.pool.get('vat.report.form').search(cr,uid,[])
        if id:
            return self.pool.get('vat.report.form').browse(cr,uid,id[0]).partner_1.id
        else:
            return False
    
    def _partner_2(self,cr,uid,id,context=None):
        id=[]
        id=self.pool.get('vat.report.form').search(cr,uid,[])
        if id:
            return self.pool.get('vat.report.form').browse(cr,uid,id[0]).partner_2.id
        else:
            return False
    
        
    _defaults = {'period_id': _get_period,
                 'partner_1':_partner_1,
                 'partner_2':_partner_2,
                 'company_id':1,
                 }
                 
    
    
    def create(self,cr,uid,vals,context=None):
        user_id=self.pool.get('vat.report.form').search(cr,uid,[])
        if len(user_id)!=0:
            vals['set']=user_id[0]
        else:
            raise osv.except_osv(('ERROR !'), ('Please set Vat Report Settings'))
        return super(vat_report_wizard,self).create(cr,uid,vals,context)
        
    def change_81(self,cr,uid,id,field_81,field_82,context=None):
        value = {}
        if field_81 == True:
            value = {'field_82':False}
        return {'value':value}
    
    def change_82(self,cr,uid,id,field_81,field_82,context=None):
        value = {}
        if field_82 == True:
            value = {'field_81':False}
        return {'value':value}
    
    def change_91(self,cr,uid,id,field_91,field_92,context=None):
        value = {}
        if field_91 == True:
            value = {'field_92':False}
        return {'value':value}
    
    def change_92(self,cr,uid,id,field_91,field_92,context=None):
        value = {}
        if field_92 == True:
            value = {'field_91':False}
        return {'value':value}
    
