# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

MAX_ATTACHMENT_SIZE = 2 * 1024 * 1024  # 2 MB in bytes


class FaqQuestion(models.Model):
    _name = 'faq.question'
    _description = 'FAQ Question'
    _inherit = []
    _order = 'sequence, id'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------
    name = fields.Char(
        string='Question',
        required=True,
        translate=True,
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

    # ---- Attachments ----
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='faq_question_attachment_rel',
        column1='question_id',
        column2='attachment_id',
        string='Attachments',
    )
    attachment_count = fields.Integer(
        string='Attachments',
        compute='_compute_attachment_count',
    )


    # -------------------------------------------------------------------------
    # Computed
    # -------------------------------------------------------------------------
    @api.depends('state')
    def _compute_website_published(self):
        for rec in self:
            rec.website_published = rec.state == 'published'

    @api.depends('attachment_ids')
    def _compute_attachment_count(self):
        for rec in self:
            rec.attachment_count = len(rec.attachment_ids)

    # -------------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------------
    @api.constrains('attachment_ids')
    def _check_attachment_size(self):
        for rec in self:
            for attachment in rec.attachment_ids:
                if attachment.file_size and attachment.file_size > MAX_ATTACHMENT_SIZE:
                    size_mb = attachment.file_size / (1024 * 1024)
                    raise ValidationError(
                        f'Attachment "{attachment.name}" is {size_mb:.1f} MB. '
                        f'Maximum allowed size is 2 MB per file.'
                    )

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
