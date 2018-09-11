# -*- coding: utf-8 -*-

from odoo import models, fields, api


class @@prefix_class@@@@model_class@@(models.Model):
    _name = '@@prefix_name@@.@@model_name@@'
    _description = '@@model_description@@'

    sequence    = fields.Integer()
    name        = fields.Char()
    description = fields.Text()

    """ Basics methods (create, write, ...) """
    @api.model
    def create(self, vals):
        record = super(@@prefix_class@@@@model_class@@, self).create(vals)
        return record

    @api.multi
    def write(self, vals):
        record = super(@@prefix_class@@@@model_class@@, self).write(vals)
        return record


    """ Compute functions """


    """ Onchange functions """


    """ Others functions """
