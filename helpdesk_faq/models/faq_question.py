# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class FaqQuestion(models.Model):
    _name = 'faq.question'
    _description = 'FAQ Question'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------
    name = fields.Char(
        string='Question',
        required=True,
        translate=True,
        tracking=True,
    )
    answer = fields.Html(
        string='Answer',
        required=True,
        translate=True,
        sanitize=True,
    )
    category_id = fields.Many2one(
        comodel_name='faq.category',
        string='Category',
        required=True,
        ondelete='restrict',
        tracking=True,
        index=True,
    )
    tag_ids = fields.Many2many(
        comodel_name='faq.tag',
        relation='faq_question_tag_rel',
        column1='question_id',
        column2='tag_id',
        string='Tags',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('published', 'Published'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        index=True,
    )
    helpful_count = fields.Integer(
        string='Helpful Votes',
        default=0,
        readonly=True,
    )
    not_helpful_count = fields.Integer(
        string='Not Helpful Votes',
        default=0,
        readonly=True,
    )
    website_published = fields.Boolean(
        string='Visible on Website',
        compute='_compute_website_published',
        store=True,
    )

    # -------------------------------------------------------------------------
    # Computed
    # -------------------------------------------------------------------------
    @api.depends('state')
    def _compute_website_published(self):
        for rec in self:
            rec.website_published = rec.state == 'published'

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------
    def action_publish(self):
        for rec in self:
            if not rec.answer:
                raise UserError(
                    f'Cannot publish "{rec.name}" without an answer.'
                )
            rec.state = 'published'

    def action_unpublish(self):
        self.write({'state': 'draft'})

    def action_toggle_helpful(self):
        """Increment helpful counter — called from website controller."""
        self.ensure_one()
        self.sudo().helpful_count += 1

    def action_toggle_not_helpful(self):
        """Increment not-helpful counter — called from website controller."""
        self.ensure_one()
        self.sudo().not_helpful_count += 1

    # -------------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------------
    _sql_constraints = [
        (
            'name_category_unique',
            'UNIQUE(name, category_id)',
            'A question with the same text already exists in this category.',
        )
    ]
