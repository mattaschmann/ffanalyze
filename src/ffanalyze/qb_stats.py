import pandas as pd
from pandas.io.formats.style import StylerRenderer
import os

from ffanalyze import defense, math_utils, format

pd.options.mode.chained_assignment = None  # default='warn'

dirname = os.path.dirname(__file__)

def sheet() -> pd.DataFrame:
    number_cols = ['GP', 'Pts', 'PaY', 'PaTd', 'Int', 'RuAt', 'RuY', 'RuTd', 'Tar', 'Rec', 'RecY', 'RecTd', 'RetY', 'RetTd', 'TwPt', 'Fum']
    df = pd.read_json(os.path.join(dirname, '../../data/QBs.json'))
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
    result['P/Y Z'] = math_utils.z_score(result['Pts/Yd'])   # Points per yard z-score
    result['Y/G Z'] = math_utils.z_score(result['Yds/G'])    # Yards per game z-score
    result['P/G Z'] = math_utils.z_score(result['Pts/G'])    # Points per game z-score
    result['Zval'] = (result['Y/G Z'] + result['P/G Z']) / 2 # Z value score

    # get defense
    pts_ag = defense.sheet(os.path.join(dirname, '../../data/QBPtsAg.json'))
    df = pd.read_json(os.path.join(dirname, '../../data/QBs.json'))

    return result

def style_sheet(sheet: pd.DataFrame) -> StylerRenderer:
    return format.style_sheet(sheet, opp_col='Yds',
                              pt_opp_col='Pts/Yd',
                              opp_g_col='Yds/G',
                              pt_opp_z_col='P/Y Z',
                              opp_g_z_col='Y/G Z',
                              )

if __name__ == '__main__':
    print(sheet())
    # style = style_sheet('data/QBs.json')
    # style.data.to_excel('out/qbs.xlsx')
    # print(df.style.to_html())
    # print(df)
