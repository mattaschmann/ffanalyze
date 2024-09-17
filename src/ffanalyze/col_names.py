class ColNames:
    opp_col: str
    pt_opp_col: str
    ops_g_col: str
    pt_opp_z_col: str
    ops_g_z_col: str

    def __init__(self, opp_abbr: str) -> None:
        self.opp_col = f'{opp_abbr}s'
        self.pt_opp_col = f'Pts/{opp_abbr}'
        self.ops_g_col = f'{opp_abbr}/G'
        self.pt_opp_z_col = f'P/{opp_abbr} Z'
        self.ops_g_z_col = f'{opp_abbr}/G Z'
