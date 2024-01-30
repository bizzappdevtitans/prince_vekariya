from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QuizQuestion(models.Model):
    _name = "quiz.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Quiz Detail"
    video_caption = "course_name"

    course_id = fields.Many2one(
        "course.detail", ondelete="cascade", string="Course Name"
    )
    teacher_id = fields.Many2one(string="Teacher Name", related="course_id.teacher_id")
    question = fields.Char(string="Question", required=True)
    option_1 = fields.Char(string="Option 1", required=True)
    option_2 = fields.Char(string="Option 2", required=True)
    option_3 = fields.Char(string="Option 3")
    option_4 = fields.Char(string="Option 4")
    right_answer = fields.Char(string="Answer", required=True)
    verified = fields.Boolean(string="verified", default=False)

    # Condition Check For Option Can Be Different
    @api.constrains("option_1", "option_2", "option_3", "option_4")
    def _check_option(self):
        for record in self:
            if (
                record.option_1 == record.option_2
                or record.option_1 == record.option_3
                or record.option_1 == record.option_4
                or record.option_2 == record.option_3
                or record.option_2 == record.option_4
                or record.option_3 == record.option_4
            ):
                raise ValidationError("Option must be different")
