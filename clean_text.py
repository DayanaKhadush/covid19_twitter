"""Preprocess textual content from hydrated tweets"""
import pandas as pd
import argparse
import logging
import re

from nltk import tokenize
import tokenize_uk

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--l",
                        default=None,
                        type=str,
                        required=True,
                        help="which language to sample"
                        )

    parser.add_argument("--hashtags",
                        default=False,
                        type=bool,
                        required=False,
                        help="analyse hashtags"
                        )

    parser.add_argument("--data_dir",
                        default='data/',
                        type=str,
                        required=False,
                        help="directory with dailies directory")
    args = parser.parse_args()
    return args


def clean(texts, uk=False):
    stop_words = ['читать', 'книга', 'магия', 'чтопочитать', 'fantasy', 'reading', 'book', 'книга', 'фэнтези', 'читаем']
    import demoji

    current = []
    for i, text in enumerate(texts):
        if i % 1000 == 0:
            print(i)
        if any(sw in text.lower() for sw in stop_words):
            continue
        # remove links
        text = re.sub(r"(?:http?\://|https?\://|www)\S+", " ", text)

        # hide usernames
        text = re.sub(r"(?:\@)\S+", "@username", text)

        # remove emojis
        text = demoji.replace(text, " ")
        #text = emoji.demojize(text)
        #text = re.sub(r":\S*:", " ", text)

        # remove retweets chain
        text = re.sub("^(\@username )*", "", text)

        # remove one word lines
        text = re.sub(r'\\n', '\n', text)
        text = re.sub('\s*\n[^\s]*\s*\n', '\n', text)
        text = re.sub('^(?:\s*[^\s]*\s*)\n', '\n', text)

        # remove newlines and punctuation between
        text = re.sub(r'^[^\w]*\n+', '\n', text)
        text = re.sub(r'\n+[^\w]*\n+', '\n', text)
        text = re.sub(r'\s*\n+\s*', '\n', text)
        text = text.replace(".\n", ". ")
        text = re.sub(' +', ' ', text)
        text = text.replace("\n", ". ")
        text = text.replace("(.+|(. )+)+", ". ")
        # remove all punktuation at the beginning
        text = re.sub('^([^\w]+)', '', text)

        try:
            if not uk:
                sent = tokenize.sent_tokenize(text)
                sent = [x for x in sent if len(x.split()) >= 3]
            else:
                sent = tokenize_uk.tokenize_text(text)
                sent = [x for x in sent[0] if len([y for y in x if bool(re.search('\w', y))]) >= 3]
                sent = [" ".join(x) for x in sent]
                sent = [re.sub(' (\.|,|!|\?|-)', '\g<1>', x) for x in sent]
                sent = [re.sub(' ,', ',', x) for x in sent]
            current += sent
        except:
            pass
    return current


def main():
    inputs = parse_args()
    lang = inputs.l
    logger.info(f"Clean {lang} tweets")

    cur = pd.read_csv(f'{inputs.data_dir}texts_{lang}.csv', names=['tweets'], header=0)

    if inputs.hashtags:
        wordcloud(hashtags(cur['tweets']), lang, inputs.data_dir)

    cur = clean(list(cur['tweets']) , lang == 'uk')
    if inputs.hashtags:
        wordcloud(hashtags(pd.Series(cur)), lang, inputs.data_dir, n=1)
    logger.info(f"Total number: {len(cur)}")
    # pd.DataFrame(cur).to_csv(f'{inputs.data_dir}cleaned_{lang}.csv')
    print(len(cur))
    cur = set(cur)
    print(len(cur))
    with open(f'{inputs.data_dir}cleaned_{lang}.txt', 'w', encoding='utf-8') as f:
        for line in cur:
            f.write(line + '\n')


def hashtags(texts):
    import numpy as np
    hashtag_re = re.compile("#(\w+)")
    hashtag_list = texts.str.extractall(hashtag_re)
    hashtag_list = list(hashtag_list[0])
    return hashtag_list


def wordcloud(words, lang, dir, n=0):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    from collections import Counter
    logger.info(f"Created a wordcloud for {lang} tweets")
    words = [w.lower() for w in words]
    words_dict = Counter(words)
    wc = WordCloud(width=1000, height=500).generate_from_frequencies(words_dict)
    plt.figure(figsize=(15, 8))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(f"{dir}{lang}_{n}.png", bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('clean_text.log')
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.info('start create annotators')
    main()
