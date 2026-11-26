"""Design dials for Anco Heist.

Everything else in the font is derived from these numbers, so changing one here
and rerunning `python scripts/generate.py` reshapes the whole alphabet.

Tuned for a dense, boxy sign-painter display look (retro game-title feel,
without decorative tails): heavy strokes, boxy squircle corners, crisp
rectangular counters/slots, tight sidebearings, and near-unicase x-height.
"""

# ---- vertical metrics ----------------------------------------------------
CAP = 700        # capital height
XH = 650         # lowercase x-height (near-unicase display proportion)
ASC = 770        # lowercase ascender (compact, no tall tails)
DESC = -165      # descender (compact, no long tails)

# ---- stroke weights ------------------------------------------------------
WV = 205         # vertical stem weight
WH = 155         # horizontal weight (capitals)
WHL = 148        # horizontal weight (lowercase)
WD = 205         # diagonal stroke weight

# ---- corner shape --------------------------------------------------------
RO = 86          # outer corner radius of boxy capitals
ROL = 80         # outer corner radius of boxy lowercase
SOFT_CONVEX = 5  # subtle rounding on outside corners
SOFT_CONCAVE = 3 # subtle rounding on inside corners

# ---- spacing -------------------------------------------------------------
SB_STR = 26      # sidebearing next to a straight stem
SB_RND = 22      # next to a round/boxy side
SB_OPEN = 14     # next to a diagonal or open side

DIGIT_ADV = 560  # all digits share this width (tabular)
