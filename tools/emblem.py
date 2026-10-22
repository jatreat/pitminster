"""The Friends of Pitminster emblem: St Andrew and St Mary's as it stands in
the editors' June 2026 photograph from the churchyard (images/church-at-dusk),
traced from that photograph rather than drawn from imagination.

Every coordinate below was measured on the photograph scaled to 1000 px wide
(the tower, the broach spire and its weathercock, the stair turret with its
chimney pot, the nave with its east-gable cross, the south chapel, the
chancel and its east-gable finial, the porch and the real window openings). `art()` maps them into the roundel; `mark()` is
the small roundel for the masthead; `seal()` adds the lettered ring for
larger uses; `favicon()` zooms on the tower and spire."""

# ---- measured on the photograph (1000 px wide frame; y grows downwards) ----
GROUND = 462          # foot of the walls
G = 470               # walls run a little below the ground line, under the turf

# The skyline of the church, west (left) to east (right).
OUTLINE = [
    (276, G), (276, 391),                     # porch, west wall
    (309.5, 379),                             # porch gable apex
    (321.7, 385), (321.7, 312),               # tower, lower stage
    (340.6, 302.5), (340.6, 227),             # tower, west face up to the parapet
    (363, 227), (389, 68), (417.5, 227),      # broach spire
    (436.5, 227), (436.5, 300),               # tower, east side
    (452.5, 321.5),                           # set-off down to the nave roof
    (453.75, 321.5), (453.75, 305.5),         # stair turret
    (456, 305.5), (456, 299.5), (460.5, 299.5), (460.5, 305.5),  # its chimney pot
    (495, 305.5), (495, 315),
    (590, 301.3), (597.5, 294),               # nave ridge up to the nave's east gable
    (614.5, 327.8),                           # down to the chancel roof
    (768.75, 310), (776.25, 305), (782.5, 306),  # chancel ridge, east gable apex
    (807.5, 377.5), (809, 380), (809, G),     # east gable and east wall
]

# Window and door openings: (left, right, apex, springing, sill). Rectangular
# openings have apex == springing.
OPENINGS = [
    (350.0, 359.4, 247.8, 254.0, 277.5),      # belfry lancet, west
    (415.3, 424.7, 247.8, 254.0, 277.5),      # belfry lancet, east
    (385.0, 410.0, 381.25, 397.5, 452.5),     # nave windows
    (428.75, 450.0, 378.75, 395.0, 452.5),
    (520.0, 562.5, 371.25, 392.5, 453.75),
    (636.0, 661.0, 362.5, 378.0, 442.5),      # south chapel window
    (690.0, 715.0, 387.5, 387.5, 410.0),      # chancel two-light window
    (773.75, 793.75, 340.0, 360.0, 440.0),    # east window
    (296.0, 314.0, 430.0, 441.0, GROUND),     # porch doorway
]

# Roof edges and copings, cut as hairlines so the roofs read apart from the walls.
LINES = [
    [(340.6, 240), (436.5, 240)],                          # tower parapet string course
    [(379.4, 363.3), (419.4, 327.8), (453.75, 323)],       # nave roof, west end
    [(323, 372.8), (453.75, 356)],                         # nave eaves, west of the turret
    [(495, 352.5), (605, 341)],                            # nave eaves, east of the turret
    [(591, 299.5), (560, 344.5)],                          # nave east gable coping
    [(614, 340), (650, 335.5), (677.5, 355), (668, 380)],  # south chapel gable
    [(668, 380), (753.75, 380)],                           # chancel eaves
    [(769, 310), (752.5, 380)],                            # chancel east gable coping
    [(-800, GROUND), (1800, GROUND)],                      # the churchyard turf
]

# ---- placing the photograph inside the roundel ----
SCALE = 0.266                 # 1 photo px -> roundel units
ORIGIN = (539, 271)           # photo point that sits at the roundel centre


