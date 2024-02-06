from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    total_right_answer = fields.Integer(string="Total Right Answers")
    total_wrong_answer = fields.Integer(string="Total Wrong Answers")
    question = fields.Many2one(
        "quiz.detail", string="Questions", ondelete="cascade", required=True
    )
    user_input = fields.Char(string="User Input : ")
    right_answer = fields.Char(string="Answer")
    percentge = fields.Float("percentges", default=0.0)
    verified = fields.Boolean(string="verifieds", default=False)
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

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "category_name" in vals and vals["category_name"]:
            vals["category_name"] = vals["category_name"].capitalize()
            return super(QuizResult, self).write(vals)

    # get Name of record Of Using name_get ORM Method
    def name_get(self):
        response = []
        for record in self:
            response.append(
                (record.id, "%s, %s" % (record.category_name, record.reference_no))
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
                "|",
                "|",
                ("course_id", operator, name),
                ("user_id", operator, name),
                ("user_last_name", operator, name),
                ("reference_no", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for verified is False
    def unlink(self):
        for states in self:
            if states.verified not in ("False"):
                raise ValidationError(
                    _("You cannot delete an Verified which is not Verified. ")
                )
        return super(QuizResult, self).unlink()

    # Using search_read method can Check state is verified amd in True,False
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            ("verified", "ilike", "True"),
            ("verified", "ilike", "False"),
        ]
        return super(QuizResult, self).search_read(domain, fields, offset, limit, order)
