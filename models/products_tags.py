from db import db



class ProductsTags(db.Model):
    __tablename__ = "products_tags"


    id = db.Column(db.Integer, primary_key=True)


    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)


