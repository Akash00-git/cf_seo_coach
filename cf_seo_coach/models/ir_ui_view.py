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
        _cf_init_seo_models(self.env)
        return res
