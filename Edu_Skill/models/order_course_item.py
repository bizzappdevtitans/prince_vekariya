from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CourseOrderItem(models.Model):
    _name = "course.item.order.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Order Detail"
    _rec_name = "order_id"

    order_id = fields.Many2one(
        "order.detail",
        ondelete="cascade",
        string="Order Ids",
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
        string="Course Names",
        required=True,
    )
    price = fields.Float(string="Price : ")
    reference_no = fields.Char(
        string="Order Item Reference",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
    )
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

    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "course.item.order.detail"
            ) or _("New")
        res = super(CourseOrderItem, self).create(vals)
        return res

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "course_name" in vals and vals["course_name"]:
            vals["course_name"] = vals["course_name"].capitalize()
            return super(CourseOrderItem, self).write(vals)

    # get Name of record Of Using name_get ORM Method
    def name_get(self):
        response = []
        for record in self:
            response.append(
                (
                    record.id,
                    "%s: %s , %s"
                    % (
                        record.user_first_name,
                        record.user_last_name,
                        record.course_name.course_name,
                    ),
                )
            )
        return response

    # using name_search Method We Can Find Multipal Field Record
    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                "|",
                "|",
                "|",
                ("user_first_name", operator, name),
                ("user_last_name", operator, name),
                ("course_name", operator, name),
                ("order_id", operator, name),
                ("reference_no", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for state is Pending And Cancel then
    # Delete
    def unlink(self):
        for states in self:
            if states.state not in ("pending", "cancel"):
                raise ValidationError(
                    _("You cannot delete an Order which is not cancelled or pending. ")
                )
        return super(CourseOrderItem, self).unlink()

    # Using search_read method can Check state is actepted amd in pending cancel
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            "|",
            ("state", "ilike", "actepted"),
            ("state", "ilike", "pending"),
            ("state", "ilike", "cancel"),
        ]
        return super(CourseOrderItem, self).search_read(
            domain, fields, offset, limit, order
        )
