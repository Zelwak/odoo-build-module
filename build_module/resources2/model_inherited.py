# -*- coding: utf-8 -*-

from odoo import models, fields, api


class @@model_inherited_class@@(models.Model):
    _inherit = '@@model_inherited_name@@'

    field   = fields.Char()

    """ Basics methods (create, write, ...) """
    @api.model
    def create(self, vals):
        record = super(@@model_inherited_class@@, self).create(vals)
        return record

    @api.multi
    def write(self, vals):
        record = super(@@model_inherited_class@@, self).write(vals)
        return record


    """ Compute functions """


    """ Onchange functions """


    """ Others functions """
