from sqlalchemy.orm import Session
import db_models


def get_all_products_service(db: Session):
    return db.query(db_models.Product).all()


def get_product_by_id_service(product_id: int, db: Session):
    return db.query(db_models.Product).filter(
        db_models.Product.product_id == product_id
    ).first()
