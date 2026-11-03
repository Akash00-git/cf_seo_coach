/** @odoo-module **/
// Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. Part of SEO Coach (LGPL-3).
// Extends Odoo's built-in "Optimize SEO" dialog (website.OptimizeSEODialog)
// with the SEO Coach: a focus-keyphrase + readability analysis, social
// sharing fields, a JSON-LD schema box and advanced canonical / robots
// controls. Because this dialog opens on ANY website page (static pages,
// blog posts, products, events...), one extension covers every page type.
import { patch } from "@web/core/utils/patch";
import { onWillStart, useState } from "@odoo/owl";
import { OptimizeSEODialog } from "@website/components/dialog/seo";
import { analyze } from "../seo_coach/seo_analysis";

const CF_FIELDS = [
    "cf_seo_keyphrase",
    "cf_seo_related_keyphrases",
    "cf_is_cornerstone",
    "cf_social_title",
    "cf_social_description",
    "cf_social_image",
    "cf_schema_jsonld",
    "cf_canonical_url",
    "cf_robots_noindex",
    "cf_robots_nofollow",
    "cf_robots_noarchive",
    "cf_robots_nosnippet",
    "cf_robots_noimageindex",
];

patch(OptimizeSEODialog.prototype, {
    setup() {
        super.setup();
        this.cf = useState({
            loaded: false,
            keyphrase: "",
            related: "",
            cornerstone: false,
            socialTitle: "",
            socialDescription: "",
            socialImage: "",
            schema: "",
            canonical: "",
            noindex: false,
            nofollow: false,
            noarchive: false,
            nosnippet: false,
            noimageindex: false,
        });
        onWillStart(async () => {
            // The base dialog sets this.object only AFTER `await this.waitForIframe()`,
            // and OWL runs all onWillStart hooks concurrently (Promise.all). So if we
            // read this.object here it is still undefined and we return early, leaving
            // every field blank on reopen. Resolve the record ourselves (exactly like
            // the base does) after awaiting the iframe, so saved values load back in.
            await this.waitForIframe();
            this.cf.loaded = true;
            const {
                metadata: { mainObject, seoObject },
            } = this.website.currentWebsite;
            const object = seoObject || mainObject;
            if (!object) {
                return;
            }
            let recs;
            try {
                recs = await this.orm.read(object.model, [object.id], CF_FIELDS);
            } catch {
                return; // never crash the dialog if the read fails
            }
            const r = recs && recs[0];
            if (!r) {
                return;
            }
            this.cf.keyphrase = r.cf_seo_keyphrase || "";
            this.cf.related = r.cf_seo_related_keyphrases || "";
            this.cf.cornerstone = !!r.cf_is_cornerstone;
            this.cf.socialTitle = r.cf_social_title || "";
            this.cf.socialDescription = r.cf_social_description || "";
            this.cf.socialImage = r.cf_social_image || "";
            this.cf.schema = r.cf_schema_jsonld || "";
            this.cf.canonical = r.cf_canonical_url || "";
            this.cf.noindex = !!r.cf_robots_noindex;
            this.cf.nofollow = !!r.cf_robots_nofollow;
            this.cf.noarchive = !!r.cf_robots_noarchive;
            this.cf.nosnippet = !!r.cf_robots_nosnippet;
            this.cf.noimageindex = !!r.cf_robots_noimageindex;
        });
    },

    // Content of the current page, read from the rendered preview DOM.
    get cfPageContent() {
        const docEl = this.website.pageDocument && this.website.pageDocument.documentElement;
        const wrap = docEl && docEl.querySelector("#wrap, main, body");
        return wrap ? wrap.innerHTML : "";
    },

    get cfAnalysis() {
        // memoised so typing a keyphrase does not re-parse the whole page DOM
        const content = this.cfPageContent;
        const key = [content, this.cf.keyphrase, this.cf.related, this.cf.cornerstone].join("||CF||");
        if (this._cfKey !== key) {
            this._cfKey = key;
            let metaDescription = "";
            try {
                metaDescription = this.getMeta({ name: "description" }) || "";
            } catch {
                metaDescription = "";
            }
            this._cfAnalysis = analyze({
                title: this.defaultTitle || "",
                metaTitle: this.defaultTitle || "",
                metaDescription,
                slug: (this.data && this.data.seo_name) || "",
                content,
                keyphrase: this.cf.keyphrase,
                relatedKeyphrases: this.cf.related,
                cornerstone: this.cf.cornerstone,
            });
        }
        return this._cfAnalysis;
    },

    cfDot(score) {
        return "cf-seo-dot cf-seo-dot-" + score;
    },
    cfSchemaValid() {
        const raw = (this.cf.schema || "").trim();
        if (!raw) {
            return "";
        }
        try {
            JSON.parse(raw);
            return "Valid JSON";
        } catch {
            return "Check JSON";
        }
    },

    async save() {
        if (this.object && this.canEditSeo) {
            await this.orm.write(
                this.object.model,
                [this.object.id],
                {
                    cf_seo_keyphrase: this.cf.keyphrase,
                    cf_seo_related_keyphrases: this.cf.related,
                    cf_is_cornerstone: this.cf.cornerstone,
                    cf_social_title: this.cf.socialTitle,
                    cf_social_description: this.cf.socialDescription,
                    cf_social_image: this.cf.socialImage,
                    cf_schema_jsonld: this.cf.schema,
                    cf_canonical_url: this.cf.canonical,
                    cf_robots_noindex: this.cf.noindex,
                    cf_robots_nofollow: this.cf.nofollow,
                    cf_robots_noarchive: this.cf.noarchive,
                    cf_robots_nosnippet: this.cf.nosnippet,
                    cf_robots_noimageindex: this.cf.noimageindex,
                },
                {
                    context: {
                        lang: this.website.currentWebsite.metadata.lang,
                        website_id: this.website.currentWebsite.id,
                    },
                }
            );
        }
        return super.save(...arguments);
    },
});
