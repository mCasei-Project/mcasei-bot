"""
mCasei — Upload Images via Imgbb API
--------------------------------------
Envia os PNGs do triplet para o Imgbb (hosting gratuito, permanente)
e gera Posts/{date}/upload_urls.json com URLs directas para o Buffer.

Substitui publish_images_github.py — sem git, sem PAT tokens.

Pré-requisito: variavel de ambiente IMGBB_API_KEY
  Obtém chave gratuita em https://api.imgbb.com/ (conta gratuita)

Uso:
    python upload_images_imgbb.py --date 2026-06-04

Gera Posts/{date}/upload_urls.json com a mesma estrutura do uploader GitHub.
"""

import json, sys, os, argparse, base64, time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")

IMGBB_UPLOAD = "https://api.imgbb.com/1/upload"


def upload_file(api_key: str, file_path: Path, name: str) -> str:
    """Faz upload de um PNG para o Imgbb e devolve a URL directa."""
    image_b64 = base64.b64encode(file_path.read_bytes()).decode("utf-8")
    resp = requests.post(
        IMGBB_UPLOAD,
        data={"key": api_key, "image": image_b64, "name": name},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Imgbb recusou {name}: {data}")
    url = data["data"]["url"]
    print(f"  ✓ {name} → {url}")
    return url


def publish(date_str: str) -> dict:
    api_key = os.environ.get("IMGBB_API_KEY", "").strip()
    if not api_key:
        print("❌ IMGBB_API_KEY não definida — adiciona ao set-env.bat")
        sys.exit(1)

    base_dir  = Path(__file__).parent
    posts_dir = base_dir / "Posts" / date_str

    if not posts_dir.exists():
        print(f"❌ Pasta não existe: {posts_dir}")
        sys.exit(1)

    results = {}

    p1 = posts_dir / "post1_impacto.png"
    if p1.exists():
        url = upload_file(api_key, p1, f"{date_str}_post1_impacto")
        results["post1"] = {"file": p1.name, "download_url": url}
        time.sleep(0.5)  # rate-limit cortesia

    p3 = posts_dir / "post3_lema.png"
    if p3.exists():
        url = upload_file(api_key, p3, f"{date_str}_post3_lema")
        results["post3"] = {"file": p3.name, "download_url": url}
        time.sleep(0.5)

    # Pasta canónica dos slides do carrossel: <date>/slides/ (escrita pela skill
    # mcasei-carrousel). Só recorre a post2_slides/ (legado) se slides/ não existir.
    slides_dir = posts_dir / "slides"
    if not slides_dir.exists():
        slides_dir = posts_dir / "post2_slides"
    if slides_dir.exists():
        slides = sorted(slides_dir.glob("slide_*.png"))
        results["post2_slides"] = []
        for s in slides:
            url = upload_file(api_key, s, f"{date_str}_{s.stem}")
            results["post2_slides"].append({"file": s.name, "download_url": url})
            time.sleep(0.5)

    out = posts_dir / "upload_urls.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Data no formato YYYY-MM-DD")
    args = parser.parse_args()

    print(f"\n📤 A fazer upload dos PNGs {args.date} para Imgbb...")
    results = publish(args.date)
    print(f"\n✅ Upload concluído — {sum(1 if k in ('post1','post3') else len(v) for k,v in results.items())} ficheiros")
    print(json.dumps(results, indent=2, ensure_ascii=False))
