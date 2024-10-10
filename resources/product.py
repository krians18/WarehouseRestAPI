from flask.views import MethodView
from flask_smorest import Blueprint, abort
from uuid import uuid4
from schemas import ProductSchema, ProductUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt

#Connect to SQLAlchemy db
from db import db
from models.product import ProductModel
from models.warehouse import WarehouseModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

#create a blueprint for this resource
blp = Blueprint("products", __name__, description="Operations on products endpoint.")

@blp.route('/product/<string:product_id>')
class Product(MethodView):

    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product
         
    @jwt_required(fresh=True)
    def delete(self, product_id):
        jwt = get_jwt() 

        try:
            if jwt["is_admin"] == True:

                product = ProductModel.query.get_or_404(product_id)

                db.session.delete(product)
                db.session.commit()

                return {"message": "Product deleted"}, 200
        except:
            abort(400, message="You are not an admin.")
       
    @jwt_required(fresh=True)
    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductUpdateSchema)
    def put(self, product_update_data, product_id):
        product = ProductModel.query.get(product_id)

        if product:
            product.name = product_update_data["name"]
            product.price = product_update_data['price']
        else:
            product = ProductModel(
                name = product_update_data["name"], 
                price = product_update_data["price"],
                warehouse_id = product_update_data["warehouse_id"]
            )
                
        try:
            db.session.add(product)   
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while editing the product")

        return product
      

@blp.route('/product')
class ProductList(MethodView):
    @blp.response(201, ProductSchema(many=True))
    def get(self): 
        return ProductModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ProductSchema) 
    @blp.response(201, ProductSchema)  
    def post(self, new_product_data):
        warehouse =  WarehouseModel.query.get(new_product_data["warehouse_id"])

        if not warehouse:
            abort(404, message="Warehouse ID not found")
        
        #Create New Record
        product = ProductModel(
          name = new_product_data["name"], 
          price = new_product_data["price"],
          warehouse_id = new_product_data["warehouse_id"]
        )
        
        try:
        #Add the new product to the database session
            db.session.add(product)
            db.session.commit() # Save to the database
        
        except SQLAlchemyError:
            abort(500, message="An error occured when creating a product.")
     
        return product