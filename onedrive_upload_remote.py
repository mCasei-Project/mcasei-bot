"""
mCasei — OneDrive Upload (versão remota/cloud)
------------------------------------------------
Lê credenciais de variáveis de ambiente (não de ficheiro local).
Para usar no agente remoto Cowork.

Variáveis de ambiente necessárias:
    ONEDRIVE_CLIENT_ID
    ONEDRIVE_CLIENT_SECRET
    ONEDRIVE_REFRESH_TOKEN
    ONEDRIVE_TENANT_ID      (usar "consumers" para conta pessoal)
    ONEDRIVE_BASE_PATH      (ex: "mCasei/Posts")

Uso:
    python onedrive_upload_remote.py --date 2026-06-03
"""

import json, sys, os, requests, argparse
from pathlib import Path
from datetime import datetime

GRAPH = "https://graph.microsoft.com/v1.0"

def get_access_token() -> tuple[str, str]:
    """Usa o refresh_token para obter um novo access_token. Retorna (access_token, novo_refresh_token)."""
    client_id     = os.environ["ONEDRIVE_CLIENT_ID"]
    client_secret = os.environ["ONEDRIVE_CLIENT_SECRET"]
    refresh_token = os.environ["ONEDRIVE_REFRESH_TOKEN"]
    tenant_id     = os.environ.get("ONEDRIVE_TENANT_ID", "consumers")

    resp = requests.post(
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        data={
            "client_id":     client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type":    "refresh_token",
            "scope":         "https://graph.microsoft.com/Files.ReadWrite offline_access",
        }
    )
    resp.raise_for_status()
    data = resp.json()
    return data["access_token"], data["refresh_token"]


def upload_png(access_token: str, local_path: Path, remote_path: str) -> dict:
    """Faz upload de um PNG e retorna URLs."""
    headers   = {"Authorization": f"Bearer {access_token}", "Content-Type": "image/png"}
    png_bytes = local_path.read_bytes()
    upload_uri = f"{GRAPH}/me/drive/root:/{remote_path}:/content"

    resp = requests.put(upload_uri, headers=headers, data=png_bytes)
    resp.raise_for_status()
    item    = resp.json()
    item_id = item["id"]

    info = requests.get(f"{GRAPH}/me/drive/items/{item_id}",
                        headers={"Authorization": f"Bearer {access_token}"}).json()
    download_url = info.get("@microsoft.graph.downloadUrl", "")

    share_resp = requests.post(
        f"{GRAPH}/me/drive/items/{item_id}/createLink",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json={"type": "view", "scope": "anonymous"}
    )
    share_url = share_resp.json().get("link", {}).get("webUrl", "") if share_resp.ok else ""

    return {"file": local_path.name, "item_id": item_id,
            "download_url": download_url, "share_url": share_url}


def upload_triplet(date_str: str) -> dict:
    base_dir   = Path(__file__).parent
    posts_dir  = base_dir / "Posts" / date_str
    remote_base = f"{os.environ.get('ONEDRIVE_BASE_PATH', 'mCasei/Posts')}/{date_str}"

    access_token, new_refresh = get_access_token()
    print(f"  ℹ novo refresh_token gerado — actualiza ONEDRIVE_REFRESH_TOKEN no ambiente mCasei")
    print(f"  NEW_REFRESH_TOKEN={new_refresh}")

    results = {}

    p1 = posts_dir / "post1_impacto.png"
    if p1.exists():
        results["post1"] = upload_png(access_token, p1, f"{remote_base}/post1_impacto.png")
        print(f"  ✓ post1 → {results['post1']['download_url'][:70]}...")

    p3 = posts_dir / "post3_lema.png"
    if p3.exists():
        results["post3"] = upload_png(access_token, p3, f"{remote_base}/post3_lema.png")
        print(f"  ✓ post3 → {results['post3']['download_url'][:70]}...")

    slides_dir = posts_dir / "post2_slides"
    if slides_dir.exists():
        slides = sorted(slides_dir.glob("slide_*.png"))
        results["post2_slides"] = []
        for slide in slides:
            r = upload_png(access_token, slide, f"{remote_base}/post2_slides/{slide.name}")
            results["post2_slides"].append(r)
            print(f"  ✓ {slide.name} → {r['download_url'][:70]}...")

    output = posts_dir / "upload_urls.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    print(f"\n📤 Upload triplet {args.date} → OneDrive...")
    results = upload_triplet(args.date)
    print(f"\n✅ {len(results)} item(s) enviado(s)")
    print(json.dumps(results, indent=2))
