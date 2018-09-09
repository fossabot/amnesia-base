from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy import and_


from amnesia.models import Article
from amnesia.extensions import ma, db
from amnesia.commons.pagination import paginate


class ArticleSchema(ma.ModelSchema):

    class Meta:
        model = Article
        sqla_session = db.session

class ArticleResource(Resource):
    """Single object resource."""

    method_decorators = [
        jwt_required
    ]

    def get(self, corpus_id: int, article_id: int):
        schema = ArticleSchema()
        article = Article.query.filter(
            and_(
                Article.id == article_id,
                Article.corpus_id == corpus_id,
            )
        ).first_or_404()
        return {'article': schema.dump(article).data}

    def put(self, corpus_id: int, article_id: int):
        schema = ArticleSchema(partial=True)
        article = Article.query.filter(
            and_(
                Article.id == article_id,
                Article.corpus_id == corpus_id,
            )
        ).first_or_404()
        article, errors = schema.load(request.json, instance=article)
        if errors:
            return errors, 422

        return {'message': 'article updated', 'article': schema.dump(article).data}

    def delete(self, corpus_id: int, article_id: int):
        article = Article.query.filter(
            and_(
                Article.id == article_id,
                Article.corpus_id == corpus_id,
            )
        ).first_or_404()
        db.session.delete(article)
        db.session.commit()

        return {'message': 'article deleted'}


class ArticleList(Resource):

    method_decorators = [
        jwt_required,
    ]

    def get(self, corpus_id: int):
        schema = ArticleSchema(many=True)
        articles = Article.query.filter(Article.corpus_id == corpus_id)
        return paginate(articles, schema)

    def post(self, corpus_id: int):
        schema = ArticleSchema()
        article, errors = schema.load(request.json)
        if errors:
            return errors, 422
        article.corpus_id = corpus_id
        article.author_id = get_jwt_identity()
        db.session.add(article)
        db.session.commit()
        return {
            'message': 'article created',
            'article': schema.dump(article).data,
        }
