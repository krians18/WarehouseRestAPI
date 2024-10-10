from db import db

class ProductModel(db.Model):
    #Table name
    __tablename__ = "products"

    #Table fields(column)

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False, unique=True)

    price = db.Column(db.Float(precision=2))

    description = db.Column(db.String(250), nullable=False)

    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), unique=False, nullable=False)

    #Establish relationship with warehouse
    warehouse =  db.relationship("WarehouseModel", back_populates="products")

    # Add a many to many relationship from item to tags
    tags = db.relationship("TagModel", back_populates="products", secondary="products_tags")