def art(cx=100, cy=100, s=1.0, uid="a", clip_r=None):
    """The church in a circle of radius 80*s centred on (cx, cy)."""
    ox, oy = ORIGIN

    def P(x, y):
        return (cx + (x - ox) * SCALE * s, cy + (y - oy) * SCALE * s)

    def pt(x, y):
        X, Y = P(x, y)
        return f"{X:.2f},{Y:.2f}"

    def u(v):                 # a length in roundel units
        return v * s

    r = 80 * s
    cr = r if clip_r is None else clip_r
    gy = P(0, GROUND)[1]

    ground = f'<rect x="{cx - 2 * cr:.2f}" y="{gy:.2f}" width="{4 * cr:.2f}" height="{2 * cr:.2f}"/>'

    church = f'<path d="M{" L".join(pt(x, y) for x, y in OUTLINE)} Z"/>'

    # Finials, sized up a little so they survive small sizes.
    def cross(px, py_top, py_base, arm_at, stem=1.05, arm=2.7):
        X, Yt = P(px, py_top)
        _, Yb = P(px, py_base)
        _, Ya = P(px, arm_at)
        return (f'<rect x="{X - u(stem) / 2:.2f}" y="{Yt:.2f}" width="{u(stem):.2f}" height="{Yb - Yt:.2f}"/>'
                f'<rect x="{X - u(arm) / 2:.2f}" y="{Ya - u(stem) / 2:.2f}" width="{u(arm):.2f}" height="{u(stem):.2f}"/>')

    nave_cross = cross(597.5, 280.5, 296, 285.5)
    chancel_cross = cross(776.25, 280.5, 302, 286.5)
    bx, by = P(776.25, 300)
    chancel_base = f'<rect x="{bx - u(1.6):.2f}" y="{by:.2f}" width="{u(3.2):.2f}" height="{u(1.6):.2f}"/>'
    px_, py_ = P(309.5, 379)
    porch_pin = (f'<path d="M{px_ - u(0.8):.2f},{py_ + u(0.6):.2f} L{px_:.2f},{py_ - u(3.9):.2f} '
                 f'L{px_ + u(0.8):.2f},{py_ + u(0.6):.2f} Z"/>')

    # Weathercock: ball, rod, the compass arms, and the bird facing east.
    ax, ay = P(389, 68)
    top = ay - u(6.4)
    vane = (f'<circle cx="{ax:.2f}" cy="{ay - u(0.3):.2f}" r="{u(0.75):.2f}"/>'
            f'<rect x="{ax - u(0.45):.2f}" y="{top:.2f}" width="{u(0.9):.2f}" height="{ay - top:.2f}"/>'
            f'<rect x="{ax - u(1.5):.2f}" y="{ay - u(2.7):.2f}" width="{u(3.0):.2f}" height="{u(0.6):.2f}"/>')
    bird = [(-2.2, -0.2), (-1.5, -2.6), (-0.9, -1.2), (0.6, -1.0), (0.8, -2.5), (1.5, -2.3),
            (1.7, -1.5), (2.5, -1.2), (1.7, -0.7), (1.3, 0.5), (-0.6, 0.5)]
    vane += f'<path d="M{" L".join(f"{ax + u(x):.2f},{top + u(y) + u(0.6):.2f}" for x, y in bird)} Z"/>'

    # Openings and hairlines are cut through with a mask.
    def opening(x0, x1, apex, spring, sill):
        a, b = P(x0, sill), P(x1, sill)
        c0, c1 = P(x0, spring), P(x1, spring)
        if apex >= spring:
            return f'M{a[0]:.2f},{a[1]:.2f} L{c0[0]:.2f},{c0[1]:.2f} L{c1[0]:.2f},{c1[1]:.2f} L{b[0]:.2f},{b[1]:.2f} Z'
        m = P((x0 + x1) / 2, apex)
        h = spring - apex
        k0, k1 = P(x0, apex + 0.7 * h), P(x1, apex + 0.7 * h)
        return (f'M{a[0]:.2f},{a[1]:.2f} L{c0[0]:.2f},{c0[1]:.2f} Q{k0[0]:.2f},{k0[1]:.2f} {m[0]:.2f},{m[1]:.2f} '
                f'Q{k1[0]:.2f},{k1[1]:.2f} {c1[0]:.2f},{c1[1]:.2f} L{b[0]:.2f},{b[1]:.2f} Z')

    holes = " ".join(opening(*o) for o in OPENINGS)
    lines = " ".join("M" + " L".join(pt(x, y) for x, y in seg) for seg in LINES)
    mask = (f'<mask id="k-{uid}" maskUnits="userSpaceOnUse" x="-100" y="-100" width="400" height="400">'
            f'<rect x="-100" y="-100" width="400" height="400" fill="#fff"/>'
            f'<path d="{holes}" fill="#000"/>'
            f'<path d="{lines}" fill="none" stroke="#000" stroke-width="{u(1.05):.2f}" stroke-linejoin="round"/>'
            f'</mask>')
    clip = f'<clipPath id="c-{uid}"><circle cx="{cx}" cy="{cy}" r="{cr:.2f}"/></clipPath>'

    body = f'<g mask="url(#k-{uid})">{ground}{church}{nave_cross}{chancel_cross}{chancel_base}{porch_pin}{vane}</g>'
    return f'<defs>{clip}{mask}</defs><g clip-path="url(#c-{uid})" fill="currentColor">{body}</g>'


