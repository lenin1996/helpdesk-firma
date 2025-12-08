from odoo import models, fields, _
from odoo.exceptions import UserError


class HelpdeskFirmaWizard(models.TransientModel):
    _name = 'helpdesk.firma.wizard'
    _description = 'Wizard Firma Ticket (Enterprise)'

    ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Ticket',
        required=True,
        readonly=True
    )

    signature = fields.Binary(
        string='Firma',
        required=True
    )

    signed_by = fields.Char(
        string='Firmado por',
        readonly=True,
        default=lambda self: self.env.user.name
    )

    signed_on = fields.Datetime(
        string='Fecha de firma',
        readonly=True,
        default=fields.Datetime.now
    )

    def action_confirm_firma(self):
        self.ensure_one()

        if not self.signature:
            raise UserError(_('Debe firmar antes de confirmar.'))

        if self.ticket_id.estado_firma == 'firmado':
            raise UserError(_('Este ticket ya fue firmado.'))

        self.ticket_id.write({
            'firma': self.signature,
            'firma_signed_by': self.signed_by,
            'firma_signed_on': self.signed_on,
            'estado_firma': 'firmado',
        })

        return {'type': 'ir.actions.act_window_close'}
