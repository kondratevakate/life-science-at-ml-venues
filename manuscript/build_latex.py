"""Render manuscript.md and tables.json to a LaTeX project for Overleaf.

Same source as build_docx.py, so the Word and LaTeX versions cannot drift apart: edit manuscript.md, then rebuild
both. Numeric citations [n] become \\cite{rn}; bracketed placeholders such as [EMAIL] are kept and shown in red so
co-authors see what is still missing.

Usage: python manuscript/build_latex.py   -> manuscript/latex/ (main.tex, figures/), manuscript/out/overleaf.zip
"""
from __future__ import annotations

import json
import re
import shutil
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEX = HERE / "latex"
ZIP = HERE / "out" / "overleaf.zip"
INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\^[^^]+\^|https?://[^\s)]+[^\s).,;]|\[[^\]]+\])")
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
           "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage{setspace}
\usepackage{graphicx}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{lineno}
\usepackage[hidelinks]{hyperref}
\usepackage{xurl}
\DeclareUnicodeCharacter{2212}{\ensuremath{-}}
\newcommand{\todo}[1]{\textcolor{red}{#1}}
\onehalfspacing
\linenumbers
"""
TABLE_TITLES = {
    "table1": "Reproducibility practices stated in the full text, medical versus other papers, nine venue-years. "
              "Shares among papers with a known value; pooled difference is the Mantel-Haenszel risk difference over "
              "venue-years with a 95\\% paper bootstrap interval.",
    "table2": "Reproduction outcomes of attempted ICML 2026 papers, medical minus other, unadjusted and adjusted "
              "(post hoc analyses, Notes 9-9 to 9-15).",
    "table3": "Agreement of stated practices with what reproducers obtained (222 attempted ICML 2026 frame papers; "
              "pooled with the 300-paper extension sample in the last column).",
    "table4": "Sensitivity of the documentation differences (medical minus other, Mantel-Haenszel over venue-years, "
              "points with 95\\% CI): main analysis, empirical papers only, and all coded papers with unstated "
              "releases counted as none (post hoc, Note 9-22).",
}


def esc(s: str) -> str:
    return "".join(SPECIAL.get(c, c) for c in s)


def inline(text: str) -> str:
    out = []
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**"):
            out.append(r"\textbf{" + inline(part[2:-2]) + "}")
        elif part.startswith("*") and len(part) > 2:
            out.append(r"\textit{" + inline(part[1:-1]) + "}")
        elif part.startswith("`"):
            out.append(r"\texttt{" + esc(part[1:-1]) + "}")
        elif part.startswith("^"):
            out.append(r"\textsuperscript{" + esc(part[1:-1]) + "}")
        elif part.startswith("http"):
            out.append(r"\url{" + part.replace("%", r"\%").replace("#", r"\#") + "}")
        elif part.startswith("["):
            inner = part[1:-1]
            if re.fullmatch(r"\d+(\s*,\s*\d+)*", inner):
                out.append(r"~\cite{" + ",".join("r" + n.strip() for n in inner.split(",")) + "}")
            elif inner in ("Internet", "Preprint", "dataset"):
                out.append(esc(part))
            else:
                out.append(r"\todo{" + esc(part) + "}")
        else:
            out.append(esc(part))
    return "".join(out).replace(" ~\\cite", "~\\cite")


def table(rows: list[list[str]], caption: str, label: str) -> str:
    n = len(rows[0])
    spec = "X" + "l" * (n - 1) if n > 3 else "X" + "l" * (n - 1)
    body = [" & ".join(r"\textbf{" + esc(c) + "}" for c in rows[0]) + r" \\ \midrule"]
    body += [" & ".join(esc(c) for c in r) + r" \\" for r in rows[1:]]
    return ("\\begin{table}[p]\n\\centering\\footnotesize\n\\caption{" + caption + "}\\label{" + label + "}\n"
            "\\begin{tabularx}{\\textwidth}{" + spec + "}\n\\toprule\n" + "\n".join(body) +
            "\n\\bottomrule\n\\end{tabularx}\n\\end{table}\n")


def main() -> None:
    lines = (HERE / "manuscript.md").read_text(encoding="utf-8").splitlines()
    tables = json.loads((HERE / "tables.json").read_text(encoding="utf-8"))
    title = lines[0].lstrip("# ").strip()
    head, i = [], 1
    while not lines[i].startswith("## "):
        if lines[i].strip():
            head.append(inline(lines[i]))
        i += 1
    doc = [PREAMBLE, "\\title{" + esc(title) + "}", "\\author{" + head[0] + "}", "\\date{}",
           "\\begin{document}", "\\maketitle", "\\begin{flushleft}\\small", r" \\ ".join(head[1:]),
           "\\end{flushleft}"]
    section, refs, figures = None, [], []
    for line in lines[i:]:
        m = re.match(r"(#{2,3}) (.*)", line)
        if m:
            section = m.group(2)
            if section in ("References", "Figure legends"):
                continue
            if section == "Tables":
                doc.append("\\clearpage")
                continue
            doc.append(("\\section*{" if len(m.group(1)) == 2 else "\\subsection*{") + esc(section) + "}")
            continue
        if not line.strip():
            continue
        if section == "References":
            rm = re.match(r"(\d+)\. (.*)", line)
            refs.append((rm.group(1), inline(rm.group(2))))
        elif section == "Figure legends":
            fm = re.match(r"\*\*Figure (\d)\.\*\* (.*)", line)
            figures.append((fm.group(1), inline(fm.group(2))))
        elif line.strip().upper() in ("TABLE1", "TABLE2", "TABLE3", "TABLE4"):
            key = line.strip().lower()
            doc.append(table(tables[key], TABLE_TITLES[key], "tab:" + key))
        else:
            doc.append(inline(line) + "\n")
    for n, cap in figures:
        doc.append("\\begin{figure}[p]\n\\centering\n\\includegraphics[width=\\textwidth]{figures/fig" + n +
                   ".png}\n\\caption{" + cap + "}\\label{fig:" + n + "}\n\\end{figure}\n")
    bib = ["\\begin{thebibliography}{99}"] + [f"\\bibitem{{r{n}}} {t}" for n, t in refs] + ["\\end{thebibliography}"]
    # References go before the floats so they print after the Declarations, as in the Word version.
    doc.insert(next(k for k, d in enumerate(doc) if d == "\\clearpage"), "\n".join(bib))
    doc.append("\\end{document}")
    TEX.mkdir(exist_ok=True)
    (TEX / "figures").mkdir(exist_ok=True)
    (TEX / "main.tex").write_text("\n".join(doc), encoding="utf-8")
    for f in (HERE / "figures").glob("fig*.png"):
        shutil.copy(f, TEX / "figures" / f.name)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(TEX.rglob("*")):
            if f.is_file() and f.suffix in (".tex", ".png"):
                z.write(f, f.relative_to(TEX).as_posix())
    print(f"written {TEX / 'main.tex'} and {ZIP.name}")


if __name__ == "__main__":
    main()
