"""Design tokens loader: colors per volume, color mixing, EPUB CSS generation."""
import pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOK = yaml.safe_load(open(ROOT / "design" / "tokens.yaml"))

def theme(vol):
    v = TOK["volumes"][str(vol if str(vol) in TOK["volumes"] else 1)]
    n = TOK["neutrals"]
    return {**n, **v}

def mix(hex_a, hex_b, t):
    """t=0 -> a, t=1 -> b"""
    a = [int(hex_a[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(hex_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(x * (1 - t) + y * t) for x, y in zip(a, b))

def css(vol):
    th = theme(vol)
    return f"""
/* generated from design/tokens.yaml (volume {vol}) */
h1 {{ border-bottom: 0.18em solid {th['accent']}; padding-bottom: 0.25em; margin-top: 1.2em; }}
h2 {{ border-left: 0.35em solid {th['accent']}; padding-left: 0.5em; margin-top: 1.6em; }}
h3 {{ color: {th['accent_dark']}; margin-top: 1.3em; }}
blockquote {{ border-left: 0.3em solid {th['accent']}; background: {th['tint']}; margin: 1em 0; padding: 0.6em 1em; }}
table {{ border-collapse: collapse; width: 100%; font-size: 0.92em; margin: 1em 0; }}
th {{ background: {th['accent']}; color: {th['on_accent']}; padding: 0.35em 0.5em; text-align: left; }}
td {{ border-bottom: 1px solid {th['light']}; padding: 0.35em 0.5em; vertical-align: top; }}
figure {{ margin: 1.2em 0; text-align: center; page-break-inside: avoid; }}
figure img {{ max-width: 100%; height: auto; }}
figcaption {{ font-size: 0.85em; color: {th['mid']}; margin-top: 0.3em; }}
"""
