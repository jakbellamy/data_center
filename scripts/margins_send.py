from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import logging
import pandas as pd
from src.io.Email.Email import Message, parse_out_email


def main():
    report_path = '/Users/jakobbellamy/Desktop/Margins Email/Margins Report.xlsx'
    send_list = pd.read_excel(report_path, sheet_name='Final Send List')
    send_list['email'] = send_list['email'].apply(parse_out_email)

    html_path = '/Users/jakobbellamy/Desktop/Margins Email/index.html'
    html_string = Path(html_path).read_text()

    for _,row in send_list.iterrows():
        html = html_string.replace('{VAR: mtd_adjusted_margin}', str(row['mtd_adjusted_margin']))
        html = html.replace('{VAR: ytd_adjusted_margin}', str(row['ytd_adjusted_margin']))
        html = html.replace('{VAR: lo_rank}', str(row['lo_rank']))

        msg = Message(
            subject='January - June 2021 Margins Report',
            body=html,
            to_recipients=row['email'],
            cc_recipients=['Phil.Blankstein@supremelending.com']
        )
        # msg.show()
        print(html)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    main()
