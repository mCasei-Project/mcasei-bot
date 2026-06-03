"""
mCasei — Export Triplet via Playwright
---------------------------------------
Recebe um ficheiro HTML e exporta como PNG 1080x1350px.

Uso:
    python export_triplet.py --html post1.html --out Posts/2026-06-03/post1_impacto.png
    python export_triplet.py --dir Posts/2026-06-03/  # exporta todos os .html na pasta
"""

import argparse
import sys
from pathlib import Path


def export_html_to_png(html_path: Path, out_path: Path, width: int = 1080, height: int = 1350):
    """Renderiza um HTML e exporta como PNG usando Playwright."""
    from playwright.sync_api import sync_playwright

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(f"file:///{html_path.resolve()}")
        page.wait_for_timeout(1000)  # aguarda fontes e animações
        page.screenshot(path=str(out_path), full_page=False)
        browser.close()

    print(f"  ✓ {out_path.name} exportado ({width}x{height}px)")
    return out_path


def export_directory(dir_path: Path, width: int = 1080, height: int = 1350):
    """Exporta todos os ficheiros .html numa pasta como PNG."""
    html_files = sorted(dir_path.glob("*.html"))
    if not html_files:
        print(f"Nenhum ficheiro .html encontrado em {dir_path}")
        return []

    results = []
    for html_file in html_files:
        out_file = html_file.with_suffix(".png")
        export_html_to_png(html_file, out_file, width, height)
        results.append(out_file)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporta HTMLs do triplet mCasei como PNGs")
    parser.add_argument("--html",   help="Ficheiro HTML a exportar")
    parser.add_argument("--out",    help="Caminho de saída do PNG")
    parser.add_argument("--dir",    help="Pasta com ficheiros HTML a exportar")
    parser.add_argument("--width",  type=int, default=1080)
    parser.add_argument("--height", type=int, default=1350)
    args = parser.parse_args()

    if args.dir:
        results = export_directory(Path(args.dir), args.width, args.height)
        print(f"\n✅ {len(results)} PNG(s) exportado(s)")
    elif args.html:
        out = Path(args.out) if args.out else Path(args.html).with_suffix(".png")
        export_html_to_png(Path(args.html), out, args.width, args.height)
        print(f"\n✅ PNG exportado: {out}")
    else:
        parser.print_help()
        sys.exit(1)
