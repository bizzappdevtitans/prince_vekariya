from odoo import api, fields, models, _


class QuizResult(models.Model):
    _name = "quiz.result"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Quiz Detail"
    video_caption = "video_caption"

    course_id = fields.Many2one(
        "course.detail", ondelete="cascade", string="Video Caption"
    )

    user_id = fields.Many2one(
        "user.detail", ondelete="cascade", string="User", required=True
    )
    user_last_name = fields.Char(string="Last Name", related="user_id.last_name")
    total_right_answer = fields.Integer(string="Total Right Answer")
    total_wrong_answer = fields.Integer(string="Total Wrong Answer")
    question = fields.Many2one(
        "quiz.detail", string="Question", ondelete="cascade", required=True
    )
    user_input = fields.Char(string="User Input")
    right_answer = fields.Char(string="Answer")
    percentge = fields.Float("percentge", default=0.0)
    verified = fields.Boolean(string="verified", default=False)
    reference_no = fields.Char(
        string="Quiz Result Reference",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
    )
    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "quiz.result"
            ) or _("New")
        res = super(QuizResult, self).create(vals)
        return res
