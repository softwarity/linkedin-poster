#!/usr/bin/env python3
"""Animated SVG (SMIL) "8 products -> 1 door", in plug's diagram style.

python3 make-svg.py  ->  app-gateway.fr.svg, app-gateway.en.svg
Rendered to GIF by render.sh (same Playwright + ffmpeg recipe as plug's about-diagram).
"""
from html import escape

T = {
    "fr": {
        "title_a": "Sans app-gateway : la pile assemblée",
        "title_b": "Avec une app-gateway : une seule porte",
        "browser": "Navigateur",
        "app": "Vos services",
        "boxes": [
            ("API gateway", "Kong ×3 + Redis"),
            ("Proxy d'auth", "oauth2-proxy ×2"),
            ("Identité", "Keycloak ×3 + PostgreSQL"),
            ("Coffre", "Vault, 5 nœuds Raft"),
            ("Certificats", "cert-manager"),
            ("Supervision", "Prometheus, Grafana"),
            ("Audit", "Retraced + Elastic"),
        ],
        "todo": ("À développer vous-même", "menu, portail, écrans d'organisation"),
        "count_a": "≈ 38 pods à opérer · 5 moteurs de stockage",
        "meerkat_sub": "app-gateway",
        "chips": [
            "connexion · MFA · passkeys · SSO",
            "rôles · organisations · jetons d'API",
            "routage · débit · quotas",
            "TLS · ACME · coffre à secrets",
            "audit · tableaux de bord",
        ],
        "jwt": "JWT signé",
        "jwt_sub": "identité · rôles · organisation",
        "count_b": "1 binaire · 0 dépendance · 22 Mo au repos",
    },
    "en": {
        "title_a": "Without an app-gateway: the assembled stack",
        "title_b": "With an app-gateway: one single door",
        "browser": "Browser",
        "app": "Your services",
        "boxes": [
            ("API gateway", "Kong ×3 + Redis"),
            ("Auth proxy", "oauth2-proxy ×2"),
            ("Identity", "Keycloak ×3 + PostgreSQL"),
            ("Vault", "Vault, 5 Raft nodes"),
            ("Certificates", "cert-manager"),
            ("Monitoring", "Prometheus, Grafana"),
            ("Audit", "Retraced + Elastic"),
        ],
        "todo": ("Build it yourself", "menu, portal, organisation screens"),
        "count_a": "≈ 38 pods to run · 5 storage engines",
        "meerkat_sub": "app-gateway",
        "chips": [
            "login · MFA · passkeys · SSO",
            "roles · organisations · API tokens",
            "routing · rate limits · quotas",
            "TLS · ACME · secrets vault",
            "audit · dashboards",
        ],
        "jwt": "signed JWT",
        "jwt_sub": "identity · roles · organisation",
        "count_b": "1 binary · 0 dependency · 22 MB at rest",
    },
}

BG, PANEL, BORDER, TEXT, MUTED = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
GREEN, PURPLE, BLUE, ORANGE, RED = "#3fb950", "#a371f7", "#58a6ff", "#d29922", "#f85149"
DUR = 16  # loop length, seconds


def fade(begin, end=None, dur=0.4):
    """Opacity 0 -> 1 at `begin`, back to 0 at `end` (absolute seconds)."""
    a = f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
    if end is not None:
        a += f'<animate attributeName="opacity" from="1" to="0" begin="{end}s" dur="{dur}s" fill="freeze"/>'
    return a


def box(x, y, w, h, stroke, title, sub, begin, end, title_size=15):
    return f'''<g opacity="0">{fade(begin, end)}
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{PANEL}" stroke="{stroke}" stroke-width="2"/>
  <text x="{x + w / 2}" y="{y + h / 2 - 4}" text-anchor="middle" fill="{TEXT}" font-size="{title_size}" font-weight="600">{escape(title)}</text>
  <text x="{x + w / 2}" y="{y + h / 2 + 16}" text-anchor="middle" fill="{MUTED}" font-size="12">{escape(sub)}</text>
</g>'''


