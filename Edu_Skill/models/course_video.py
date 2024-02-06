from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class VideoDetails(models.Model):
    _name = "video.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Video Detail"
    _rec_name = "course_id"

    course_id = fields.Many2one("course.detail", ondelete="cascade", string="Course")
    series_number = fields.Integer(string="Series Numbers", null=False)
    video_caption = fields.Char(string="Caption", null=False)
    image = fields.Binary("Images", null=False)
    video = fields.Binary("Videos", null=False)
    description = fields.Html(string="Video Description", null=False)
    preview = fields.Boolean(string="Previews", default=False)
    time_duration = fields.Char(string="Time Durations", null=False)
    reference_no = fields.Char(
        string="Course Video Reference",
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

    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "video.detail"
            ) or _("New")
        res = super(VideoDetails, self).create(vals)
        return res

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "video_caption" in vals and vals["video_caption"]:
            vals["video_caption"] = vals["video_caption"].capitalize()
            return super(VideoDetails, self).write(vals)

    # get Name of record Of Using name_get ORM Method
    def name_get(self):
        response = []
        for record in self:
            response.append(
                (
                    record.id,
                    "%s: %s , %s"
                    % (
                        record.series_number,
                        record.video_caption,
                        record.course_id.course_name,
                    ),
                )
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
                ("series_number", operator, name),
                ("video_caption", operator, name),
                ("course_id", operator, name),
                ("reference_no", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for state is Draft And Cancel then
    # Delete
    def unlink(self):
        for states in self:
            if states.state not in ("draft", "cancel"):
                raise ValidationError(
                    _("You cannot delete an Category which is not draft or cancelled. ")
                )
        return super(VideoDetails, self).unlink()

    # Using search_read method can Check state is Draft amd in Process,done
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            "|",
            ("state", "ilike", "draft"),
            ("state", "ilike", "in_process"),
            ("state", "ilike", "done"),
        ]
        return super(VideoDetails, self).search_read(
            domain, fields, offset, limit, order
        )
