import pandas as pd

from ffanalyze import math_utils, teams


def sheet(file_path: str) -> pd.DataFrame:
    df = pd.read_json(file_path)
    # add a bye week to the end
    df.loc[-1] = [0, "Bye Week", df["PtsAg"].mean()]

    abbr = teams.team_abbr()
    joined = df.set_index("Team").join(abbr.set_index("Team"))
    result = joined.copy()

    result["D PCo"] = math_utils.coef(joined["PtsAg"])

    return result


if __name__ == "__main__":
    print(sheet("data/DEFPtsAg.json").sort_values(by="Team"))
