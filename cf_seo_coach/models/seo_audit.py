# Part of SEO Coach. Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. See LICENSE for details.
#
# Site-wide SEO audit: scan every published website page/post/product, score
# the on-page SEO and list the issues found. Field checks always run; a
# best-effort HTML fetch adds deep checks (H1, image alt, word count) when the
# page is reachable, and degrades silently when it is not.
import logging
import re

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

_AUDIT_MODELS = ('website.page', 'blog.post', 'product.template', 'event.event')
_SEVERITY_WEIGHT = {'error': 6, 'warning': 3, 'info': 1}
_TAG_RE = re.compile(r'<[^>]+>')


class CfSeoAudit(models.Model):
    _name = 'cf.seo.audit'
    _description = 'SEO Audit'
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(string='Audit', required=True,
                       default=lambda self: fields.Datetime.now())
    date = fields.Datetime(string='Run on', default=fields.Datetime.now)
    website_id = fields.Many2one('website', string='Website')
    pages_scanned = fields.Integer(string='Pages scanned')
    score = fields.Integer(string='Health score', help="0-100; higher is better.")
    issue_ids = fields.One2many('cf.seo.audit.issue', 'audit_id', string='Issues')
    issue_count = fields.Integer(compute='_compute_counts', store=True)
    error_count = fields.Integer(compute='_compute_counts', store=True)
    warning_count = fields.Integer(compute='_compute_counts', store=True)

    @api.depends('issue_ids', 'issue_ids.severity')
    def _compute_counts(self):
        for a in self:
            a.issue_count = len(a.issue_ids)
            a.error_count = len(a.issue_ids.filtered(lambda i: i.severity == 'error'))
            a.warning_count = len(a.issue_ids.filtered(lambda i: i.severity == 'warning'))

    # ── Crawl + score ───────────────────────────────────────────────────
    @api.model
    def _cf_auditable_records(self):
        recs = []
        for model_name in _AUDIT_MODELS:
            if model_name not in self.env:
                continue
            Model = self.env[model_name].sudo()
            if 'website_meta_title' not in Model._fields:
                continue
            domain = [('website_published', '=', True)] if \
                'website_published' in Model._fields else []
            recs += list(Model.search(domain, limit=2000))
        return recs

    @staticmethod
    def _cf_url(rec):
        for attr in ('website_url', 'url'):
            if attr in rec._fields and rec[attr]:
                return rec[attr]
        return ''

    def _cf_fetch_html(self, url):
        """Best-effort fetch of a public page for deep checks. Returns '' on
        any failure so the audit never breaks on an unreachable page."""
        try:
            import requests
            base = (self.website_id or self.env['website'].search([], limit=1)) \
                .sudo().get_base_url().rstrip('/')
            full = url if url.startswith('http') else base + (
                '' if url.startswith('/') else '/') + url
            resp = requests.get(full, timeout=8)
            return resp.text if resp.status_code == 200 else ''
        except Exception:  # noqa: BLE001
            return ''

    @api.model
    def action_run_audit(self):
        website = self.env['website'].get_current_website() or \
            self.env['website'].search([], limit=1)
        audit = self.create({
            'name': 'Audit %s' % fields.Datetime.now().strftime('%Y-%m-%d %H:%M'),
            'website_id': website.id,
        })
        recs = self._cf_auditable_records()
        Issue = self.env['cf.seo.audit.issue'].sudo()
        titles, descs = {}, {}
        issues = []

        def add(rec, url, name, check, severity, message):
            issues.append({
                'audit_id': audit.id, 'page_name': name, 'page_url': url,
                'check': check, 'severity': severity, 'message': message,
            })

        for rec in recs:
            url = self._cf_url(rec)
            name = rec.display_name or url or 'Page'
            mt = (rec.website_meta_title or '').strip()
            md = (rec.website_meta_description or '').strip()
            # ── meta title
            if not mt:
                add(rec, url, name, 'meta_title_missing', 'error', 'Missing meta title')
            elif len(mt) < 30:
                add(rec, url, name, 'meta_title_short', 'warning',
                    'Meta title is short (%d chars; aim for 30-60)' % len(mt))
            elif len(mt) > 60:
                add(rec, url, name, 'meta_title_long', 'warning',
                    'Meta title is long (%d chars; aim for 30-60)' % len(mt))
            # ── meta description
            if not md:
                add(rec, url, name, 'meta_desc_missing', 'error', 'Missing meta description')
            elif len(md) < 70:
                add(rec, url, name, 'meta_desc_short', 'warning',
                    'Meta description is short (%d chars; aim for 70-160)' % len(md))
            elif len(md) > 160:
                add(rec, url, name, 'meta_desc_long', 'warning',
                    'Meta description is long (%d chars; aim for 70-160)' % len(md))
            # ── focus keyphrase (SEO Coach)
            if 'cf_seo_keyphrase' in rec._fields and not (rec.cf_seo_keyphrase or '').strip():
                add(rec, url, name, 'keyphrase_missing', 'info', 'No focus keyphrase set')
            # ── no-index
            if rec._fields.get('cf_robots_noindex') and rec.cf_robots_noindex:
                add(rec, url, name, 'noindex', 'info', 'Page is set to no-index')
            # ── duplicates bookkeeping
            if mt:
                titles.setdefault(mt.lower(), []).append((rec, url, name))
            if md:
                descs.setdefault(md.lower(), []).append((rec, url, name))
            # ── deep checks (best effort)
            html = self._cf_fetch_html(url) if url else ''
            if html:
                body = html
                h1 = len(re.findall(r'<h1[\s>]', body, re.I))
                if h1 == 0:
                    add(rec, url, name, 'h1_missing', 'error', 'No <h1> heading on the page')
                elif h1 > 1:
                    add(rec, url, name, 'h1_multiple', 'warning',
                        'Multiple <h1> headings (%d) on the page' % h1)
                imgs = re.findall(r'<img\b[^>]*>', body, re.I)
                no_alt = [i for i in imgs if not re.search(r'\balt\s*=\s*["\'][^"\']', i, re.I)]
                if no_alt:
                    add(rec, url, name, 'img_alt', 'warning',
                        '%d image(s) missing alt text' % len(no_alt))
                text = _TAG_RE.sub(' ', re.sub(r'(?is)<(script|style).*?</\1>', ' ', body))
                words = len(text.split())
                if words < 300:
                    add(rec, url, name, 'thin_content', 'info',
                        'Thin content (~%d words; aim for 300+)' % words)

        for title, group in titles.items():
            if len(group) > 1:
                for rec, url, name in group:
                    add(rec, url, name, 'meta_title_dup', 'warning',
                        'Duplicate meta title (shared by %d pages)' % len(group))
        for desc, group in descs.items():
            if len(group) > 1:
                for rec, url, name in group:
                    add(rec, url, name, 'meta_desc_dup', 'warning',
                        'Duplicate meta description (shared by %d pages)' % len(group))

        if issues:
            Issue.create(issues)
        penalty = sum(_SEVERITY_WEIGHT.get(i['severity'], 1) for i in issues)
        max_penalty = max(len(recs) * 12, 1)
        score = max(0, round(100 - (penalty * 100.0 / max_penalty)))
        audit.write({'pages_scanned': len(recs), 'score': score})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cf.seo.audit', 'res_id': audit.id,
            'view_mode': 'form', 'target': 'current',
        }


class CfSeoAuditIssue(models.Model):
    _name = 'cf.seo.audit.issue'
    _description = 'SEO Audit Issue'
    _order = 'severity, page_name'

    audit_id = fields.Many2one('cf.seo.audit', string='Audit', required=True,
                               ondelete='cascade', index=True)
    page_name = fields.Char(string='Page')
    page_url = fields.Char(string='URL')
    check = fields.Char(string='Check')
    severity = fields.Selection(
        [('error', 'Error'), ('warning', 'Warning'), ('info', 'Info')],
        string='Severity', default='warning', index=True)
    message = fields.Char(string='Issue')
