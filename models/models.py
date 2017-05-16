# -*- coding: utf-8 -*-

from openerp import models, fields, api

class LibraryBook(models.Model):
	_name='library.book'
	_description = 'Library Book'
	_order = 'date_release desc, name'
	_rec_name ='short_name'

	name=fields.Char('Title', required=True)
	short_name = fields.Char(
	    string='Short Title',
	)
	date_release = fields.Date('Release Date')
	author_ids = fields.Many2many('res.partner', string="Authors")
	