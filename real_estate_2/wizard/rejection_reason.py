from odoo import models, api, fields
from datetime import date, datetime, time


class RejectionReason(models.TransientModel):
    _name = "rejection.reason"
    _description = "rejection reason"

    @api.model
    def default_get(self, fields):
        rec = super(RejectionReason, self).default_get(fields)
        active_id = self._context.get('active_ids')
        # current_partner = self.env['real.state'].search([('id', '=', active_id)]).partner_id.id
        current_partner = self.env['real.state'].browse(active_id).partner_id.id
        rec['partner'] = current_partner
        return rec

    name = fields.Text("Rejection Reason", required=True)
    partner = fields.Many2one('res.partner', "Partner")

    def action_add_rejection(self):
        active_id = self.env.context.get('active_id')
        # to get only count of records
        # current_real = self.env['real.state'].search_count([])
        current_real = self.env['real.state'].search([('id', '=', active_id)])
        print(current_real.reason)
        current_real.reason = self.name
