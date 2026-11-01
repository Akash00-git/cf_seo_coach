# SEO Coach — all-in-one Odoo 19 SEO toolkit

A Yoast-style, real-time **SEO & readability coach** for every Odoo website page,
plus the site-wide tools you need to rank. Built natively in OWL — no external
libraries, depends only on **Website**.

**On-page coach (every page)**
- Focus keyphrase + readability scoring (traffic-light checks)
- Editable **Google snippet preview**, **meta title & description**
- **Open Graph / Twitter** social tags and per-page **JSON-LD** schema
- Canonical URL override and meta-robots directives

**Site-wide SEO toolkit (v3)**
- **Google Tag Manager + GA4** injection from Website settings
- **`/llms.txt`** generator for AI search (ChatGPT, Perplexity, Gemini)
- **Bulk SEO editor** — set keyphrase/robots/canonical across many pages at once
- **SEO hardening** — no-index filtered / search URLs to avoid duplicate pages
- **Auto JSON-LD schema** (Organization + WebSite) on the homepage


All features opt-in and website-scoped. Tested end-to-end on Odoo 19 Enterprise,
including no conflicts with POS and Inventory.

## Install
Copy `cf_seo_coach/` into your Odoo add-ons path (or **Apps → Upload** the zip),
then **Apps → Update Apps List** and install **SEO Coach**.

Module: [`cf_seo_coach/`](cf_seo_coach/) · License: LGPL-3 · Support: akash00.hit@gmail.com
