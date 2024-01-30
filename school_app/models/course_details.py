from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CourseDetails(models.Model):
    _name = "course.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Course Detail"
    _rec_name = "course_name"

    teacher_id = fields.Many2one(
        "teacher.detail", ondelete="cascade", string="Teacher", required=True
    )  # Teacher Id Given From Teacher Detail Model
    teacher_last_name = fields.Char(string="Last Name", related="teacher_id.last_name")
    course_name = fields.Char(string="Course Name", required=True)
    image = fields.Image(string="Image")
    video = fields.Binary(String="Video")
    course_upload_date = fields.Date(string="Upload Date", default=fields.Datetime.now)
    description = fields.Html(string="Description")

    level = fields.Selection(
        [
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
        ],
        string="Level",
        required=True,
    )

    language = fields.Selection(
        [
            ("english", "English"),
        ],
        string="Language",
        required=True,
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
    price = fields.Integer(
        "Price",
        null=False,
    )
    image = fields.Image(string="Course Image", required=True)

    # Creating Action Button
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

    def _compute_video_count(self):
        for res in self:  # For Loop Creating For Count A video
            video_count = self.env["video.detail"].search_count(
                [("course_id", "=", res.id)]
            )
            res.video_count = video_count

    def action_open_course(self):
        if self.video_count == 1:  # Conditon Check For Open A Form View
            return {
                "type": "ir.actions.act_window",
                "name": "Course",
                "res_model": "video.detail",
                "res_id": int(
                    self.env["video.detail"].search([("course_id", "=", self.id)])
                ),
                "domain": [("course_id", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }
        else:  # Conditon Check For Open A Tree View
            return {
                "name": "Course",
                "res_model": "video.detail",
                "view_mode": "list,form",
                "context": {},
                "domain": [("course_id", "=", self.id)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    _sql_constraints = [
        ("course_name_uniqe", "unique(course_name)", "Course Name must be unique.")
    ]  # Condition check for Uniqe Course Name
