#!/usr/bin/env python3
"""The natural evolution of the API gateway, in an isometric cluster.

1. an api-gateway in front of the application's services;
2. the stack grows around it (iam, auth-proxy, dev-tunnel, an openapi-ui per
   service, config files, telemetry from everywhere): the traffic tangles;
3. the gateway glows, swallows the bricks around it and evolves into Meerkat,
   while the title flips API-GATEWAY into APP-GATEWAY;
4. traffic becomes a star around Meerkat, which carries what it absorbed and
   sends metrics, traces and logs to the collector from the one right place.

Generic names only (no third-party product). Writes meerkat-cluster.svg."""
import base64
import math
from pathlib import Path

W, H = 900, 900
DUR = 19.0
CX, CY, U = 450, 206, 38
N = 10

LOGO = "data:image/png;base64," + base64.b64encode(Path(__file__).with_name("meerkat.png").read_bytes()).decode()
INK, TEAL, RED, CABLE, GREY = "#2d2b29", "#0f6f78", "#d9534f", "#8b95a3", "#7d8796"
MONO = "Liberation Mono, DejaVu Sans Mono, Menlo, monospace"


def P(x, y, z=0.0):
    return (CX + (x - y) * 0.866 * U, CY + (x + y) * 0.5 * U - z * U)


def pts(*ps):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)


def shade(hex_, f):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f > 1:
        r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    else:
        r, g, b = (int(c * f) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def box(x, y, s, h, color):
    top = pts(P(x, y, h), P(x + s, y, h), P(x + s, y + s, h), P(x, y + s, h))
    left = pts(P(x, y + s, h), P(x + s, y + s, h), P(x + s, y + s, 0), P(x, y + s, 0))
    right = pts(P(x + s, y, h), P(x + s, y + s, h), P(x + s, y + s, 0), P(x + s, y, 0))
    return (f'<polygon points="{left}" fill="{shade(color, 0.84)}"/>'
            f'<polygon points="{right}" fill="{shade(color, 0.66)}"/>'
            f'<polygon points="{top}" fill="{shade(color, 1.22)}"/>')


SPLINE = 'calcMode="spline" keySplines="0.2 0.8 0.3 1"'
EASE_IN = 'calcMode="spline" keySplines="0.6 0 0.9 0.5"'
POP = 'calcMode="spline" keyTimes="0;0.6;1" keySplines="0.2 0.8 0.3 1;0.4 0 0.6 1"'
DASHED = 'stroke-dasharray="7 6" opacity="0.8"'


def appear(b, d=0.3):
    return f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur="{d}s" fill="freeze"/>'


def fade_out(b, d=0.4):
    return f'<animate attributeName="opacity" to="0" begin="{b:.2f}s" dur="{d}s" fill="freeze"/>'


def line(a, b, color, extra="", width=2.5):
    return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" {extra}/>')


def seg(*ps):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in ps)


def drawn(a, b, color, begin, dur, width=4):
    L = math.dist(a, b)
    return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}" opacity="0.85">'
            f'<animate attributeName="stroke-dashoffset" to="0" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/></line>')


def dot(path, begin, dur, fill, r=7.5, stroke=""):
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<circle r="{r}" fill="{fill}"{st} opacity="0"><set attributeName="opacity" to="1" begin="{begin:.2f}s" dur="{dur:.2f}s"/>'
            f'<animateMotion path="{path}" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/></circle>')


def chip(label, color, fill="#ffffff", size=13):
    w = 14 + size * 0.6 * len(label)
    text = color if fill == "#ffffff" else "#ffffff"
    return (f'<rect x="{-w / 2:.1f}" y="-12" width="{w:.1f}" height="22" rx="11" fill="{fill}" stroke="{color}" stroke-width="2"/>'
            f'<text y="4" text-anchor="middle" font-size="{size}" font-weight="700" fill="{text}">{label}</text>')


# ---- the cast ------------------------------------------------------------------
S = 1.1
SERVICES = {  # the application's own services: they stay
    "web": (0.9, 6.1, "#3b8fd9"),
    "orders": (1.4, 3.1, "#5b5fc7"),
    "billing": (3.1, 1.4, "#d99a2b"),
    "catalog": (6.1, 0.9, "#2fa36b"),
}
GW = (6.4, 6.4)                 # the api-gateway, then Meerkat
BRICKS = {                      # what the stack grows around the gateway
    "iam": (8.5, 4.7, 3.3),
    "auth-proxy": (4.7, 8.5, 3.6),
    "dev-tunnel": (3.0, 5.6, 3.9),
}                               # x, y, pop time
OTEL = (5.6, 3.0)               # the team's collector: it stays
YAML = [(4.3, 4.3), (8.9, 7.3), (7.3, 8.9)]
USERS = [(300, 830), (450, 848), (600, 830)]

