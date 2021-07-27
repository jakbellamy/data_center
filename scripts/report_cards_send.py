from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import logging
import pandas as pd
from src.io.Email.Email import Message, parse_out_email


def main():
    report_path = '/Users/jakobbellamy/Desktop/email/distribution_list.csv'
    send_list = pd.read_csv(report_path)


    html_path = '/Users/jakobbellamy/Desktop/email/index.html'
    html_string = Path(html_path).read_text()

    for _,row in send_list[:1].iterrows():
        for _, record in send_list.iterrows():
            partner_emails = [v for k, v in record.items() if k.startswith('Partner') and isinstance(v, str)]
            supreme_emails = [v for k, v in record.items() if k.startswith('Supreme') and isinstance(v, str)]

            html = html_string
            attachment_path = record['Attachment']
            name = record['ASA']


            msg = Message(
                subject=f'{name} & Supreme Lending May Partnership Update',
                body=html,
                to_recipients=supreme_emails,
                cc_recipients=[partner_emails]
            )
            msg.add_attachment(attachment_path)
            msg.show()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    main()
