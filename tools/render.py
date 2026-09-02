#!/usr/bin/env python3
"""Render a protocol Markdown file to a paginated, print-ready HTML document.

The Markdown files are canonical. This exists so a PDF can be regenerated from
them instead of maintaining a second copy by hand — a specification with two
divergent renderings is worse than one with none.

Standard library only. Handles the subset of Markdown the specs actually use:
ATX headings, paragraphs, pipe tables, fenced code, blockquotes, unordered
lists, thematic breaks, and inline bold / italic / code / links.

    python3 tools/render.py SPEC.md build/SPEC.html
    # then: Chrome --headless --print-to-pdf
"""
import html
import os
import re
import sys

CSS = """
@page { size: A4; margin: 16mm 17mm 18mm; }
:root {
  --ink:#171A18; --ink2:#333937; --muted:#5C6663; --faint:#8A9491;
  --rule:#D8DDDB; --rule2:#ECEFEE; --norm:#1C4E5C; --card:#FAFBFB;
}
* { box-sizing:border-box; }
body {
  font-family:"Spectral",Georgia,serif; font-size:9.6pt; line-height:1.5;
  color:var(--ink); background:#fff; margin:0; padding:0;
  -webkit-font-smoothing:antialiased;
}
.doc { max-width:none; }
h1,h2,h3 { font-family:"Libre Franklin",system-ui,sans-serif; text-wrap:balance; }
h1 {
  font-size:21pt; font-weight:600; line-height:1.12; letter-spacing:-.02em;
  margin:0 0 8pt; padding-bottom:8pt; border-bottom:2.2pt solid var(--ink);
}
h2 {
  font-size:12.5pt; font-weight:600; line-height:1.2; letter-spacing:-.01em;
  margin:15pt 0 5pt; padding-top:7pt; border-top:.5pt solid var(--rule);
  break-after:avoid; page-break-after:avoid;
}
h3 {
  font-size:10.4pt; font-weight:600; margin:10pt 0 4pt;
  break-after:avoid; page-break-after:avoid;
}
p { margin:0 0 5.5pt; max-width:none; orphans:2; widows:2; }
strong { font-weight:600; }
em { font-style:italic; }
a { color:var(--norm); text-decoration:none; }
code {
  font-family:"JetBrains Mono",ui-monospace,monospace; font-size:.86em;
  background:var(--card); padding:.5pt 2pt; border-radius:2px; color:var(--norm);
}
pre {
  font-family:"JetBrains Mono",ui-monospace,monospace; font-size:7.6pt; line-height:1.5;
  background:var(--card); border:.5pt solid var(--rule); border-radius:2px;
  padding:7pt 9pt; margin:7pt 0; overflow-x:auto; white-space:pre;
  break-inside:avoid; page-break-inside:avoid;
}
pre code { background:none; padding:0; color:var(--ink); font-size:inherit; }
blockquote {
  margin:7pt 0; padding:7pt 9pt; background:#EAF2F4;
  border:.5pt solid rgba(28,78,92,.28); border-radius:2px;
  break-inside:avoid; page-break-inside:avoid;
}
blockquote p { margin:0; }
blockquote strong:first-child { color:var(--norm); }
ul { margin:0 0 6pt; padding-left:0; list-style:none; }
li { position:relative; padding-left:11pt; margin-bottom:3pt; }
li::before {
  content:""; position:absolute; left:1.5pt; top:.62em;
  width:3.4pt; height:3.4pt; border:.6pt solid var(--faint); border-radius:50%;
}
table {
  border-collapse:collapse; width:100%; font-size:8.6pt; margin:7pt 0;
  break-inside:avoid; page-break-inside:avoid;
}
th,td { text-align:left; padding:3.5pt 7pt 3.5pt 0; border-bottom:.5pt solid var(--rule2); vertical-align:top; }
th {
  font-family:"JetBrains Mono",monospace; font-size:6.9pt; letter-spacing:.08em;
  text-transform:uppercase; color:var(--muted); font-weight:500;
  border-bottom:.6pt solid var(--rule);
}
td code { font-size:.92em; }
hr { border:none; border-top:.5pt solid var(--rule); margin:9pt 0; }
.docmeta { font-size:8.4pt; color:var(--muted); margin:0 0 9pt; }
"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=JetBrains+Mono:wght@400;500&family=Libre+Franklin:wght@400;500;600&'
         'family=Spectral:ital,wght@0,400;0,600;1,400&display=swap">')


def inline(t):
    t = html.escape(t, quote=False)
    out, i, n = [], 0, len(t)
    while i < n:                                    # code spans first, verbatim
        if t[i] == "`":
            j = t.find("`", i + 1)
            if j > i:
                out.append("<code>" + t[i + 1:j] + "</code>")
                i = j + 1
                continue
        out.append(t[i])
        i += 1
    t = "".join(out)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<em>\1</em>", t)
    return t


def render(md):
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)

    def flush_para(buf):
        if buf:
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
            buf.clear()

    para = []
    while i < n:
        ln = lines[i]

        if ln.startswith("```"):
            flush_para(para)
            i += 1
            block = []
            while i < n and not lines[i].startswith("```"):
                block.append(html.escape(lines[i], quote=False))
                i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(block) + "</code></pre>")
            continue

        if re.match(r"^\|.*\|\s*$", ln) and i + 1 < n and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush_para(para)
            hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and re.match(r"^\|.*\|\s*$", lines[i]):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>"] + [f"<th>{inline(c)}</th>" for c in hdr] + ["</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        if ln.startswith(">"):
            flush_para(para)
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(x for x in buf if x)) + "</p></blockquote>")
            continue

        if re.match(r"^[-*] ", ln):
            flush_para(para)
            items = []
            while i < n and (re.match(r"^[-*] ", lines[i]) or (items and lines[i].startswith("  ") and lines[i].strip())):
                if re.match(r"^[-*] ", lines[i]):
                    items.append(lines[i][2:].strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue

        m = re.match(r"^(#{1,3}) +(.*)$", ln)
        if m:
            flush_para(para)
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        if re.match(r"^---+\s*$", ln):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        if not ln.strip():
            flush_para(para)
            i += 1
            continue

        para.append(ln.strip())
        i += 1

    flush_para(para)
    return "\n".join(out)


def main(src, dst):
    md = open(src, encoding="utf-8").read()
    title = re.search(r"^# +(.*)$", md, re.M)
    title = title.group(1) if title else os.path.basename(src)
    body = render(md)
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f"<title>{html.escape(title)}</title>{FONTS}"
           f"<style>{CSS}</style></head><body><div class=\"doc\">{body}</div></body></html>")
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    open(dst, "w", encoding="utf-8").write(doc)
    print(f"{src} -> {dst}  ({len(body)} bytes of body)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
