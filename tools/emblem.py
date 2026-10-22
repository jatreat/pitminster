"""The Friends of Pitminster emblem: the church's south elevation (square west
tower, octagon stage, lead spire with its weathercock, nave and chancel), the
yew behind the tower, and the line of the Blackdown Hills, inside a double ring.
`art()` returns the drawing; `mark()` is the small roundel for the masthead and
favicon; `seal()` adds the lettered ring for larger uses."""

def art(cx=100, cy=100, s=1.0, uid="a"):
    # Drawn on a 200x200 grid centred at (100,100); scaled about the centre.
    def T(x, y):
        return f"{cx + (x - 100) * s:.2f},{cy + (y - 100) * s:.2f}"
    r = 80 * s
    clip = f'<clipPath id="c-{uid}"><circle cx="{cx}" cy="{cy}" r="{r:.2f}"/></clipPath>'
    hills = f'<path d="M{T(16,138)} C{T(52,118)} {T(82,126)} {T(108,121)} C{T(138,115)} {T(160,124)} {T(186,130)} L{T(186,190)} L{T(16,190)} Z" opacity=".32"/>'
    yew = (f'<path d="M{T(48,152)} C{T(46,140)} {T(50,128)} {T(56,122)} C{T(58,113)} {T(66,108)} {T(72,110)} '
           f'C{T(78,106)} {T(84,112)} {T(80,120)} L{T(80,152)} Z" opacity=".62"/>')
    ground = f'<rect x="{cx - r:.2f}" y="{cy + 52 * s:.2f}" width="{2 * r:.2f}" height="{30 * s:.2f}"/>'
    # Tower with a belfry lancet knocked out (even-odd)
    tower = (f'<path fill-rule="evenodd" d="M{T(82,152)} L{T(82,110)} L{T(80,110)} L{T(80,104)} L{T(108,104)} L{T(108,110)} L{T(106,110)} L{T(106,152)} Z '
             f'M{T(91,126)} L{T(91,118)} Q{T(94,113)} {T(97,118)} L{T(97,126)} Z '
             f'M{T(91,144)} L{T(91,137)} Q{T(94,133)} {T(97,137)} L{T(97,144)} Z"/>')
    octagon = f'<path d="M{T(86,104)} L{T(86,93)} L{T(102,93)} L{T(102,104)} Z"/>'
    spire = f'<path d="M{T(85,94)} L{T(94,34)} L{T(103,94)} Z"/>'
    vane = (f'<path d="M{T(94,35)} L{T(94,25)}" stroke="currentColor" stroke-width="{1.6 * s:.2f}" fill="none"/>'
            f'<path d="M{T(94,25)} L{T(100.5,27.5)} L{T(94,30)} Z"/>')
    # Nave (higher) and chancel (lower), with pointed windows knocked out
    nave = (f'<path fill-rule="evenodd" d="M{T(106,152)} L{T(106,122)} L{T(146,122)} L{T(146,152)} Z '
            f'M{T(114,146)} L{T(114,136)} Q{T(117.5,130)} {T(121,136)} L{T(121,146)} Z '
            f'M{T(130,146)} L{T(130,136)} Q{T(133.5,130)} {T(137,136)} L{T(137,146)} Z"/>')
    chancel = (f'<path fill-rule="evenodd" d="M{T(146,152)} L{T(146,130)} L{T(162,130)} L{T(162,152)} Z '
               f'M{T(151,147)} L{T(151,139)} Q{T(154,134)} {T(157,139)} L{T(157,147)} Z"/>')
    cross = (f'<path d="M{T(146,122)} L{T(146,112)} M{T(142.5,116)} L{T(149.5,116)}" stroke="currentColor" '
             f'stroke-width="{1.8 * s:.2f}" fill="none" stroke-linecap="square"/>')
    body = hills + yew + ground + tower + octagon + spire + vane + nave + chancel + cross
    return f'<defs>{clip}</defs><g clip-path="url(#c-{uid})" fill="currentColor">{body}</g>'


def mark(uid="m", title="Friends of Pitminster", cls="mark"):
    label = f'role="img" aria-label="{title}"' if title else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="{cls}" viewBox="0 0 200 200" {label}>'
            f'<circle cx="100" cy="100" r="94" fill="none" stroke="currentColor" stroke-width="6"/>'
            f'<circle cx="100" cy="100" r="84.5" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'{art(100, 100, 1.04, uid)}</svg>')


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
            f'{art(100, 100, 0.85, uid)}</svg>')


def favicon():
    # Zoomed on the tower and spire so it still reads at 16px.
    s = 1.5
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
            '<defs><clipPath id="fc"><circle cx="100" cy="100" r="99"/></clipPath></defs>'
            '<circle cx="100" cy="100" r="99" fill="#23292E"/>'
            f'<g clip-path="url(#fc)" style="color:#D2A95B">{art(100 + (100 - 96) * s, 100 + (100 - 92) * s, s, "f")}</g></svg>')


if __name__ == "__main__":
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent / "public" / "assets"
    (root / "favicon.svg").write_text(favicon(), encoding="utf-8")
    (root / "mark.svg").write_text(mark().replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1), encoding="utf-8")
    print("wrote favicon.svg and mark.svg")