T_ABSORB = 7.7     # bricks start flying into the gateway
T_FLASH = 9.0      # the gateway turns into Meerkat
T_STAR = 10.1      # new wiring
MH = 150


def foot(x, y):
    return P(x + S / 2, y + S / 2, 0)


GW_FOOT = foot(*GW)
GW_MID = P(GW[0] + S / 2, GW[1] + S / 2, S * 0.5)
MK_CENTER = (GW_FOOT[0], GW_FOOT[1] - MH * 0.55)

out = []
add = out.append
add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter, Helvetica, Arial, sans-serif">')
add('''<defs>
<radialGradient id="bg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#fbf6ec"/><stop offset="1" stop-color="#efe3cc"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset="0.45" stop-color="#bff3ee" stop-opacity="0.8"/><stop offset="1" stop-color="#bff3ee" stop-opacity="0"/></radialGradient>
<radialGradient id="shadow"><stop offset="0" stop-color="#3b3226" stop-opacity="0.35"/><stop offset="1" stop-color="#3b3226" stop-opacity="0"/></radialGradient>
<filter id="white"><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/></filter>
</defs>''')
add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# ---- platform ----------------------------------------------------------------
plat = [f'<polygon points="{pts(P(0, N), P(N, N), P(N, N, -0.4), P(0, N, -0.4))}" fill="#9fb3c2"/>',
        f'<polygon points="{pts(P(N, 0), P(N, N), P(N, N, -0.4), P(N, 0, -0.4))}" fill="#84999f"/>',
        f'<polygon points="{pts(P(0, 0), P(N, 0), P(N, N), P(0, N))}" fill="#e3ebf0"/>']
for i in range(1, N):
    plat.append(line(P(i, 0), P(i, N), "#d2dde5", width=1) + line(P(0, i), P(N, i), "#d2dde5", width=1))
add(f'<g opacity="0"><animateTransform attributeName="transform" type="translate" values="0 40;0 0" dur="0.7s" begin="0.1s" fill="freeze" {SPLINE}/>'
    f'{appear(0.1, 0.5)}{"".join(plat)}</g>')

for i, (ux, uy) in enumerate(USERS):
    add(f'<g opacity="0" transform="translate({ux},{uy})">{appear(0.4 + 0.15 * i, 0.4)}'
        f'<circle cy="-30" r="11" fill="#6b7280"/><path d="M-19,6 a19,19 0 0 1 38,0 z" fill="#6b7280"/></g>')

# ---- title: API-GATEWAY, whose I flips into a P ------------------------------------
FS = 30
CW = FS * 0.6
x0 = W / 2 - 11 * CW / 2
TY = 98
recolor = f'<animate attributeName="fill" to="{TEAL}" begin="{T_FLASH + 0.2:.2f}s" dur="0.4s" fill="freeze"/>'
lx, ly = x0 + 2.5 * CW, TY - FS * 0.35
title = [f'<text x="{x0:.1f}" y="{TY}" font-family="{MONO}" font-size="{FS}" font-weight="700" fill="#6b7280">AP{recolor}</text>',
         f'<text x="{x0 + 3 * CW:.1f}" y="{TY}" font-family="{MONO}" font-size="{FS}" font-weight="700" fill="#6b7280">-GATEWAY{recolor}</text>',
         f'<g transform="translate({lx:.1f},{ly:.1f})"><g>'
         f'<animateTransform attributeName="transform" type="scale" values="1 1;1 0" dur="0.18s" begin="{T_FLASH:.2f}s" fill="freeze"/>'
         f'<text y="{FS * 0.35:.1f}" text-anchor="middle" font-family="{MONO}" font-size="{FS}" font-weight="700" fill="#6b7280">I'
         f'<animate attributeName="fill" to="{RED}" begin="5.6s" dur="0.3s" fill="freeze"/></text></g></g>',
         f'<g transform="translate({lx:.1f},{ly:.1f})"><g transform="scale(1 0)">'
         f'<animateTransform attributeName="transform" type="scale" values="1 0;1 1.3;1 1" dur="0.35s" begin="{T_FLASH + 0.18:.2f}s" fill="freeze"/>'
         f'<text y="{FS * 0.35:.1f}" text-anchor="middle" font-family="{MONO}" font-size="{FS}" font-weight="700" fill="{TEAL}">P</text></g></g>']
