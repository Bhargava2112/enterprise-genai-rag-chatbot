from fastapi.testclient import TestClient
from app.api import app, retriever


def test_health_ingest_ask():
    retriever.chunks.clear()
    client = TestClient(app)
    assert client.get('/health').json() == {'status': 'ok', 'chunks': 0}
    assert client.post('/documents', json={'name': 'guide.txt', 'text': 'Lambda provides serverless computing.'}).status_code == 200
    result = client.post('/ask', json={'question': 'Lambda serverless'}).json()
    assert result['citations'] == ['guide.txt']
    assert result['matches'][0]['source'] == 'guide.txt'


def test_invalid_document():
    client = TestClient(app)
    assert client.post('/documents', json={'name': 'x', 'text': ''}).status_code == 422
