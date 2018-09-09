from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy import and_

from amnesia.models import Corpus, Article, Annotation
from amnesia.extensions import ma, db
from amnesia.commons.pagination import paginate


class AnnotationSchema(ma.ModelSchema):

    class Meta:
        model = Annotation
        sqla_session = db.session


class AnnotationList(Resource):

    method_decorators = [
        jwt_required
    ]

    def get(self, corpus_id: int, article_id: int):
        schema = AnnotationSchema(many=True)
        corpus = Corpus.query.get_or_404(corpus_id)
        annotations = Annotation.query.filter(
            Annotation.article_id == article_id
        )
        return {
            'total': annotations.count(),
            'results': schema.dumps(annotations).data,
        }

    def post(self, corpus_id: int, article_id: int):
        schema = AnnotationSchema(many=True)
        author_id = get_jwt_identity()
        corpus = Corpus.query.get_or_404(corpus_id)
        article = Article.query.get_or_404(article_id)
        annotations, errors = schema.load(request.json)
        if errors:
            return errors, 422
        for annotation in annotations:
            annotation.article_id = article.id
            annotation.author_id = author_id
            db.session.add(annotation)
        db.session.commit()
        return {
            'message': 'annotations saved',
            'annotations': schema.dumps(annotations).data
        }

