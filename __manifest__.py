{
    'name': 'Helpdesk Firma (Enterprise)',
    'summary': 'Firma digital y envío de tickets con PDF tipo factura',
    'description': """
Extiende Helpdesk para permitir:

- Firma digital del ticket desde el formulario
- Generación de PDF firmado
- Envío del ticket por correo con PDF adjunto
- Integración con Odoo Sign (Enterprise)

Diseñado para Odoo 18 Enterprise
""",
    'version': '18.0.1.1.0',
    'author': 'Lenin Chela',
    'maintainer': 'Lenin Chela',
    'website': 'https://github.com/lenin1996/helpdesk-firma',
    'license': 'OPL-1',
    'category': 'Helpdesk',
    'depends': ['mail','helpdesk','sign',],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/helpdesk_ticket_views.xml',
        'wizard/envio_wizard_views.xml',
        'wizard/firma_wizard_views.xml',
        'report/report_ticket_firma.xml',
        'report/ticket_firma_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
