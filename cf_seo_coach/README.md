# SEO Coach — user manual

A Yoast-style SEO & readability coach built natively in Odoo (OWL). It works on
**every website page**: static pages (Home, About, service pages), blog posts,
eCommerce products, events — anything that uses Odoo's website SEO. No other app
is required; it depends only on **Website**.

---

## 1. Install

1. Copy the `cf_seo_coach` folder into your Odoo add-ons path
   (or upload the `.zip` in **Apps → Upload**).
2. **Apps → Update Apps List**.
3. Search **SEO Coach** and click **Install**.

That's it. Nothing to configure.

---

## 2. Where to find it (locate exactly)

The SEO Coach lives inside Odoo's own **Optimize SEO** window, so it is in the
same place for every page type:

1. Open the page you want to optimise on your website (a static page, a blog
   post, a product…).
2. Click **Edit** (top-right) to open the website editor.
3. Open the SEO window:
   - Click the page **title** area → **Optimize SEO**, **or**
   - top menu **Edit / Promote → Optimize SEO**.
4. Scroll down in that window. Below Odoo's standard fields you will see a
   section titled **"SEO Coach"**.

> Tip: for blog posts you can also reach the page from
> **Website → Blog → Blog Posts**, open the post and click **Go to Website →
> Edit → Optimize SEO**.

---

## 3. What each part does

The SEO Coach section has six parts, top to bottom:

| Part | What it does |
|---|---|
| **Score badges** (top) | Two live traffic-light scores out of 100: **SEO** and **Readability**. Green = good, orange = ok, red = needs work. |
| **Focus keyphrase** | The one phrase (*oru sol thoguppu*) you want this page to rank for. Type it and the analysis updates instantly. |
| **Related keyphrases** | Extra phrases, comma-separated. The coach checks each one is actually used in the page. |
| **Cornerstone content** | Tick it for your most important "pillar" pages. The coach then expects more words (900+). |
| **SEO analysis** | A checklist: keyphrase in the title / URL / first paragraph / subheadings, keyphrase density (*adarthi* = how often), title & meta length, word count, links, image alt text. |
| **Readability** | A checklist: long sentences, long paragraphs, subheadings, Flesch reading ease (*padippu elimai* = how easy to read), complex words. |
| **Social (Facebook / X)** | The title, description and image shown when the page is shared on social media. Leave empty to use the SEO title/description. |
| **Schema (JSON-LD)** | Paste structured data (one JSON object or an array). A small label shows **Valid JSON** / **Check JSON**. It is printed into the page `<head>`. |
| **Advanced** | **Canonical URL** (point a duplicate page to the original) and **robots** switches: No index, No follow, No archive, No snippet, No image index. |

Press **Save** in the window. Everything is stored on that page and takes
effect immediately on the live site.

---

## 4. What it changes on the live page

When you save, the SEO Coach writes the right tags into the page `<head>`:

- `<link rel="canonical" …>` — your canonical URL (if you set one).
- `<meta name="robots" …>` — your index/follow/archive/snippet choices.
- `<meta property="og:*">` and `<meta name="twitter:*">` — your social title,
  description and image.
- `<script type="application/ld+json">…</script>` — your schema, one script per
  JSON object.

Search engines read these directly. You can confirm them in your browser with
**right-click → View Page Source**.

---

## 5. Already built into Odoo (no plugin needed)

These are standard Odoo website features, so the coach does not duplicate them:

- **XML sitemap** — `/sitemap.xml`.
- **robots.txt** — editable in the website settings.
- **URL redirects** — **Website → Configuration → Redirects**.

---

## 6. Notes & limits

- The live analysis reads the page content shown in the editor preview, the same
  way a search engine reads the rendered page.
- The "Generate with AI" feature of some paid tools is **not** included — that
  needs an external AI key. You write the keyphrase and text yourself.
- Supported Odoo version: **19.0**.

---

## 7. Uninstall

**Apps → SEO Coach → Uninstall.** Your pages keep working; only the extra SEO
fields and the coach panel are removed.

---

Built by **Webooz** · [webooz.in](https://webooz.in/) · Support: akash00.hit@gmail.com
