from elasticsearch import Elasticsearch
from database_classes import ForumPost
import os

# BONSAI_URL = (f"https://{os.getenv("BONSAI_USERNAME")}:"
#               f"{os.getenv("BONSAI_PASSWORD")}@"
#               f"{os.getenv("BONSAI_HOST")}:"
#               f"{os.getenv("BONSAI_PORT")}"
# )

BONSAI_URL = "https://qyxa461jsp:jpt78uryu9@individual-search-9901961089.eu-central-1.bonsaisearch.net:443"
# ElasticSearch Setup
es = Elasticsearch(BONSAI_URL)
if not es.indices.exists(index="posts"):
    es.indices.create(index="posts")


def index_post(post):
    doc = {
        "title": post.title,
        "body": post.body,
        "author": post.author.username,
        "date": post.date.isoformat(),
        "category": post.category.name,
    }
    es.index(index="posts", id=post.id, body=doc)


def search_posts(query):
    es.indices.refresh(index="posts")
    result = es.search(index="posts", body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "body"]
            }
        }
    })
    # Extract post IDs from search hits
    post_ids = [int(hit["_id"]) for hit in result["hits"]["hits"]]
    # Query your database for those posts (in order)
    posts = ForumPost.query.filter(ForumPost.id.in_(post_ids)).all()
    return posts