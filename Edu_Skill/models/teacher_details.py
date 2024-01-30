from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date


class TeacherDetail(models.Model):
    _name = "teacher.detail"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Teacher Details"
    _rec_name = "first_name"

    first_name = fields.Char(
        string="First Name :",
        required=True,
        size=16,
        null=False,
        help="Enter  A First Name.",
    )
    last_name = fields.Char(
        string="Last Name",
        tracking=True,
        required=True,
        size=16,
    )
    age = fields.Integer(
        string="Age :",
        compute="_compute_age",
    )
    address = fields.Text(string="Address :", required=True)
    gender = fields.Selection(
        [("Male", "Male"), ("Female", "Female")], string="Gender", required=True
    )
    active = fields.Boolean(string="Active", default=True)
    birth_date = fields.Date(string="Birth Date :", required=True)
    email = fields.Char("Email :", required=True)
    phone_number = fields.Char("Phone Number :", required=True)
    course_count = fields.Integer(
        string="Course Count", compute="_compute_course_count"
    )
    qualification = fields.Char(string="Qualification :", required=True)
    description = fields.Text(string="Description :", required=True)
    image = fields.Image(string="Image")

    # Compute Age Of Using Enter A date of Birth
    @api.depends("birth_date")
    def _compute_age(self):
        for reference in self:
            today = date.today()
            if reference.birth_date:
                reference.age = today.year - reference.birth_date.year
            else:
                reference.age = 1

    # Count Course With Releted Teacher
    def _compute_course_count(self):
        for res in self:
            course_count = self.env["course.detail"].search_count(
                [("teacher_id", "=", res.id)]
            )
            res.course_count = course_count

    def action_open_course(self):
        if self.course_count == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Course",
                "res_model": "course.detail",
                "res_id": int(
                    self.env["course.detail"].search([("teacher_id", "=", self.id)])
                ),
                "domain": [("teacher_id", "=", self.id)],
                "view_mode": "form",
                "view_type": "form",
                "target": "current",
            }
        else:
            return {
                "name": "Course",
                "res_model": "course.detail",
                "view_mode": "list,form",
                "context": {},
                "domain": [("teacher_id", "=", self.id)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # Condition Check For First Name And Last Name Must Be different
    @api.constrains("first_name", "last_name")
    def _check_name(self):
        for record in self:
            if record.first_name == record.last_name:
                raise ValidationError("First Name and Last Name must be different")

    # Condition Check for Database Unique Email Id
    _sql_constraints = [("email_uniqe", "unique(email)", "Email must be unique.")]

    # Condition Check for Database Unique Phone Number
    _sql_constraints = [
        ("phone_number_uniqe", "unique(phone_number)", "Phone Number must be unique.")
    ]
