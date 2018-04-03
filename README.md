# Cumulus

## How to install

You need to run this  also: python -m textblob.download_corpora

- Obviously install everything listed in [Software Reqs](#reqs)
- Download the Kaggle's dataset listed in [Credits](#credits)
- Extract it
- Enter your database configuration in `config.json`
- Run `extract_data.py` and specify path to point to the path of the files extraction.

## <a href="#reqs">Software Reqs</a>

- PostGre SQL installed

## <a href="#credits">Credits</a>

- Obviously, all the packages listed in `requirements.txt`
- This [Kaggle's Dataset](https://www.kaggle.com/snapcrack/all-the-news) which contains **a lot** of news.