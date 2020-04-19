import requests
import pytest


base_url = "http://localhost:8081"

def test_get_papers():
    resp = requests.get(f"{base_url}/papers")
    assert resp.status_code == 200


@pytest.mark.parametrize(
    "published_date,expected",
    [
        ("20-02-2020", False),
        ("2020-02-20", True),
        ("12-01-2020", False),
        ("2020-01-12", True),
    ],
)
def test_get_papers_by_date_validate(published_date, expected):
    resp = requests.get(f"{base_url}/papers?published_date={published_date}")
    assert (resp.status_code == 200) == expected


@pytest.mark.parametrize(
    "published_date,expected",
    [
        ("1988-01-01", 3),
        ("1975-01-01", 8),
    ],
)
def test_get_papers_by_date(published_date, expected):
    resp = requests.get(f"{base_url}/papers?published_date={published_date}")
    assert resp.status_code == 200
    assert len(resp.json()['hits']) == expected


def test_get_papers_by_search_query():
    resp = requests.get(f"{base_url}/papers?q=virus")
    assert resp.status_code == 200
    hits = resp.json()['hits']
    assert len(hits) == 1
    assert "virus" in hits[0]["title"].lower()


@pytest.mark.parametrize(
    "cord_uid,expected_url",
    [
        ("8q5ondtn", "https://doi.org/10.1016/0002-8703(72)90077-4"),
        ("zp9k1k3z", "https://doi.org/10.1016/0002-9343(73)90176-9"),
    ],
)
def test_get_paper_by_cord_uid(cord_uid, expected_url):
    resp = requests.get(f"{base_url}/paper/{cord_uid}")

    assert resp.status_code == 200
    json_resp = resp.json()
    assert json_resp["cord_uid"] == cord_uid
    assert json_resp["url"] == expected_url
