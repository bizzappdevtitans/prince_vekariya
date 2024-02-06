from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CourseDetails(models.Model):
    _name = "course.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Course Detail"
    _rec_name = "course_name"

    teacher_id = fields.Many2one(
        "teacher.detail",
        ondelete="cascade",
        string="Teacher",
    )
    category_id = fields.Many2one(
        "category.detail", ondelete="cascade", string="Category"
    )
    teacher_last_name = fields.Char(string="Last Name", related="teacher_id.last_name")
    course_name = fields.Char(string="Course Name : ")
    course_upload_date = fields.Date(string="Upload Date", default=fields.Datetime.now)
    description = fields.Html(string="Description : ")

    level = fields.Selection(
        [
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
        ],
        string="Levels",
    )

    language = fields.Selection(
        [
            ("english", "English"),
        ],
        string="Languages",
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
    video_count = fields.Integer(string="Video Counts", compute="_compute_video_count")
    price = fields.Integer(
        "Prices",
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
        len_course_name = len(vals.get("course_name"))
        check_len = int(self.env["ir.config_parameter"].get_param("allowed_course"))
        if len_course_name <= check_len:
            raise ValidationError(_("You cannot Add an Course."))
        return res

    # Using name_get method pass Course name and category_name and first_name
    def name_get(self):
        res = []
        for rec in self:
            res.append(
                (
                    rec.id,
                    "%s, %s , %s %s"
                    % (
                        rec.course_name,
                        rec.category_id.category_name,
                        rec.teacher_id.first_name,
                        rec.teacher_last_name,
                    ),
                )
            )
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
                ("category_id", operator, name),
                ("teacher_last_name", operator, name),
                ("teacher_id", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "course_name" in vals and vals["course_name"]:
            vals["course_name"] = vals["course_name"].capitalize()
            return super(CourseDetails, self).write(vals)

    # In Using Unlink ORM Method Condtion Check for state is Draft And Cancel then
    # Delete
    def unlink(self):
        for states in self:
            if states.state not in ("draft", "cancel"):
                raise ValidationError(
                    _("You cannot delete an Course which is not draft or cancelled. ")
                )
        return super(CourseDetails, self).unlink()

    # Using search_read method can Check state and Level language
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            "|",
            "|",
            "|",
            "|",
            ("state", "ilike", "draft"),
            ("state", "ilike", "in_process"),
            ("state", "ilike", "done"),
            ("level", "ilike", "beginner"),
            ("level", "ilike", "intermediate"),
            ("language", "ilike", "english"),
        ]
        return super(CourseDetails, self).search_read(
            domain, fields, offset, limit, order
        )
