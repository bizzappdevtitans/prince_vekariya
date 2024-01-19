from odoo import api, fields, models


class CourseDetails(models.Model):
    _name = "course.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Course Detail"

    teacher_id = fields.Many2one("teacher.detail", ondelete="cascade", string="Teacher")
    course_name = fields.Char(string="Course Name", required=True)
    course_upload_date = fields.Datetime(
        string="Upload Date", default=fields.Datetime.now
    )
    first_name = fields.Char(string="First Name", related="teacher_id.first_name")
    reference = fields.Char(string="Reference")
    description = fields.Html(string="Description")

    priority = fields.Selection(
        [
            ("0", "Normal"),
            ("1", "Low"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="Priority",
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

    @api.onchange("teacher_id")
    def onchange_teacher_id(self):
        self.reference = self.teacher_id.first_name

    def object_button(self):
        print("Button clicked")

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


class SubjectDetails(models.Model):
    _name = "subject.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Subject Details"
