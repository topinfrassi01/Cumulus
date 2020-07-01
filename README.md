# Cumulus

## What is Cumulus?

Cumulus is a tool to explore the news in a different way than with the common categories like Sports, Politics, Economy, etc.

Cumulus works differently. In this very case, after exploring a few thousand news articles from a Kaggle dataset, it has determined the average at which noun phrase occur per day.

Using this, is a noun phrase happens more than its usual, it knows for sure it was an important noun for the day.

For a very simple example, imagine the keyword "Basketball" occurs on average 4 times a day for every articles in the database and that, for one particular day, it occurs 14 times. It's pretty obvious something special happened in Basketball that day. In this case, the noun Basketball would be prioritized by Cumulus.

How is it presented? This way!

<img src="https://i.imgur.com/lQNwr9P.png"/>

The amount of nouns that are presented using Cumulus is entirely variable in the application. The "Metro Style" visual makes it easy to see all nouns and their information. In the image above, you see that if you hover over one tile, it displays some information about the noun that explain why it is mentioned by Cumulus.

If you click on one of the keywords, you get a list of the articles that mention the noun for the day.

## What's next?

I really wish I could run this application in a live scenario. Sadly, it is quite difficult to access news articles per day. Even if it was possible to scrape the web to get articles, the volume of articles needed to train Cumulus is pretty big and I don't think scraping would work well for this. Also, I wouldn't be able to cover the costs of exploitation.

So, many in some future Cumulus will become a live application, but for the moment it's only a prototype.

## How to install

You need to run this  also: python -m textblob.download_corpora

- Obviously install everything listed in [Software Reqs](#reqs)
- Download the Kaggle's dataset listed in [Credits](#credits)
- Extract it
- Restore the `cumulus_empty` postgre backup.
- Edit `config.json`
- Run `generate_all_data.py` and specify path to point to the path of the files extraction.
- Run Flask and hit localhost:5000

## <a href="#reqs">Software Reqs</a>

- PostGre SQL installed
- The requirements.txt file contains all the dependencies

## <a href="#credits">Credits</a>

- Obviously, all the packages listed in `requirements.txt`
- This [Kaggle's Dataset](https://www.kaggle.com/snapcrack/all-the-news) which contains **a lot** of news.
