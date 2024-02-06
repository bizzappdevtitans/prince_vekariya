from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    allowed_category = fields.Integer(
        string="Allowed Categorys",
        config_parameter="allowed_category",
    )
    allowed_course = fields.Integer(
        string="Allowed Courses",
        config_parameter="allowed_course",
    )
    unsplash_access_key = fields.Integer()
