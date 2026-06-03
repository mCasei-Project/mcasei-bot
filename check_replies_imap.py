"""
mCasei — Ler respostas de aprovação via IMAP (appsuite.cloud)
--------------------------------------------------------------
O Agente 2 usa isto para ler a resposta do humano na inbox contacto@mcasei.co.mz.
(O Gmail MCP não serve — a conta está no appsuite.cloud, não no Gmail.)

Variáveis de ambiente:
    IMAP_HOST      (ex: imap.us.appsuite.cloud)
    IMAP_PORT      (default 993)
    IMAP_USER      (ex: contacto@mcasei.co.mz)
    IMAP_PASSWORD

Uso:
    python check_replies_imap.py --date 2026-06-03 --from-addr noreply@app.mcasei.co.mz

Imprime JSON: {"decision":"OK|EDITAR|NONE","instruction":"...","raw":"..."}
- Procura a resposta mais recente cujo assunto contém "[mCasei] Triplet {date}"
  e que NÃO foi enviada pelo próprio bot (exclui --from-addr).
"""

import imaplib, email, os, sys, json, argparse, re
from email.header import decode_header


def _decode(s):
    if not s:
        return ""
    parts = decode_header(s)
    out = ""
    for txt, enc in parts:
        out += txt.decode(enc or "utf-8", "ignore") if isinstance(txt, bytes) else txt
    return out


def _body_text(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(part.get_content_charset() or "utf-8", "ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(msg.get_content_charset() or "utf-8", "ignore")
    return ""


def _strip_quoted(body: str) -> str:
    """Remove texto citado da resposta (linhas > e tudo após 'On ... wrote:')."""
    lines = []
    for ln in body.splitlines():
        if ln.strip().startswith(">"):
            break
        if re.match(r"^(On .+wrote:|Em .+escreveu:|-{2,} ?Mensagem)", ln.strip()):
            break
        lines.append(ln)
    return "\n".join(lines).strip()


def check(date_str: str, from_addr: str) -> dict:
    host = os.environ.get("IMAP_HOST", "imap.us.appsuite.cloud")
    port = int(os.environ.get("IMAP_PORT", "993"))
    user = os.environ["IMAP_USER"]
    pwd  = os.environ["IMAP_PASSWORD"]

    M = imaplib.IMAP4_SSL(host, port)
    M.login(user, pwd)
    M.select("INBOX")

    typ, data = M.search(None, "ALL")
    ids = data[0].split()
    subject_key = f"[mCasei] Triplet {date_str}"

    best = None  # (uid_int, decision, instruction, raw)
    for num in reversed(ids):  # mais recentes primeiro
        typ, msg_data = M.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        subj = _decode(msg.get("Subject"))
        sender = _decode(msg.get("From"))

        if subject_key not in subj:
            continue
        if from_addr and from_addr.lower() in sender.lower():
            continue  # é o email original enviado pelo bot

        body = _strip_quoted(_body_text(msg))
        up = body.upper()
        decision, instruction = "NONE", ""
        if up.startswith("OK") or "\nOK" in up or up.strip() == "OK":
            decision = "OK"
        m = re.search(r"EDITAR\s*(.*)", body, re.IGNORECASE | re.DOTALL)
        if m and "EDITAR" not in (from_addr or ""):
            instruction = m.group(1).strip()
            decision = "EDITAR"
        best = {"decision": decision, "instruction": instruction, "raw": body[:500], "from": sender}
        break

    M.logout()
    return best or {"decision": "NONE", "instruction": "", "raw": "", "from": ""}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--from-addr", default="noreply@app.mcasei.co.mz")
    args = parser.parse_args()
    print(json.dumps(check(args.date, args.from_addr), ensure_ascii=False, indent=2))
