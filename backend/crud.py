from sqlalchemy.orm import Session
from models import ProductModel
from schemas import ProductUpdate, ProductCreate


def get_products(db: Session):
    """
    SELECT *
    FROM products
    """
    return db.query(ProductModel).all()


def get_product(db: Session, product_id: int):
    """
    DECLARE @product_id INT
    SELECT *
    FROM products p
    WHERE p.id = product_id
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    """
    DECLARE @product_name
    DECLARE @product_desc
    DECLARE @product_catg
    DECLARE @supp_email
    INSERT INTO product (name, description, price, supplier_email)
    VALUES(@product_name, @product_desc, @product_catg, @supp_email)
    """
    # Transformar dados inputados para ORM
    db_product = ProductModel(**product.model_dump())

    # Adicionar na Tabela, Commitar e dar Refresh no DB
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Retornar ao usuário validação
    return db_product


def delete_product(db: Session, product_id: int):
    """
    DECLARE @product_id
    DELETE FROM product
    WHERE product.id = @product_id
    """
    db_product = db.query(ProductModel).filter(
        ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(ProductModel).filter(
        ProductModel.id == product_id).first()

    if db_product is None:
        return None

    if product.name is not None:
        db_product.name = product.name

    if product.description is not None:
        db_product.description = product.description

    if product.price is not None:
        db_product.price = product.price

    if product.category is not None:
        db_product.category = product.category

    if product.supplier_email is not None:
        db_product.supplier_email = product.supplier_email

    db.commit()
    db.refresh(db_product)

    return db_product
