from matplotlib.colors import LinearSegmentedColormap

rwg_cm = LinearSegmentedColormap.from_list('rwg_cm', (
    # Edit this gradient at https://eltos.github.io/gradient/#FF0000-FFFFFF-00FF00
    (0.000, (1.000, 0.000, 0.000)),
    (0.500, (1.000, 1.000, 1.000)),
    (1.000, (0.000, 1.000, 0.000))))

dark_rwg_cm = LinearSegmentedColormap.from_list('dark_rwg_cm', (
    # Edit this gradient at https://eltos.github.io/gradient/#CC0000-FFFFFF-6AA84F
    (0.000, (0.800, 0.000, 0.000)),
    (0.500, (1.000, 1.000, 1.000)),
    (1.000, (0.416, 0.659, 0.310))))

cwy_cm = LinearSegmentedColormap.from_list('cwy_cm', (
    # Edit this gradient at https://eltos.github.io/gradient/#00FFFF-FFFFFF-FFFF00
    (0.000, (0.000, 1.000, 1.000)),
    (0.500, (1.000, 1.000, 1.000)),
    (1.000, (1.000, 1.000, 0.000))))

bwo_cm = LinearSegmentedColormap.from_list('bwo_cm', (
    # Edit this gradient at https://eltos.github.io/gradient/#3300FF-FFFFFF-FF9900
    (0.000, (0.200, 0.000, 1.000)),
    (0.500, (1.000, 1.000, 1.000)),
    (1.000, (1.000, 0.600, 0.000))))
