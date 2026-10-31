/** @odoo-module **/
/**
 * Pure-JS SEO + readability analysis engine, modelled on Yoast SEO 28.7.
 * Mirrors Yoast's real assessments (titleWidth[px], textLength, metaDescription*,
 * keyphraseDensity, introductionKeyword, subheadings*, sentenceLength,
 * paragraphLength, fleschReadingEase, wordComplexity) and its scoring: each
 * check scores 9/6/3 (good/ok/bad), overall = sum/(9·n)·100, rated
 * good ≥71 / ok 41–70 / bad <41 — the same traffic light Yoast shows.
 *
 * analyze({title, metaTitle, metaDescription, slug, content, keyphrase,
 *          titlePixelWidth, siteHost})
 *   -> {seo:{results, score, rating}, readability:{results, score, rating},
 *       wordCount, flesch}
 */

const SITE_HOST = "choiceflowers";
const SCORE = { good: 9, ok: 6, bad: 3 };

function parse(html) {
    return new DOMParser().parseFromString(html || "", "text/html");
}
function textOf(doc) {
    return (doc.body.textContent || "").replace(/\s+/g, " ").trim();
}
function wordsOf(text) {
    // ASCII-only word match: unicode property escapes / apostrophes in a regex
    // literal confuse Odoo's rjsmin minifier and corrupt the bundle.
    return (text || "").match(/[A-Za-z0-9]+/g) || [];
}
function sentencesOf(text) {
    return (text || "")
        .split(/[.!?]+(?:\s+|$)/)
        .map((s) => s.trim())
        .filter((s) => s.length);
}
function count(haystack, needle) {
    const h = (haystack || "").toLowerCase();
    const n = (needle || "").toLowerCase().trim();
    if (!n) {
        return 0;
    }
    let c = 0;
    let i = 0;
    while ((i = h.indexOf(n, i)) !== -1) {
        c += 1;
        i += n.length;
    }
    return c;
}
function slugify(s) {
    return (s || "")
        .toString()
        .toLowerCase()
        .normalize("NFKD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");
}
function syllables(word) {
    const w = (word || "").toLowerCase().replace(/[^a-z]/g, "");
    if (!w) {
        return 0;
    }
    if (w.length <= 3) {
        return 1;
    }
    const g = w
        .replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, "")
        .replace(/^y/, "")
        .match(/[aeiouy]{1,2}/g);
    return g ? g.length : 1;
}
function fleschReadingEase(text) {
    const s = sentencesOf(text);
    const w = wordsOf(text);
    if (!s.length || !w.length) {
        return 0;
    }
    const syl = w.reduce((a, x) => a + syllables(x), 0);
    const score = 206.835 - 1.015 * (w.length / s.length) - 84.6 * (syl / w.length);
    return Math.max(0, Math.min(100, Math.round(score)));
}
// roll per-check 9/6/3 into a 0-100 overall + Yoast-style rating
function overall(results) {
    const scored = results.filter((r) => SCORE[r.score]);
    if (!scored.length) {
        return { score: 0, rating: "bad" };
    }
    const sum = scored.reduce((a, r) => a + SCORE[r.score], 0);
    const score = Math.round((sum / (9 * scored.length)) * 100);
    const rating = score >= 71 ? "good" : score >= 41 ? "ok" : "bad";
    return { score, rating };
}

