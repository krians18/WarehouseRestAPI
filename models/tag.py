from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    #ForeignKey
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)

    #Establish Relationship
    warehouse = db.relationship("WarehouseModel", back_populates="tags")

    ## secondary = conjunction table  
    products = db.relationship("ProductModel", back_populates="tags", secondary="products_tags")




    