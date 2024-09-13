import pprint
from unicodedata import name
import pandas as pd

def qb_stats():
    number_cols = ['GP', 'Pts', 'PaY', 'PaTd', 'Int', 'RuAt', 'RuY', 'RuTd', 'Tar', 'Rec', 'RecY', 'RecTd', 'RetY', 'RetTd', 'TwPt', 'Fum']
    qbs = pd.read_json('data/QBs.json')

    # cleanup
    for col in number_cols:
        qbs[col] = pd.to_numeric(qbs[col], errors='coerce')
        qbs[col] = qbs[col].fillna(0)

    # total yards
    qbs['TotY'] = qbs['PaY'] + qbs['RuY']

    print(qbs.dtypes)
    pprint.pp(qbs)

if __name__ == '__main__':
    qb_stats()
