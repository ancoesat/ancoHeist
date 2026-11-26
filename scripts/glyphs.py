"""Glyph drawings for Anco Heist.

Each entry: name -> (unicode or None, function returning a Path, left sidebearing, right sidebearing)
Edit the numbers here and run scripts/generate.py to rebuild the UFO source.

Styled for a dense, boxy sign-painter display look (retro game-title feel,
with clean tail-free terminals and crisp rectangular counters/slots).
"""
from shapes import U, D, I, rect, poly, rrect, ring, disk, diag, seg, rotate, move, mirror_x
from tuning import (CAP, XH, ASC, DESC, WV, WH, WHL, WD, RO, ROL,
                    SB_STR, SB_RND, SB_OPEN, DIGIT_ADV)

G = {}


def glyph(name, uni, lsb=SB_STR, rsb=SB_STR, clip=None):
    def deco(fn):
        G[name] = dict(uni=uni, fn=fn, lsb=lsb, rsb=rsb, clip=clip)
        return fn
    return deco


def cring(x0, y0, x1, y1, r=RO, ri=10):
    return ring(x0, y0, x1, y1, r, WV, WH, ri=ri)


def lring(x0, y0, x1, y1, r=ROL, ri=10):
    return ring(x0, y0, x1, y1, r, WV, WHL, ri=ri)


# ---- closed-counter helpers ---------------------------------------------
# Boxy squircle outer frame minus crisp rectangular counters / horizontal slots.

def box(w, h, r=ROL):
    """Solid rounded rectangle anchored at the origin."""
    return rrect(0, 0, w, h, r)


def hole(p, x0, y0, x1, y1, r=8):
    """Cut a crisp rectangular counter out of a glyph."""
    return D(p, rrect(x0, y0, x1, y1, r))


def slot(p, y0, y1, x0, x1):
    """Cut a horizontal band, normally running off one edge to open it."""
    return D(p, rect(x0, y0, x1, y1))


def boxed(w, h, upper, lower, r=ROL, cw=96):
    """Boxy rounded rectangle with an upper and a lower opening.

    `upper` / `lower` are (y0, y1, side) where side is "left", "right", or None (closed).
    """
    p = box(w, h, r)
    cx0, cx1 = (w - cw) / 2, (w + cw) / 2
    for y0, y1, side in (upper, lower):
        if side is None:
            p = hole(p, cx0, y0, cx1, y1, 8)
        elif side == "left":
            p = slot(p, y0, y1, -10, cx1)
        else:
            p = slot(p, y0, y1, cx0, w + 10)
    return p


# ---- capitals ------------------------------------------------------------
@glyph("A", 0x41, SB_OPEN, SB_OPEN, clip=(0, 0, 580, CAP))
def _():
    # Heavy flat-topped tapered A: unmistakably distinct from R while keeping boxy display weight
    return U(diag(105, 0, 235, CAP, WD - 10),
             diag(475, 0, 345, CAP, WD - 10),
             rect(200, CAP - WH, 380, CAP),
             rect(115, 130, 465, 130 + 135))


@glyph("B", 0x42, SB_STR, SB_RND)
def _():
    # Boxy B with slight waist and two crisp, generous rectangular counters
    outer = U(rrect(0, 295, 500, CAP, (0, 78, 78, 0)),
              rrect(0, 0, 525, 415, (0, 86, 86, 0)))
    top_hole = rrect(WV, 415, 500 - 180, CAP - 140, (0, 12, 12, 0))
    bot_hole = rrect(WV, 140, 525 - 180, 295, (0, 12, 12, 0))
    return D(outer, top_hole, bot_hole)


@glyph("C", 0x43, SB_RND, SB_OPEN)
def _():
    return D(cring(0, 0, 500, CAP), rect(260, 240, 600, 460))


@glyph("D", 0x44, SB_STR, SB_RND)
def _():
    return cring(0, 0, 515, CAP, (0, RO, RO, 0))


@glyph("E", 0x45, SB_STR, SB_OPEN)
def _():
    return U(rect(0, 0, WV, CAP), rect(0, CAP - WH, 445, CAP),
             rect(0, 278, 415, 422), rect(0, 0, 450, WH))


@glyph("F", 0x46, SB_STR, SB_OPEN)
def _():
    return U(rect(0, 0, WV, CAP), rect(0, CAP - WH, 445, CAP),
             rect(0, 278, 415, 422))


