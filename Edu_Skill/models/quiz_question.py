from odoo import api, fields, models, _
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
    reference_no = fields.Char(
        string="Quiz Question Reference",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
    )

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

    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "quiz.detail"
            ) or _("New")
        res = super(QuizQuestion, self).create(vals)
        return res

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "question" in vals and vals["question"]:
            vals["question"] = vals["question"].capitalize()
            return super(QuizQuestion, self).write(vals)

    # get Name of record Of Using name_get ORM Method
    def name_get(self):
        response = []
        for record in self:
            response.append(
                (record.id, "%s, %s" % (record.question, record.course_id.course_name))
            )
        return response

    # using name_search Method We Can Find Multipal Field Record
    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("question", operator, name),
                ("question", operator, name),
                ("course_name", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for verified is False Delete
    def unlink(self):
        for states in self:
            if states.verified not in ("False"):
                raise ValidationError(
                    _("You cannot delete an Verified which is not Verified. ")
                )
        return super(QuizQuestion, self).unlink()

    # Using search_read method can Check verified
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            ("verified", "ilike", "True"),
            ("verified", "ilike", "False"),
        ]
        return super(QuizQuestion, self).search_read(
            domain, fields, offset, limit, order
        )
