# Part of SEO Coach. Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. See LICENSE for details.
import json

from markupsafe import Markup

from odoo import api, fields, models
from odoo.http import request


class WebsiteSeoMetadata(models.AbstractModel):
    """Add the SEO Coach fields to Odoo's shared SEO base. Every website
    record type that can be optimised (static pages, blog posts, products,
    events, courses, forum, jobs...) inherits ``website.seo.metadata``, so a
    single definition here gives all of them the same SEO capabilities.

    Note: static pages (``website.page``) inherit this base only by *field*
    delegation through ``ir.ui.view`` (``_inherits``), which forwards fields
    but NOT methods. Everything the page <head> needs is therefore exposed as
    a (computed) *field*, never a method, so it works on every page type."""
    _inherit = 'website.seo.metadata'

    # ── Focus keyphrase + content flags ─────────────────────────────────
    cf_seo_keyphrase = fields.Char(
        string='Focus keyphrase',
        help="The main search phrase this page should rank for. The SEO Coach "
             "analyses the page against this phrase.")
    cf_seo_related_keyphrases = fields.Char(
        string='Related keyphrases',
        help="Extra phrases (comma-separated) the page should also mention. "
             "The SEO Coach checks each one appears in the content.")
    cf_is_cornerstone = fields.Boolean(
        string='Cornerstone content',
        help="Mark pillar pages. Cornerstone content is held to a higher "
             "word-count target in the analysis.")

    # ── Social (Facebook / X) ───────────────────────────────────────────
    cf_social_title = fields.Char(
        string='Social title',
        help="Title used when the page is shared (Facebook / X). "
             "Defaults to the SEO title.")
    cf_social_description = fields.Text(
        string='Social description',
        help="Description used when shared. Defaults to the meta description.")
    cf_social_image = fields.Char(
        string='Social image',
        help="Image shown when shared, e.g. /web/image/... or a full URL.")

    # ── Schema (JSON-LD) ────────────────────────────────────────────────
    cf_schema_jsonld = fields.Text(
        string='Schema (JSON-LD)',
        help="Structured data for this page. Paste a single JSON-LD object or "
             "an array of objects. Each is rendered as a "
             '<script type="application/ld+json"> in the page <head>.')
    cf_schema_head = fields.Html(
        string='Schema (rendered)', compute='_compute_cf_schema_head',
        sanitize=False,
        help="Rendered <script> markup for the page head (internal).")

    # ── Advanced: canonical + robots ────────────────────────────────────
    cf_canonical_url = fields.Char(
        string='Canonical URL',
        help="Override the canonical link for this page (e.g. point a "
             "duplicate to the original). Leave empty to use the default URL.")
    cf_robots_noindex = fields.Boolean(
        string='No index',
        help="Ask search engines NOT to show this page in results.")
    cf_robots_nofollow = fields.Boolean(
        string='No follow',
        help="Ask search engines not to follow links from this page.")
    cf_robots_noarchive = fields.Boolean(string='No archive (no cached copy)')
    cf_robots_nosnippet = fields.Boolean(string='No snippet')
    cf_robots_noimageindex = fields.Boolean(string='No image index')
    cf_robots_content = fields.Char(
        string='Robots directive', compute='_compute_cf_robots_content',
        help="The <meta name=robots> directive string for the page head "
             "(internal); empty when everything is default.")

    # ── Computed render helpers (fields, so static pages inherit them) ───
    @api.depends('cf_robots_noindex', 'cf_robots_nofollow', 'cf_robots_noarchive',
                 'cf_robots_nosnippet', 'cf_robots_noimageindex')
    def _compute_cf_robots_content(self):
        for rec in self:
            flags = (rec.cf_robots_noindex or rec.cf_robots_nofollow
                     or rec.cf_robots_noarchive or rec.cf_robots_nosnippet
                     or rec.cf_robots_noimageindex)
            if not flags:
                rec.cf_robots_content = ''
                continue
            parts = [
                'noindex' if rec.cf_robots_noindex else 'index',
                'nofollow' if rec.cf_robots_nofollow else 'follow',
            ]
            if rec.cf_robots_noarchive:
                parts.append('noarchive')
            if rec.cf_robots_nosnippet:
                parts.append('nosnippet')
            if rec.cf_robots_noimageindex:
                parts.append('noimageindex')
            rec.cf_robots_content = ', '.join(parts)

    @api.depends('cf_schema_jsonld')
    def _compute_cf_schema_head(self):
        for rec in self:
            raw = (rec.cf_schema_jsonld or '').strip()
            if not raw:
                rec.cf_schema_head = False
                continue
            try:
                data = json.loads(raw)
            except (ValueError, TypeError):
                data = None
            if isinstance(data, dict) and isinstance(data.get('cf_blocks'), list):
                # SEO Coach multi-block format: one <script> per named block.
                parts = []
                for b in data['cf_blocks']:
                    js = (b.get('json') or '').strip() if isinstance(b, dict) else ''
                    if not js:
                        continue
                    try:
                        parts.append('<script type="application/ld+json">%s</script>'
                                     % json.dumps(json.loads(js)))
                    except (ValueError, TypeError):
                        parts.append('<script type="application/ld+json">%s</script>' % js)
                out = ''.join(parts)
            elif data is not None:
                # legacy: a single raw JSON-LD object or an array of them.
                blocks = data if isinstance(data, list) else [data]
                out = ''.join(
                    '<script type="application/ld+json">%s</script>' % json.dumps(b)
                    for b in blocks
                )
            else:
                # not valid JSON: the user may have pasted full <script> tags;
                # emit as-is so nothing is silently dropped.
                out = raw if '<script' in raw.lower() else \
                    '<script type="application/ld+json">%s</script>' % raw
            rec.cf_schema_head = Markup(out) if out else False

    def get_website_meta(self):
        """Let the social fields override the OpenGraph / Twitter tags on page
        types that inherit this base directly (blog posts, products, events...)."""
        res = super().get_website_meta()
        og = res.get('opengraph_meta') or {}
        tw = res.get('twitter_meta') or {}
        if self.cf_social_title:
            og['og:title'] = self.cf_social_title
            tw['twitter:title'] = self.cf_social_title
        if self.cf_social_description:
            og['og:description'] = self.cf_social_description
            tw['twitter:description'] = self.cf_social_description
        if self.cf_social_image:
            img = self.cf_social_image
            if not img.startswith('http'):
                root = (request.website.domain or request.httprequest.url_root).rstrip('/')
                img = root + ('' if img.startswith('/') else '/') + img
            og['og:image'] = img
            tw['twitter:image'] = img
        return res
