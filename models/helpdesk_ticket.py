from odoo import models, fields, api
from odoo.exceptions import UserError

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    firma = fields.Binary('Firma', attachment=True)
    firma_signed_by = fields.Char('Firmado por')
    firma_signed_on = fields.Datetime('Fecha de firma')
    estado_firma = fields.Selection([('sin_firma','Sin firma'),('firmado','Firmado')], default='sin_firma', copy=False)

    def action_enviar_ticket(self):
        self.ensure_one()
        if self.estado_firma != 'firmado':
            raise UserError('El ticket debe estar firmado antes de enviarlo.')
        return {
            'name': 'Enviar Ticket Firmado',
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.envio.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_ticket_id': self.id},
        }
