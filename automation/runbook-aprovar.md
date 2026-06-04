Estás a executar a VERIFICAÇÃO DE APROVAÇÃO do triplet mCasei de hoje, no PC local. cwd = C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot. Autónomo, sem perguntar. DATA = hoje (YYYY-MM-DD).

PASSO 1 — Ler resposta por IMAP:
```
python check_replies_imap.py --date DATA
```
Lê o JSON impresso: {"decision":"OK|EDITAR|NONE","instruction":"..."}.

SE decision = OK:
- Confirma via MCP buffer que os 3 posts no canal $BUFFER_CHANNEL_ID estão agendados para hoje 17:30/17:32/17:34 UTC. Escreve "Aprovado — publicação confirmada para 19h30 Maputo."

SE decision = EDITAR:
- Aplica a instrução. Se for nos posts 1/3, regenera com a skill mcasei-sideposts; se for no carrossel, ajusta com a skill instagram-carousel. Re-exporta os PNGs afetados em Posts/DATA/.
- Corre `python publish_images_github.py --date DATA` para republicar e obter novas URLs.
- Atualiza os posts correspondentes no Buffer (MCP) com as novas download_url.
- Envia confirmação:
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] Triplet DATA — Actualizado" --body "Alteracoes aplicadas e posts actualizados no Buffer para 19h30 Maputo." --attach Posts/DATA/post1_impacto.png --attach Posts/DATA/post3_lema.png
```

SE decision = NONE (sem resposta):
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] LEMBRETE — Triplet DATA aguarda aprovacao" --body "Os 3 posts estao prontos e agendados no Buffer. Responde OK para confirmar ou EDITAR [instrucao] para alterar. Publicacao automatica as 19h30 Maputo."
```

No fim, escreve um resumo curto da decisão detetada e da ação tomada.
