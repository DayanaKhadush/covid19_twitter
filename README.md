## Preprocess twitter data from [Covid-19 Twitter chatter dataset for scientific use](https://github.com/thepanacealab/covid19_twitter) for further training of language models

The covid19_twitter dataset contains ids of approximately 1.5Mio russian, 9Mio german and more than 447Mio english tweets among other languages.
To sample a certain amount _n_ of tweets in a certain language _lang_ (e.g. ru) from _dailies_ contained in _covid19_twitter_ directory::

```sh 
python read_ids.py --n n --l ru --data_dir ../covid19_twitter/
```

### Hydrating tweets from ids.txt
```sh 
twarc2 configure
```
paste your bearer token and press enter, note that you can continue without api keys and secrets.

To hydrate tweets given a `ids.txt` file with tweet_ids: 
```sh
twarc2 hydrate ids_ru.txt ru.json
twarc2 csv ru.json ru.csv
```

To obtain only textual content from hydrated tweets:
```sh
python read_tweets.py --l ru
```

To clean the textual data in texts_*.csv:
```sh
python clean_text.py --l de --data_dir data/ 
```
cleaned_*.txt are for the training

(install twarc, pandas, WordCloud, emoji)