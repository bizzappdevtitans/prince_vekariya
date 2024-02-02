from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ReviewRattingDetails(models.Model):
    _name = "review.rating.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Review Ratting Detail"
    _rec_name = "course_name"

    course_name = fields.Many2one("course.detail", string="Course Name")
    user = fields.Many2one("user.detail", string="User Name")
    subject = fields.Char("Subject")
    review = fields.Text("Review")
    reference_no = fields.Char(
        string="Category Order Reference",
        required=True,
        default=lambda self: _("New"),
    )
    rating = fields.Float("Rating", required=True)
    status = fields.Boolean("Status", default=True)
    created_at = fields.Date("Date", default=fields.Datetime.now)

    # Condition Check For Subject And Review Must Be different
    @api.constrains("subject", "review")
    def _check_name(self):
        for record in self:
            if record.subject == record.review:
                raise ValidationError("Subject and Review must be different")

    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "teacher.detail"
            ) or _("New")
        res = super(ReviewRattingDetails, self).create(vals)
        return res

    # get Name of record Of Using name_get ORM Method
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s %s" % (rec.user, rec.course_name)))
        return res

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
                ("course_name", operator, name),
                ("user", operator, name),
                ("subject", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for state is Draft And Cancel then
    # Delete
    def unlink(self):
        for states in self:
            if states.status in ("True"):
                raise ValidationError(
                    _("You cannot delete an Ratting which is Active. ")
                )
        return super(ReviewRattingDetails, self).unlink()

    # Using search_read method can Check state is Draft amd in Process
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            "|",
            "|",
            "|",
            ("course_name", "ilike", "False"),
            ("user", "ilike", "True"),
            ("review", "ilike", "True"),
            ("subject", "ilike", "True"),
            ("rating", "ilike", "True"),
        ]
        return super(ReviewRattingDetails, self).search_read(
            domain, fields, offset, limit, order
        )
