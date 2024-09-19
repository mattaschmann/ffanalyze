import os

import pandas as pd
from pandas.io.formats.style import StylerRenderer

from ffanalyze import defense, format, math_utils
from ffanalyze.col_names import ColNames
from ffanalyze.position import Position

pd.options.mode.chained_assignment = None  # default='warn'

dirname = os.path.dirname(__file__)

RET_YDS_PT = 50  # return yards per point

def sheet(position: Position) -> pd.DataFrame:
    match position:
        case Position.K:
            number_cols = ["GP", "Pts", "0-19", "20-29", "30-39", "40-49", "50+", "Pat"]
        case Position.DEF:
            number_cols = [
                "GP",
                "Pts",
                "PtsVs",
                "Sack",
                "Safe",
                "Int",
                "FumR",
                "TDs",
                "BlkK",
                "RetTD",
            ]
        case _:
            number_cols = [
                "GP",
                "Pts",
                "PaY",
                "PaTd",
                "Int",
                "RuAt",
                "RuY",
                "RuTd",
                "Tar",
                "Rec",
                "RecY",
                "RecTd",
                "RetY",
                "RetTd",
                "TwPt",
                "Fum",
            ]

    df = pd.read_json(os.path.join(dirname, f"../../data/{position.value}s.json"))
    pos_df = df.copy()

    # cleanup
    for col in number_cols:
        pos_df[col] = pd.to_numeric(df[col].replace("-", 0))

    # needs to have actually played and scored positive points
    result = pos_df.query("GP > 0 & Pts > 0")

    # dynamic columns
    match position:  # total opp
        case Position.QB:
            col_names = ColNames("Y")
            result[col_names.opp_col] = pos_df[["PaY", "RuY"]].sum(axis=1)
        case Position.WR | Position.RB | Position.TE:
            col_names = ColNames("O")
            result[col_names.opp_col] = pos_df[["RuAt", "Tar"]].sum(axis=1) + (pos_df["RetY"] / RET_YDS_PT)
        case Position.K:
            col_names = ColNames("O")
            result[col_names.opp_col] = pos_df[["Pat", "0-19", "20-29", "30-39", "40-49", "50+"]].sum(axis=1)
        case Position.DEF:
            col_names = ColNames("O")
            result[col_names.opp_col] = pos_df[["Sack", "Safe", "Int", "FumR", "TDs", "BlkK", "RetTD"]].sum(axis=1)

    result[col_names.pt_opp_col] = pos_df["Pts"] / result[col_names.opp_col]  # Points per opp
    result[col_names.ops_g_col] = result[col_names.opp_col] / pos_df["GP"]  # Ops per game
    result["Pts/G"] = pos_df["Pts"] / pos_df["GP"]  # Points per game
    result[col_names.pt_opp_z_col] = math_utils.z_score(result[col_names.pt_opp_col])  # Points per opp z-score
    result[col_names.ops_g_z_col] = math_utils.z_score(result[col_names.ops_g_col])  # Ops per game z-score
    result["P/G Z"] = math_utils.z_score(result["Pts/G"])  # Points per game z-score
    result["Zval"] = (
        (result[col_names.pt_opp_z_col] / 2) + (result[col_names.ops_g_z_col] / 2) + result["P/G Z"]
    ) / 2  # Z value score

    # move opponent to end
    opponent = result.pop("Opp")
    result["Opp"] = opponent

    # get defense
    pts_ag = defense.sheet(os.path.join(dirname, f"../../data/{position.value}PtsAg.json"))
    result = result.merge(pts_ag, left_on="Opp", right_on="Abbr")

    # expected points
    result["EP"] = result["Pts/G"] * result["D PCo"]

    # remove unneeded columns
    result = result.drop(["Abbr"], axis=1)

    return result


def style_sheet(sheet: pd.DataFrame, position: Position) -> StylerRenderer:
    match position:
        case Position.QB:
            opp_abbr = "Y"
        case _:
            opp_abbr = "O"

    return format.style_sheet(sheet, ColNames(opp_abbr), position)


# if __name__ == '__main__':
# print(qb_sheet())