add(f'<g opacity="0">{appear(0.9, 0.5)}{"".join(title)}</g>')
# a red ring pulses around the I while the stack grows: the API gateway is not enough any more
add(f'<g opacity="0" transform="translate({lx:.1f},{ly:.1f})">'
    f'<animate attributeName="opacity" values="0;1;0.2;1;0.2;1;0" dur="2.6s" begin="5.6s" fill="freeze"/>'
    f'<circle r="21" fill="none" stroke="{RED}" stroke-width="2.5"/></g>')

# ---- the simple API-gateway era: user -> gateway -> service --------------------------
svcs = list(SERVICES.values())
add(f'<g opacity="0">{appear(1.6, 0.4)}{fade_out(5.0, 0.4)}'
    + "".join(line((ux, uy - 50), GW_FOOT, CABLE, DASHED) for ux, uy in USERS)
    + "".join(line(GW_FOOT, foot(*s[:2]), CABLE, DASHED) for s in svcs) + "</g>")
add("".join(dot(seg((USERS[k % 3][0], USERS[k % 3][1] - 50), GW_FOOT, foot(*svcs[k % 4][:2])), 1.9 + 0.38 * k, 1.1, "#8a8f98")
            for k in range(7)))

# ---- the grown stack: cables, then tangled traffic ------------------------------------
AP, IAM = foot(*BRICKS["auth-proxy"][:2]), foot(*BRICKS["iam"][:2])
cables = [line((ux, uy - 50), GW_FOOT, CABLE, DASHED) for ux, uy in USERS]
cables += [line(GW_FOOT, AP, CABLE, DASHED), line(AP, IAM, CABLE, DASHED)]
cables += [line(AP, foot(*s[:2]), CABLE, DASHED) for s in svcs]
cables += [line(foot(*BRICKS["dev-tunnel"][:2]), foot(*SERVICES["orders"][:2]), CABLE, DASHED),
           line(foot(*BRICKS["dev-tunnel"][:2]), GW_FOOT, CABLE, DASHED)]
for a in [GW, *[b[:2] for b in BRICKS.values()], *[s[:2] for s in svcs]]:  # everyone ships its own telemetry
    cables.append(line(foot(*a), foot(*OTEL), "#b08fd8", 'stroke-dasharray="3 6" opacity="0.9"', 2))
add(f'<g opacity="0">{appear(5.0, 0.6)}{fade_out(T_ABSORB, 0.5)}{"".join(cables)}</g>')

tangled = []
for k in range(8):
    b = 5.3 + 0.3 * k
    u = USERS[k % 3]
    d = min(2.4, T_ABSORB + 0.2 - b)
    if d < 0.5:
        continue
    tangled.append(f'<circle r="7" fill="{RED}" opacity="0"><set attributeName="opacity" to="1" begin="{b:.2f}s" dur="{d:.2f}s"/>'
                   f'<animateMotion path="{seg((u[0], u[1] - 50), GW_FOOT, AP, IAM, AP, foot(*svcs[k % 4][:2]))}" '
                   f'begin="{b:.2f}s" dur="2.4s" fill="freeze"/></circle>')
add("".join(tangled))

# ---- the new wiring ------------------------------------------------------------------
OT = foot(*OTEL)
add("".join(drawn((ux, uy - 50), GW_FOOT, TEAL, T_STAR + 0.1 * i, 0.4) for i, (ux, uy) in enumerate(USERS)))
add("".join(drawn(GW_FOOT, foot(*s[:2]), TEAL, T_STAR + 0.35 + 0.12 * i, 0.45) for i, s in enumerate(svcs)))
add(drawn(GW_FOOT, OT, "#8b5cf6", 12.6, 0.5, 7))  # one telemetry stream, from the place that sees everything


