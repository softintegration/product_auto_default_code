# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

DEFAULT_CODE_SEQUENCE_CODE = "product.product.default_code"


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Internal Reference', index=True, readonly=True)

    @api.model_create_multi
    def create(self, vals):
        products = super(ProductProduct, self).create(vals)
        for product in products:
            if self._sequence_dynamic_installed():
                # here we have to expect using of dynamic sequence,if no dynamic sequence will be configured or used, nothing will be changed in this code
                #FIXME:We have to test this in important data volume
                dynamic_prefix_fields = product._build_dynamic_prefix_fields()
                default_code = self.env['ir.sequence'].with_context(dynamic_prefix_fields=dynamic_prefix_fields).next_by_code(
                    DEFAULT_CODE_SEQUENCE_CODE)
            else:
                default_code = self.env['ir.sequence'].next_by_code(
                    DEFAULT_CODE_SEQUENCE_CODE)
            product.write({'default_code': default_code})
        return products

    @api.model
    def _sequence_dynamic_installed(self):
        "This method return True if the sequence_dynamic module is installed"
        return 'sequence_dynamic' in self.env['ir.module.module']._installed().keys()

    def _build_dynamic_prefix_fields(self):
        self.ensure_one()
        vals = {}
        for field_name,_ in self._fields.items():
            vals.update({field_name:getattr(self,field_name)})
        return vals