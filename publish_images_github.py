"""
mCasei — Publish Images via GitHub raw
----------------------------------------
Commita os PNGs do triplet no repo e gera URLs raw.githubusercontent.com
para o Buffer usar. Substitui o OneDrive (sem tokens que expiram).

Pré-requisito: o repo deve ter sido clonado com credencial de push, ex:
    git clone https://x-access-token:$GITHUB_PAT@github.com/mCasei-Project/mcasei-bot.git

Uso:
    python publish_images_github.py --date 2026-06-03

Gera Posts/{date}/upload_urls.json com a mesma estrutura do uploader OneDrive.
"""

import json, sys, os, argparse, subprocess
from pathlib import Path

REPO   = "mCasei-Project/mcasei-bot"
BRANCH = "master"
RAW    = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"


def run(cmd: list[str], cwd: Path):
    print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"    stderr: {r.stderr.strip()}")
    return r


def publish(date_str: str) -> dict:
    base_dir  = Path(__file__).parent
    posts_dir = base_dir / "Posts" / date_str
    rel_base  = f"Posts/{date_str}"

    if not posts_dir.exists():
        print(f"❌ Pasta não existe: {posts_dir}")
        sys.exit(1)

    # Configurar identidade git (idempotente)
    run(["git", "config", "user.email", "noreply@mcasei.co.mz"], base_dir)
    run(["git", "config", "user.name", "mCasei Bot"], base_dir)

    # Adicionar e commitar os PNGs
    run(["git", "add", "-f", f"{rel_base}"], base_dir)
    run(["git", "commit", "-m", f"Posts triplet {date_str}"], base_dir)
    push = run(["git", "push", "origin", BRANCH], base_dir)
    if push.returncode != 0:
        print("❌ git push falhou — verifica GITHUB_PAT")
        sys.exit(1)

    # Construir URLs raw
    results = {}

    p1 = posts_dir / "post1_impacto.png"
    if p1.exists():
        results["post1"] = {"file": p1.name, "download_url": f"{RAW}/{rel_base}/post1_impacto.png"}

    p3 = posts_dir / "post3_lema.png"
    if p3.exists():
        results["post3"] = {"file": p3.name, "download_url": f"{RAW}/{rel_base}/post3_lema.png"}

    slides_dir = posts_dir / "post2_slides"
    if slides_dir.exists():
        slides = sorted(slides_dir.glob("slide_*.png"))
        results["post2_slides"] = [
            {"file": s.name, "download_url": f"{RAW}/{rel_base}/post2_slides/{s.name}"}
            for s in slides
        ]

    out = posts_dir / "upload_urls.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    args = parser.parse_args()

    print(f"\n📤 A publicar PNGs {args.date} via GitHub raw...")
    results = publish(args.date)
    print(f"\n✅ URLs geradas:")
    print(json.dumps(results, indent=2))
