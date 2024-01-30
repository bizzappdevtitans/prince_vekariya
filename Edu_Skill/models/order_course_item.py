from odoo import api, fields, models


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
