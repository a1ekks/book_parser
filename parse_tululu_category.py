import argparse
import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from exceptions import ResponseRedirectException
from parse_tululu_books import get_page, download_tululu
from set_default_options import set_default_options_parser


def parse_category_page(response_text, url):
    soup: BeautifulSoup = BeautifulSoup(response_text, 'lxml')
    books_urls = []

    for book_item in soup.select('div.bookimage'):
        parsed_part_of_url = book_item.select_one('a')
        if not parsed_part_of_url or not parsed_part_of_url.get('href'):
            continue
        _url = urljoin(url, parsed_part_of_url.get('href'))
        if _url in books_urls:
            continue
        books_urls.append(_url)

    return books_urls


def generate_category_page_urls(start_page_number, end_page_number, category_id):
    for page_number in range(start_page_number, end_page_number):
        yield f'https://tululu.org/l{category_id}/{page_number}'


def download_category_page(page_url,
                           images_path,
                           books_path,
                           json_file_path,
                           skip_images,
                           skip_text):

    response = get_page(page_url)
    books_urls = parse_category_page(response.text, response.request.url)
    download_tululu(
        books_urls,
        images_path=images_path,
        books_path=books_path,
        json_file_path=json_file_path,
        skip_images=skip_images,
        skip_text=skip_text
    )


def parse_options(default_parsers: list = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(parents=default_parsers)

    parser.add_argument(
        "-sp", "--start_page", default='1', type=int,
        help="Setting start value for generation categories url, default = 1"
    )

    parser.add_argument(
        "-ep", "--end_page",
        default='10', type=int,
        help="Setting start value for generation categories url, default is 10. End_page must be greater than "
             "start_page! "
    )

    return parser.parse_args()


if __name__ == '__main__':
    default_options_parser: argparse.ArgumentParser = set_default_options_parser()
    args = parse_options([default_options_parser])

    disable_warnings(InsecureRequestWarning)

    destination_directory_path = args.dest_folder or os.path.abspath(os.path.dirname(__file__))
    books_path = os.path.join(destination_directory_path, 'books')
    images_path = os.path.join(destination_directory_path, 'images')
    scifi_category = 55

    json_file_path = args.json_path or os.path.join(destination_directory_path, 'book_info.json')
    
    for category_page_url in generate_category_page_urls(args.start_page, args.end_page, scifi_category):
        print(f'Current url is {category_page_url}')
        try:
            download_category_page(
                category_page_url, images_path,
                books_path, json_file_path,
                args.skip_imgs, args.skip_txt
            )
        except ResponseRedirectException:
            print(f'Page with url: {category_page_url} has some redirection')