@glyph("G", 0x47, SB_RND, SB_STR)
def _():
    # Boxy G: rectangular right slot and clean inner horizontal bar
    w = 515
    p = cring(0, 0, w, CAP)
    p = D(p, rect(255, 345, w + 20, CAP - WH))
    return U(p, rect(265, 245, w, 365))


@glyph("H", 0x48)
def _():
    return U(rect(0, 0, WV, CAP), rect(510 - WV, 0, 510, CAP),
             rect(WV, 275, 510 - WV, 425))


@glyph("I", 0x49)
def _():
    return rect(0, 0, WV, CAP)


@glyph("J", 0x4A, SB_OPEN, SB_STR)
def _():
    # Clean boxy J without protruding tail
    return D(cring(0, 0, 455, CAP, (RO, RO, 0, 0)),
             rect(-10, 240, 455 - WV, CAP + 10))


@glyph("K", 0x4B, SB_STR, SB_OPEN, clip=(0, 0, 530, CAP))
def _():
    return U(rect(0, 0, WV, CAP),
             diag(120, 230, 445, CAP, WD - 10),
             diag(445, 0, 220, 410, WD - 10))


@glyph("L", 0x4C, SB_STR, SB_OPEN)
def _():
    return U(rect(0, 0, WV, CAP), rect(0, 0, 430, WH))


@glyph("M", 0x4D, SB_STR, SB_STR)
def _():
    # Boxy M: 3 crisp vertical stems with flat top & open bottom slots
    w, mv = 740, 198
    cw = (w - 3 * mv) / 2
    p = box(w, CAP, (0, 0, RO, 0))
    return D(p,
             rect(mv, -10, mv + cw, CAP - WH),
             rect(w - mv - cw, -10, w - mv, CAP - WH))


@glyph("N", 0x4E, SB_STR, SB_STR, clip=(0, 0, 530, CAP))
def _():
    return U(rect(0, 0, WV, CAP), rect(530 - WV, 0, 530, CAP),
             diag(435, 0, 95, CAP, WD - 15))


@glyph("O", 0x4F, SB_RND, SB_RND)
def _():
    return cring(0, 0, 520, CAP)


@glyph("P", 0x50, SB_STR, SB_RND)
def _():
    outer = U(rect(0, 0, WV, CAP), rrect(0, 255, 505, CAP, (0, RO, RO, 0)))
    return hole(outer, WV, 255 + 140, 505 - 185, CAP - 145, 10)


@glyph("Q", 0x51, SB_RND, SB_RND)
def _():
    # Boxy O with a short, clean straight stub inside/bottom-right (no long tail)
    return U(cring(0, 0, 520, CAP), rect(355, -55, 505, 145))


@glyph("R", 0x52, SB_STR, SB_OPEN, clip=(0, 0, 540, CAP))
def _():
    # Boxy R: clear rounded upper bowl + crisp waist notch + clean angled/stepped leg (no tail)
    bowl = rrect(0, 285, 515, CAP, (0, 86, RO, 0))
    stem = rect(0, 0, WV, CAP)
    leg = diag(440, 0, 315, 330, WD - 15)
    p = U(stem, bowl, leg)
    return hole(p, WV, 415, 515 - 180, CAP - 145, 10)


@glyph("S", 0x53, SB_RND, SB_RND)
def _():
    # Boxed S: squircle frame with two crisp opposing rectangular slots
    w = 505
    t = 148
    return boxed(w, CAP, (CAP - t - 102, CAP - t, "right"),
                 (t, t + 102, "left"), r=RO, cw=108)


@glyph("T", 0x54, SB_OPEN, SB_OPEN)
def _():
    return U(rect(0, CAP - WH, 500, CAP),
             rect(250 - WV / 2, 0, 250 + WV / 2, CAP))


@glyph("U", 0x55)
def _():
    return D(cring(0, 0, 510, CAP, (RO, RO, 0, 0)),
             rect(WV, 280, 510 - WV, CAP + 10))


@glyph("V", 0x56, SB_OPEN, SB_OPEN, clip=(0, 0, 560, CAP))
def _():
    return U(diag(280, 0, 95, CAP, WD), diag(280, 0, 465, CAP, WD))


@glyph("W", 0x57, SB_OPEN, SB_OPEN, clip=(0, 0, 800, CAP))
def _():
    return U(diag(210, 0, 88, CAP, WD - 10), diag(210, 0, 400, 530, WD - 10),
             diag(590, 0, 400, 530, WD - 10), diag(590, 0, 712, CAP, WD - 10))