export function analyze(input) {
    const title = input.title || "";
    const metaTitle = input.metaTitle || title;
    const metaDescription = input.metaDescription || "";
    const slug = input.slug || slugify(title);
    const keyphrase = (input.keyphrase || "").trim();
    const doc = parse(input.content);
    const bodyText = textOf(doc);
    const words = wordsOf(bodyText);
    const wordCount = words.length;
    const host = input.siteHost || SITE_HOST;

    const seo = [];
    const add = (score, text) => seo.push({ score, text });

    if (!keyphrase) {
        add("bad", "Set a focus keyphrase to unlock the full SEO analysis.");
    } else {
        const kpWords = keyphrase.split(/\s+/).filter(Boolean);
        add(
            kpWords.length >= 1 && kpWords.length <= 4 ? "good" : "ok",
            `Keyphrase length: ${kpWords.length} word(s) (Yoast likes 1–4).`
        );
        const inTitle = count(metaTitle, keyphrase);
        const atStart =
            metaTitle.toLowerCase().trim().indexOf(keyphrase.toLowerCase()) === 0;
        add(
            inTitle ? (atStart ? "good" : "ok") : "bad",
            inTitle
                ? atStart
                    ? "Keyphrase is at the start of the SEO title."
                    : "Keyphrase is in the SEO title (move it nearer the front)."
                : "Keyphrase is not in the SEO title."
        );
        add(
            count(metaDescription, keyphrase) ? "good" : "bad",
            count(metaDescription, keyphrase)
                ? "Keyphrase is in the meta description."
                : "Keyphrase is not in the meta description."
        );
        const kpSlug = slugify(keyphrase);
        add(
            slug && kpSlug && slug.includes(kpSlug) ? "good" : "bad",
            slug && kpSlug && slug.includes(kpSlug)
                ? "Keyphrase is in the URL slug."
                : "Keyphrase is missing from the URL slug."
        );
        const firstP = doc.querySelector("p");
        add(
            firstP && count(firstP.textContent, keyphrase) ? "good" : "bad",
            firstP && count(firstP.textContent, keyphrase)
                ? "Keyphrase appears in the first paragraph."
                : "Keyphrase is not in the first paragraph — introduce it early."
        );
        const subs = [...doc.querySelectorAll("h2, h3")];
        const subsKp = subs.filter((h) => count(h.textContent, keyphrase)).length;
        add(
            subs.length === 0 ? "ok" : subsKp ? "good" : "ok",
            subs.length === 0
                ? "No subheadings yet to carry the keyphrase."
                : subsKp
                ? `Keyphrase is used in ${subsKp} subheading(s).`
                : "Keyphrase is in none of the subheadings — add it to one."
        );
        const occ = count(bodyText, keyphrase);
        const density = wordCount ? (occ * kpWords.length * 100) / wordCount : 0;
        add(
            density >= 0.5 && density <= 3 ? "good" : density > 3 ? "bad" : "ok",
            `Keyphrase density: ${density.toFixed(1)}% (${occ}× in ${wordCount} words; Yoast target 0.5–3%).`
        );
    }

    // related keyphrases: each extra phrase should appear in the content
    const related = (input.relatedKeyphrases || "")
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
    for (const rk of related) {
        const hit = count(bodyText, rk);
        add(
            hit ? "good" : "ok",
            hit
                ? `Related keyphrase "${rk}" appears in the content.`
                : `Related keyphrase "${rk}" is not in the content yet.`
        );
    }

    // titleWidth — Yoast measures pixels (≈600px max, 400 min); we use a measured
    // pixel width if the widget supplied one, else fall back to characters.
    if (input.titlePixelWidth) {
        const px = Math.round(input.titlePixelWidth);
        add(
            px >= 400 && px <= 600 ? "good" : px ? "ok" : "bad",
            `SEO title width: ${px}px (Yoast ideal 400–600px).`
        );
    } else {
        const t = metaTitle.length;
        add(
            t >= 30 && t <= 60 ? "good" : t ? "ok" : "bad",
            `SEO title length: ${t} characters (≈ Yoast 400–600px).`
        );
    }
    const mLen = metaDescription.length;
    add(
        mLen >= 120 && mLen <= 156 ? "good" : mLen && mLen <= 156 ? "ok" : "bad",
        `Meta description length: ${mLen} characters (Yoast max 156).`
    );
    const goodW = input.cornerstone ? 900 : 600;
    const okW = input.cornerstone ? 600 : 300;
    add(
        wordCount >= goodW ? "good" : wordCount >= okW ? "ok" : "bad",
        `Article length: ${wordCount} words (${input.cornerstone ? "cornerstone target " + goodW + "+" : "Yoast minimum 300"}).`
    );
    const links = [...doc.querySelectorAll("a[href]")].map((a) => a.getAttribute("href") || "");
    const internal = links.filter((h) => h.startsWith("/") || h.includes(host)).length;
    const external = links.filter((h) => (h.startsWith("http://") || h.startsWith("https://")) && !h.includes(host)).length;
    add(internal ? "good" : "ok", `Internal links: ${internal}${internal ? "" : " — link to related pages."}`);
    add(external ? "good" : "ok", `Outbound links: ${external}${external ? "" : " — cite a source where useful."}`);
    const imgs = [...doc.querySelectorAll("img")];
    const noAlt = imgs.filter((i) => !(i.getAttribute("alt") || "").trim()).length;
    add(
        imgs.length === 0 ? "ok" : noAlt ? "ok" : "good",
        imgs.length === 0
            ? "No images in the article."
            : noAlt
            ? `${noAlt} of ${imgs.length} image(s) have no alt text.`
            : `All ${imgs.length} image(s) have alt text.`
    );

    // ---- Readability ----
    const read = [];
    const radd = (score, text) => read.push({ score, text });
    const sents = sentencesOf(bodyText);
    const longPct = sents.length
        ? Math.round((100 * sents.filter((s) => wordsOf(s).length > 20).length) / sents.length)
        : 0;
    radd(
        longPct <= 25 ? "good" : longPct <= 40 ? "ok" : "bad",
        `Long sentences: ${longPct}% over 20 words (Yoast max 25%).`
    );
    const paras = [...doc.querySelectorAll("p")].map((p) => wordsOf(p.textContent).length);
    const longParas = paras.filter((n) => n > 150).length;
    radd(
        longParas === 0 ? "good" : "ok",
        longParas === 0 ? "No over-long paragraphs." : `${longParas} paragraph(s) exceed 150 words.`
    );
    const subsCount = doc.querySelectorAll("h2, h3").length;
    radd(
        wordCount > 300 && subsCount === 0 ? "bad" : "good",
        subsCount === 0 ? "No subheadings — add H2/H3 (Yoast max 300 words per section)." : `Subheadings: ${subsCount}.`
    );
    const complex = words.filter((w) => syllables(w) >= 4).length;
    const complexPct = wordCount ? Math.round((100 * complex) / wordCount) : 0;
    radd(
        complexPct <= 10 ? "good" : "ok",
        `Complex words (4+ syllables): ${complexPct}% (Yoast flags high complexity).`
    );
    const flesch = fleschReadingEase(bodyText);
    radd(
        flesch >= 60 ? "good" : flesch >= 30 ? "ok" : "bad",
        `Flesch reading ease: ${flesch}/100 (60+ is good).`
    );

    const seoScore = overall(seo);
    if (!keyphrase) {
        // no focus keyphrase = incomplete SEO; show red like Yoast
        seoScore.score = Math.min(seoScore.score, 30);
        seoScore.rating = "bad";
    }
    return {
        seo: { results: seo, ...seoScore },
        readability: { results: read, ...overall(read) },
        wordCount,
        flesch,
    };
}

export { slugify };
