from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CourseDetails(models.Model):
    _name = "course.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Course Detail"
    _rec_name = "course_name"

    teacher_id = fields.Many2one(
        "teacher.detail", ondelete="cascade", string="Teacher", required=True
    )
    category_id = fields.Many2one(
        "category.detail", ondelete="cascade", string="Category", required=True
    )
    teacher_last_name = fields.Char(string="Last Name", related="teacher_id.last_name")
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
    video_count = fields.Integer(string="Video Count", compute="_compute_video_count")
    price = fields.Integer(
        "Price",
        null=False,
    )
    image = fields.Image(string="Course Image", required=True)

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

    def _compute_video_count(self):
        for res in self:
            video_count = self.env["video.detail"].search_count(
                [("course_id", "=", res.id)]
            )
            res.video_count = video_count

    def action_open_course(self):
        # return {
        #     "name": "Video",
        #     "res_model": "video.detail",
        #     "view_mode": "list,form",
        #     "context": {},
        #     "domain": [("course_id", "=", self.id)],
        #     "target": "current",
        #     "type": "ir.actions.act_window",
        # }
        action = {
            'name': 'video',
            'type': 'ir.actions.act_window',
            'res_model': 'video.detail',
            'target': 'current',
        }
        for res in self:
            video_count = self.env["video.detail"].search_count(
                [("course_id", "=", res.id)]
            )
            res.video_count = int(video_count)

        if res.video_count == 1:
            action['domain'] = [('course_id', '=', self.id)]
            action['view_mode'] = 'form'
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('course_id', '=', self.id)]
        return action

    _sql_constraints = [
        ("course_name_uniqe", "unique(course_name)", "Course Name must be unique.")
    ]
