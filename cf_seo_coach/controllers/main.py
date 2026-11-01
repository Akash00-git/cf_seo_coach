# Part of SEO Coach. Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. See LICENSE for details.
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SeoCoachLlms(http.Controller):
    """Serve /llms.txt — a plain-text map of the site's pages for AI search
    engines (ChatGPT, Perplexity, Gemini). Opt-in per website; returns 404
    when disabled. Every section is defensive so a missing model or field can
    never 500 the route."""

    @http.route('/llms.txt', type='http', auth='public', website=True, sitemap=False)
    def llms_txt(self, **kw):
        website = request.website
        if not website or not website.cf_llms_txt_enabled:
            return request.not_found()

        base = (website.get_base_url() or '').rstrip('/')
        lines = ['# %s' % (website.name or 'Website'), '']

        intro = (website.cf_llms_txt_intro or '').strip()
        if intro:
            lines.append('> %s' % ' '.join(intro.split()))
            lines.append('')

        def link(title, url):
            if not url:
                return None
            if not url.startswith(('http://', 'https://')):
                url = base + (url if url.startswith('/') else '/' + url)
            return '- [%s](%s)' % ((title or url).strip(), url)

        def section(header, model_name, domain, title_field='name'):
            if model_name not in request.env:
                return
            try:
                recs = request.env[model_name].sudo().search(domain, limit=2000)
            except Exception as err:  # noqa: BLE001 - never break the route
                _logger.warning("llms.txt: skipped %s (%s)", model_name, err)
                return
            rows = []
            for rec in recs:
                try:
                    if 'website_url' in rec._fields:
                        url = rec.website_url
                    else:
                        url = rec.url if 'url' in rec._fields else None
                    row = link(rec[title_field] if title_field in rec._fields else None, url)
                    if row:
                        rows.append(row)
                except Exception:  # noqa: BLE001
                    continue
            if rows:
                lines.append('## %s' % header)
                lines.extend(sorted(set(rows)))
                lines.append('')

        pub = [('is_published', '=', True)]
        section('Pages', 'website.page', pub + [('website_id', 'in', [False, website.id])])
        section('Blog', 'blog.post', pub)
        section('Products', 'product.template', pub)
        section('Events', 'event.event', [('website_published', '=', True)])

        body = '\n'.join(lines).rstrip() + '\n'
        return request.make_response(
            body, headers=[('Content-Type', 'text/plain; charset=utf-8')])
