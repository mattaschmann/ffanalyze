import re

import pandas as pd
from pandas.io.formats.style import StylerRenderer
pd.options.mode.chained_assignment = None  # default='warn'

def sheet(file_path: str) -> pd.DataFrame:
    number_cols = ['GP', 'Pts', 'PaY', 'PaTd', 'Int', 'RuAt', 'RuY', 'RuTd', 'Tar', 'Rec', 'RecY', 'RecTd', 'RetY', 'RetTd', 'TwPt', 'Fum']
    df = pd.read_json(file_path)
    qbs = df.copy()

    # cleanup
    for col in number_cols:
        qbs[col] = pd.to_numeric(df[col].replace('-', 0))

    # needs to have actually played and scored positive points
    result = qbs.query('GP > 0 & Pts > 0')

    # dynamic columns
    result['Yds'] = qbs[['PaY', 'RuY']].sum(axis = 1)        # total yards
    result['Pts/Yd'] = qbs['Pts'] / result['Yds']            # Points per yard
    result['Yds/G'] = result['Yds'] / qbs['GP']              # Yards per game
    result['Pts/G'] = qbs['Pts'] / qbs['GP']                 # Points per game
    result['P/Y Z'] = z_score(result['Pts/Yd'])              # Points per yard z-score
    result['Y/G Z'] = z_score(result['Yds/G'])               # Yards per game z-score
    result['P/G Z'] = z_score(result['Pts/G'])               # Points per game z-score
    result['Zval'] = (result['Y/G Z'] + result['P/G Z']) / 2 # Z value score?

    return result

def style_sheet(file_path: str) -> StylerRenderer:
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    result = sheet(file_path)

    def highlight_owner(val: str):
        match val:
            case 'Injured Reserves':
                return 'background-color: #b7e1cd; color: black'
            case 'FA':
                return 'background-color: #c9daf8; color: black'
            case _:
                if re.match(r'^W\ .*', val):
                    return 'background-color: #ffd966; color: black'

                return ''

    styled = result.sort_values(by='Zval', ascending=False)\
        .style\
        .map(highlight_owner, subset='Owner')\
        .format(precision=2, subset=['Pts', 'Pts/Yd', 'P/Y Z', 'Pts/G', 'Y/G Z', 'P/G Z', 'Zval'])\
        .format(precision=0, subset=['Yds/G'])

    return styled

def z_score(s) -> float:
    return (s - s.mean()) / s.std()

if __name__ == '__main__':
    style = style_sheet('data/QBs.json')
    # style.data.to_excel('out/qbs.xlsx')
    # print(df.style.to_html())
    # print(df)
