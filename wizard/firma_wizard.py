from odoo import models, fields, api, fields as f
class HelpdeskFirmaWizard(models.TransientModel):
    _name = 'helpdesk.firma.wizard'
    _description = 'Wizard Firma Ticket (Enterprise)'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', required=True)
    signature = fields.Binary('Firma', widget='signature')
    signed_by = fields.Char('Firmado por')
    signed_on = fields.Datetime('Fecha de firma')

    def action_confirm_firma(self):
        self.ensure_one()
        self.ticket_id.write({
            'firma': self.signature,
            'firma_signed_by': self.signed_by or '',
            'firma_signed_on': self.signed_on or fields.Datetime.now(),
            'estado_firma': 'firmado',
        })
        return {'type': 'ir.actions.act_window_close'}
