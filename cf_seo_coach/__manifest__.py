{
    'name': 'CF SEO Coach',
    'version': '19.0.2.0.8',
    'summary': 'Live Yoast-style SEO & readability coach: keyphrase, meta tags, Google snippet preview, JSON-LD schema, Open Graph, canonical & robots — every page',
    'description': """
CF SEO Coach
============
A Yoast-inspired, real-time SEO and readability assistant built natively in
Odoo (OWL). It analyses your focus keyphrase, meta title and meta description,
Google snippet preview, Open Graph / Twitter cards and JSON-LD structured data,
and works on **every website page** — static pages, blog posts, eCommerce
products, events and anything else that uses Odoo's website SEO — with no extra
apps required.

What it adds to each page
-------------------------
* A focus-keyphrase analysis (keyphrase in the title, URL, intro, subheadings,
  density) with a traffic-light score.
* A readability analysis (sentence length, paragraphs, subheadings, Flesch
  reading ease, complex words).
* An editable Google snippet preview (desktop / mobile).
* Social sharing control (Facebook / X title, description and image).
* A structured-data (JSON-LD schema) box rendered into the page <head>.
* Advanced controls: canonical URL override and meta-robots directives
  (noindex / nofollow / noarchive / nosnippet / noimageindex).

Native already handled by Odoo (no plugin needed): XML sitemap, robots.txt and
URL redirects.

No external libraries — the analysis engine is pure JavaScript.

Ideal if you are searching for an Odoo SEO app, "Yoast for Odoo", a meta tag
manager, schema / structured-data (JSON-LD) tools, readability analysis or
on-page SEO optimisation for your Odoo website.
""",
    'category': 'Website/Website',
    'author': 'ChoiceFlow',
    'website': 'https://github.com/Akash00-git/cf_seo_coach',
    'support': 'akash00.hit@gmail.com',
    'maintainer': 'ChoiceFlow',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'views/seo_head.xml',
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
    'application': False,
}
