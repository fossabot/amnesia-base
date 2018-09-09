import json
import pytest

from amnesia.app import create_app
from amnesia.extensions import db as _db
from amnesia.models import User, Corpus, Article, Annotation


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }

@pytest.fixture
def corpus(db, admin_user):
    corpus = Corpus(
        title='Example corpus title',
        description='Example corpus description',
        author_id=admin_user.id,
    )
    db.session.add(corpus)
    db.session.commit()
    return corpus


@pytest.fixture
def article(db, admin_user, corpus):
    article = Article(
        content='Example content',
        corpus_id=corpus.id,
        author_id=admin_user.id,
    )
    db.session.add(article)
    db.session.commit()
    return article


@pytest.fixture
def annotation(db, admin_user, article):
    annotation = Annotation(
        article_id=article.id,
        author_id=admin_user.id,
        span_start=0,
        span_finish=7,
        type=0,
        tag=0,
    )
    db.session.add(annotation)
    db.session.commit()
    return annotation
