Estás a executar a GERAÇÃO DIÁRIA do triplet do mCasei (@mcasei.mz), no PC local. Trabalha a partir de C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot (cwd atual). Faz tudo de forma autónoma, sem perguntar.

OBJETIVO: gerar 3 posts (1080×1350), agendá-los no Buffer para hoje 19h30/19h32/19h34 (Maputo) e enviar email de aprovação. Define DATA = data de hoje (YYYY-MM-DD) e usa a pasta Posts/DATA/.

ESTRATÉGIA: lê o tema de hoje em "Estrategia de posts.docx" (descompacta e lê word/document.xml se necessário). Conteúdo PT-MZ ("vosso/a"), elegante, premium. Regras pré-lançamento: não revelar URL, não pedir cadastro, falar de Moçambique/Maputo.

PASSO 1 — POST 2 (Carrossel central): usa a skill instagram-carousel para criar UM carrossel de 6–8 slides seguindo a estratégia do dia. Usa fotos adequadas de "Imagens Casais/" nos slides apropriados e os logótipos de "Logo Files/". Exporta os slides como PNG 1080×1350 para Posts/DATA/post2_slides/ com nomes slide_01.png, slide_02.png, ... (renomeia se a skill usar outro padrão).

PASSO 2 — POSTS 1 e 3 (laterais clean): usa a skill mcasei-sideposts para gerar Posts/DATA/post1_impacto.png e Posts/DATA/post3_lema.png alinhados ao tema do dia.

PASSO 3 — Hospedar imagens: corre `python publish_images_github.py --date DATA` (commita os PNGs e gera Posts/DATA/upload_urls.json com URLs raw do GitHub). Garante que slide_*.png e post1/post3 existem antes.

PASSO 4 — Buffer (MCP buffer): cria 3 publicações no canal $BUFFER_CHANNEL_ID (org $BUFFER_ORG_ID), Instagram, usando as download_url do upload_urls.json, agendadas para HOJE:
- Post 3 (post3_lema) → 17:30 UTC (19h30 Maputo)
- Post 2 (carrossel, TODOS os slides numa publicação, por ordem) → 17:32 UTC (19h32)
- Post 1 (post1_impacto) → 17:34 UTC (19h34)
Escreve uma caption PT-MZ para cada + hashtags #CasamentoMocambique #NoivosMocambique #MaputoWeddings.

PASSO 5 — Email de aprovação (Mailgun): escreve o corpo com o conteúdo/captions dos 3 posts num ficheiro e envia com as imagens anexadas:
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] Triplet DATA" --body-file body.txt --attach Posts/DATA/post1_impacto.png --attach Posts/DATA/post3_lema.png --attach Posts/DATA/post2_slides/slide_01.png --attach Posts/DATA/post2_slides/slide_02.png
```
(substitui DATA pela data real; usa o caminho python do sistema). No corpo inclui: as 3 captions e a instrução "Responde OK para confirmar, ou EDITAR [instrução] para alterar."

No fim, escreve um resumo curto: ficheiros gerados, IDs/links dos posts Buffer, e confirmação do email.
