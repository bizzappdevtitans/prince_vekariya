from odoo import api, fields, models


class CategoryDetails(models.Model):
    _name = "category.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Category Detail"
    _rec_name = "category_name"

    category_name = fields.Char(
        "Category Name",
        tracking=True,
        required=True,
    )
    category_image = fields.Image(
        "Cetegory Image",
        tracking=True,
        required=True,
    )
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
            ("cancle", "cancle"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    def _compute_course_count(self):
        for res in self:
            course_count = self.env["course.detail"].search_count(
                [("category_id", "=", res.id)]
            )
            res.course_count = course_count

    def action_open_course(self):
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
