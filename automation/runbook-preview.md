MODO PREVIEW LOCAL: gerar o triplet mCasei e enviar por email para validação visual. NÃO usar Buffer. NÃO fazer git push. cwd = C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot. Autónomo, sem perguntar. DATA = hoje (YYYY-MM-DD); usa a pasta Posts/DATA/.

Conteúdo PT-MZ ("vosso/a"), elegante. Lê o tema de hoje em "Estrategia de posts.docx". Regras: não revelar URL, falar de Moçambique/Maputo.

PASSO 1 — POST 2 (carrossel): usa a skill instagram-carousel para um carrossel de 6–8 slides do tema do dia, com fotos de "Imagens Casais/" nos slides apropriados e logótipos de "Logo Files/". Exporta PNG 1080×1350 para Posts/DATA/post2_slides/ como slide_01.png, slide_02.png, ...

PASSO 2 — POSTS 1 e 3: usa a skill mcasei-sideposts para gerar Posts/DATA/post1_impacto.png e Posts/DATA/post3_lema.png do tema do dia.

PASSO 3 — Email de PREVIEW (Mailgun) com TODAS as imagens anexadas e as captions no corpo. Cria body.txt com as 3 captions e envia (usa as variáveis de ambiente já definidas):
```
python send_email_mailgun.py --to "$APPROVAL_EMAIL" --reply-to "$APPROVAL_EMAIL" --subject "[mCasei] PREVIEW Triplet DATA" --body-file body.txt --attach Posts/DATA/post1_impacto.png --attach Posts/DATA/post3_lema.png --attach Posts/DATA/post2_slides/slide_01.png --attach Posts/DATA/post2_slides/slide_02.png --attach Posts/DATA/post2_slides/slide_03.png --attach Posts/DATA/post2_slides/slide_04.png
```
(substitui DATA pela data real e anexa todos os slides existentes).

No fim escreve um resumo: ficheiros gerados (com tamanhos) e confirmação do envio do email.
