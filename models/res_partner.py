# -*- coding: utf-8 -*-
import os
from openerp import models, fields, api
from termcolor import colored

class res_partner(models.Model):
    _inherit = 'res.partner'
    passed_override = fields.Boolean(string='Has passed our super method')
    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(res_partner, self).create(values)

        # Change the values of a variable in this super function
        record['passed_override'] = True

        print colored(("<<<<<<<>>>>>>><<<<>>>>================>"),'red')
        print 'Passed this function. passed_override_write_function value: ' + str(record['passed_override'])
        print ("<<<<<<<>>>>>>><<<<>>>>================>")

        # Return the record so that the changes are applied and everything is stored.
	return record


class res_books(models.Model):
	_inherit = 'library.book'

	@api.model
	def create(self,values):
		record = super(res_books,self).create(values)

		record['book_read'] = list(record['author_ids'])
		print colored(("<<<<<<<>>>>>>><<<<>>>>================>"),'red')
		print colored(("<<<<<<<>>>>>>><<<<>>>>================>"),'yellow')
		print record['book_read']
		print colored(("<<<<<<<>>>>>>><<<<>>>>================>"),'green')
		print colored(("<<<<<<<>>>>>>><<<<>>>>================>"),'blue')
		print record['authors_ids']
		return record

