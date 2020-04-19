import os
from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import (
    Search, Document, Date, Keyword, Text, connections,
)


connections.create_connection(hosts=['localhost'])
client = Elasticsearch()


def init_es(index_name="paper-index"):
    """Initialise document mapping on an index."""
    Paper.Index.name = index_name
    Paper.init(index=index_name, using=client)


class Paper(Document):
    cord_uid = Keyword()
    sha = Keyword()
    source_x = Keyword()
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    publish_time = Date()
    abstract = Text(analyzer='snowball')

    class Index:
        name = 'paper-index'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }


def get_paper_models(published_date=None, q=None, offset=0, limit=10, index_name=None):
    index_name = index_name or os.environ.get("INDEX", "paper-index")
    search_query = Search(using=client, index=index_name)
    if published_date:
        search_query = search_query.filter("range", publish_time={'gte': published_date})
    if q:
        search_query = search_query.query("match", title=q)
    search_query = search_query[offset:limit]
    resp = search_query.execute()
    return {
        "total": resp.hits.total,
        "offset": offset,
        "limit": limit,
        "hits": [hit.to_dict() for hit in resp.hits]
    }

def get_paper_model(cord_uid, index_name=None):
    index_name = index_name or os.environ.get("INDEX", "paper-index")
    search_query = (
        Search(using=client, index=index_name)
        .filter("term", cord_uid=cord_uid)
    )
    resp = search_query.execute()
    if len(resp) == 0:
        return {}
    if len(resp) > 1:
        print(f"Unexpected - more than one document with id {cord_uid}.")  # Should be log
    return resp[0].to_dict()


def delete_papers(index_name="paper-index"):
    # For testing purposes
    client.indices.delete(index=index_name)


