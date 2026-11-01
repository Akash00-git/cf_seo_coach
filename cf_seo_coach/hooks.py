# Part of SEO Coach. Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. See LICENSE for details.

# Stored SEO Coach fields (cf_robots_content / cf_schema_head are computed, so
# they have no column).
CF_STORED_FIELDS = (
    'cf_seo_keyphrase', 'cf_seo_related_keyphrases', 'cf_is_cornerstone',
    'cf_social_title', 'cf_social_description', 'cf_social_image',
    'cf_schema_jsonld', 'cf_canonical_url',
    'cf_robots_noindex', 'cf_robots_nofollow', 'cf_robots_noarchive',
    'cf_robots_nosnippet', 'cf_robots_noimageindex',
)


def _cf_init_seo_models(env):
    """Make sure every model that inherits ``website.seo.metadata`` has the
    SEO Coach columns.

    The fields live on the shared (abstract) SEO base, so they are added to
    models owned by other modules (blog.post, product.template, event.event,
    ...). Odoo creates those columns on a fresh install, but an *upgrade* of
    this module churns the inherited field records and drops the columns while
    the ORM still selects them, which breaks those website pages. This is
    called from ``_register_hook`` (after every registry load, when the fields
    are already propagated) to re-create any missing column idempotently."""
    for _name, model in env.registry.items():
        if not getattr(model, '_auto', False) or model._abstract:
            continue
        if 'cf_schema_jsonld' not in model._fields:
            continue
        for col in CF_STORED_FIELDS:
            field = model._fields.get(col)
            if not field or not field.store or not field.column_type:
                continue
            env.cr.execute(
                'ALTER TABLE "%s" ADD COLUMN IF NOT EXISTS "%s" %s'
                % (model._table, col, field.column_type[1])
            )


def _cf_uninstall_cleanup(env):
    """Safety net on uninstall: drop every SEO Coach stored column from all
    tables, so no orphan ``cf_*`` columns are left behind on core tables
    (res_partner, product_template, blog_post, blog_tag, ...) even if a
    registry reload re-created them. Column names are unique to this module,
    so matching by name across tables is safe. Idempotent (DROP ... IF EXISTS)."""
    env.cr.execute(
        "SELECT table_name, column_name FROM information_schema.columns "
        "WHERE column_name = ANY(%s)",
        (list(CF_STORED_FIELDS),),
    )
    for table, col in env.cr.fetchall():
        env.cr.execute(
            'ALTER TABLE "%s" DROP COLUMN IF EXISTS "%s"' % (table, col)
        )
