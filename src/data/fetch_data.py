import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from src.io.Database.Database import Database
from os import getenv
import datetime


@click.command()
@click.option('--dataset',
              default='asa',
              help='ex. margins',
              type=str)
@click.option('--output',
              default='data/raw',
              help='Output Folder',
              type=click.Path(exists=True))
@click.option('--worksheet',
              default=False,
              help='If True, outputs as excel file with tabs.',
              type=bool)
def fetch_data(dataset, output, worksheet):
    db_production = Database(getenv('db_production'))
    db_margins = Database(getenv('db_margins'))

    """ Runs SQL or Fetch request scripts to import new data from the web.
    """
    logger = logging.getLogger(__name__)
    dataset = dataset if dataset else 'asa'

    dataset_options = {
        'margins': [
            (db_margins, 'Commission Rates'),
            (db_margins, 'LO Emails'),
            (db_margins, 'Loan Officer'),
            (db_margins, 'Name Key')
        ],
        'asa': [
            (db_production, '_temp_asa_production'),
            (db_production, 'additional_payments'),
            (db_production, 'asa_accounts'),
            (db_production, 'asa_contracts'),
            (db_production, 'lite_accounts'),
            (db_production, 'lite_contracts'),
            (db_production, 'lite_production')
        ]
    }

    dataset_options = {
        'margins': {
            'database': db_margins,
            'tables': [
                'Commission Rates',
                'LO Emails',
                'Loan Officer',
                'Name Key'
            ]
        },
        'asa': {
            'database': db_production,
            'tables': [
                '_temp_asa_production',
                'additional_payments',
                'asa_accounts',
                'asa_contracts',
                'lite_accounts',
                'lite_contracts',
                'lite_production'
            ]
        }
    }

    if dataset in dataset_options.keys():
        logger.info('Fetching Dataset: ' + dataset)
        for db, table in dataset_options[dataset]:
            df = db.fetch_table(table)
            uniq_filename = table + '__' \
                            + str(datetime.datetime.now().date()) + '_' \
                            + str(datetime.datetime.now().time()).replace(':', '.')
            df.to_csv(output + f'/{uniq_filename}.csv', index=False)

    else:
        logger.info('No Dataset Found: ' + dataset)
        return -1


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    fetch_data()
