from odoo import api, fields, models, _


class CourseOrderItem(models.Model):
    _name = "course.item.order.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Order Detail"
    _rec_name = "order_id"

    order_id = fields.Many2one(
        "order.detail",
        ondelete="cascade",
        string="Order Id",
        required=True,
    )
    user_first_name = fields.Char(
        related="order_id.first_name", readonly=True, required=True
    )
    user_last_name = fields.Char(
        string="Last Name", readonly=True, related="order_id.last_name"
    )
    course_name = fields.Many2one(
        "course.detail",
        ondelete="cascade",
        string="Course Name",
        required=True,
    )
    price = fields.Float(string="Price : ")
    reference_no = fields.Char(
            string="Order Item Reference",
            required=True,
            readonly=True,
            default=lambda self: _("New"),
        )
    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "course.item.order.detail"
            ) or _("New")
        res = super(CourseOrderItem, self).create(vals)
        return res
