from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import WarehouseSchema, TagSchema, TagAndProductSchema

#Connect to SQLAlchemy db
from db import db
from models.warehouse import WarehouseModel
from models.tag import TagModel
from models.product import ProductModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("tags", __name__, description="Operations on tags.")


@blp.route("/product/<int:product_id>/tag/<int:tag_id>")
class LinkTags(MethodView):

    
    def post(self, product_id, tag_id):
        product =  ProductModel.query.get_or_404(product_id)
        tag =  TagModel.query.get_or_404(tag_id)

        if product.warehouse_id  != tag.warehouse_id:
            abort(400, message="Make sure that product and tags belong to the same store before linking.")

        
        product.tags.append(tag)

        try:

            db.session.add(product)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occured while linking the tags and the product")

        return {"message": "Tag and porduct is successfully linkned."}, 200
    
    
    @blp.response(200, TagAndProductSchema)
    def delete(self, product_id, tag_id):
        product =  ProductModel.query.get_or_404(product_id)
        tag =  TagModel.query.get_or_404(tag_id)

        product.tags.remove(tag)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while unlinking the product and the tag")
 
        return {"message": "Tag removed from the product", "product": product, "tag": tag}




@blp.route("/warehouse/<int:warehouse_id>/tag")
class TagsInWarehouse(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, warehouse_id):
        warehouse = WarehouseModel.query.get_or_404(warehouse_id)
        return warehouse.tags.all()
      
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, req_body, warehouse_id):
        if TagModel.query.filter(
            TagModel.warehouse_id ==  warehouse_id,
            TagModel.name == req_body["name"]
        ).first():
            abort(400, message="A tag with that name already exists in the same warehouse.")


        tag = TagModel(name=req_body["name"], warehouse_id=warehouse_id)

        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occured while ceating a tag.")

        return tag
    
    @blp.route("/tag/<int:tag_id>")
    class Tag(MethodView):

        @blp.response(200, TagSchema)
        def get(self, tag_id):
            tag = TagModel.query.get_or_404(tag_id)
            return tag
        
        def delete(sefl, tag_id):
            tag = TagModel.query.get_or_404(tag_id)

            if tag.product:
                abort(400, message="Could not delete tag. Please unlink all products to this tag before deleting")

            db.sesion.delete(tag)
            db.session.commit()

            return {"message": "Tag deleted"}, 200



