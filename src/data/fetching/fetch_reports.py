import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from os import getenv
from requests import get
from requests_ntlm import HttpNtlmAuth as ForgeAuth
from src.constants import myreports_options


def derive_report_url(report: dict):
    coerce_url_rules = lambda x: '%2F' + x.replace(' ', '%20')
    if report['parent']:
        report_identifier = coerce_url_rules(report['parent']) + coerce_url_rules(report['child'])
    else:
        report_identifier = coerce_url_rules(report['child'])
    url = f"http://10.20.231.55/ReportServer/Pages/ReportViewer.aspx?{report_identifier}&rs:Format=EXCELOPENXML"
    return url


def fetch_report(report_name):
    username = getenv("REPORTING_USER")
    password = getenv("REPORTING_PASS")
    if report_name in myreports_options.keys():
        if myreports_options[report_name]['parent'] == 'raw':
            res = get(myreports_options[report_name]['child'],
                      auth=ForgeAuth(username, password))
        else:
            res = get(derive_report_url(myreports_options[report_name]),
                      auth=ForgeAuth(username, password))
        if res.status_code == 200:
            report = res.__dict__['_content']
            return report
        else:
            raise Exception('Could Not Connect.')
    else:
        raise Exception('Invalid Report Option.')


@click.command()
@click.option('--report_name', type=str)
def main(report_name):
    report = fetch_report(report_name)
    with open(f'data/raw/{myreports_options[report_name]["child"]}.xlsx', "wb") as file:
        file.write(report)
        file.close()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    main()
