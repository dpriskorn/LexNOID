import pytest
from pydantic import ValidationError
from models.search_result import SearchResult, SourceFields, Source, Hit, Hits

# Sample JSON response to mock
sample_json = {
    "hits": {
        "hits": [
            {
                "_source": {
                    "fields": {"chronology": 1957},
                    "title_headword": "a-",
                    "headword_id": "a"
                }
            }
        ]
    }
}


def test_source_fields():
    sf = SourceFields(chronology=1900)
    assert sf.chronology == 1900

def test_source_model():
    src = Source(
        fields=SourceFields(chronology=1957),
        title_headword="a-",
        headword_id="a"
    )
    assert src.url == "https://noid.dsn.dk/ordbog/a-/"
    assert src.noid == "a"
    assert src.lemma == "a-"
    assert src.year == 1957

def test_hit_model():
    data = {
        "_source": {
            "fields": {"chronology": 1957},
            "title_headword": "a-",
            "headword_id": "a"
        }
    }
    hit = Hit(**data)
    assert hit.lemma == "a-"
    assert hit.noid == "a"
    assert hit.year == 1957
    assert hit.url == "https://noid.dsn.dk/ordbog/a-/"

def test_hits_model():
    data = {
        "hits": [
            {
                "_source": {
                    "fields": {"chronology": 1957},
                    "title_headword": "a-",
                    "headword_id": "a"
                }
            }
        ]
    }
    hits = Hits(hits=[Hit(**h) for h in data["hits"]])
    assert len(hits.hits) == 1
    assert hits.hits[0].lemma == "a-"

def test_search_result_model():
    result = SearchResult.model_validate(sample_json)
    assert len(result.hits.hits) == 1
    hit = result.hits.hits[0]
    assert hit.lemma == "a-"
    assert hit.year == 1957
    assert hit.noid == "a"
    assert hit.url == "https://noid.dsn.dk/ordbog/a-/"

def test_invalid_source_fields():
    with pytest.raises(ValidationError):
        SourceFields(chronology="not-an-int") # ignore
