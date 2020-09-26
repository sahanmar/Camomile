import argparse
import requests
import re
import sys

from tqdm import tqdm
from bs4 import BeautifulSoup
from typing import Optional, List
from pathlib import Path

NEWS_PAT = re.compile(re.escape("www.bbc.com/news/"))  # English pattern
SITEMAPS_LINK = "https://www.bbc.com/sitemaps/https-index-com-news.xml"


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="bbc_links.txt",
        help="output txt file with links",
    )
    return parser


def get_text_from_link(maybe_link: str) -> Optional[List[str]]:
    try:
        html_text = requests.get(maybe_link).text
        soup = BeautifulSoup(html_text, "html.parser")
        return [token for token in soup.get_text().split("\n") if token]
    except requests.exceptions.InvalidSchema:
        return None


def write_into_file(output_list: List[str], file_path: Path) -> None:
    with open(file_path, "w") as f:
        for item in output_list:
            f.write("%s\n" % item)


def main():

    args = argparser().parse_args()
    output_path = Path(args.output)

    if not output_path.parent.is_dir():
        print("Given pashh is not valid...")
        sys.exit()

    # Next chunk of code could be done with a recursion but I'm lazy...
    first_level_indent = get_text_from_link(SITEMAPS_LINK)

    seond_level_indent = [
        res
        for maybe_link in tqdm(first_level_indent)
        if (
            res_list := get_text_from_link(maybe_link)
        )  # New python 3.8 feature (Walrus operator)
        for res in res_list
    ]
    news_links = [
        maybe_link for maybe_link in seond_level_indent if NEWS_PAT.search(maybe_link)
    ]

    write_into_file(news_links, output_path)


if __name__ == "__main__":
    main()
