# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp

class LibraryBook(models.Model):
	_name='library.book'
	_description = 'Library Book'
	_order = 'date_release desc, name'
	_rec_name ='short_name'

	name=fields.Char('Title', required=True)
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
		'res,partner', string='Publisher',
		ondelete='set null',
		context={},
		domain=[],
		)


class ResPartner(models.Model):
	_inherit = 'res.partner'
	book_ids = fields.One2many(
		'library.book','publisher_id',string="Published Books"
		)
	book_ids = fields.Many2many('library.book',string='Authored Books')