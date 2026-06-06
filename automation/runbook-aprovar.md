Estás a executar a VERIFICAÇÃO DE APROVAÇÃO do triplet mCasei de hoje, no PC local. cwd = C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot. Autónomo, sem perguntar. Usa a DATA fornecida na INSTRUÇÃO CRÍTICA no topo desta mensagem (não recalcules nem adivinhes).

PASSO 1 — Ler resposta por IMAP:
```
python check_replies_imap.py --date DATA
```
Lê o JSON impresso: {"decision":"OK|EDITAR|NONE","instruction":"..."}.

---

SE decision = OK:
PRIMEIRO garante imagens frescas: corre `python upload_images_imgbb.py --date DATA` para re-hospedar os PNGs atuais (post1, post3 e TODOS os slides do carrossel em Posts/DATA/slides/) e regenerar Posts/DATA/upload_urls.json — isto evita carrosséis desatualizados ou repetidos entre triplets.
Depois lê Posts/DATA/upload_urls.json para obter as URLs das imagens e Posts/DATA/triplet_buffer.json para as captions.
Cria 3 posts no Buffer (MCP buffer, canal $BUFFER_CHANNEL_ID, org $BUFFER_ORG_ID) com as regras seguintes:

REGRAS DE AGENDAMENTO (críticas — nunca quebrar):
- Modo: customScheduled + dueAt exacto (NUNCA addToQueue — usaria slots aleatórios da fila)
- schedulingType: automatic
- Timezone Maputo = UTC+2. ATENÇÃO ao formato ISO 8601:
  ✅ CORRECTO: T19:30:00+02:00 = 19h30 hora local Maputo = 17:30 UTC
  ❌ ERRADO:   T17:30:00+02:00 = 17h30 hora local Maputo = 15:30 UTC (2 horas cedo!)
- ORDEM DE CRIAÇÃO (determina a grelha Instagram — no Instagram o post mais recente fica top-left):
  1.º a criar → Post 1 (impacto, post1_impacto.png) → dueAt HOJE T19:30:00+02:00 → publica 1.º → fica à DIREITA da grelha
  2.º a criar → Post 2 (carrossel, TODOS os slides por ordem) → dueAt HOJE T19:35:00+02:00 → fica ao CENTRO
  3.º a criar → Post 3 (lema, post3_lema.png) → dueAt HOJE T19:40:00+02:00 → publica último → fica à ESQUERDA
  Resultado visual na grelha (esquerda→direita): Post3 | Post2 | Post1(foto)
  NOTA: 5 minutos entre posts (19:30/19:35/19:40) — margem para notificação Instagram antes da publicação seguinte.

Usa as captions do triplet_buffer.json. Não adicionar músicas (música só funciona em Reels, não em posts normais — retirada do pipeline).
Após criar os 3 posts, envia confirmação:
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] Triplet DATA — Aprovado e agendado" --body "Posts aprovados e agendados no Buffer para 19h30/35/40 Maputo." --flag-id Posts/DATA/email_confirmacao.flag
```

---

SE decision = EDITAR:
- Aplica a instrução. Usa a skill mcasei-triplet para regenerar o post afectado (Posts 1 e/ou 3); se for o carrossel (Post 2), usa a skill mcasei-carrousel. Re-exporta os PNGs em Posts/DATA/.
- Corre `python upload_images_imgbb.py --date DATA` para obter novas URLs.
- Cria os 3 posts no Buffer com as mesmas regras de agendamento acima (customScheduled, ordem correcta).
- Envia confirmação:
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] Triplet DATA — Actualizado e agendado" --body "Alteracoes aplicadas. Posts agendados no Buffer para 19h30 Maputo." --flag-id Posts/DATA/email_edicao.flag --attach Posts/DATA/post1_impacto.png --attach Posts/DATA/post3_lema.png
```

---

SE decision = NONE (sem resposta):
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] LEMBRETE — Triplet DATA aguarda aprovacao" --body "Os 3 posts estao prontos. Responde OK para agendar no Buffer, ou EDITAR [instrucao] para alterar. Publicacao as 19h30 Maputo." --flag-id Posts/DATA/email_lembrete.flag
```

---

No fim, escreve um resumo curto da decisão detectada, IDs dos posts Buffer criados (se aplicável) e confirmação do email.
