import os
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

csat_path = './data/raw/Customer Satisfaction Surveys (3099).xlsx'
referrals_path = './data/raw/Funding By Referral Source (2006).xlsx'

csat = pd.read_excel(csat_path, sheet_name='LO Details', skiprows=5)
csat.columns = ['Loan Number'] + list(csat.columns[1:])
csat.dropna(subset=['LOS System'], inplace=True)
csat['Loan Number'] = csat['Loan Number'].apply(pd.to_numeric)
csat.set_index('Loan Number', inplace=True)

referrals = pd.read_excel(referrals_path, sheet_name='Details', skiprows=4)
referrals.columns = [col.split('\n')[0] for col in referrals.columns]
referrals['Loan Number'] = referrals['Loan Number'].apply(pd.to_numeric)
referrals.set_index('Loan Number', inplace=True)

df = csat.join(referrals[['Funded Month', 'Loan Officer']])


def run_mr_process():
    bucket = []
    for file in [f for f in os.listdir('/Users/jakobbellamy/Desktop/CSAT Files') if 'xlsx' in f]:
        csat_path = f'/Users/jakobbellamy/Desktop/CSAT Files/{file}'
        csat = pd.read_excel(csat_path, sheet_name='LO Details', skiprows=5)
        csat.columns = ['Loan Number'] + list(csat.columns[1:])
        csat.dropna(subset=['LOS System'], inplace=True)
        csat['Loan Number'] = csat['Loan Number'].apply(pd.to_numeric)
        csat.set_index('Loan Number', inplace=True)
        df = csat.join(referrals[['Funded Month', 'Loan Officer', 'Referral Source', 'Referral Name']])
        bucket += [df]
    return pd.concat(bucket)


my_reports = run_mr_process()
my_reports = my_reports[['LOS System', 'Top Box CSAT Feedback', 'Strength Feedback', 'Recommendation Feedback',
                         'Notes Feedback', 'Borrower Last Name', 'Borrower First Name', 'Borrower Email',
                         'Funded Month', 'Loan Officer', 'Referral Source', 'Referral Name']]

def run_old_process():
    bucket = []
    for file in [f for f in os.listdir('/Users/jakobbellamy/Desktop/CSAT Files') if 'xlsx' not in f and 'xls' in f]:
        try:
            csat_path = f'/Users/jakobbellamy/Desktop/CSAT Files/{file}'
            df = pd.read_excel(csat_path,
                               sheet_name='Details',
                               skiprows=2)
            df.columns = [x.split('\n')[0] for x in df.columns]
            df.rename(columns={'Branch': 'Loan Number'}, inplace=True)
            df = df[df['Loan Number'].apply(lambda x: len(str(x)) == 12)]
            df['Loan Number'] = df['Loan Number'].apply(pd.to_numeric)
            df.set_index('Loan Number', inplace=True)
            df = df.join(referrals[['Funded Month', 'Loan Officer', 'Referral Source', 'Referral Name']])
            df['LOS System'] = 'Unplugged'
            df = df[['LOS System', 'Top Box CSAT', 'Strength', 'Recommendation', 'Notes', 'Borrower Last Name',
                     'Borrower First Name', 'Borrower Email Address', 'Funded Month', 'Loan Officer', 'Referral Source',
                     'Referral Name']]
            # df.columns = my_reports.columns
            bucket += [df]
        except:
            print(file, ' not behaving very well >:(')
    return pd.concat(bucket)


old_reports = run_old_process()
old_reports.columns = my_reports.columns

full_reports = pd.concat([my_reports, old_reports])

def create_word_cloud(dataframe: 'pd.DataFrame', col_name: str):
    text = dataframe[col_name].dropna().values
    wordcloud = WordCloud(
        width=3000,
        height=2000,
        background_color='white',
        stopwords=STOPWORDS).generate(str(text))
    fig = plt.figure(
        figsize=(40, 30),
        facecolor='white',
        edgecolor='white')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
