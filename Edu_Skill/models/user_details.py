from datetime import date

from odoo import _, api, fields, models
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
        string="Last Name :",
        tracking=True,
        required=True,
        size=16,
    )
    password = fields.Char(string="Passwords", required=True)
    age = fields.Integer(
        string="Age :",
        # compute="_compute_age",
    )
    address = fields.Text(string="Address :", required=True)
    gender = fields.Selection(
        [("Male", "Male"), ("Female", "Female")], string="Gender : ", required=True
    )
    active = fields.Boolean(string="Active :", default=True)
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
        string="Graduation :",
        required=True,
    )
    reference_no = fields.Char(
        string="User Reference",
        required=True,
        readonly=True,
        default=lambda self: _("New"),
    )
    qualification = fields.Char(string="Qualification :", required=True)
    description = fields.Text(string="Description :", required=True)
    image = fields.Image(string="Images")

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
                raise ValidationError(_("First Name and Last Name must be different"))

    _sql_constraints = [("email_uniqe", "unique(email)", "Email must be unique.")]

    _sql_constraints = [
        ("phone_number_uniqe", "unique(phone_number)", "Phone Number must be unique.")
    ]

    # Calculate Age Using Date Of Birth.
    # @api.onchange("birth_date")
    # def _compute_age(self):
    #     for reference in self:
    #         today = date.today()
    #         if reference.birth_date:
    #             reference.age = today.year - reference.birth_date.year
    #         else:
    #             reference.age = 1

    # Generate Sequence Using Create ORM Method
    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "user.detail"
            ) or _("New")
        res = super(UserDetail, self).create(vals)
        return res

    # get Name of record Of Using name_get ORM Method
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s %s" % (rec.first_name, rec.last_name)))
        return res

    def write(self, vals):  # Using Write Orm First Leter Can be Capital
        if "qualification" in vals and vals["qualification"]:
            vals["qualification"] = vals["qualification"].upper()
            return super(UserDetail, self).write(vals)

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
                "|",
                "|",
                "|",
                ("first_name", operator, name),
                ("last_name", operator, name),
                ("email", operator, name),
                ("phone_number", operator, name),
                ("graduation", operator, name),
                ("reference_no", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # In Using Unlink ORM Method Condtion Check for state is Draft And Cancel then
    # Delete
    def unlink(self):
        for states in self:
            if states.active not in ("False"):
                raise ValidationError(_("You cannot delete an User which is Active. "))
        return super(UserDetail, self).unlink()

    # Using search_read method can Check active is Draft amd in False,True
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            ("active", "ilike", "False"),
            ("active", "ilike", "True"),
        ]
        return super(UserDetail, self).search_read(domain, fields, offset, limit, order)
