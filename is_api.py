# -*- coding: utf-8 -*-

import time
import datetime

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


''' Calculer les jours de fermeture des clients et de l'usine '''
class is_api(osv.osv):
    _name = 'is.api'
    
    def num_closing_days(self, cr, uid, partner_id, context=None):
        """ Retourner les jours de fermetures de l'usine 
        """
        jours_fermes = []
        if partner_id.close_monday:
            jours_fermes.append(1)
        if partner_id.close_tuesday:
            jours_fermes.append(2)
        if partner_id.close_wednesday:
            jours_fermes.append(3)
        if partner_id.close_thursday:
            jours_fermes.append(4)
        if partner_id.close_friday:
            jours_fermes.append(5)
        if partner_id.close_saturday:
            jours_fermes.append(6)
        if partner_id.close_sunday:
            jours_fermes.append(0)
        return jours_fermes
    

    def get_leave_dates(self, cr, uid, partner_id, context=None):
        """ Retourner les jours de congé de l'usine 
        """
        leave_dates = []
        if partner_id.calendar_line:
            for line in partner_id.calendar_line:                                                                                                                                                            
                delta = datetime.datetime.strptime(line.date_to, DATETIME_FORMAT) - datetime.datetime.strptime(line.date_from, DATETIME_FORMAT)
                for i in range(delta.days + 1):
                    date = datetime.datetime.strptime(line.date_from, DATETIME_FORMAT) + datetime.timedelta(days=i)
                    leave_dates.append(date.strftime('%Y-%m-%d'))
        return leave_dates
    
    def get_day_except_weekend(self, cr, uid, date, num_day, context=None):
        """ Calculer la date d'expédition en exceptant les weekends
        """
        if int(num_day) not in [0, 6]:
            return date
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=1)
            date = date.strftime('%Y-%m-%d')
            num_day = time.strftime('%w', time.strptime(date, '%Y-%m-%d'))
            return self.get_day_except_weekend(cr, uid, date, num_day, context=context)

        
    def get_working_day(self, cr, uid, date, num_day, jours_fermes, leave_dates, context=None):
        """ Déterminer la date d'expédition en fonction des jours de fermeture de l'usine ou des jours de congés de l'usine 
        """
        if int(num_day) not in jours_fermes and date not in leave_dates:
            return date
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=1)
            date = date.strftime('%Y-%m-%d')
            num_day = time.strftime('%w', time.strptime(date, '%Y-%m-%d'))
            return self.get_working_day(cr, uid, date, num_day, jours_fermes, leave_dates, context=context)
        
is_api()