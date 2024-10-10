from flask.views import MethodView
from flask_smorest import Blueprint, abort
from uuid import uuid4
from schemas import WarehouseSchema

#Connect to SQLAlchemy db
from db import db
from models.product import ProductModel
from models.warehouse import WarehouseModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


#create a blueprint for this resource
blp = Blueprint("warehouses", __name__, description="Operations on warehouses endpoint.")

#Class for specific warehouse

@blp.route("/warehouse/<string:warehouse_id>")
class Warehouse(MethodView):

    @blp.response(200, WarehouseSchema)
    def get(self, warehouse_id):
        warehouse = WarehouseModel.query.get_or_404(warehouse_id)
        return warehouse
    
        
    
    def delete(self, warehouse_id):
        warehouse =  WarehouseModel.query.get_or_404(warehouse_id)


        db.session.delete(warehouse)
        db.session.commit()
       
        return {"message": "Warehouse deleted."}, 200


@blp.route("/warehouse")
class WarehouseList(MethodView):

    @blp.response(200, WarehouseSchema(many=True))
    def get(self):
        return WarehouseModel.query.all()

     # Request body to Marshmallow (WarhouseSchema)
    @blp.arguments(WarehouseSchema)
    @blp.response(201, WarehouseSchema)
    def post(self, new_warehouse_data):
       
       warehouse = WarehouseModel(
           name = new_warehouse_data["name"]
        )
       
       try:
           db.session.add(warehouse)
           db.session.commit()
           
       except SQLAlchemyError:
           abort(500, message="An error occured while adding the warehouse")

       except IntegrityError:
           abort(400, message="Warehouse name already exists.")
           
       return warehouse




