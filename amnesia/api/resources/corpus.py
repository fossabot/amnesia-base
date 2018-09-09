from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


from amnesia.models import Corpus
from amnesia.extensions import ma, db
from amnesia.commons.pagination import paginate


class CorpusSchema(ma.ModelSchema):

    class Meta:
        model = Corpus
        sqla_session = db.session
        fields = (
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
        )

class CorpusResource(Resource):
    """Single object resource."""

    method_decorators = [
        jwt_required
    ]

    def get(self, corpus_id):
        schema = CorpusSchema()
        corpus = Corpus.query.get_or_404(corpus_id)
        return {'corpus': schema.dump(corpus).data}

    def put(self, corpus_id):
        schema = CorpusSchema(partial=True)
        corpus = Corpus.query.get_or_404(corpus_id)
        corpus, errors = schema.load(request.json, instance=corpus)
        if errors:
            return errors, 422

        return {'msg': 'corpus updated', 'corpus': schema.dump(corpus).data}

    def delete(self, corpus_id):
        corpus = Corpus.query.get_or_404(corpus_id)
        db.session.delete(corpus)
        db.session.commit()

        return {'msg': 'corpus deleted'}


class CorpusList(Resource):

    method_decorators = [
        jwt_required,
    ]

    def get(self):
        schema = CorpusSchema(many=True)
        return paginate(Corpus.query, schema)

    def post(self):
        schema = CorpusSchema()
        corpus, errors = schema.load(request.json)
        if errors:
            return errors, 422
        corpus.author_id = get_jwt_identity()
        db.session.add(corpus)
        db.session.commit()
        return {
            'msg': 'corpus created',
            'item': schema.dump(corpus).data,
        }
