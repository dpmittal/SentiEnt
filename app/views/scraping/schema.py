import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.views.scraping.models import db_session, Products as ProductsModel, Reviews as ReviewsModel


class Products(SQLAlchemyObjectType):
    class Meta:
        model = ProductsModel
        interfaces = (relay.Node, )

class ProductsConnection(relay.Connection):
    class Meta:
        node = Products

class Reviews(SQLAlchemyObjectType):
    class Meta:
        model = ReviewsModel
        interfaces = (relay.Node, )

class ReviewsConnection(relay.Connection):
    class Meta:
        node = Reviews


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_products = SQLAlchemyConnectionField(ProductsConnection)
    # Disable sorting over this field
    all_reviews = SQLAlchemyConnectionField(ReviewsConnection, sort=None)

schema = graphene.Schema(query=Query)