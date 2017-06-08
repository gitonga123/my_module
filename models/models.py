# -*- coding: utf-8 -*-

import os
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.fields import Date as fDate
from datetime import timedelta as td
from termcolor import colored
class LibraryBook(models.Model):
	_name='library.book'
	_description = 'Library Book'
	_order = 'date_release desc, name'
	_rec_name ='short_name'
	#_inherit = ['base.archive']


	name=fields.Char('Title', required=True)
	_sql_constraints = [
	    ('name_uniq', 'unique (name)',('The Book Title must be unique !')),
	]
	short_name = fields.Char(
	    string='Short Title',
	    size=100,
	    translate=False,
	)
	date_release = fields.Date('Release Date')
	author_ids = fields.Many2many('res.partner', string="Authors")
	book_read = fields.Many2many('res.partner', 'book_ids','book_read',string="Book Read")
	notes = fields.Text('Intermal Notes')
	state = fields.Selection(
			[('draft','Not Available'),
			 ('available','Available'),
			 ('Lost','Lost Copy')
			 ],'State'
		)
	description = fields.Html(string='Description',
		sanitize=True,
		strip_style=False,
		translate=False,)
	cover = fields.Binary('Book Cover')
	out_of_print = fields.Boolean('Out of Print')
	date_updated = fields.Datetime('Last Updated')
	pages = fields.Integer(string='Number of Pages',
		default=0,
		help='Total Book Pages',
		groups='base.group_user',
		states={'cancel':[('readonly',True)]},
		copy=True,
		readonly=False,
		index=False,
		required=False,
		company_dependent=False, )
	reader_rating = fields.Float('Reader Average Rating',(14,4),
		)
	cost_price = fields.Float(
		'Book Cost', dp.get_precision('Book Price'))
	currency_id = fields.Many2one('res.currency', string='Currency')
	retail_price = fields.Monetary(
		'Retail Price')
	publisher_id = fields.Many2one(
		'res.partner', string='Publisher',
		ondelete='set null',
		context={},
		domain=[],
		)
	age_days = fields.Float(
		string='Days Since Release',
		compute='_compute_age',
		#inverse='_inverse_age',
		search ='_search_age',
		store=False,
		compute_sudo=False,)
	publisher_city = fields.Char(
		'publisher City',related='publisher_id.city')
	ref_doc_id =fields.Reference(
		selection='_referencable_models',string='Reference Document')

	@api.model
	def is_allowed_transition(self,old_state,new_state):
		allowed = [('draft','available'),
					('available','borrowed'),
					('borrowed','avaialable'),
					('avaialable','lost'),
					('borrowed','lost'),
					('lost','available')
					]
		return (old_state,new_state) in allowed

	@api.multi
	def change_state(self,new_state):
		for book in self:
			if book.is_allowed_transition(book.state,new_state):
				book.state = new_state
			else:
				continue

	@api.constrains('date_release')
	def _check_release_date(self):
		for r in self:
			if r.date_release > fields.Date.today():
				raise models.ValidationError(
					'Release Date must be in the past'
				)
		
	@api.depends('date_release')
	def _compute_age(self):
		today = fDate.from_string(fDate.today())
		for book in self.filtered('date_release'):
			release = fDate.from_string(book.date_release)
			
			delta =  release-today
			book.age_days = delta.days

	# def _inverse_age(self): 
	# 	today = fDate.from_string(fDate.today())
	# 	for book in self.filtered('date_release'):
	# 		d = td(days=book.age_days) - today
	# 		book.date_release = fDate.to_string(d)
					
	def _search_age(self):
		today = fDate.from_string(fDate.today())
		value_days = td(days=value)
		value_date = fDate.to_string(today - value_days)

		return [('date_release',operator, value_date)]

	@api.model
	def _referencable_models(self):
		models = self.env['res.request.link'].search([])
		return [(x.object,x.name) for x in models]
		

class ResPartner(models.Model):
	_inherit = 'res.partner'
	_order = "name"

	book_ids = fields.One2many(
		'library.book','publisher_id',string="Published Books"
		)
	book_ids = fields.Many2many('library.book',string='Authored Books')
	authored_book_ids = fields.Many2many(
	    'library.book',
	    string='Authored Book',
	)
	count_books = fields.Integer(
		"Number of Authored Books",
		compute='_compute_count_books')

	@api.depends('authored_book_ids')
	def _compute_count_books(self):
		for r in self:
			r.count_books = len(r.authored_book_ids)

class BaseArchive(models.AbstractModel):
	_name = 'base.archive'
	active  = fields.Boolean(
	   default=True,
	)

	def do_archive(self):
		for record in self:
			record.active = not record.active


class LibraryMember(models.Model):
	_name = 'library.member'
	_inherits = {'res.partner': 'partner_id'}
	partner_id = fields.Many2one(
		'res.partner', ondelete='cascade')
	date_start = fields.Date('Member Since')
	date_end = fields.Date('Termination Date')
	member_number = fields.Char()

