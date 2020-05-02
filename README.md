# Springer Quarantine Books

## Introduction

This is a short python script to download the around 500 books that were provided for free by Springer during the 2020
global Corona lockdown.

The script is based on the [serch results](https://link.springer.com/search?facet-content-type=%22Book%22&package=mat-covid19_textbooks&%23038;facet-language=%22En%22&%23038;sortOrder=newestFirst&%23038;showAll=true)
which you get from the Springer website if you look for the "Covid-19 textbooks".
The search results can be downloaded as a `.csv` file to feed the [download_books.py](download_books.py) script.
Search results obtained on May 2, 2020 are included in the repository, so the script will run out of the box.

## Instructions

Just clone the repository, update the `SearchResults.csv` file if you  want, and run the [download_books.py](download_books.py) script. It will create one directory per book and attempt to download the **pdf** and **epub** file for each book. It can't be further configured at this point.

## Notes

1. The EPUB files are not available for all books, so be prepared for some `NONE_FOUND` status codes for this format.
2. Some books on the list are actually not freely available anymomre. The script tries to return the
   `NONFREE_DETECTED` status code for these books.
3. The only status code you should worry about is if you see `NOT_FOUND` for a PDF. This should not happen, as all
   books in the search results should give you valid URLs and PDFs are always available

I will not further work on this script as it already did the job for me, but I'm always happy to
receive pull requests!
