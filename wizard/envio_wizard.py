from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)


class HelpdeskEnvioWizard(models.TransientModel):
    _name = 'helpdesk.envio.wizard'
    _inherit = 'mail.compose.message'
    _description = 'Enviar Ticket Firmado (Enterprise)'

    ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Ticket',
        required=True,
        readonly=True
    )

    # ============================
    # DEFAULTS (como factura)
    # ============================
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        ticket_id = self.env.context.get('default_ticket_id') or self.env.context.get('active_id')
        if not ticket_id:
            return res

        ticket = self.env['helpdesk.ticket'].browse(ticket_id)
        
        template = False
        try:
            template = self.env.ref('helpdesk_firma.email_template_ticket_firmado')
        except Exception:
            pass

        partners = ticket.partner_id and [ticket.partner_id.id] or []

        res.update({
            'ticket_id': ticket.id,
            'model': 'helpdesk.ticket',
            'res_id': ticket.id,
            'partner_ids': [(6, 0, partners)],
            'template_id': template.id if template else False,
            'subject': template.subject if template else f'Ticket #{ticket.id}',
        })

        return res

    # ============================
    # ONCHANGE TEMPLATE
    # ============================
    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.subject = self.template_id.subject
            self.body = self.template_id.body_html

    # ============================
    # PDF
    # ============================
    def _get_or_create_pdf(self):
        self.ensure_one()

        Attachment = self.env['ir.attachment'].sudo()
        name = f'Ticket_{self.ticket_id.id}.pdf'

        attachment = Attachment.search([
            ('res_model', '=', 'helpdesk.ticket'),
            ('res_id', '=', self.ticket_id.id),
            ('name', '=', name),
        ], limit=1)

        if attachment:
            return attachment

        report = self.env.ref('helpdesk_firma.action_report_ticket_firma')
        pdf_content, _ = report._render_qweb_pdf([self.ticket_id.id])

        return Attachment.create({
            'name': name,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'helpdesk.ticket',
            'res_id': self.ticket_id.id,
            'mimetype': 'application/pdf',
        })

    # ============================
    # ENVÍO FINAL
    # ============================
    def send_mail(self, auto_commit=False):
        self.ensure_one()

        if self.ticket_id.estado_firma != 'firmado':
            raise UserError(_('El ticket debe estar firmado antes de enviarse.'))

        try:
            attachment = self._get_or_create_pdf()
            self.attachment_ids = [(4, attachment.id)]
        except Exception as e:
            _logger.exception('Error al generar PDF del ticket: %s', e)

        return super().send_mail(auto_commit=auto_commit)
