import requests

from typing import Dict, Any, List
from default_config import NewsCfg


def download_articles(config: NewsCfg) -> Dict[str, Any]:
    response = requests.get(f"{config.url}{config.news_type}1.json?api-key={config.api_key}")
    return response.json()


def stack_article_components(article: Dict[str, Any]) -> str:
    article_elements: List[str] = [article["title"], article["abstract"], article["url"]]
    return "\n\n".join(article_elements)


def get_articles(config: NewsCfg) -> List[str]:
    response = download_articles(config)
    return [stack_article_components(article) for article in response["results"]]