@glyph("X", 0x58, SB_OPEN, SB_OPEN, clip=(0, 0, 550, CAP))
def _():
    return U(diag(95, 0, 455, CAP, WD - 5), diag(455, 0, 95, CAP, WD - 5))


@glyph("Y", 0x59, SB_OPEN, SB_OPEN, clip=(0, 0, 550, CAP))
def _():
    return U(diag(275, 285, 90, CAP, WD - 5), diag(275, 285, 460, CAP, WD - 5),
             rect(275 - WV / 2, 0, 275 + WV / 2, 325))


@glyph("Z", 0x5A, SB_OPEN, SB_OPEN, clip=(0, 0, 490, CAP))
def _():
    return U(rect(0, CAP - WH, 475, CAP), rect(0, 0, 490, WH),
             diag(100, WH - 10, 380, CAP - WH + 10, WD - 10))


# ---- lowercase -----------------------------------------------------------
def arch(x0, x1, top=XH, r=ROL):
    """n-shaped boxy arch: flat left, rounded top-right, crisp rectangular bottom slot."""
    return D(ring(x0, 0, x1, top, (0, 0, r, 0), WV, WHL, ri=8),
             rect(x0 + WV, -10, x1 - WV, WHL + 20))


def bowl(r):
    return lring(0, 0, 500, XH, r)


@glyph("a", 0x61, SB_RND, SB_STR)
def _():
    # Boxy a: clean left upper slot + crisp lower rectangular counter (no tail)
    t = 142
    return boxed(500, XH, (XH - t - 94, XH - t, "left"),
                 (t, t + 104, None), r=(ROL, 0, ROL, ROL), cw=96)


@glyph("b", 0x62, SB_STR, SB_RND)
def _():
    return U(bowl((0, ROL, ROL, 0)), rect(0, 0, WV, ASC))


@glyph("c", 0x63, SB_RND, SB_OPEN)
def _():
    return D(lring(0, 0, 475, XH), rect(245, 210, 600, 440))


@glyph("d", 0x64, SB_RND, SB_STR)
def _():
    return U(bowl((ROL, 0, 0, ROL)), rect(500 - WV, 0, 500, ASC))


@glyph("e", 0x65, SB_RND, SB_OPEN)
def _():
    # Boxy e: crisp upper rectangular counter + clean right lower slot
    t = 142
    y_ap = t + 95
    return boxed(500, XH, (y_ap + 125, XH - t, None),
                 (t, y_ap, "right"), r=(ROL, ROL, ROL, ROL), cw=96)


@glyph("f", 0x66, SB_OPEN, SB_OPEN)
def _():
    # Compact boxy f without sweeping hook/tail
    return U(D(rrect(35, 0, 355, ASC, (0, 0, 0, ROL)),
               rect(35 + WV, -10, 410, ASC - WHL)),
             rect(0, XH - WHL - 95, 345, XH - 95))


@glyph("g", 0x67, SB_RND, SB_STR)
def _():
    # Boxy g with compact straight-bottom descender (no long sweeping tail)
    w, t = 500, 142
    head = lring(0, 0, w, XH, (ROL, 0, 0, ROL))
    stem = rect(w - WV, DESC, w, XH)
    foot = rrect(30, DESC, w, DESC + 130, (45, 0, 0, 0))
    return U(head, stem, foot)


@glyph("h", 0x68)
def _():
    return U(arch(0, 500), rect(0, 0, WV, ASC))


@glyph("i", 0x69)
def _():
    return U(rect(0, 0, WV, XH - 135), rrect(0, XH - 75, WV, XH + 65, 24))


@glyph("j", 0x6A, SB_OPEN, SB_STR)
def _():
    # Compact boxy j without long sweeping tail
    hook = D(rrect(0, DESC, 290, 120, (0, 65, 0, 0)),
             rect(-60, DESC + 130, 290 - WV, 260))
    return U(hook, rect(290 - WV, -20, 290, XH - 135),
             rrect(290 - WV, XH - 75, 290, XH + 65, 24))


@glyph("k", 0x6B, SB_STR, SB_OPEN, clip=(0, 0, 505, ASC))
def _():
    return U(rect(0, 0, WV, ASC),
             diag(120, 185, 420, XH, WD - 12),
             diag(425, 0, 220, 350, WD - 12))


