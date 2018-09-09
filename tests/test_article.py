from amnesia.models import Article


def test_get_all_article(client, admin_headers, article):
    response = client.get(f'/api/v1/corpus/{article.corpus_id}/articles', headers=admin_headers)
    assert response.status_code == 200
    results = response.get_json()
    assert results['total'] == 1

def test_get_single_article(client, admin_headers, article):
    response = client.get(f'/api/v1/corpus/{article.corpus_id}/articles/{article.id}', headers=admin_headers)
    assert response.status_code == 200
    results = response.get_json()
    assert results['article']['corpus'] == article.corpus_id
    assert results['article']['content'] == article.content

def test_update_article(client, admin_headers, article):
    response = client.put(f'/api/v1/corpus/{article.corpus_id}/articles/{article.id}', headers=admin_headers, json={
        'content': 'Example article content',
    })
    assert response.status_code == 200
    results = response.get_json()
    assert results['article']['corpus'] == article.corpus_id
    assert results['article']['content'] != article.content

def test_delete_article(client, admin_headers, article):
    response = client.delete(f'/api/v1/corpus/{article.corpus_id}/articles/{article.id}', headers=admin_headers)
    assert response.status_code == 200
