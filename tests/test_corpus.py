from amnesia.models import Corpus


def test_get_all_corpus(client, corpus, admin_headers):
    response = client.get(f'/api/v1/corpus', headers=admin_headers)
    assert response.status_code == 200

    results = response.get_json()
    assert results['total'] == 1

def test_get_single_corpus(client, corpus, admin_headers):
    response = client.get(f'/api/v1/corpus/{corpus.id}', headers=admin_headers)
    assert response.status_code == 200

    results = response.get_json()
    assert results['corpus']['title'] == corpus.title
    assert results['corpus']['description'] == corpus.description

def test_create_corpus(client, admin_headers):
    response = client.post(f'/api/v1/corpus', headers=admin_headers, json={
        'title': 'Example corpus',
        'description': 'Example description',
    })
    assert response.status_code == 200
    results = response.get_json()
    assert results['corpus']['title'] == 'Example corpus'
    assert results['corpus']['description'] == 'Example description'

def test_update_corpus(client, corpus, admin_headers):
    response = client.put(f'/api/v1/corpus/{corpus.id}', headers=admin_headers, json={
        'title': 'New example corpus',
    })
    assert response.status_code == 200
    results = response.get_json()

    assert results['corpus']['title'] != corpus.title
    assert results['corpus']['description'] == corpus.description
