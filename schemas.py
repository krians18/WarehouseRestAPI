from marshmallow import Schema, fields

# Separate schemas for creating relationships like one-to-many
# Warehouse schema
class PlainWarehouseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)

# Product schema
class PlainProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    description = fields.Str(required=True)

#Create Tag Schema
class PlainTagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


# Schema for updating a product
class ProductUpdateSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

    warehouse_id = fields.Integer()

# New schema with relationship (One warehouse to many products)
class WarehouseSchema(PlainWarehouseSchema):
    products = fields.List(fields.Nested(PlainProductSchema), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema), dump_only=True)

# Product schema with warehouse relationship
class ProductSchema(PlainProductSchema):  
    warehouse_id = fields.Integer(required=True)
    warehouse = fields.Nested(PlainWarehouseSchema, dump_only=True)

    tags = fields.List(fields.Nested(PlainTagSchema, dump_only=True))

class TagSchema(PlainTagSchema):
    warehouse_id = fields.Integer(load_only=True)
    warehouse = fields.Nested(PlainWarehouseSchema, dump_only=True)

    products = fields.List(fields.Nested(PlainProductSchema), dump_only=True)

class TagAndProductSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ProductSchema)
    tag = fields.Nested(TagSchema())

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(required=True)

    
    