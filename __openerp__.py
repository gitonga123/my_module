# -*- coding: utf-8 -*-
{
    'name': "my_module",

    'summary': """
        **Google Definition** - a building or room containing collections of books, periodicals, 
        and sometimes films and recorded music for people to read, borrow, or refer to.
        """,

    'description': """
    A library is a collection of sources of information and similar resources, made accessible to a defined community for reference or borrowing.
    It provides physical or digital access to material, and may be a physical building or room, or a virtual space, or both.

    .. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Melk_-_Abbey_-_Library.jpg/800px-Melk_-_Abbey_-_Library.jpg


    A library's collection can include books, periodicals, newspapers, manuscripts, films, maps, prints, documents,
     **microform**,** CDs**, **cassettes**, **videotapes**, **DVDs**, **Blu-ray Discs, e-books, audio books, databases**, and **other formats**. 

    .. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Halifax_central_library_June_2015.jpg/800px-Halifax_central_library_June_2015.jpg

    Libraries range in size from a few shelves of books to several million items. 
    In Latin and Greek, the idea of a bookcase is represented by Bibliotheca and Bibliothēkē (Greek: βιβλιοθήκη): 
    derivatives of these mean library in many modern languages, e.g. French bibliothèque.
    """,

    'author': "Library Books Kenya",
    'website': "http://www.librarybooks.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}