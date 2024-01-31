from odoo import api, fields, models, _


class CategoryDetails(models.Model):
    _name = "category.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Category Detail"
    _rec_name = "category_name"

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
        readonly=True,
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

    def write(self, vals):
        if "category_name" in vals and vals["category_name"]:
            vals["category_name"] = vals["category_name"].capitalize()
            return super(CategoryDetails, self).write(vals)

    def unlink(self):
        return super(CategoryDetails, self).unlink()

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s, %s" % (rec.category_name, rec.reference_no)))
        return res