def svg(lang):
    t = T[lang]
    out = [f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="511" viewBox="0 0 900 511" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system, Segoe UI, Roboto, sans-serif">
<rect x="2" y="2" width="896" height="507" rx="18" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>''']

    # Phase A: 0 -> 7.4 s ; phase B: 8 -> 15.4 s ; everything faded out by 16 s so the GIF loops cleanly.
    A_END, B_BEGIN, B_END = 7.4, 8.0, 15.3

    # Titles
    out.append(f'<text x="40" y="52" fill="{TEXT}" font-size="22" font-weight="700" opacity="0">{escape(t["title_a"])}{fade(0.2, A_END)}</text>')
    out.append(f'<text x="40" y="52" fill="{TEXT}" font-size="22" font-weight="700" opacity="0">{escape(t["title_b"])}{fade(B_BEGIN, B_END)}</text>')

    out.append('<g transform="translate(0,28)">')

    # Browser and services: present in both phases
    for x, label, stroke in ((30, t["browser"], BLUE), (740, t["app"], GREEN)):
        out.append(box(x, 205, 130, 80, stroke, label, "", 0.1, B_END, title_size=16))

    # Phase A: the assembled stack, one product after another
    cols, rows = (192, 372, 552), (95, 180, 265)
    for i, (title, sub) in enumerate(t["boxes"]):
        x, y = cols[i % 3], rows[i // 3]
        out.append(box(x, y, 156, 64, ORANGE, title, sub, 0.6 + i * 0.35, A_END))
    out.append(box(cols[1], rows[2], 336, 64, RED, t["todo"][0], t["todo"][1], 0.6 + 7 * 0.35, A_END))
    out.append(f'''<g opacity="0">{fade(0.4, A_END)}
  <path d="M162,245 L188,245" stroke="{BORDER}" stroke-width="2" stroke-dasharray="4 4"/>
  <path d="M712,245 L738,245" stroke="{BORDER}" stroke-width="2" stroke-dasharray="4 4"/>
</g>''')
    out.append(f'<text x="450" y="395" text-anchor="middle" fill="{ORANGE}" font-size="17" font-weight="600" opacity="0">{escape(t["count_a"])}{fade(3.6, A_END)}</text>')

    # Phase A request: hops through the stack before reaching the services
    hops = "M160,245 L192,127 L708,127 L708,212 L192,212 L192,297 L740,245"
    out.append(f'''<circle r="7" fill="{BLUE}" opacity="0">
  <set attributeName="opacity" to="1" begin="4.2s"/><set attributeName="opacity" to="0" begin="7.0s"/>
  <animateMotion path="{hops}" begin="4.2s" dur="2.8s" fill="freeze"/>
</circle>''')

    # Phase B: one door
    mx, my, mw, mh = 250, 88, 400, 290
    chips = "".join(
        f'<circle cx="{mx + 34}" cy="{my + 108 + k * 34}" r="5" fill="{GREEN if k % 2 == 0 else PURPLE}"/>'
        f'<text x="{mx + 50}" y="{my + 113 + k * 34}" fill="{TEXT}" font-size="14">{escape(c)}</text>'
        for k, c in enumerate(t["chips"])
    )
    out.append(f'''<g opacity="0">{fade(B_BEGIN + 0.2, B_END)}
  <rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="14" fill="{PANEL}" stroke="{PURPLE}" stroke-width="2.5"/>
  <text x="{mx + mw / 2}" y="{my + 44}" text-anchor="middle" fill="{TEXT}" font-size="26" font-weight="700">Meerkat</text>
  <text x="{mx + mw / 2}" y="{my + 68}" text-anchor="middle" fill="{PURPLE}" font-size="14" letter-spacing="2">{escape(t["meerkat_sub"].upper())}</text>
  {chips}
</g>''')
    # Arrows and labels
    out.append(f'''<g opacity="0">{fade(B_BEGIN + 0.6, B_END)}
  <line x1="162" y1="245" x2="{mx - 4}" y2="245" stroke="{BLUE}" stroke-width="2"/>
  <line x1="{mx + mw + 4}" y1="245" x2="738" y2="245" stroke="{GREEN}" stroke-width="2"/>
  <text x="{(mx + mw + 740) / 2}" y="232" text-anchor="middle" fill="{GREEN}" font-size="14" font-weight="600">{escape(t["jwt"])}</text>
</g>''')
    out.append(f'<text x="805" y="305" text-anchor="middle" fill="{MUTED}" font-size="11" opacity="0">{escape(t["jwt_sub"])}{fade(B_BEGIN + 2.6, B_END)}</text>')
    out.append(f'<text x="450" y="425" text-anchor="middle" fill="{GREEN}" font-size="17" font-weight="600" opacity="0">{escape(t["count_b"])}{fade(B_BEGIN + 1.2, B_END)}</text>')

    # Phase B request: straight through, once
    out.append(f'''<circle r="7" fill="{BLUE}" opacity="0">
  <set attributeName="opacity" to="1" begin="{B_BEGIN + 1.4}s"/><set attributeName="opacity" to="0" begin="{B_BEGIN + 3.6}s"/>
  <animateMotion path="M160,245 L{mx},245" begin="{B_BEGIN + 1.4}s" dur="0.7s" fill="freeze"/>
  <animateMotion path="M{mx + mw},245 L740,245" begin="{B_BEGIN + 2.4}s" dur="0.7s" fill="freeze"/>
  <animate attributeName="fill" to="{GREEN}" begin="{B_BEGIN + 2.3}s" dur="0.01s" fill="freeze"/>
</circle>''')

    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    for lang in T:
        with open(f"app-gateway.{lang}.svg", "w", encoding="utf-8") as f:
            f.write(svg(lang))
        print(f"app-gateway.{lang}.svg")
