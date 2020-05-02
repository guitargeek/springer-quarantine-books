import pandas as pd
import urllib.request
import os
from enum import Enum


class DownloadStatus(Enum):
    SUCCESS = 1
    NOT_FOUND = 2
    NONFREE_DETECTED = 4
    FILE_EXISTS = 5


def pdf_url(book_url):
    """Get the pdf link for a given book URL."""

    assert "/book/" in book_url

    isbn = book_url.split("/book/")[1]

    isbn.replace("/", "%")

    return "link.springer.com/content/pdf/" + isbn + ".pdf"


def epub_url(book_url):
    """Get the pdf link for a given book URL."""

    assert "/book/" in book_url

    isbn = book_url.split("/book/")[1]

    isbn.replace("/", "%")

    return "link.springer.com/download/epub/" + isbn + ".epub"


def make_filename(entry):
    year = entry["Publication Year"]
    title = entry["Item Title"]
    return f"{year}_Book_{title}".replace(" ", "")


def lint_if_html(filename):
    with open(filename, "r") as f:
        try:
            is_pdf = "HTML" in f.readline()
        except UnicodeDecodeError:
            return False
    return is_pdf


def download(url, filename, ignore_existing=False):
    if ignore_existing or not os.path.isfile(filename):
        try:
            urllib.request.urlretrieve("http://" + url, filename)
        except urllib.request.HTTPError:
            return DownloadStatus.NOT_FOUND
        if os.path.isfile(filename) and lint_if_html(filename):
            os.remove(filename)
            return DownloadStatus.NONFREE_DETECTED
        else:
            return DownloadStatus.SUCCESS
    else:
        return DownloadStatus.FILE_EXISTS


def download_pdf(url, filename, ignore_existing=False):
    return download(pdf_url(url), filename + ".pdf", ignore_existing=ignore_existing)


def download_epub(url, filename, ignore_existing=False):
    return download(epub_url(url), filename + ".epub", ignore_existing=ignore_existing)


def test_1():
    nonfree_book_url = "https://link.springer.com/book/10.1007%2F978-0-387-36601-2"
    pdf_status = download_pdf(nonfree_book_url, "test_1", ignore_existing=True)
    epub_status = download_epub(nonfree_book_url, "test_1", ignore_existing=True)

    assert pdf_status == DownloadStatus.NONFREE_DETECTED
    assert epub_status == DownloadStatus.NONFREE_DETECTED


def test_2():
    invalid_book_url = "https://link.springer.com/book/1234"
    pdf_status = download_pdf(invalid_book_url, "test_2", ignore_existing=True)
    epub_status = download_epub(invalid_book_url, "test_2", ignore_existing=True)

    assert pdf_status == DownloadStatus.NOT_FOUND
    assert epub_status == DownloadStatus.NOT_FOUND


def test_3():
    no_epub_url = "http://link.springer.com/book/10.1007/978-0-387-37575-5"
    pdf_status = download_pdf(no_epub_url, "test_3", ignore_existing=True)
    epub_status = download_epub(no_epub_url, "test_3", ignore_existing=True)

    assert pdf_status == DownloadStatus.SUCCESS
    assert epub_status == DownloadStatus.NOT_FOUND


def test_4():
    pdf_and_epub_url = "http://link.springer.com/book/10.1007/978-1-4614-8933-7"
    pdf_status = download_pdf(pdf_and_epub_url, "test_4", ignore_existing=True)
    epub_status = download_epub(pdf_and_epub_url, "test_4", ignore_existing=True)

    assert pdf_status == DownloadStatus.SUCCESS
    assert epub_status == DownloadStatus.SUCCESS

    pdf_status = download_pdf(pdf_and_epub_url, "test_4", ignore_existing=False)
    epub_status = download_epub(pdf_and_epub_url, "test_4", ignore_existing=False)

    assert pdf_status == DownloadStatus.FILE_EXISTS
    assert epub_status == DownloadStatus.FILE_EXISTS


run_tests = False

if run_tests:
    print("Doing some tests to warm up...")
    test_1()
    test_2()
    test_3()
    test_4()
    print("Tests passed!")
    print("")

df = pd.read_csv("SearchResults.csv")
n_books = len(df)

for i_book in range(n_books):
    entry = df.loc[i_book]

    year = entry["Publication Year"]
    title = entry["Item Title"]
    enumerating_string = f"[{i_book+1}/{n_books}]"
    indent = " " * len(enumerating_string)
    print(enumerating_string + f" {title} ({year})")

    book_dir = f"{year}-{title}".replace(" ", "_")

    if not os.path.exists(book_dir):
        os.makedirs(book_dir)

    filename = os.path.join(book_dir, make_filename(entry))
    print(indent + " " + "-" * len(f"{title} ({year})"))
    pdf_status = download_pdf(entry["URL"], filename)
    print(indent + f" pdf: {pdf_status.name}")
    epub_status = download_epub(entry["URL"], filename)
    print(indent + f" epub: {epub_status.name}")
    print("")
