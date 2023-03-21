"""Create csv files with textual data"""
import pandas as pd
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

    parser.add_argument("--data_dir",
                        default='',
                        type=str,
                        required=False,
                        help="directory with dailies directory")
    args = parser.parse_args()
    return args


def main():

    logger.info("Annotators creation")

    inputs = parse_args()
    lang = inputs.l
    try:
        df = pd.read_csv(f'data/{lang}.csv', header=0, usecols=['text'], dtype={'text': str})
        df.to_csv(f'{inputs.data_dir}texts_{lang}.csv')

    except FileNotFoundError:
        print('No data found')



if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('read_tweets.log')
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.info('start create annotators')
    main()
