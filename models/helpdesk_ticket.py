from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    firma = fields.Binary(
        string='Firma',
        attachment=True,
        tracking=True
    )
    firma_signed_by = fields.Char(
        string='Firmado por',
        tracking=True
    )
    firma_signed_on = fields.Datetime(
        string='Fecha de firma',
        tracking=True
    )
    estado_firma = fields.Selection(
        [
            ('sin_firma', 'Sin firma'),
            ('firmado', 'Firmado'),
        ],
        string='Estado de firma',
        default='sin_firma',
        copy=False,
        tracking=True
    )

    def action_enviar_ticket(self):
        self.ensure_one()

        # ✅ Validación fuerte (Enterprise)
        if self.estado_firma != 'firmado' or not self.firma:
            raise UserError(_(
                'No puede enviar el ticket.\n\n'
                'El ticket debe estar firmado antes de enviarlo.'
            ))

        return {
            'name': _('Enviar Ticket Firmado'),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.envio.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_ticket_id': self.id
            },
        }
