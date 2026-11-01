=========
SEO Coach
=========

All-in-one, Yoast-style SEO toolkit built natively in Odoo 19. A live SEO &
readability coach on every website page, plus the site-wide tools you need to
rank: Google Tag Manager & GA4, an ``llms.txt`` file for AI search, a bulk SEO
editor, SEO hardening and automatic JSON-LD schema. No external libraries;
depends only on **Website**.

Features
========

Live SEO & readability coach
----------------------------

* Focus keyphrase analysis: keyphrase in the title, URL, intro, subheadings
  and keyphrase density.
* Readability analysis: sentence length, paragraphs, subheadings and the
  Flesch reading-ease score.
* Editable Google snippet preview (desktop / mobile).
* Social sharing control (Facebook / X title, description and image).
* Per-page JSON-LD schema, canonical URL and meta-robots directives.

Google Tag Manager & GA4
------------------------

Paste your GTM container id and GA4 measurement id in the website settings and
the scripts are injected across the whole site automatically.

llms.txt for AI search
----------------------

Publish an ``/llms.txt`` file that lists your pages, blog posts, products and
events so AI search engines (ChatGPT, Perplexity, Gemini) can discover you.

Bulk SEO editor
---------------

Set the focus keyphrase, robots flags and canonical URL across many pages at
once from a single inline-editable list.

SEO hardening
-------------

Optionally no-index filtered / query-string URLs and the site-search results
page so duplicate pages do not dilute your ranking.

Auto JSON-LD schema
-------------------

Add Organization and WebSite structured data to the homepage with one toggle.

Setup and configuration
=======================

Nothing to configure to start: once installed, the live coach is already
active on every page. Below is where each feature lives.

1. Live coach (per page)
------------------------

Open any website page, click **Edit**, then **Optimize SEO**. Scroll to the
**SEO Coach** section and set the focus keyphrase, related keyphrases, social
fields, JSON-LD schema, canonical URL and robots flags. The **SEO** and
**Readability** scores update live. Click **Save**.

2. Google Tag Manager and GA4
-----------------------------

Open **Website → Configuration → Settings** and scroll to the **SEO Coach**
block. Paste your GTM id (``GTM-XXXXXXX``) and/or GA4 id (``G-XXXXXXXXXX``),
then save. Verify with right-click → **View Page Source** and search for
``googletagmanager``.

3. llms.txt
-----------

In the same **SEO Coach** settings block, turn on **AI search (llms.txt)** and
save. The file is served at ``/llms.txt``.

4. SEO hardening
----------------

In the same block, turn on **SEO hardening** to no-index filtered / query
string URLs and the site-search results page.

5. Auto JSON-LD schema
----------------------

In the same block, turn on **Auto JSON-LD schema**. Organization and WebSite
structured data is added to the homepage automatically.

6. Bulk SEO editor
------------------

Open the top-level **SEO Coach → Bulk SEO (Pages)** menu (next to
*Configuration* in the Website app). Tick several rows and set the focus
keyphrase, no-index flag or canonical URL for all of them at once.

Uninstall
=========

Open **Apps → SEO Coach → Uninstall**. Your pages keep working; only the extra
SEO fields and the coach panel are removed. The uninstall is clean and leaves
no orphan columns behind.

Support
=======

Built by **Webooz**.

* Website: https://webooz.in/
* Support: akash00.hit@gmail.com
