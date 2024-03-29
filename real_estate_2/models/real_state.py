from odoo import models, api, fields
from datetime import date, datetime, time
from odoo.exceptions import ValidationError


class RealEstate(models.Model):
    _name = "real.state"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Real Estate"
    _rec_name = "name_1"

    name_1 = fields.Char(string="Name", required=True, help="Description")
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Date()
    date_availability_2 = fields.Datetime()
    expected_price = fields.Float()
    selling_price = fields.Float(digits=(10, 5))
    bedrooms = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    state = fields.Selection(
        [('draft', 'draft'), ('pending', 'pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        string="Status", default='draft')
    garden_orientation = fields.Selection([('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South')])
    test1 = fields.Binary("Attachment")
    test2 = fields.Html("1")
    test3 = fields.Image("2")
    area = fields.Float("Area")
    garden_area = fields.Float("Garden Area")
    total_area = fields.Float("Total Area")
    remaining_days = fields.Integer("Remaining Days", compute="compute_remaining_days")
    partner_id = fields.Many2one(comodel_name="res.partner", domain=[('company_id', '!=', False)])
    offer_line_ids = fields.One2many("real.estate.offer", "real_estate_id", "Offer Lines")
    tag_ids = fields.Many2many('real.estate.tags')
    reason = fields.Text("Rejection Reason", tracking=True)
    phone = fields.Char("Phone", related="partner_id.mobile")

    @api.constrains('reason')
    def _unique_reason(self):
        count_reason = self.search_count([('reason', '=', self.reason)])
        if count_reason > 1:
            raise ValidationError("Reason Exist ,Reason Must Be Unique !")

    @api.model
    def create(self, vals):
        res = super(RealEstate, self).create(vals)
        print("1111111111", vals)
        res['name_1'] = self.env['ir.sequence'].next_by_code('seq.real.estate')
        return res

    def write(self, vals):
        res = super(RealEstate, self).write(vals)
        print("2222222222", vals.get("bedrooms"))
        if vals and 1 != 1:
            raise ValidationError("You Cannot update this record")
        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'approved':
                raise ValidationError("You Cannot delete approved record")
        return super(RealEstate, self).unlink()

    @api.onchange('area', 'garden_area')
    def onchange_total_area(self):
        if self.area > 0 and self.garden_area > 0:
            self.total_area = self.area + self.garden_area
        else:
            self.total_area = 0

    @api.depends('date_availability')
    def compute_remaining_days(self):
        if self.date_availability:
            self.remaining_days = (self.date_availability - date.today()).days
        else:
            self.remaining_days = 0

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'

    def action_pending(self):
        self.state = 'pending'

    def action_reset(self):
        self.state = 'draft'


class RealEstateOffer(models.Model):
    _name = 'real.estate.offer'
    _rec_name = 'partner_id'

    real_estate_id = fields.Many2one("real.state")
    partner_id = fields.Many2one("res.partner", "Partner")
    desc = fields.Char("Desc")
    price = fields.Float("Price")
    offer_date = fields.Date("Offer Date")


class RealEstateTags(models.Model):
    _name = 'real.estate.tags'

    name = fields.Char("Name")
