"""Create txt files with ids of russian, german and english Covid-19 related tweets"""
import pandas as pd
import random
import argparse
import logging


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--l",
                        default=None,
                        type=str,
                        required=True,
                        help="which language to sample"
                        )

    parser.add_argument("--n",
                        default=50,
                        type=int,
                        required=False,
                        help="number of ids to sample")

    parser.add_argument("--data_dir",
                        default='../covid19_twitter/',
                        type=str,
                        required=False,
                        help="directory with dailies directory")
    args = parser.parse_args()
    return args


def main():
    from datetime import date

    logger = logging.getLogger(__name__)
    logger.info("Annotators creation")

    inputs = parse_args()
    lang = inputs.l

    startdate = date(2020,7,26)   # start date
    enddate = date(2022,12,17)   # end date
    PATH_CURRENT_DATASET = 'dailies/'
    logger.info("shuffling")
    dates = [date.strftime('%Y-%m-%d') for date in pd.date_range(startdate, enddate, freq='d')]
    dates = random.sample(dates, len(dates))
    samples = []
    for i, date in enumerate(dates):
        try:
            df = pd.read_csv(inputs.data_dir + PATH_CURRENT_DATASET + date + '/' + date + '-dataset.tsv.gz', usecols=['tweet_id', 'lang'], sep='\t',
                             dtype={'lang': str})
        except (IOError, OSError):
            try:
                df = pd.read_csv(inputs.data_dir + PATH_CURRENT_DATASET + date + '/' + date + '-dataset.tsv', usecols=['tweet_id', 'lang'], sep='\t',
                                 dtype={'lang': str})
            except (IOError, OSError):
                logger.info(f'no data on {date}')
                continue
        samples += df.query(f"lang == '{lang}'")['tweet_id'].values.tolist()
        if len(samples) >= inputs.n and i >= 50:
            break
    df = pd.DataFrame()

    cur = pd.DataFrame(random.sample(samples, k=inputs.n)).rename(columns={0: 'tweet_id'})
    cur['lang'] = lang
    df = pd.concat([df, cur])
    with open(f"ids_{lang}.txt", "w") as f:
        f.write('\n'.join(str(id) for id in df['tweet_id'].values.tolist()))


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('read_ids.log')
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.info('start create annotators')
    main()
