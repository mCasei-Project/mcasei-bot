"""
mCasei — Send Email via Mailgun API
-------------------------------------
Envia emails usando a API HTTP do Mailgun (porta 443, sem bloqueios cloud).

Variáveis de ambiente necessárias:
    MAILGUN_API_KEY   (a tua chave da API Mailgun)
    MAILGUN_DOMAIN    (ex: app.mcasei.co.mz)
    MAILGUN_FROM      (ex: mCasei <noreply@app.mcasei.co.mz>)

Uso:
    python send_email_mailgun.py --to dest@email.com --subject "Assunto" --body "Corpo"
    python send_email_mailgun.py --to dest@email.com --subject "Assunto" --body-file email.txt --html
"""

import os, sys, argparse, requests


def send_email(to: str, subject: str, body: str, html: bool = False,
               reply_to: str = None, attachments: list = None) -> bool:
    api_key = os.environ["MAILGUN_API_KEY"]
    domain  = os.environ["MAILGUN_DOMAIN"]
    from_   = os.environ.get("MAILGUN_FROM", f"mCasei <noreply@{domain}>")
    reply_to = reply_to or os.environ.get("APPROVAL_EMAIL")

    data = {
        "from":    from_,
        "to":      to,
        "subject": subject,
    }
    if reply_to:
        data["h:Reply-To"] = reply_to
    if html:
        data["html"] = body
    else:
        data["text"] = body

    files = []
    for path in (attachments or []):
        p = os.path.abspath(path)
        if os.path.exists(p):
            files.append(("attachment", (os.path.basename(p), open(p, "rb").read())))
        else:
            print(f"  ! anexo não encontrado: {p}")

    resp = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data=data,
        files=files or None,
    )

    if resp.ok:
        print(f"  ✅ Email enviado para {to} (id: {resp.json().get('id', '')})")
        return True
    else:
        print(f"  ❌ Erro Mailgun {resp.status_code}: {resp.text}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enviar email via Mailgun")
    parser.add_argument("--to",        required=True)
    parser.add_argument("--subject",   required=True)
    parser.add_argument("--body",      help="Corpo do email")
    parser.add_argument("--body-file", help="Ficheiro com o corpo (- para stdin)")
    parser.add_argument("--html",      action="store_true")
    parser.add_argument("--reply-to",  help="Endereço de Reply-To (default: APPROVAL_EMAIL)")
    parser.add_argument("--attach",    action="append", default=[], help="Anexo (repetível)")
    args = parser.parse_args()

    if args.body_file == "-":
        body = sys.stdin.read()
    elif args.body_file:
        body = open(args.body_file, encoding="utf-8").read()
    elif args.body:
        body = args.body
    else:
        print("Erro: fornece --body ou --body-file")
        sys.exit(1)

    success = send_email(args.to, args.subject, body, args.html,
                         reply_to=args.reply_to, attachments=args.attach)
    sys.exit(0 if success else 1)