@glyph("l", 0x6C)
def _():
    return rect(0, 0, WV, ASC)


@glyph("m", 0x6D)
def _():
    # Boxy m: twin of n, 3 crisp vertical stems, open bottom slots, square top-left
    w, mv = 740, 198
    cw = (w - 3 * mv) / 2
    return D(box(w, XH, (0, 0, ROL, 0)),
             rect(mv, -10, mv + cw, XH - WHL),
             rect(w - mv - cw, -10, w - mv, XH - WHL))


@glyph("n", 0x6E)
def _():
    return arch(0, 500)


@glyph("o", 0x6F, SB_RND, SB_RND)
def _():
    return lring(0, 0, 500, XH)


@glyph("p", 0x70, SB_STR, SB_RND)
def _():
    return U(bowl((0, ROL, ROL, 0)), rect(0, DESC, WV, XH))


@glyph("q", 0x71, SB_RND, SB_STR)
def _():
    return U(bowl((ROL, 0, 0, ROL)), rect(500 - WV, DESC, 500, XH))


@glyph("r", 0x72, SB_STR, SB_OPEN)
def _():
    # Clean boxy r: vertical left stem + top-right shoulder, completely open underneath
    w = 395
    outer = rrect(0, 0, w, XH, (0, 0, ROL, 0))
    inner = rect(WV, -10, w + 10, XH - WHL)
    return D(outer, inner)


@glyph("s", 0x73, SB_RND, SB_RND)
def _():
    # Boxed s: squircle frame with two crisp opposing horizontal slots
    w, t = 490, 140
    return boxed(w, XH, (XH - t - 92, XH - t, "right"),
                 (t, t + 92, "left"), r=ROL, cw=104)


@glyph("t", 0x74, SB_OPEN, SB_OPEN)
def _():
    # Compact boxy t without a long protruding tail
    return U(D(rrect(35, 0, 355, ASC, (ROL, 0, 0, 0)),
               rect(35 + WV, WHL, 410, ASC + 10)),
             rect(0, XH - WHL - 40, 345, XH - 40))


@glyph("u", 0x75)
def _():
    return rotate(arch(0, 500), 180, 250, XH / 2)


@glyph("v", 0x76, SB_OPEN, SB_OPEN, clip=(0, 0, 500, XH))
def _():
    return U(diag(250, 0, 92, XH, WD - 8), diag(250, 0, 408, XH, WD - 8))


@glyph("w", 0x77, SB_OPEN, SB_OPEN, clip=(0, 0, 740, XH))
def _():
    return U(diag(192, 0, 82, XH, WD - 15), diag(192, 0, 370, 470, WD - 15),
             diag(548, 0, 370, 470, WD - 15), diag(548, 0, 658, XH, WD - 15))


@glyph("x", 0x78, SB_OPEN, SB_OPEN, clip=(0, 0, 500, XH))
def _():
    return U(diag(92, 0, 408, XH, WD - 8), diag(408, 0, 92, XH, WD - 8))


@glyph("y", 0x79, SB_OPEN, SB_OPEN)
def _():
    # Boxy y: u-top + compact straight descender (no long diagonal tail)
    w = 500
    top = D(lring(0, 0, w, XH, (ROL, ROL, 0, 0)), rect(WV, 240, w - WV, XH + 10))
    stem = rect(w - WV, DESC, w, XH)
    foot = rrect(30, DESC, w, DESC + 130, (45, 0, 0, 0))
    return U(top, stem, foot)


@glyph("z", 0x7A, SB_OPEN, SB_OPEN, clip=(0, 0, 455, XH))
def _():
    return U(rect(0, XH - WHL, 440, XH), rect(0, 0, 455, WHL),
             diag(95, WHL - 10, 350, XH - WHL + 10, WD - 12))


# ---- digits (tabular, crisp boxy style) ------------------------
@glyph("zero", 0x30)
def _():
    return cring(0, 0, 500, CAP)


@glyph("one", 0x31)
def _():
    return U(rect(195, 0, 195 + WV, CAP), rect(90, CAP - 140, 195 + WV, CAP))


@glyph("two", 0x32)
def _():
    # Boxed 2: crisp left-upper slot + right-lower slot (no spikes or overflow)
    t = 148
    return boxed(500, CAP, (CAP - t - 102, CAP - t, "left"),
                 (t, t + 102, "right"), r=(0, 0, RO, RO), cw=112)


