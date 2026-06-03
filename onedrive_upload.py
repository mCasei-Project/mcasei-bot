"""
mCasei — OneDrive Upload Helper
--------------------------------
Faz upload de PNGs para o OneDrive via Microsoft Graph API e
retorna URLs directas para usar no Buffer.

Uso:
    python onedrive_upload.py --date 2026-06-02 --config .onedrive-config.json

Retorna JSON com as URLs de cada imagem.
"""

import json, sys, os, requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
GRAPH    = "https://graph.microsoft.com/v1.0"


def get_access_token(config: dict) -> str:
    """Usa o refresh_token para obter um novo access_token."""
    resp = requests.post(config["token_url"], data={
        "client_id":     config["client_id"],
        "client_secret": config["client_secret"],
        "refresh_token": config["refresh_token"],
        "grant_type":    "refresh_token",
        "scope":         config["scope"],
    })
    resp.raise_for_status()
    data = resp.json()

    # Actualizar o refresh_token no config (pode mudar a cada renovação)
    config["refresh_token"] = data["refresh_token"]
    config["obtained_at"]   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config_path = BASE_DIR / ".onedrive-config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    return data["access_token"]


def upload_png(access_token: str, local_path: Path, remote_path: str) -> dict:
    """
    Faz upload de um PNG e retorna:
    - download_url: URL directa para o Buffer usar
    - share_url: link de partilha público
    - item_id: ID do ficheiro no OneDrive
    """
    headers    = {"Authorization": f"Bearer {access_token}"}
    png_bytes  = local_path.read_bytes()
    upload_uri = f"{GRAPH}/me/drive/root:/{remote_path}:/content"

    resp = requests.put(upload_uri, headers=headers,
                        data=png_bytes, content_type="image/png")
    if hasattr(resp, 'raise_for_status'):
        resp.raise_for_status()
    # requests
    import requests as req
    resp = req.put(upload_uri,
                   headers={**headers, "Content-Type": "image/png"},
                   data=png_bytes)
    resp.raise_for_status()
    item = resp.json()
    item_id = item["id"]

    # Obter download URL directa
    info_resp = req.get(f"{GRAPH}/me/drive/items/{item_id}", headers=headers)
    info_resp.raise_for_status()
    info = info_resp.json()
    download_url = info.get("@microsoft.graph.downloadUrl", "")

    # Criar share link público (mais permanente)
    share_resp = req.post(
        f"{GRAPH}/me/drive/items/{item_id}/createLink",
        headers={**headers, "Content-Type": "application/json"},
        json={"type": "view", "scope": "anonymous"}
    )
    share_url = share_resp.json().get("link", {}).get("webUrl", "") if share_resp.ok else ""

    return {
        "file":         local_path.name,
        "item_id":      item_id,
        "download_url": download_url,
        "share_url":    share_url,
    }


def upload_triplet(date_str: str, config_path: str = ".onedrive-config.json") -> dict:
    """
    Faz upload dos 3 posts do triplet e retorna as URLs.

    Estrutura esperada:
    Posts/{date}/post1_impacto.png
    Posts/{date}/post2_slides/slide_1.png ... slide_N.png
    Posts/{date}/post3_lema.png
    """
    config     = json.loads((BASE_DIR / config_path).read_text(encoding="utf-8"))
    token      = get_access_token(config)
    posts_dir  = BASE_DIR / "Posts" / date_str
    remote_base = f"{config['onedrive_base']}/{date_str}"

    results = {}

    # Post 1 — Impacto
    p1 = posts_dir / "post1_impacto.png"
    if p1.exists():
        results["post1"] = upload_png(token, p1, f"{remote_base}/post1_impacto.png")
        print(f"  ✓ post1_impacto.png → {results['post1']['download_url'][:60]}...")

    # Post 3 — Lema
    p3 = posts_dir / "post3_lema.png"
    if p3.exists():
        results["post3"] = upload_png(token, p3, f"{remote_base}/post3_lema.png")
        print(f"  ✓ post3_lema.png → {results['post3']['download_url'][:60]}...")

    # Post 2 — Carrossel (vários slides)
    slides_dir = posts_dir / "post2_slides"
    if slides_dir.exists():
        slides = sorted(slides_dir.glob("slide_*.png"))
        results["post2_slides"] = []
        for slide in slides:
            r = upload_png(token, slide, f"{remote_base}/post2_slides/{slide.name}")
            results["post2_slides"].append(r)
            print(f"  ✓ {slide.name} → {r['download_url'][:60]}...")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date",   default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--config", default=".onedrive-config.json")
    args = parser.parse_args()

    print(f"\n📤 Upload triplet {args.date} → OneDrive...")
    results = upload_triplet(args.date, args.config)

    output = BASE_DIR / "Posts" / args.date / "upload_urls.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n✅ URLs guardadas em: {output}")
    print(json.dumps(results, indent=2))
