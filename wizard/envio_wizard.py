from odoo import models, fields, api
import base64, logging
_logger = logging.getLogger(__name__)

class HelpdeskEnvioWizard(models.TransientModel):
    _name = 'helpdesk.envio.wizard'
    _inherit = 'mail.compose.message'
    _description = 'Enviar Ticket Firmado (wizard tipo factura - Enterprise)'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ticket_id = self._context.get('default_ticket_id') or self._context.get('active_id')
        if not ticket_id:
            return res
        ticket = self.env['helpdesk.ticket'].browse(ticket_id)
        template = False
        try:
            template = self.env.ref('helpdesk_firma.email_template_ticket_firmado')
        except Exception:
            template = False

        partners = ticket.partner_id and [ticket.partner_id.id] or []

        defaults = {
            'ticket_id': ticket.id,
            'model': 'helpdesk.ticket',
            'res_id': ticket.id,
            'partner_ids': [(6, 0, partners)] if partners else False,
        }
        defaults['subject'] = template.subject if template and template.subject else f"Ticket #{ticket.id}: {ticket.name or ''}"
        if template:
            defaults['template_id'] = template.id

        res.update(defaults)
        return res

    def _generate_pdf_attachment(self):
        report_action = self.env.ref('helpdesk_firma.action_report_ticket_firma')
        pdf_content, _ = report_action._render_qweb_pdf([self.ticket_id.id])
        attach = self.env['ir.attachment'].create({
            'name': f'Ticket_{self.ticket_id.id}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': 'helpdesk.ticket',
            'res_id': self.ticket_id.id,
            'mimetype': 'application/pdf',
        })
        return attach

    def send_mail(self, auto_commit=False):
        if not self.ticket_id:
            return super(HelpdeskEnvioWizard, self).send_mail(auto_commit=auto_commit)
        try:
            attachment = self._generate_pdf_attachment()
            if attachment:
                self.attachment_ids = [(4, attachment.id)]
        except Exception as e:
            _logger.exception('Failed to generate PDF attachment: %s', e)
        return super(HelpdeskEnvioWizard, self).send_mail(auto_commit=auto_commit)
