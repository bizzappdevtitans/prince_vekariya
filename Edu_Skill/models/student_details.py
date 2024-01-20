from odoo import api, fields, models
from datetime import date


class StudentDetail(models.Model):
    _name = "student.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Details"
    _rec_name = "first_name"

    first_name = fields.Char(
        string="First Name :",
        required=True,
        size=16,
        null=False,
    )
    last_name = fields.Char(
        string="Last Name",
        tracking=True,
        required=True,
        size=16,
    )
    age = fields.Integer(string="Age :", compute="_compute_age")
    address = fields.Text(string="Address :", required=True)
    gender = fields.Selection(
        [("Male", "Male"), ("Female", "Female")], string="Gender", required=True
    )
    active = fields.Boolean(string="Active", default=True)
    birth_date = fields.Date(string="Birth Date :", required=True)
    email = fields.Char("Email :", required=True)
    phone_number = fields.Char("Phone Number :", required=True)
    graduation = fields.Selection(
        [
            ("10th", "10th"),
            ("12th", "12th"),
            ("bachelor", "bachelor"),
            ("Master", "Master"),
        ],
        string="Graduation",
        required=True,
    )
    qualification = fields.Char(string="Qualification :", required=True)
    image = fields.Image(string="Image")

    @api.depends("birth_date")
    def _compute_age(self):
        for reference in self:
            today = date.today()
            if reference.birth_date:
                reference.age = today.year - reference.birth_date.year
            else:
                reference.age = 1
