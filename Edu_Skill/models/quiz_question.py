from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QuizQuestion(models.Model):
    _name = "quiz.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Quiz Detail"
    video_caption = "course_name"

    course_video_id = fields.Many2one(
        "video.detail", ondelete="cascade", string="Video Caption"
    )

    question = fields.Char(string="Question", required=True)
    option_1 = fields.Char(string="Option 1", required=True)
    option_2 = fields.Char(string="Option 2", required=True)
    option_3 = fields.Char(string="Option 3")
    option_4 = fields.Char(string="Option 4")
    user_input = fields.Char(string="User Input")
    right_answer = fields.Char(string="Answer", required=True)
    teacher_id = fields.Many2one(
        "teacher.detail", ondelete="cascade", string="Teacher", required=True
    )
    verified = fields.Boolean(string="verified", default=False)

    # @api.constrains("first_name", "last_name")
    # def _check_name(self):
    #     for record in self:
    #         if (
    #             record.option_1 == record.option_2
    #             or record.option_1 == record.option_3
    #             or record.option_1 == record.option_4
    #             or record.option_2 == record.option_3
    #             or record.option_2 == record.option_4
    #             or record.option_3 == record.option_4
    #         ):"Option must be different"))
