"""
mCasei — Send Email via SMTP
-----------------------------
Envia emails usando o servidor mCasei (appsuite.cloud).

Variáveis de ambiente necessárias:
    SMTP_HOST     (ex: smtp.us.appsuite.cloud)
    SMTP_PORT     (ex: 465)
    SMTP_USER     (ex: contacto@mcasei.co.mz)
    SMTP_PASSWORD

Uso:
    python send_email.py --to dest@email.com --subject "Assunto" --body "Corpo"
    python send_email.py --to dest@email.com --subject "Assunto" --body-file email.txt
"""

import smtplib, os, argparse, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to: str, subject: str, body: str, html: bool = False) -> bool:
    host     = os.environ.get("SMTP_HOST", "smtp.us.appsuite.cloud")
    port     = int(os.environ.get("SMTP_PORT", "465"))
    user     = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = user
    msg["To"]      = to

    mime_type = "html" if html else "plain"
    msg.attach(MIMEText(body, mime_type, "utf-8"))

    try:
        with smtplib.SMTP_SSL(host, port) as server:
            server.login(user, password)
            server.send_message(msg)
        print(f"  ✅ Email enviado para {to}")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao enviar email: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enviar email via SMTP mCasei")
    parser.add_argument("--to",        required=True, help="Destinatário")
    parser.add_argument("--subject",   required=True, help="Assunto")
    parser.add_argument("--body",      help="Corpo do email (texto)")
    parser.add_argument("--body-file", help="Ficheiro com o corpo do email")
    parser.add_argument("--html",      action="store_true", help="Enviar como HTML")
    args = parser.parse_args()

    if args.body_file:
        body = open(args.body_file, encoding="utf-8").read()
    elif args.body:
        body = args.body
    else:
        print("Erro: fornece --body ou --body-file")
        sys.exit(1)

    success = send_email(args.to, args.subject, body, args.html)
    sys.exit(0 if success else 1)
