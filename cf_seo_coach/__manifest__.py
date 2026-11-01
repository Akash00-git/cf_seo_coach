{
    'name': 'SEO Coach',
    'version': '19.0.3.0.9',
    'summary': 'All-in-one SEO toolkit: live Yoast-style coach, Google Tag Manager & GA4, llms.txt for AI search, JSON-LD schema, bulk SEO editor, SEO hardening',
    'description': """
SEO Coach — the all-in-one Odoo SEO toolkit
===========================================

A Yoast-inspired, real-time SEO and readability coach built natively in Odoo
(OWL), plus the site-wide tools you need to rank: analytics, AI-search, schema,
bulk editing and hardening. Works on every website page and depends only on
Website — no extra apps required.

1. Live SEO & readability coach (on every page)
-----------------------------------------------

- Focus keyphrase analysis: keyphrase in title, URL, intro, subheadings, density.
- Readability analysis: sentence length, paragraphs, subheadings, Flesch score.
- Editable Google snippet preview (desktop / mobile).
- Social sharing control (Facebook / X title, description, image).
- Per-page JSON-LD schema box, canonical URL and meta-robots directives.

2. Analytics injection — Google Tag Manager & GA4
-------------------------------------------------

- Paste your GTM container id and GA4 measurement id in Website settings.
- The scripts are injected site-wide (head + GTM noscript) automatically.

3. llms.txt for AI search (GEO / AEO)
-------------------------------------

- Publish an /llms.txt file that lists your pages, blog posts, products and
  events so AI search engines (ChatGPT, Perplexity, Gemini) can find you.

4. Bulk SEO editor
------------------

- Set the focus keyphrase, robots flags and canonical across many pages at once
  from one inline-editable list, instead of page by page.

5. SEO hardening
----------------

- Optionally no-index filtered / query-string URLs and the site search results
  page to avoid duplicate pages diluting your ranking.

6. Auto JSON-LD schema
----------------------

- Add Organization + WebSite structured data to the homepage with one toggle.

Already native in Odoo (not duplicated): XML sitemap, robots.txt, URL redirects.
No external libraries — the analysis engine is pure JavaScript.

Ideal if you are searching for an Odoo SEO app, "Yoast for Odoo", a meta tag
manager, Google Tag Manager / GA4, llms.txt, schema / structured data, bulk SEO
editing or on-page SEO optimisation for your Odoo website.
""",
    'category': 'Website/Website',
    'author': 'Webooz',
    'website': 'https://webooz.in/',
    'support': 'akash00.hit@gmail.com',
    'maintainer': 'Akash',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'views/seo_head.xml',
        'views/website_templates.xml',
        'views/res_config_settings_views.xml',
        'views/bulk_seo_views.xml',
    ],
    'assets': {
        'website.assets_editor': [
            'cf_seo_coach/static/src/seo_coach/seo_analysis.js',
            'cf_seo_coach/static/src/dialog/seo_coach_dialog.js',
            'cf_seo_coach/static/src/dialog/seo_coach_dialog.xml',
            'cf_seo_coach/static/src/dialog/seo_coach_dialog.scss',
        ],
    },
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'uninstall_hook': '_cf_uninstall_cleanup',
}