@glyph("three", 0x33)
def _():
    # Boxed 3: two crisp left-side horizontal slots (zero stray pinholes)
    t = 148
    return boxed(500, CAP, (CAP - t - 102, CAP - t, "left"),
                 (t, t + 102, "left"), r=RO, cw=112)


@glyph("four", 0x34, clip=(0, 0, 510, CAP))
def _():
    return U(rect(305, 0, 500, CAP),
             rect(0, 165, 510, 165 + 145),
             rect(0, 165, 195, CAP))


@glyph("five", 0x35)
def _():
    # Boxed 5: crisp right-upper slot + left-lower slot
    t = 148
    return boxed(500, CAP, (CAP - t - 102, CAP - t, "right"),
                 (t, t + 102, "left"), r=(RO, RO, 0, 0), cw=112)


@glyph("six", 0x36)
def _():
    # Boxed 6: right-upper slot + crisp closed lower counter
    t = 148
    return boxed(500, CAP, (CAP - t - 102, CAP - t, "right"),
                 (t, t + 108, None), r=RO, cw=110)


@glyph("seven", 0x37, clip=(0, 0, 495, CAP))
def _():
    return U(rect(0, CAP - WH, 495, CAP), diag(175, 0, 395, CAP - 20, WD - 5))


@glyph("eight", 0x38)
def _():
    # Boxed 8: two crisp, balanced rectangular counters
    t = 142
    return boxed(500, CAP, (CAP - t - 108, CAP - t, None),
                 (t, t + 108, None), r=RO, cw=112)


@glyph("nine", 0x39)
def _():
    # Boxed 9: crisp closed upper counter + left-lower slot
    t = 148
    return boxed(500, CAP, (CAP - t - 108, CAP - t, None),
                 (t, t + 102, "left"), r=RO, cw=110)


# ---- punctuation & symbols ----------------------------------------------
DOT = 165


def dot(x, y):
    return rrect(x, y, x + DOT, y + DOT, 28)


def comma_shape(x, y):
    return U(dot(x, y), poly((x + 65, y + 20), (x + DOT, y + 40),
                             (x + 115, y - 140), (x + 25, y - 140)))


@glyph("space", 0x20)
def _():
    return None


@glyph("period", 0x2E, 40, 40)
def _():
    return dot(0, 0)


@glyph("comma", 0x2C, 40, 40)
def _():
    return comma_shape(0, 0)


@glyph("colon", 0x3A, 40, 40)
def _():
    return U(dot(0, 0), dot(0, 360))


@glyph("semicolon", 0x3B, 40, 40)
def _():
    return U(comma_shape(0, 0), dot(0, 360))


@glyph("exclam", 0x21, 40, 40)
def _():
    return U(rect(0, 235, WV, CAP), dot(0, 0))


@glyph("question", 0x3F, SB_OPEN, SB_RND)
def _():
    top = D(cring(0, 320, 470, CAP, RO), rect(-10, 310, 175, 550))
    return U(top, rect(170, 225, 345, 395), dot(175, 0))


@glyph("quotesingle", 0x27, 40, 40)
def _():
    return rrect(0, 465, 155, CAP, 24)


@glyph("quotedbl", 0x22, 40, 40)
def _():
    return U(rrect(0, 465, 155, CAP, 24), rrect(225, 465, 380, CAP, 24))


@glyph("quoteright", 0x2019, 40, 40)
def _():
    return comma_shape(0, 535)


@glyph("quoteleft", 0x2018, 40, 40)
def _():
    return rotate(comma_shape(0, 535), 180, 82, 617)


@glyph("quotedblright", 0x201D, 40, 40)
def _():
    return U(comma_shape(0, 535), comma_shape(215, 535))


@glyph("quotedblleft", 0x201C, 40, 40)
def _():
    return rotate(U(comma_shape(0, 535), comma_shape(215, 535)), 180, 190, 617)


@glyph("hyphen", 0x2D, 35, 35)
def _():
    return rect(0, 235, 290, 375)


@glyph("endash", 0x2013, 20, 20)
def _():
    return rect(0, 245, 490, 365)


@glyph("underscore", 0x5F, 0, 0)
def _():
    return rect(0, -160, 490, -35)


@glyph("slash", 0x2F, 10, 10, clip=(0, -60, 450, 760))
def _():
    return diag(80, -60, 370, 760, 160)


@glyph("backslash", 0x5C, 10, 10, clip=(0, -60, 450, 760))
def _():
    return diag(370, -60, 80, 760, 160)


