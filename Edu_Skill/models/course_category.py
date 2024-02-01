from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, Warning


class CategoryDetails(models.Model):
    _name = "category.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Category Detail"

    category_name = fields.Char(
        "Category Name",
        tracking=True,
    )
    category_image = fields.Image("Cetegory Image")
    category_upload_date = fields.Date(
        "Upload Date",
        default=fields.Datetime.now,
        tracking=True,
    )
    course_count = fields.Integer(
        string="Course Count", compute="_compute_course_count"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_process", "In Process"),
            ("cancle", "Cancle"),
            ("done", "Done"),
        ],
        string="Status",
    )
    reference_no = fields.Char(
        string="Category Order Reference",
        required=True,
        default=lambda self: _("New"),
    )

    def _compute_course_count(self):  # Count Course Match With Category
        for res in self:
            course_count = self.env["course.detail"].search_count(
                [("category_id", "=", res.id)]
            )  # Use OF Search Conut ORM Method
            res.course_count = course_count

    def action_open_course(self):
        if self.course_count == 1:  # Condition Check For Open Form View
            return {
                "type": "ir.actions.act_window",
                "name": "Course",
                "res_model": "course.detail",
                "res_id": int(
                    self.env["course.detail"].search(
                        [("category_id", "=", self.id)]
                    )  # Use OF Search ORM Method
                ),
                "domain": [("category_id", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }
        else:
            return {
                "name": "Course",
                "res_model": "course.detail",
                "view_mode": "list,form",
                "context": {},
                "domain": [("category_id", "=", self.id)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    _sql_constraints = [
        ("category_uniqe", "unique(category_name)", "Category Name must be unique.")
    ]

    # Generate Sequence using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "category.detail"
            ) or _("New")
        res = super(CategoryDetails, self).create(vals)
        return res

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "category_name" in vals and vals["category_name"]:
            vals["category_name"] = vals["category_name"].capitalize()
            return super(CategoryDetails, self).write(vals)

    def name_get(self):  # Using name_get method pass category name and reference Number
        response = []
        for record in self:
            response.append(
                (record.id, "%s, %s" % (record.category_name, record.reference_no))
            )
        return response

    # using name_search Method search with other model can use of category_name and
    # reference_no
    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("category_name", operator, name),
                ("reference_no", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for state is Draft And Cancel then
    # Delete
    def unlink(self):
        for states in self:
            if states.state not in ("draft", "cancel"):
                raise ValidationError(
                    _("You cannot delete an Category which is not draft or cancelled. ")
                )
        return super(CategoryDetails, self).unlink()

    # Using search_read method can Check state is Draft amd in Process
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            "|",
            ("state", "ilike", "draft"),
            ("state", "ilike", "in_process"),
            ("state", "ilike", "done"),
        ]
        return super(CategoryDetails, self).search_read(
            domain, fields, offset, limit, order
        )