# ---- things that get absorbed fly into the gateway ------------------------------------
def absorbed(cx, cy, begin, inner, delay):
    t = T_ABSORB + delay
    dx, dy = GW_MID[0] - cx, GW_MID[1] - cy
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx:.1f} {dy:.1f}" dur="0.75s" begin="{t:.2f}s" fill="freeze" {EASE_IN}/>'
            f'{fade_out(t + 0.62, 0.13)}'
            f'<g transform="translate({cx:.1f},{cy:.1f})"><g transform="scale(0)">'
            f'<animateTransform attributeName="transform" type="scale" values="0;1.18;1" dur="0.45s" begin="{begin:.2f}s" fill="freeze" {POP}/>'
            f'<animateTransform attributeName="transform" type="scale" values="1;0.15" dur="0.75s" begin="{t:.2f}s" fill="freeze" {EASE_IN}/>'
            f'<g transform="translate({-cx:.1f},{-cy:.1f})">{inner}</g></g></g></g>')


def brick_inner(x, y, label):
    tx, ty = P(x + S / 2, y + S / 2, S * 0.9)
    return box(x, y, S, S * 0.9, GREY) + f'<g transform="translate({tx:.1f},{ty - 28:.1f})">{chip(label, "#5b6472")}</g>'


def yaml_inner(cx, cy):
    return (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate(-8)"><path d="M-17,-22 h24 l10,10 v34 h-34 z" fill="#ffffff" stroke="#9aa3ae" stroke-width="2"/>'
            f'<path d="M7,-22 v10 h10" fill="none" stroke="#9aa3ae" stroke-width="2"/>'
            f'<text y="6" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="#6b7280">yaml</text></g>')


def openapi_inner(cx, cy):
    return (f'<g transform="translate({cx:.1f},{cy:.1f})"><rect x="-17" y="-13" width="34" height="24" rx="6" fill="#85ea2d" stroke="#5aa516" stroke-width="2"/>'
            f'<text y="5" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="#173647">{{ }}</text></g>')


def popped(x, y, begin, inner):
    bx, by = P(x + S / 2, y + S / 2)
    return (f'<g transform="translate({bx:.1f},{by:.1f})"><g transform="scale(0)">'
            f'<animateTransform attributeName="transform" type="scale" values="0;1.18;1" dur="0.45s" begin="{begin:.2f}s" fill="freeze" {POP}/>'
            f'<g transform="translate({-bx:.1f},{-by:.1f})">{inner}</g></g></g>')


pieces = []  # (depth, svg), painted back to front
for i, (name, (x, y, b)) in enumerate(BRICKS.items()):
    c = P(x + S / 2, y + S / 2)
    pieces.append((x + y, absorbed(c[0], c[1], b, brick_inner(x, y, name), 0.12 * i)))
for i, (x, y) in enumerate(YAML):
    c = P(x, y, 0.6)
    pieces.append((x + y, absorbed(c[0], c[1], 4.2 + 0.2 * i, yaml_inner(*c), 0.3 + 0.08 * i)))
for i, (name, (x, y, color)) in enumerate(SERVICES.items()):
    tx, ty = P(x + S / 2, y + S / 2, S)
    pieces.append((x + y, popped(x, y, 0.7 + 0.2 * i, box(x, y, S, S, color)
                                 + f'<g transform="translate({tx:.1f},{ty - 30:.1f})">{chip(name, shade(color, 0.75))}</g>')))
    c = (tx + 46, ty - 4)  # each service carries its own openapi-ui
    pieces.append((x + y + 0.01, absorbed(c[0], c[1], 4.6 + 0.15 * i, openapi_inner(*c), 0.5 + 0.08 * i)))
ox, oy = OTEL
otx, oty = P(ox + S / 2, oy + S / 2, S)
pieces.append((ox + oy, popped(ox, oy, 4.9, box(ox, oy, S, S, "#8b5cf6")
                               + f'<g transform="translate({otx:.1f},{oty - 30:.1f})">{chip("otel-collector", "#6d3fd6")}</g>')))

