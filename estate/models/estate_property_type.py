from odoo import models,fields

class EstatePropertyType(models.Model):
    _name= 'estate.property.type'
    _description = ' Property Type'
    
    name=fields.Char(required=True)
    
    
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]