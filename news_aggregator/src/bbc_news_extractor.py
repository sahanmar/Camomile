import argparse
import requests
import re
import sys
import json
import urllib

from tqdm import tqdm
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
from pathlib import Path
from boilerpy3 import extractors

NEWS_PAT = re.compile(re.escape("www.bbc.com/news/"))  # English pattern
SITEMAPS_LINK = "https://www.bbc.com/sitemaps/https-index-com-news.xml"


def argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="input txt file or folder with downloaded htmls",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="bbc_links.txt",
        help="output txt file with links",
    )
    parser.add_argument(
        "-d",
        "--download_html",
        type=bool,
        default=False,
        help="falg for downloading html documents from links",
    )
    parser.add_argument(
        "-p",
        "--parse_htmls",
        type=bool,
        default=False,
        help="falg for parsing the htmls",
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


def get_from_file(input_path: Path) -> List[str]:
    with open(input_path, "r") as f:
        links_list = [line.strip() for line in f.readlines()]
    return links_list


def download_bbc_links(output_path: Path) -> List[str]:

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

    return news_links


def dowbload_htmls_from_links(links_list: List[str], output_path: Path) -> List[str]:
    
    output_path = output_path/"html"
    output_path.mkdir()

    def save_html(link: str, path: Path) -> str:
        html_path = path / f"{link.split('/')[-1]}.html"
        urllib.request.urlretrieve(link, html_path)
        return html_path

    return [save_html(link, output_path) for link in tqdm(links_list)]


def parse_htmls(html_paths_list: List[Path], output_path: Path) -> Dict[str, str]:

    extractor = extractors.ArticleExtractor()

    parsed_htmls = {
        html_path.stem: extractor.get_content_from_file(html_path)
        for html_path in tqdm(html_paths_list)
    }

    with open(output_path, "w") as f:
        json.dump(parsed_htmls, f)

    return parsed_htmls


def main():

    args = argparser().parse_args()
    input_path = Path(args.input) if args.input else None
    output_path = Path(args.output)

    if not input_path:
        links_list = download_bbc_links(output_path)
        print(
            f"{len(links_list)} downloaded links have been stored in {output_path.name} file..."
        )
    elif not input_path.is_file() and not input_path.is_dir():
        print("Given input path is not valid...")
        sys.exit()
    elif input_path.is_file() and input_path.suffix == ".txt":
        links_list = get_from_file(input_path)
        print(f"{len(links_list)} links were extracted from a given file...")
    elif input_path.is_dir():
        html_paths_list = [html_path for html_path in input_path.iterdir()]
        print(
            f"{len(html_paths_list)} html paths were extracted from a given folder..."
        )

    if args.download_html and not input_path.is_dir():
        html_paths_list = dowbload_htmls_from_links(links_list, output_path.parent)
        print(f"{len(html_paths_list)} html were downloaded from given links...")

    if args.parse_htmls:
        parsed_htmls = parse_htmls(html_paths_list, output_path.parent/"parsed_htmls.json")
        print(f"{len(list(parsed_htmls.keys()))} htmls were parsed from given paths...")

    print("The program has successfully terminated its work...")


if __name__ == "__main__":
    main()