# the api-gateway: pops, shakes while it swallows the rest, and is gone in the flash
gx, gy = GW
gb = P(gx + S / 2, gy + S / 2)
gtx, gty = P(gx + S / 2, gy + S / 2, S)
shake = ";".join(f"{a} {gb[0]:.1f} {gb[1]:.1f}" for a in [0, -3, 3, -4, 4, -5, 5, -6, 6, -7, 7, 0])
pieces.append((gx + gy, f'<g transform="translate({gb[0]:.1f},{gb[1]:.1f})"><g transform="scale(0)">'
                        f'<animateTransform attributeName="transform" type="scale" values="0;1.18;1" dur="0.45s" begin="1.3s" fill="freeze" {POP}/>'
                        f'<animateTransform attributeName="transform" type="scale" values="1;1.25;0" keyTimes="0;0.5;1" dur="0.25s" begin="{T_FLASH - 0.1:.2f}s" fill="freeze"/>'
                        f'<g transform="translate({-gb[0]:.1f},{-gb[1]:.1f})"><g>'
                        f'<animateTransform attributeName="transform" type="rotate" values="{shake}" dur="1.3s" begin="{T_ABSORB:.2f}s"/>'
                        f'{box(gx, gy, S, S, "#5f6b7a")}<g transform="translate({gtx:.1f},{gty - 30:.1f})">{chip("api-gateway", "#3f4855")}</g></g></g></g></g>'))

for _, svg in sorted(pieces, key=lambda p: p[0]):
    add(svg)

# glow while it absorbs, then the flash
add(f'<circle cx="{GW_MID[0]:.1f}" cy="{GW_MID[1]:.1f}" r="0" fill="url(#glow)" opacity="0">'
    f'<animate attributeName="r" values="20;70;55;95;80;130" dur="{T_FLASH - T_ABSORB:.2f}s" begin="{T_ABSORB:.2f}s" fill="freeze"/>'
    f'<animate attributeName="opacity" values="0;0.9;0.7;1" dur="{T_FLASH - T_ABSORB:.2f}s" begin="{T_ABSORB:.2f}s" fill="freeze"/>'
    f'<animate attributeName="opacity" to="0" dur="0.5s" begin="{T_FLASH + 0.3:.2f}s" fill="freeze"/></circle>')

# Meerkat: a white silhouette grows out of the flash, then colours in
w = MH / 2
fx, fy = GW_FOOT
mk = f'<image href="{LOGO}" xlink:href="{LOGO}" x="{-w / 2:.1f}" y="{-MH + 6}" width="{w:.1f}" height="{MH}"/>'
add(f'<ellipse cx="{fx:.1f}" cy="{fy:.1f}" rx="{w * 0.75:.1f}" ry="{w * 0.24:.1f}" fill="url(#shadow)" opacity="0">{appear(T_FLASH + 0.1, 0.3)}</ellipse>')
add(f'<g transform="translate({fx:.1f},{fy:.1f})"><g transform="scale(0)">'
    f'<animateTransform attributeName="transform" type="scale" values="0;1.15;1" keyTimes="0;0.6;1" dur="0.5s" begin="{T_FLASH:.2f}s" fill="freeze" '
    f'calcMode="spline" keySplines="0.2 0.8 0.3 1;0.4 0 0.6 1"/>'
    f'<g>{mk}</g>'
    f'<g filter="url(#white)">{mk}<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.45;1" dur="1.1s" begin="{T_FLASH:.2f}s" fill="freeze"/></g>'
    f'</g></g>')
add(f'<circle cx="{GW_MID[0]:.1f}" cy="{GW_MID[1]:.1f}" r="10" fill="none" stroke="#ffffff" stroke-width="14" opacity="0">'
    f'<animate attributeName="r" values="10;270" dur="0.7s" begin="{T_FLASH:.2f}s" fill="freeze"/>'
    f'<animate attributeName="stroke-width" values="18;1" dur="0.7s" begin="{T_FLASH:.2f}s" fill="freeze"/>'
    f'<animate attributeName="opacity" values="1;0" dur="0.7s" begin="{T_FLASH:.2f}s" fill="freeze"/></circle>')
add(f'<rect width="{W}" height="{H}" fill="#ffffff" opacity="0"><animate attributeName="opacity" values="0;0.75;0" dur="0.35s" begin="{T_FLASH - 0.05:.2f}s" fill="freeze"/></rect>')
for k in range(7):
    a = -math.pi / 2 + (k - 3) * 0.5
    r = 95 + 12 * (k % 2)
    sx, sy = MK_CENTER[0] + math.cos(a) * r, MK_CENTER[1] + math.sin(a) * r * 0.9
    b = T_FLASH + 0.35 + 0.07 * k
    add(f'<g transform="translate({sx:.1f},{sy:.1f})"><g transform="scale(0)">'
        f'<animateTransform attributeName="transform" type="scale" values="0;1.2;0" dur="0.6s" begin="{b:.2f}s" fill="freeze"/>'
        f'<path d="M0,-12 Q2,-2 12,0 Q2,2 0,12 Q-2,2 -12,0 Q-2,-2 0,-12 z" fill="#f2b84b"/></g></g>')

