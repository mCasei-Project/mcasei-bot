MODO PREVIEW LOCAL: gerar o triplet mCasei e enviar por email para validação visual. NÃO usar Buffer. NÃO fazer git push. cwd = C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot. Autónomo, sem perguntar.

DATA: usa a DATA fornecida na INSTRUÇÃO CRÍTICA no topo desta mensagem (não recalcules nem adivinhes). Essa é a pasta de saída: Posts/DATA/. Para o conteúdo, lê o plano disponível em "Plano de Postagens/" — se DATA não estiver coberta pelo plano, usa o primeiro dia disponível no ficheiro mais recente sem alterar o nome da pasta de saída.

Conteúdo PT-MZ ("vosso/a"), elegante, premium. Regras: não revelar URL, não pedir cadastro, falar de Moçambique/Maputo.

PASSO 1 — TRIPLET COMPLETO: usa a skill mcasei-triplet para gerar o triplet do dia de forma autónoma (sem parar para aprovação intermédia). A skill:
- Lê a estratégia do dia em "Plano de Postagens/" (ficheiro mais recente)
- Escolhe a foto adequada de "Imagens Casais/"
- Gera Posts/DATA/post1_impacto.png e Posts/DATA/post3_lema.png (Posts 1 e 3)
- Invoca a skill mcasei-carrousel para gerar o Post 2 (carrossel 6–8 slides) em Posts/DATA/slides/slide_1.png ... slide_N.png
- Escreve Posts/DATA/triplet_buffer.json com as captions e hashtags dos 3 posts

Confirma que os ficheiros existem antes de avançar: post1_impacto.png, post3_lema.png, slides/slide_1.png.

PASSO 2 — Email de PREVIEW (Mailgun) com TODAS as imagens anexadas e as captions no corpo. Lê as captions de Posts/DATA/triplet_buffer.json. Cria body.txt com as 3 captions e a nota "PREVIEW — não agendado no Buffer" e envia:
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] PREVIEW Triplet DATA" --body-file body.txt --flag-id Posts/DATA/email_preview.flag --attach Posts/DATA/post1_impacto.png --attach Posts/DATA/post3_lema.png --attach Posts/DATA/slides/slide_1.png --attach Posts/DATA/slides/slide_2.png --attach Posts/DATA/slides/slide_3.png --attach Posts/DATA/slides/slide_4.png --attach Posts/DATA/slides/slide_5.png --attach Posts/DATA/slides/slide_6.png --attach Posts/DATA/slides/slide_7.png --attach Posts/DATA/slides/slide_8.png
```
(substitui DATA pela data real; os slides vêm todos de Posts/DATA/slides/slide_1..8.png).

No fim escreve um resumo: ficheiros gerados (com tamanhos) e confirmação do envio do email.
