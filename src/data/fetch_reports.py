import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from os import getenv
from requests import get
from requests_ntlm import HttpNtlmAuth as ForgeAuth
from src.io.constants import reports


def derive_report_url(report: dict):
    coerce_url_rules = lambda x: '%2F' + x.replace(' ', '%20')
    if report['parent']:
        report_identifier = coerce_url_rules(report['parent']) + coerce_url_rules(report['child'])
    else:
        report_identifier = coerce_url_rules(report['child'])
    url = f"http://10.20.231.55/ReportServer/Pages/ReportViewer.aspx?{report_identifier}&rs:Format=EXCELOPENXML"
    return url


@click.command()
@click.option('--report_name', type=str)
def main(report_name):
    username = getenv("REPORTING_USER")
    password = getenv("REPORTING_PASS")

    if report_name in reports.keys():
        res = get(derive_report_url(reports[report_name]),
                  auth=ForgeAuth(username, password))
        if res.status_code == 200:
            report = res.__dict__['_content']
            with open(f'data/raw/{reports[report_name]["child"]}.xlsx', "wb") as file:
                file.write(report)
                file.close()
        else:
            raise Exception('Could Not Connect.')
    else:
        raise Exception('Invalid Report Option.')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    main()
