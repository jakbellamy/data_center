import logging
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from src.constants import funding_by_referral_columns
from src.io.Database.Database import Database
from src.io.Files.Files import retrieve_latest_file


def main():
    raw_referrals = pd.read_excel('../../data/raw/Funding By Referral Source (2006).xlsx',
                                  sheet_name='Details',
                                  skiprows=5,
                                  header=None,
                                  names=funding_by_referral_columns)
    referral_changes = pd.read_csv(retrieve_latest_file('referral_changes', 'raw'))


# if __name__ == '__main__':
#     log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_fmt)
#
#     # not used in this stub but often useful for finding various files
#     project_dir = Path(__file__).resolve().parents[2]
#
#     # find .env automagically by walking up directories until it's found, then
#     # load up the .env entries as environment variables
#     load_dotenv(find_dotenv())
#     main()
