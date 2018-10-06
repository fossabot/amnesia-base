import click
import ujson

from sqlalchemy import Integer, func
from flask.cli import FlaskGroup

from amnesia.app import create_app


def create_amnesia(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_amnesia)
def cli():
    '''Main entry point'''


@cli.command('init')
def init():
    '''Init application, create database tables
    and create a new user named admin with password admin
    '''
    from amnesia.extensions import db
    from amnesia.models import User
    click.echo('create database')
    db.create_all()
    click.echo('done')

    click.echo('create user')
    user = User(
        username='admin',
        email='admin@mail.com',
        password='admin',
        active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo('created user admin')


@cli.command('export', help='Export corpus annotations')
@click.option('--corpus-id', default=1, help='Corpus ID')
@click.option('--agreement', default=3, help='Count of annotations per tag/span pair')
@click.option('--output-directory', required=True, help='Location of output directory')
def export(corpus_id: int, agreement: int, output_directory: str):
    from amnesia.extensions import db
    from amnesia.models import Corpus, Article, Annotation

    corpus_id = (
        db
        .session
        .query(
            Corpus.id
        )
        .filter(
            Corpus.id == corpus_id
        )
        .first()
    )

    corpus_articles = (
        db
        .session
        .query(
            Article.id,
            Article.content,
        )
        .filter(
            Article.corpus_id == corpus_id
        )
        .order_by(Article.id)
    )

    corpus_articles_count = corpus_articles.count()

    offset = 0
    limit = 1000

    tags = {
        1: 'PER',
        2: 'ORG',
        3: 'LOC',
    }

    while offset <= corpus_articles_count:
        corpus_articles = corpus_articles.limit(limit).offset(offset)
        for article_id, article_content in corpus_articles:
            annotations = (
                db
                .session
                .query(
                    Annotation.article_id,
                    Annotation.span_start,
                    Annotation.span_finish,
                    Annotation.tag,
                )
                .filter(
                    Annotation.article_id == article_id
                )
                .group_by(
                    Annotation.article_id,
                    Annotation.span_start,
                    Annotation.span_finish,
                    Annotation.tag,
                )
                .having(
                    func.count(Annotation.tag) >= agreement
                )
                .all()
            )
            if not annotations:
                continue
            item = {
                'article_id': article_id,
                'content': article_content,
                'annotations': [
                    {
                        'span': {
                            'start': span_start,
                            'end': span_finish,
                        },
                        'type': tags[tag],
                        'text': article_content[span_start:span_finish],
                    } for (article_id, span_start, span_finish, tag) in annotations
                ]
            }
            item = ujson.dumps(item, indent=2, ensure_ascii=False)
            with open(f'{output_directory}/{article_id}.json', 'w') as output:
                output.write(item)
            print(article_id)
        offset += limit


if __name__ == '__main__':
    cli()
