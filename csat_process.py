import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)


csat_path = './data/raw/Customer Satisfaction Surveys - Jan - June 21.xlsx'
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

csat = csat.join(referrals[['Funded Month', 'Loan Officer', 'Referral Source', 'Referral Name']]).dropna(axis=1, how='all')
csat.columns = ['LOS System', 'Q1 Score', 'Q2 Score','Q3 Score', 'Q4 Score',
                'Q5 Score','Q6 Score', 'Strength Feedback', 'Recommendation Feedback',
                'Borrower Last Name','Borrower First Name', 'Borrower Email',
                'Funded Month', 'Loan Officer', 'Referral Source', 'Referral Name']


def create_word_cloud(df: 'pd.dataframe', col_name: str):
    text = df[col_name].dropna().values
    wordcloud = WordCloud(
        width=3000,
        height=2000,
        background_color='white',
        stopwords=STOPWORDS).generate(str(text))
    fig = plt.figure(
        figsize=(40, 30),
        facecolor='k',
        edgecolor='white')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
