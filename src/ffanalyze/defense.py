import pandas as pd

from ffanalyze import teams, math_utils

def sheet(file_path: str) -> pd.DataFrame:
    df = pd.read_json(file_path)

    abbr = teams.team_abbr()
    joined = df.set_index('Team').join(abbr.set_index('Team'))
    result = joined.copy()

    result['P/G Z'] = math_utils.z_score(joined['PtsAg'])

    return result

# def qb_def(file: str) -> pd.DataFrame:


if __name__ == '__main__':
    print(sheet('data/DEFPtsAg.json').sort_values(by='Team'))