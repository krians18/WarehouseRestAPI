from db import db


class WarehouseModel(db.Model):
    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    #Connect to ProductModel
    products =  db.relationship("ProductModel", back_populates="warehouse", lazy="dynamic",
    cascade="all, delete")

    #Connect to TagModel
    tags =  db.relationship("TagModel", back_populates="warehouse") 