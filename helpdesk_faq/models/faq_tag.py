# -*- coding: utf-8 -*-
from odoo import models, fields


class FaqTag(models.Model):
    _name = 'faq.tag'
    _description = 'FAQ Tag'
    _order = 'name'

    name = fields.Char(
        string='Tag Name',
        required=True,
        translate=True,
    )
    color = fields.Integer(
        string='Color Index',
        default=0,
    )
    question_ids = fields.Many2many(
        comodel_name='faq.question',
        relation='faq_question_tag_rel',
        column1='tag_id',
        column2='question_id',
        string='Questions',
    )
    question_count = fields.Integer(
        string='Questions Count',
        compute='_compute_question_count',
    )

    def _compute_question_count(self):
        for rec in self:
            rec.question_count = len(rec.question_ids)
