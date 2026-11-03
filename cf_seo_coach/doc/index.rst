=========
SEO Coach
=========

:Version: 19.0.3.1.0 (for Odoo 19, LGPL-3, by Webooz)

A live, Yoast-style SEO coach for Odoo 19 — plus every site-wide tool you need
to rank. Built natively in Odoo, with no external libraries, and depends only
on **Website**.

.. tip::

   Nothing to set up to start. The moment you install it, the live SEO and
   readability coach is active on every website page.

What you get
============

- **Live coach** — SEO and readability scores on every page, with green /
  orange / red tips as you write.
- **Google Tag Manager & GA4** — add both to the whole site, no code.
- **llms.txt** — let AI search (ChatGPT, Perplexity, Gemini) find your pages.
- **Bulk SEO editor** — edit many pages at once.
- **SEO hardening** — keep duplicate pages out of Google.
- **Auto JSON-LD schema** — structured data on your homepage with one toggle.
- **Site Audit** — crawl your pages, posts and products and get a 0-100 SEO
  health score with a prioritised list of issues to fix.

Installation
============

SEO Coach is a full app (it has code), so install it the standard Odoo way: put
the module folder in your Odoo **add-ons** (modules) folder, then install it
from **Apps**.

.. warning::

   Do **not** use **Apps -> Import Module** / "Upload a Module" (the zip upload).
   That screen loads data-only add-ons and does not load code, so the coach and
   other features would not actually run. Use one of the methods below.

Odoo.sh
-------

1. Add the ``cf_seo_coach`` folder to your Odoo.sh project's add-ons (commit it
   to your project's GitHub repository, or add this repository as a submodule)
   and push. Odoo.sh rebuilds automatically.
2. Open **Apps -> Update Apps List**, search **SEO Coach**, click **Install**.

Self-hosted / on-premise
------------------------

1. Get the ``cf_seo_coach`` folder (the one that contains ``__manifest__.py``)
   from the Odoo Apps download or from git.
2. Copy that folder into your server's add-ons path. With git::

      git clone -b 19.0 https://github.com/Akash00-git/cf_seo_coach.git /tmp/src
      cp -r /tmp/src/cf_seo_coach /path/to/your/odoo/addons/cf_seo_coach

3. Restart the Odoo service.
4. In Odoo open **Apps**, click **Update Apps List**, clear the search filter,
   type **SEO Coach**, and click **Install**.

Odoo Online (the free odoo.com / SaaS)
--------------------------------------

Odoo Online does not allow third-party apps, so this app cannot run there. Use
Odoo.sh or a self-hosted Odoo.

Where everything is
===================

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Feature
     - Where to set it
   * - Live coach (keyphrase, scores, social, schema, robots)
     - Open a page, click **Edit**, then **Optimize SEO** (section *SEO Coach*)
   * - GTM / GA4 / llms.txt / hardening / auto-schema
     - **Configuration -> Settings -> SEO Coach**
   * - Bulk SEO editor
     - Top menu **SEO Coach -> Bulk SEO (Pages)**
   * - llms.txt file
     - ``your-site.com/llms.txt``

Step by step
============

1. Live coach
-------------

Open any page, click **Edit**, then **Optimize SEO**. Scroll to **SEO Coach**,
type your focus keyphrase, and watch the scores and tips update live. Save.

2. Analytics (GTM and GA4)
--------------------------

Go to **Configuration -> Settings -> SEO Coach**. Paste your GTM id
(``GTM-XXXXXXX``) and/or GA4 id (``G-XXXXXXXXXX``) and save. Check it with
right-click -> **View Page Source** and search for ``googletagmanager``.

3. llms.txt, hardening and schema
---------------------------------

In the same **SEO Coach** settings block, turn on what you need. Once enabled,
llms.txt is served at ``/llms.txt``.

4. Bulk editing
---------------

Open **SEO Coach -> Bulk SEO (Pages)**, tick several rows, and set the
keyphrase or robots flags for all of them at once.

.. note::

   You can uninstall any time from **Apps -> SEO Coach -> Uninstall**. Your
   pages keep working and nothing is left behind.

Support
=======

Built by **Webooz** — https://webooz.in/ — akash00.hit@gmail.com
