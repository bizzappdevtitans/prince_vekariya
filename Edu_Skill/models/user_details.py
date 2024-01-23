from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError


class UserDetail(models.Model):
    _name = "user.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Teacher Details"
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
    password = fields.Char(string="password", required=True)
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
    description = fields.Text(string="Description :", required=True)
    image = fields.Image(string="Image")

    @api.depends("birth_date")
    def _compute_age(self):
        for reference in self:
            today = date.today()
            if reference.birth_date:
                reference.age = today.year - reference.birth_date.year
            else:
                reference.age = 1

    @api.constrains("first_name", "last_name")
    def _check_name(self):
        for record in self:
            if record.first_name == record.last_name:
                raise ValidationError("First Name and Last Name must be different")

    _sql_constraints = [("email_uniqe", "unique(email)", "Email must be unique.")]

    _sql_constraints = [
        ("phone_number_uniqe", "unique(phone_number)", "Phone Number must be unique.")
    ]

    @api.onchange("birth_date")
    def _compute_age(self):
        for reference in self:
            today = date.today()
            if reference.birth_date:
                reference.age = today.year - reference.birth_date.year
            else:
                reference.age = 1
