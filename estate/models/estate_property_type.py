from odoo import models,fields

class EstatePropertyType(models.Model):
    _name= 'estate.property.type'
    _description = ' Property Type'
    
    name=fields.Char(required=True)
    
    property_ids = fields.One2many('test_model', 'property_type_id', string="Properties")
    
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]