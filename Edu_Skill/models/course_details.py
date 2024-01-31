from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CourseDetails(models.Model):
    _name = "course.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Course Detail"

    teacher_id = fields.Many2one(
        "teacher.detail",
        ondelete="cascade",
        string="Teacher",
    )
    category_id = fields.Many2one(
        "category.detail", ondelete="cascade", string="Category"
    )
    teacher_last_name = fields.Char(string="Last Name", related="teacher_id.last_name")
    course_name = fields.Char(string="Course Name")
    course_upload_date = fields.Date(string="Upload Date", default=fields.Datetime.now)
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
    reference_no = fields.Char(
        string="Course Reference",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
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
    )
    video_count = fields.Integer(string="Video Count", compute="_compute_video_count")
    price = fields.Integer(
        "Price",
        null=False,
    )
    image = fields.Image(string="Course Image", required=True)

    # Action For Mode Of Course
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
        for res in self:  # Count Number Of Video In video.detail
            video_count = self.env["video.detail"].search_count(
                [("course_id", "=", res.id)]
            )  # Use OF Search Conut ORM Method
            res.video_count = video_count

    def action_open_course(self):
        if self.video_count == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Course",
                "res_model": "video.detail",
                "res_id": int(
                    self.env["video.detail"].search([("course_id", "=", self.id)])
                ),  # Use OF Search ORM Method
                "domain": [("course_id", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }
        else:
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
    ]

    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "course.detail"
            ) or _("New")
        res = super(CourseDetails, self).create(vals)
        return res

    @api.model
    def create(self, vals):
        res = super(CourseDetails, self).create(
            {"language": "english", "level": "beginner", "state": "draft"}
        )
        return res

    def name_get(self):
        res = []
        for rec in self:
            res.append(
                (
                    rec.id,
                    "%s, %s" % (rec.category_id,),
                )
            )
        return res

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
                ("teacher_id", operator, name),
                ("teacher_last_name", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
