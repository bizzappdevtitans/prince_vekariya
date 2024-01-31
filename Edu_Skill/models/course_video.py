from odoo import api, fields, models, _


class VideoDetails(models.Model):
    _name = "video.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Video Detail"
    _rec_name = "course_id"

    course_id = fields.Many2one("course.detail", ondelete="cascade", string="Course")
    series_number = fields.Integer(string="Series Number", null=False)
    video_caption = fields.Char(string="Caption", null=False)
    image = fields.Binary("Image", null=False)
    video = fields.Binary("Video", null=False)
    description = fields.Html(string="Video Description", null=False)
    preview = fields.Boolean(string="Preview", default=False)
    time_duration = fields.Char(string="Time Duration", null=False)
    reference_no = fields.Char(
        string="Course Video Reference",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
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
