# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FaqCategory(models.Model):
    _name = 'faq.category'
    _description = 'FAQ Category'
    _order = 'sequence, name'

    name = fields.Char(
        string='Category Name',
        required=True,
        translate=True,
    )
    description = fields.Text(
        string='Description',
        translate=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    color = fields.Integer(
        string='Color Index',
        default=0,
    )
    question_ids = fields.One2many(
        comodel_name='faq.question',
        inverse_name='category_id',
        string='Questions',
    )
    question_count = fields.Integer(
        string='Questions Count',
        compute='_compute_question_count',
        store=True,
    )
    published_question_count = fields.Integer(
        string='Published Questions',
        compute='_compute_question_count',
        store=True,
    )

    @api.depends('question_ids', 'question_ids.state')
    def _compute_question_count(self):
        for rec in self:
            rec.question_count = len(rec.question_ids)
            rec.published_question_count = len(
                rec.question_ids.filtered(lambda q: q.state == 'published')
            )

    def action_view_questions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'FAQ - {self.name}',
            'res_model': 'faq.question',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }
