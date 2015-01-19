# coding=utf-8
from openerp.osv import osv , orm , fields

class vat_report_form(osv.osv):
    _name='vat.report.form'
    _columns={'company':fields.char('Mokesčių mokėtojo / pavadinimas vardas, pavardė',size=30),
              'tax_code':fields.char('Mokesčių mokėtojo identifikacinis numeris (kodas)',size=11),
              'vat_code':fields.char('PVM mokėtojo kodas',size=14),
              'address':fields.char('Buveinės adresas',size=30),
              'email':fields.char('El. pašto adresas ar telefonas',size=30),
              'registration_no':fields.char('Registracijos Nr. ',size=20),
              'code_custom':fields.char('EVRK Kodas',size=6),
              'field_11':fields.many2one('account.tax.code','11) PVM apmokestinami sandoriai'),
              'field_12':fields.many2one('account.tax.code','12) PVM apmokestinami sandoriai,kai PVM išskaito pirkėjas (96 str. nustatytais atvejais)'),
              'field_13':fields.many2one('account.tax.code','13) PVM neapmokestinami sandoriai'),
              'field_14':fields.many2one('account.tax.code','14) Suvartojimas privatiems poreikiams'),
              'field_15':fields.many2one('account.tax.code','15) Ilgalaikio materialiojo turto pasigaminimas'),
              'field_16':fields.many2one('account.tax.code','16) Sandorių, kuriems taikoma spec. apmokestinimo schema, marža '),
              'field_17':fields.many2one('account.tax.code','17) Prekių eksportas (0 proc.)'),
              'field_18':fields.many2one('account.tax.code','18) ES PVM mokėtojams patiektos prekės (0 proc.)'),
              'field_19':fields.many2one('account.tax.code','19) Kiti PVM apmokestinami sandoriai (0 proc.) *'),
              'field_20':fields.many2one('account.tax.code','20) Už Lietuvos ribų įvykę sandoriai (ne PVM objektas Lietuvoje)'),
              'field_21':fields.many2one('account.tax.code','21) Iš ES įsigytos prekės'),
              'field_22':fields.many2one('account.tax.code','22) Iš ES įsigytos prekės trikampei prekybai'),
              'field_23':fields.many2one('account.tax.code','23) Iš užsienio valstybių įsigytos paslaugos'),
              'field_24':fields.many2one('account.tax.code','24) Iš jų: įsigytos iš ES PVM mokėtojų'),
              'field_25':fields.many2one('account.tax.code','25) Įsigytų prekių ir paslaugų pirkimo PVM'),
              'field_26':fields.many2one('account.tax.code','26) Sumokėtas importo PVM'),
              'field_27':fields.many2one('account.tax.code','27) Importo PVM, kurio įskaitymą kontroliuoja VMI'),
              'field_28':fields.many2one('account.tax.code','28) Kalendorinių metų proporcinis PVM atskaitos procentas'),
              'field_29':fields.many2one('account.tax.code','29) Standartinio tarifo pardavimo PVM'),
              'field_30':fields.many2one('account.tax.code','30) 9 proc. pardavimo PVM'),
              'field_31':fields.many2one('account.tax.code','31) 5 proc. pardavimo PVM '),
              'field_32':fields.many2one('account.tax.code','32) Pardavimo PVM (95 str. nustatytais atvejais)'),
              'field_33':fields.many2one('account.tax.code','33) Pardavimo PVM (96 str. nustatytais atvejais)'),
              'field_34':fields.many2one('account.tax.code','34) Iš ES įsigytų prekių pardavimo PVM'),
              'field_35':fields.many2one('account.tax.code','35) Atskaitomas PVM'),
              'partner_1':fields.many2one('res.partner','Vadovas(asmuo)'),
              'partner_2':fields.many2one('res.partner','Vyr. buhalteris(buhalteris) '),
              #'wizard_id':fields.many2one('vat.report.wizard')
              }
    _defaults={'company':lambda self,cr,uid,c:self.pool.get('res.company').browse(cr,uid,1).name or '',
               'tax_code':lambda self,cr,uid,c:self.pool.get('res.company').browse(cr,uid,1).company_registry or '',
               'vat_code':lambda self,cr,uid,c:self.pool.get('res.company').browse(cr,uid,1).vat or '',
               'address':lambda self,cr,uid,c:(self.pool.get('res.company').browse(cr,uid,1).street or ' ') +' '+(self.pool.get('res.company').browse(cr,uid,1).city or ' '),
               'email':lambda self,cr,uid,c:self.pool.get('res.company').browse(cr,uid,1).email or '',
               }
    
    def create(self,cr,uid,vals,context=None):
        #print('5555555555555',type(self.pool.get('account.period').browse(cr,uid,5).date_start))
        id=[]
        id=self.search(cr,uid,[])
        if (len(id)>=1):
            raise osv.except_osv(('ERROR !'), ('Only one set of settings allowed'))
            #return super(vat_report_form,self).create(cr,uid,vals,context=context)
        else:
            return super(vat_report_form,self).create(cr,uid,vals,context=context)
                