@glyph("parenleft", 0x28, 45, 10)
def _():
    return D(rrect(0, -140, 285, 810, (120, 0, 0, 120)),
             rrect(155, -15, 400, 685, (55, 0, 0, 55)))


@glyph("parenright", 0x29, 10, 45)
def _():
    return mirror_x(D(rrect(0, -140, 285, 810, (120, 0, 0, 120)),
                      rrect(155, -15, 400, 685, (55, 0, 0, 55))), 142)


@glyph("bracketleft", 0x5B, 45, 10)
def _():
    return D(rect(0, -140, 275, 810), rect(WV - 15, -15, 400, 685))


@glyph("bracketright", 0x5D, 10, 45)
def _():
    return D(rect(0, -140, 275, 810), rect(-120, -15, 275 - (WV - 15), 685))


@glyph("plus", 0x2B, 35, 35)
def _():
    return U(rect(0, 260, 470, 400), rect(165, 95, 305, 565))


@glyph("equal", 0x3D, 35, 35)
def _():
    return U(rect(0, 155, 455, 285), rect(0, 385, 455, 515))


@glyph("asterisk", 0x2A, 25, 25)
def _():
    bar = rect(0, 520, 330, 625)
    return U(bar, rotate(bar, 60, 165, 572), rotate(bar, 120, 165, 572))


@glyph("numbersign", 0x23, 20, 20, clip=(0, 0, 550, CAP))
def _():
    return U(diag(130, 0, 225, CAP, 128), diag(325, 0, 420, CAP, 128),
             rect(0, 170, 550, 290), rect(0, 410, 550, 530))


@glyph("percent", 0x25, 25, 25, clip=(0, 0, 650, CAP))
def _():
    return U(ring(0, 375, 250, CAP, 60, 92, 88, ri=8),
             ring(400, 0, 650, 325, 60, 92, 88, ri=8),
             diag(130, 0, 520, CAP, 128))


@glyph("dollar", 0x24, SB_RND, SB_RND)
def _():
    s = G["S"]["fn"]()
    return U(s, rect(252 - 52, -85, 252 + 52, CAP + 85))


@glyph("lira", 0x20BA, SB_OPEN, SB_RND)
def _():
    base = D(rrect(120, 0, 545, 400, (0, RO, 0, 0)),
             rect(120 + WV, 135, 545 - 155, 500))
    return U(rect(120, 0, 120 + WV, CAP), base,
             seg(10, 300, 395, 440, 108), seg(10, 470, 395, 610, 108))


# ---- Turkish -------------------------------------------------------------
def dieresis(cx, y):
    return U(rrect(cx - 170, y, cx - 35, y + 135, 24),
             rrect(cx + 35, y, cx + 170, y + 135, 24))


def dotabove(cx, y):
    return rrect(cx - 82, y, cx + 82, y + 140, 24)


def breve(cx, y):
    outer = rrect(cx - 155, y, cx + 155, y + 165, (65, 65, 0, 0))
    return D(outer, rrect(cx - 55, y + 90, cx + 55, y + 300, (16, 16, 0, 0)))


def cedilla(cx):
    return U(rect(cx - 42, -160, cx + 52, 30),
             rrect(cx - 120, -255, cx + 52, -155, (36, 36, 0, 36)))


def accented(name, uni, base, mark):
    b = G[base]

    @glyph(name, uni, b["lsb"], b["rsb"], b["clip"])
    def _():
        return U(b["fn"](), mark)


accented("Ccedilla", 0xC7, "C", cedilla(250))
accented("ccedilla", 0xE7, "c", cedilla(238))
accented("Scedilla", 0x15E, "S", cedilla(252))
accented("scedilla", 0x15F, "s", cedilla(245))
accented("Odieresis", 0xD6, "O", dieresis(260, CAP + 75))
accented("odieresis", 0xF6, "o", dieresis(250, XH + 65))
accented("Udieresis", 0xDC, "U", dieresis(255, CAP + 75))
accented("udieresis", 0xFC, "u", dieresis(250, XH + 65))
accented("Gbreve", 0x11E, "G", breve(258, CAP + 75))
accented("gbreve", 0x11F, "g", breve(250, XH + 65))
accented("Idotaccent", 0x130, "I", dotabove(102, CAP + 75))
@glyph("dotlessi", 0x131)
def _():
    return rect(0, 0, WV, XH)
