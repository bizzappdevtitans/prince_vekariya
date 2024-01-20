from odoo import api, fields, models


class CategoryDetails(models.Model):
    _name = "category.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Category Detail"
    _rec_name = "category_name"

    category_name = fields.Char("Category Name")
    category_image = fields.Image("Cetegory Image")
    category_upload_date = fields.Date("Upload Date")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_process", "In Process"),
            ("cancle", "cancle"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        required=True,
    )
