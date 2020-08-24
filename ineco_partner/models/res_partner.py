import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "ข้อมูล res.partner"

    # branch_no = fields.Char(string="ลำดับสาขา", track_visibility="onchange")
    with_holding_tax_type = fields.Selection(
        [("pp4", "ภงด 3"), ("pp7", "ภงด 53")],
        string="ประเภทภาษีหัก ณ ที่จ่าย",
        index=True,
        track_visibility="onchange",
    )
    cheque_payment_id = fields.Many2one(
        "account.payment.term",
        string="เงื่อนไขรับชำระ (รับเช็ค)",
        index=True,
        track_visibility="onchange",
    )
    billing_payment_id = fields.Many2one(
        "account.payment.term",
        string="เงื่อนไขการวางบิล",
        index=True,
        track_visibility="onchange",
    )
    name2 = fields.Char(string="Name Other", index=True, track_visibility="onchange")
    name_short = fields.Char(string="Short Name", track_visibility="onchange")

    # กรมสรรพากร
    th_vat_no = fields.Char(
        string="เลขประจำตัวผู้เสียภาษี", size=13, track_visibility="onchange"
    )
    th_branch_no = fields.Char(string="ลำดับสาขา", size=5, track_visibility="onchange")
    th_title = fields.Char(string="คำนำหน้า", size=40, track_visibility="onchange")
    th_firstname = fields.Char(string="ชื่อ", size=100, track_visibility="onchange")
    th_lastname = fields.Char(string="นามสกุล", size=80, track_visibility="onchange")
    th_home_no = fields.Char(string="บ้านเลขที่", size=20, track_visibility="onchange")
    th_moo = fields.Char(string="หมู่", size=2, track_visibility="onchange")
    th_soi = fields.Char(string="ซอย", size=30, track_visibility="onchange")
    th_street = fields.Char(string="ถนน", size=30, track_visibility="onchange")
    th_tambon = fields.Char(string="ตำบล/แขวง", size=30, track_visibility="onchange")
    th_amphur = fields.Char(string="อำเภอ/เขต", size=30, track_visibility="onchange")
    th_province = fields.Char(string="จังหวัด", size=40, track_visibility="onchange")
    th_zip = fields.Char(string="รหัสไปรษณีย์", size=5, track_visibility="onchange")

    def _do_something(self):
        _logger(_("Hello Guy"))

    @api.onchange("company_type")
    def onchange_company_type(self):
        self.is_company = self.company_type == "company"
        if self.is_company:
            self.with_holding_tax_type = "pp7"
        else:
            self.with_holding_tax_type = "pp4"

    @api.onchange("th_title")
    def onchange_th_title(self):
        if not self.is_company:
            self.name = "{}{} {}".format(
                self.th_title, self.th_firstname, self.th_lastname
            )

    @api.onchange("th_firstname")
    def onchange_th_firstname(self):
        if not self.is_company:
            self.name = "{}{} {}".format(
                self.th_title, self.th_firstname, self.th_lastname
            )

    @api.onchange("th_lastname")
    def onchange_th_lastname(self):
        if not self.is_company:
            self.name = "{}{} {}".format(
                self.th_title, self.th_firstname, self.th_lastname
            )

    @api.onchange("th_province")
    def onchange_th_province(self):
        if self.th_province:
            self.city = self.th_province

    @api.onchange("th_zip")
    def onchange_th_zip(self):
        if self.th_zip:
            self.zip = self.th_zip

    @api.onchange("th_vat_no")
    def onchange_th_vat_no(self):
        if self.th_vat_no:
            self.vat = self.th_vat_no

    @api.onchange("th_tambon")
    def onchange_th_tambon(self):
        self.street2 = "{} {}".format(self.th_tambon or "", self.th_amphur or "")

    @api.onchange("th_amphur")
    def onchange_th_amphur(self):
        self.street2 = "{} {}".format(self.th_tambon or "", self.th_amphur or "")

    @api.onchange("th_home_no")
    def onchange_th_home_no(self):
        moo_name = ""
        if self.th_moo:
            moo_name = "หมู่ {}".format(self.th_moo)
        self.street = "{} {} {} {}".format(
            self.th_home_no or "", moo_name, self.th_soi or "", self.th_street or ""
        ).replace("  ", " ")

    @api.onchange("th_moo")
    def onchange_th_moo(self):
        moo_name = ""
        if self.th_moo:
            moo_name = "หมู่ {}".format(self.th_moo)
        self.street = "{} {} {} {}".format(
            self.th_home_no or "", moo_name, self.th_soi or "", self.th_street or ""
        ).replace("  ", " ")

    @api.onchange("th_soi")
    def onchange_th_soi(self):
        moo_name = ""
        if self.th_moo:
            moo_name = "หมู่ {}".format(self.th_moo)
        self.street = "{} {} {} {}".format(
            self.th_home_no or "", moo_name, self.th_soi or "", self.th_street or ""
        ).replace("  ", " ")

    @api.onchange("th_street")
    def onchange_th_street(self):
        moo_name = ""
        if self.th_moo:
            moo_name = "หมู่ {}".format(self.th_moo)
        self.street = "{} {} {} {}".format(
            self.th_home_no or "", moo_name, self.th_soi or "", self.th_street or ""
        ).replace("  ", " ")
