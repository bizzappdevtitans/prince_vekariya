from odoo import api, fields, models


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
