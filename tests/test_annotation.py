def test_get_all_annotation(client, admin_headers, article, annotation):
    response = client.get(
        f'/api/v1/corpus/{article.corpus_id}/articles/{article.id}/annotations',
        headers=admin_headers,
    )
    assert response.status_code == 200
    results = response.get_json()
    assert results['total'] == 1


def test_create_annotation(client, admin_headers, article):
    response = client.post(
        f'/api/v1/corpus/{article.corpus_id}/articles/{article.id}/annotations',
        headers=admin_headers,
        json=[{
            'span_start': 0,
            'span_finish': 1,
            'type': 0,
            'tag': 0,
        }]
    )
    assert response.status_code == 200
