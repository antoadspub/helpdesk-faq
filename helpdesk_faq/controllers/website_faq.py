# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteFaq(http.Controller):

    @http.route('/faq', type='http', auth='public', website=True)
    def faq_index(self, search='', category_id=None, **kwargs):
        """Public FAQ listing page."""
        FaqQuestion = request.env['faq.question'].sudo()
        FaqCategory = request.env['faq.category'].sudo()

        domain = [('state', '=', 'published')]

        if search:
            domain += [
                '|',
                ('name', 'ilike', search),
                ('answer', 'ilike', search),
            ]

        if category_id:
            domain += [('category_id', '=', int(category_id))]

        questions = FaqQuestion.search(domain, order='sequence, id')
        categories = FaqCategory.search([
            ('question_ids.state', '=', 'published')
        ])

        selected_category = None
        if category_id:
            selected_category = FaqCategory.browse(int(category_id)).exists()

        values = {
            'questions': questions,
            'categories': categories,
            'search': search,
            'selected_category': selected_category,
        }
        return request.render('helpdesk_faq.website_faq_index', values)

    @http.route('/faq/<int:question_id>', type='http', auth='public', website=True)
    def faq_detail(self, question_id, **kwargs):
        """Public FAQ detail page."""
        question = request.env['faq.question'].sudo().browse(question_id)
        if not question.exists() or question.state != 'published':
            return request.not_found()

        related = request.env['faq.question'].sudo().search([
            ('category_id', '=', question.category_id.id),
            ('state', '=', 'published'),
            ('id', '!=', question.id),
        ], limit=5)

        values = {
            'question': question,
            'related': related,
        }
        return request.render('helpdesk_faq.website_faq_detail', values)

    @http.route('/faq/<int:question_id>/vote', type='json', auth='public', website=True)
    def faq_vote(self, question_id, helpful=True, **kwargs):
        """Ajax vote endpoint."""
        question = request.env['faq.question'].sudo().browse(question_id)
        if not question.exists() or question.state != 'published':
            return {'error': 'Not found'}
        if helpful:
            question.action_toggle_helpful()
        else:
            question.action_toggle_not_helpful()
        return {
            'helpful_count': question.helpful_count,
            'not_helpful_count': question.not_helpful_count,
        }
