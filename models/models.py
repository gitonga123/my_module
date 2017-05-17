# -*- coding: utf-8 -*-

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


class ResPartner(models.Model):
	_inherit = 'res.partner'
	book_ids = fields.One2many(
		'library.book','publisher_id',string="Published Books"
		)
	book_ids = fields.Many2many('library.book',string='Authored Books')