# ---- what Meerkat now carries: badges in a crown around it ---------------------------------
CARRY = ["iam", "auth-proxy", "openapi-ui", "config", "dev-tunnel", "audit"]
for side, ccx in enumerate((140, W - 140)):  # two cards in the free corners: what is now inside Meerkat
    add(f'<g opacity="0">{appear(10.8 + 0.1 * side, 0.3)}'
        f'<rect x="{ccx - 78}" y="548" width="156" height="158" rx="16" fill="#ffffff" fill-opacity="0.75" stroke="{TEAL}" stroke-width="2" stroke-dasharray="6 5"/>'
        f'<image href="{LOGO}" xlink:href="{LOGO}" x="{ccx - 9}" y="554" width="18" height="36"/></g>')
for k, label in enumerate(CARRY):  # two columns in the free corners under the cluster
    cx = 140 if k < 3 else W - 140
    cy = 612 + 38 * (k % 3)
    b = 11.0 + 0.18 * k
    add(f'<g transform="translate({cx:.1f},{cy:.1f})"><g opacity="0">{appear(b, 0.15)}'
        f'<animateMotion path="M{MK_CENTER[0] - cx:.1f},{MK_CENTER[1] - cy:.1f} L0,0" dur="0.45s" begin="{b:.2f}s" fill="freeze" {SPLINE}/>'
        f'{chip(label, TEAL, TEAL, 14)}</g></g>')

# ---- the new traffic: user -> Meerkat -> service, some turned away -------------------------
new = []
k = 0
for wave in range(12):
    for i, (ux, uy) in enumerate(USERS):
        b = 10.7 + wave * 0.6 + i * 0.2
        if b > 17.6:
            continue
        new.append(dot(seg((ux, uy - 50), GW_FOOT), b, 0.4, "#8a8f98"))
        if (wave * 3 + i) % 7 == 5:
            new.append(f'<g opacity="0" transform="translate({GW_FOOT[0] + 32:.1f},{GW_FOOT[1] - 12:.1f})">'
                       f'<animate attributeName="opacity" values="0;1;0" dur="0.7s" begin="{b + 0.4:.2f}s"/>'
                       f'<circle r="11" fill="{RED}"/><path d="M-4,-4 L4,4 M4,-4 L-4,4" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></g>')
            continue
        new.append(dot(seg(GW_FOOT, foot(*svcs[k % 4][:2])), b + 0.42, 0.5, TEAL, stroke="#ffffff"))
        k += 1
add("".join(new))

# telemetry riding the single stream
for rep in range(2):
    for j, label in enumerate(["metrics", "traces", "logs"]):
        b = 13.1 + rep * 1.9 + j * 0.55
        add(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{b:.2f}s" dur="0.9s"/>'
            f'<animateMotion path="{seg(GW_FOOT, OT)}" begin="{b:.2f}s" dur="0.9s" fill="freeze"/>{chip(label, "#7c4dea", "#7c4dea", 12)}</g>')

# ---- final title -------------------------------------------------------------------------
add(f'<g opacity="0">{appear(15.4, 0.5)}'
    f'<animateTransform attributeName="transform" type="translate" values="0 -14;0 0" dur="0.5s" begin="15.4s" fill="freeze" {SPLINE}/>'
    f'<text x="{W / 2}" y="58" text-anchor="middle" font-size="44" font-weight="800" fill="{INK}" letter-spacing="1">Meerkat</text></g>')
add(f'<g opacity="0">{appear(15.8, 0.5)}<text x="{W - 24}" y="{H - 20}" text-anchor="end" font-size="16" font-weight="600" fill="#7a6a55" letter-spacing="1">meerkat.softwarity.dev</text></g>')
add(f'<rect width="{W}" height="{H}" fill="#f6efe1" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{DUR - 0.45}s" dur="0.45s" fill="freeze"/></rect>')
add("</svg>")

Path(__file__).with_name("meerkat-cluster.svg").write_text("\n".join(out))
print("meerkat-cluster.svg")
