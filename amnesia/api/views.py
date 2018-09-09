from flask import Blueprint
from flask_restful import Api

from amnesia.api.resources import (
    UserResource,
    UserList,

    CorpusResource,
    CorpusList,

    ArticleResource,
    ArticleList,
)


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(CorpusResource, '/corpus/<int:corpus_id>')
api.add_resource(CorpusList, '/corpus')

api.add_resource(ArticleResource, '/corpus/<int:corpus_id>/articles/<int:article_id>')
api.add_resource(ArticleList, '/corpus/<int:corpus_id>/articles')
