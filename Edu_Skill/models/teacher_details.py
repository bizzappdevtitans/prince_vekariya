from odoo import api, fields, models
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
    course_count = fields.Integer(
        string="Course Count", compute="_compute_course_count"
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

    def action_teacher_detail(self):
        print("Teacher Button clicked")

    def _compute_course_count(self):
        for res in self:
            course_count = self.env["course.detail"].search_count(
                [("teacher_id", "=", res.id)]
            )
            res.course_count = course_count

    def action_open_course(self):
        return {
            "name": "Course",
            "res_model": "course.detail",
            "view_mode": "list,form",
            "context": {},
            "domain": [("teacher_id", "=", self.id)],
            "target": "current",
            "type": "ir.actions.act_window",
        }
