# Part of SEO Coach. Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. See LICENSE for details.
import json

from markupsafe import Markup

from odoo import fields, models


class Website(models.Model):
    """Per-website SEO Coach settings: analytics injection, llms.txt for AI
    search engines, SEO hardening toggles, and auto JSON-LD schema. All opt-in
    and website-scoped so nothing changes until the admin turns it on."""
    _inherit = 'website'

    # ── Analytics injection (Google Tag Manager / GA4) ──────────────────
    cf_gtm_container_id = fields.Char(
        string='Google Tag Manager ID',
        help="Your GTM container id, e.g. GTM-XXXXXXX. Leave empty to disable.")
    cf_ga4_measurement_id = fields.Char(
        string='GA4 Measurement ID',
        help="Your Google Analytics 4 id, e.g. G-XXXXXXXXXX. Leave empty to disable.")

    # ── llms.txt (AI search / GEO) ──────────────────────────────────────
    cf_llms_txt_enabled = fields.Boolean(
        string='Publish /llms.txt',
        help="Serve an /llms.txt file listing your pages so AI search engines "
             "(ChatGPT, Perplexity, Gemini) can discover your content.")
    cf_llms_txt_intro = fields.Text(
        string='llms.txt intro',
        help="Optional description of your site, written at the top of /llms.txt.")

    # ── SEO hardening ───────────────────────────────────────────────────
    cf_harden_queryparams = fields.Boolean(
        string='No-index filtered URLs',
        help="Add a noindex tag to URLs that carry query parameters "
             "(filtered / sorted / tracking links) to avoid duplicate pages.")
    cf_harden_search = fields.Boolean(
        string='No-index site search',
        help="Add a noindex tag to the website search results page.")

    # ── Auto JSON-LD schema ─────────────────────────────────────────────
    cf_auto_schema_enabled = fields.Boolean(
        string='Auto JSON-LD schema',
        help="Add Organization + WebSite structured data to the homepage "
             "automatically (helps Google show your brand and a search box).")

    def cf_get_auto_schema(self):
        """Markup with Organization + WebSite JSON-LD for the homepage."""
        self.ensure_one()
        base = (self.get_base_url() or '').rstrip('/')
        url = base or '/'
        org = {"@context": "https://schema.org", "@type": "Organization",
               "name": self.name or "", "url": url}
        if self.logo:
            org["logo"] = "%s/web/image/website/%s/logo" % (base, self.id)
        site = {"@context": "https://schema.org", "@type": "WebSite",
                "name": self.name or "", "url": url}
        scripts = "".join(
            '<script type="application/ld+json">%s</script>'
            % json.dumps(d, ensure_ascii=False)
            for d in (org, site)
        )
        return Markup(scripts)
