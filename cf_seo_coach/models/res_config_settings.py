# Part of SEO Coach. Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. See LICENSE for details.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Expose the per-website SEO Coach settings in Website → Configuration →
    Settings. The fields are related to the selected website, so they follow
    Odoo's standard website settings pattern."""
    _inherit = 'res.config.settings'

    cf_gtm_container_id = fields.Char(
        related='website_id.cf_gtm_container_id', readonly=False)
    cf_ga4_measurement_id = fields.Char(
        related='website_id.cf_ga4_measurement_id', readonly=False)
    cf_llms_txt_enabled = fields.Boolean(
        related='website_id.cf_llms_txt_enabled', readonly=False)
    cf_llms_txt_intro = fields.Text(
        related='website_id.cf_llms_txt_intro', readonly=False)
    cf_harden_queryparams = fields.Boolean(
        related='website_id.cf_harden_queryparams', readonly=False)
    cf_harden_search = fields.Boolean(
        related='website_id.cf_harden_search', readonly=False)
    cf_auto_schema_enabled = fields.Boolean(
        related='website_id.cf_auto_schema_enabled', readonly=False)
