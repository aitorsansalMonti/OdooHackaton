{
    'name': 'Promocions i Ofertes Especials',
    'version': '1.0',
    'summary': 'Crea promocions especials durant un periode de temps per qualsevol producte',
    'category': 'Custom',
    'author': 'Jaume Rotger i Arnau Guerra',
    'depends': ['base', 'sale'],
    'data': [
        'views/vista.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}