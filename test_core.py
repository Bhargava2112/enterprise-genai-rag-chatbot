from app.core import Retriever, answer, tokenize


def test_tokenization():
    assert tokenize("Hello, AWS-Lambda!") == ["hello", "aws", "lambda"]


def test_retrieval_and_citation():
    engine = Retriever()
    assert engine.add("aws.txt", "AWS Lambda runs serverless functions on demand.") == 1
    engine.add("database.txt", "PostgreSQL stores relational tables and indexes.")
    hits = engine.search("serverless lambda")
    assert hits[0]["source"] == "aws.txt"
    assert answer("serverless lambda", hits)["citations"] == ["aws.txt"]


def test_empty_and_no_match():
    engine = Retriever()
    assert engine.search("hello") == []
    engine.add("x", "banana pear")
    assert engine.search("kubernetes") == []
    assert "couldn't find" in answer("x", [])["answer"]


def test_overlap_validation():
    engine = Retriever()
    try:
        engine.add("x", "a b", chunk_size=5, overlap=5)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
