from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    allowed_category = fields.Integer(
        string="Allowed Category",
        config_parameter="allowed_category",
    )
    unsplash_access_key = fields.Integer()
