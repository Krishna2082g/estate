from odoo import models, fields, api, _
from odoo.exceptions import UserError

class TestModel(models.Model):
    _name = 'test_model'
    _description = 'Test Model'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sq ft)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sq ft)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garden Orientation")

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="Status", default='new')

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_mark_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be marked as sold.")
            record.state = 'sold'
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'
        return True
