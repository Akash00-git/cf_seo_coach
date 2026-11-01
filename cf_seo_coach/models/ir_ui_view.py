# Part of SEO Coach. Copyright (C) 2026 Webooz <akash00.hit@gmail.com>. See LICENSE for details.
from odoo import models

from ..hooks import _cf_init_seo_models


class IrUiView(models.Model):
    # ir.ui.view inherits website.seo.metadata (and is always present), so it
    # is a reliable, always-loaded place to hang the column guard.
    _inherit = 'ir.ui.view'

    def _register_hook(self):
        res = super()._register_hook()
        # Runs once per registry load (install / upgrade / restart), after the
        # SEO fields are propagated to every concrete model, so it heals any
        # columns dropped by an upgrade. Idempotent (ADD COLUMN IF NOT EXISTS).
        #
        # Skip while this module is being uninstalled ('to remove'): otherwise
        # we re-create the very columns the uninstall just dropped and leave
        # orphan cf_* columns on core tables (res_partner, product_template,
        # blog_post, ...), i.e. an unclean uninstall.
        mod = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'cf_seo_coach')], limit=1)
        if mod and mod.state not in ('to remove', 'uninstalled'):
            _cf_init_seo_models(self.env)
        return res
