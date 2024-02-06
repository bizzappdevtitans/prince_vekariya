from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
        string="Last Name :",
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

    # Check Condition For First Name And Last Name Must Be different
    @api.constrains("first_name", "last_name")
    def _check_name(self):
        for record in self:
            if record.first_name == record.last_name:
                raise ValidationError(_("First Name and Last Name must be different"))

    # Condition Check For Uniq Payment Id
    _sql_constraints = [
        ("payment_id_uniqe", "unique(payment_id)", "Payment id  must be unique.")
    ]

    # Condition Check For Uniq Order Id
    _sql_constraints = [
        ("order_id_uniqe", "unique(order_id)", "Order id must be unique.")
    ]

    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "order.detail"
            ) or _("New")
        res = super(CourseOrder, self).create(vals)
        return res

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "admin_note" in vals and vals["admin_note"]:
            vals["admin_note"] = vals["admin_note"].capitalize()
            return super(CourseOrder, self).write(vals)

    # get Name of record Of Using name_get ORM Method
    def name_get(self):
        response = []
        for record in self:
            response.append(
                (
                    record.id,
                    "%s, %s %s"
                    % (record.order_id, record.first_name, record.last_name),
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
                "|",
                ("first_name", operator, name),
                ("last_name", operator, name),
                ("payment_mode", operator, name),
                ("payment_id", operator, name),
                ("reference_no", operator, name),
                ("order_id", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for state is Draft And Cancel then
    # Delete
    def unlink(self):
        for states in self:
            if states.state not in ("pending", "cancel"):
                raise ValidationError(
                    _("You cannot delete an Order which is not cancelled or pending. ")
                )
        return super(CourseOrder, self).unlink()

    # Using search_read method can Check state is Draft and in Process and Cancel
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            "|",
            ("state", "ilike", "actepted"),
            ("state", "ilike", "pending"),
            ("state", "ilike", "cancel"),
        ]
        return super(CourseOrder, self).search_read(
            domain, fields, offset, limit, order
        )