def mark(uid="m", title="Friends of Pitminster", cls="mark"):
    label = f'role="img" aria-label="{title}"' if title else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="{cls}" viewBox="0 0 200 200" {label}>'
            f'<circle cx="100" cy="100" r="94" fill="none" stroke="currentColor" stroke-width="6"/>'
            f'<circle cx="100" cy="100" r="84.5" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'{art(100, 100, 1.0, uid)}</svg>')


def seal(uid="s", cls="seal"):
    top = 'M 22,100 A 78,78 0 0 1 178,100'
    bot = 'M 14,100 A 86,86 0 0 0 186,100'
    diamond = lambda x: f'<path d="M{x},96 L{x+4},100 L{x},104 L{x-4},100 Z"/>'
    return (f'<svg class="{cls}" viewBox="0 0 200 200" role="img" aria-label="Friends of Pitminster, Somerset">'
            f'<defs><path id="t-{uid}" d="{top}"/><path id="b-{uid}" d="{bot}"/></defs>'
            f'<circle cx="100" cy="100" r="96" fill="none" stroke="currentColor" stroke-width="3"/>'
            f'<circle cx="100" cy="100" r="91" fill="none" stroke="currentColor" stroke-width="1"/>'
            f'<circle cx="100" cy="100" r="70" fill="none" stroke="currentColor" stroke-width="1.5"/>'
            f'<g fill="currentColor" font-family="Libre Caslon Text, Georgia, serif" font-size="13" letter-spacing="2.6">'
            f'<text><textPath href="#t-{uid}" startOffset="50%" text-anchor="middle">FRIENDS OF PITMINSTER</textPath></text>'
            f'<text><textPath href="#b-{uid}" startOffset="50%" text-anchor="middle">SOMERSET</textPath></text>'
            f'{diamond(13)}{diamond(187)}</g>'
            f'{art(100, 100, 0.84, uid)}</svg>')


FAVICON_FOCUS = (66, 93)      # roundel point (tower and spire) placed at the icon's centre
FAVICON_ZOOM = 1.55


def favicon():
    s = FAVICON_ZOOM
    fx, fy = FAVICON_FOCUS
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
            '<defs><clipPath id="fc"><circle cx="100" cy="100" r="99"/></clipPath></defs>'
            '<circle cx="100" cy="100" r="99" fill="#23292E"/>'
            f'<g clip-path="url(#fc)" style="color:#D2A95B">{art(100 + (100 - fx) * s, 100 + (100 - fy) * s, s, "f", clip_r=400)}</g></svg>')


if __name__ == "__main__":
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent / "public" / "assets"
    (root / "favicon.svg").write_text(favicon(), encoding="utf-8")
    (root / "mark.svg").write_text(mark().replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1), encoding="utf-8")
    print("wrote favicon.svg and mark.svg")
