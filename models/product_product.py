# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

DEFAULT_CODE_SEQUENCE_CODE = "product.product.default_code"

class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Internal Reference', index=True,readonly=True)

    @api.model_create_multi
    def create(self, vals):
        products = super(ProductProduct, self).create(vals)
        for product in products:
            default_code = self.env['ir.sequence'].next_by_code(DEFAULT_CODE_SEQUENCE_CODE)
            product.write({'default_code':default_code})
        return products
