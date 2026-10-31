# Part of CF SEO Coach. See LICENSE file for full copyright and licensing details.
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
        _cf_init_seo_models(self.env)
        return res
