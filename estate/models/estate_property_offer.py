# models/estate_property_offer.py

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)

    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('test_model', string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Datetime.now()
            record.date_deadline = base_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Datetime.now()
            record.validity = (record.date_deadline - base_date.date()).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError(_("Cannot accept offers for sold properties."))
            if offer.status == 'accepted':
                continue

            # Refuse all other offers
            offer.property_id.offer_ids.filtered(lambda o: o != offer).write({'status': 'refused'})

            # Set this offer as accepted
            offer.status = 'accepted'
            offer.property_id.state = 'offer_received'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True
