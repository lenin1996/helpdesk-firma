{
    'name': 'Helpdesk Firma (Enterprise)',
    
    'version': '18.0.1.1.0',
    'summary': 'Firma digital y envío de tickets con PDF',
    'author': 'Lenin Chela',
    'maintainer': 'Lenin Chela',
    'website': 'https://github.com/lenin1996/helpdesk_firma',
    'license': 'OPL-1',
    'category': 'Helpdesk',
    'depends': [
        'mail',
        'helpdesk',
        'sign',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/helpdesk_ticket_views.xml',
        'wizard/envio_wizard_views.xml',
        'wizard/firma_wizard_views.xml',
        'report/report_ticket_firma.xml',
    ],
    'qweb': [
        'report/ticket_firma_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
