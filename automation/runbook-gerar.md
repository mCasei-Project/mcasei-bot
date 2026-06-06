Estás a executar a GERAÇÃO DIÁRIA do triplet do mCasei (@mcasei.mz), no PC local. Trabalha a partir de C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot (cwd atual). Faz tudo de forma autónoma, sem perguntar.

OBJETIVO: gerar 3 posts (1080×1350) e enviar o email de aprovação. NÃO agendar no Buffer aqui — o agendamento é feito SÓ na rotina de aprovação (16h), depois do OK humano. Usa a DATA fornecida na INSTRUÇÃO CRÍTICA no topo desta mensagem (não recalcules nem adivinhes) e a pasta Posts/DATA/.

ESTRATÉGIA: a skill mcasei-triplet lê o plano automaticamente. Conteúdo PT-MZ ("vosso/a"), elegante, premium. Regras pré-lançamento: não revelar URL, não pedir cadastro, falar de Moçambique/Maputo.

PASSO 1 — TRIPLET COMPLETO: usa a skill mcasei-triplet para gerar o triplet do dia de forma autónoma (sem parar para aprovação intermédia). A skill:
- Lê a estratégia do dia em "Plano de Postagens/"
- Escolhe a foto adequada de "Imagens Casais/"
- Gera Posts/DATA/post1_impacto.png e Posts/DATA/post3_lema.png (Posts 1 e 3)
- Invoca a skill mcasei-carrousel para gerar o Post 2 (carrossel 6–8 slides) em Posts/DATA/slides/slide_1.png ... slide_N.png
- Escreve Posts/DATA/triplet_buffer.json com as captions e hashtags dos 3 posts

Confirma que os ficheiros existem antes de avançar: post1_impacto.png, post3_lema.png, slides/slide_1.png.

PASSO 2 — Hospedar imagens: corre `python upload_images_imgbb.py --date DATA` (faz upload dos PNGs para o Imgbb e gera Posts/DATA/upload_urls.json com URLs permanentes). Garante que todos os slides e post1/post3 existem antes. Se IMGBB_API_KEY não estiver definida o script termina com erro.

PASSO 3 — Email de aprovação (Mailgun): escreve o corpo com o conteúdo/captions dos 3 posts num ficheiro e envia com imagens anexadas:
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] Triplet DATA" --body-file body.txt --flag-id Posts/DATA/email_aprovacao.flag --attach Posts/DATA/post1_impacto.png --attach Posts/DATA/post3_lema.png --attach Posts/DATA/slides/slide_1.png --attach Posts/DATA/slides/slide_2.png --attach Posts/DATA/slides/slide_3.png --attach Posts/DATA/slides/slide_4.png --attach Posts/DATA/slides/slide_5.png --attach Posts/DATA/slides/slide_6.png --attach Posts/DATA/slides/slide_7.png --attach Posts/DATA/slides/slide_8.png
```
(substitui DATA pela data real e anexa TODOS os slides existentes em Posts/DATA/slides/, slide_1..N — não só 2). No corpo inclui: as 3 captions e a instrução "Responde OK para confirmar, ou EDITAR [instrução] para alterar." Se mencionares horário no corpo, usa 19h30 / 19h35 / 19h40 (Maputo).

No fim, escreve um resumo curto: ficheiros gerados, URLs Imgbb e confirmação do email. O Buffer é tratado na rotina de aprovação (16h).
