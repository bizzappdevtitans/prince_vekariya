from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
import random


class CourseOrder(models.Model):
    _name = "order.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Order Detail"
    _rec_name = "order_id"

    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("actepted", "Actepted"),
            ("cancle", "Cancle"),
        ],
        string="Status",
        default="pending",
        required=True,
    )
    first_name = fields.Char(
        string="First Name :",
        required=True,
        size=16,
        null=False,
    )
    last_name = fields.Char(
        string="Last Name",
        tracking=True,
        required=True,
        size=16,
    )
    is_paid = fields.Boolean(default=False)
    total_price = fields.Float(string="Total : ", default=0)
    payment_mode = fields.Char(string="Payment Mode : ")
    payment_id = fields.Char(string="Payment Id : ")
    order_id = fields.Char(
        string="Order Id ",
        default=id,
        readonly=True,
    )
    reference_no = fields.Char(
        string="Course Order Reference",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
    )
    admin_note = fields.Text(string="Admin Note : ")

    @api.constrains("first_name", "last_name")
    def _check_name(self):
        for record in self:
            if record.first_name == record.last_name:
                raise ValidationError("First Name and Last Name must be different")

    # Condition Check For Uniq Payment Id
    _sql_constraints = [
        ("payment_id_uniqe", "unique(payment_id)", "Payment id  must be unique.")
    ]

    # Condition Check For Uniq Order Id
    _sql_constraints = [
        ("order_id_uniqe", "unique(order_id)", "Order id must be unique.")
    ]

    # Generate Sequence
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "order.detail"
            ) or _("New")
        res = super(CourseOrder, self).create(vals)
        return res
