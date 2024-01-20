from odoo import api, fields, models


class CourseDetails(models.Model):
    _name = "course.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Course Detail"
    _rec_name = "course_name"

    teacher_id = fields.Many2one("teacher.detail", ondelete="cascade", string="Teacher")
    category_id = fields.Many2one(
        "category.detail", ondelete="cascade", string="Category"
    )
    teacher_first_name = fields.Char(
        string="First Name", related="teacher_id.first_name"
    )
    course_name = fields.Char(string="Course Name", required=True)
    course_upload_date = fields.Date(string="Upload Date", default=fields.Datetime.now)
    reference = fields.Char(string="Reference")
    description = fields.Html(string="Description")

    level = fields.Selection(
        [
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
        ],
        string="Level",
    )

    language = fields.Selection(
        [
            ("english", "English"),
        ],
        string="Language",
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

    price = fields.Integer("Price", null=False)
    image = fields.Image(string="Course Image")

    @api.onchange("teacher_id")
    def onchange_teacher_id(self):
        self.reference = self.teacher_id.first_name

    def action_in_process(self):
        for rec in self:
            rec.state = "in_process"

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancle(self):
        for rec in self:
            rec.state = "cancle"
