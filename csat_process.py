import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

csat_path = './data/raw/Customer Satisfaction Surveys (3099).xlsx'
referrals_path = './data/raw/Funding By Referral Source (2006).xlsx'

csat = pd.read_excel(csat_path, sheet_name='LO Details', skiprows=5)
csat.columns = ['Loan Number'] + list(csat.columns[1:])
csat.dropna(subset=['LOS System'], inplace=True)
csat.set_index('Loan Number', inplace=True)

referrals = pd.read_excel(referrals_path, sheet_name='Details', skiprows=4)
referrals.columns = [col.split('\n')[0] for col in referrals.columns]
referrals.set_index('Loan Number', inplace=True)


def create_word_cloud(col_name: str):
    text = csat[col_name].dropna().values
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
