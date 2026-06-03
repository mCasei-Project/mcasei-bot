---
name: mcasei-carousel
description: >
  Gera um triplet coordenado de posts para o Instagram do mCasei (@mcasei.mz) -
  plataforma de casamentos em Mocambique. Cria 3 posts 4:5 (1080x1350px) que
  preenchem uma linha da grade: (1) post de impacto, (2) carrossel, (3) lema.
  Le o arquivo de estrategia semanal (.docx no OneDrive) automaticamente.
  Roda a paleta de cores a cada dia. Cria drafts no Buffer e envia e-mail de aprovacao.

  Use este skill sempre que o utilizador mencionar "post mCasei", "carrossel mCasei",
  "triplet", "publicar no Instagram do mCasei", "gerar posts de hoje", "posts da semana
  mCasei" ou qualquer pedido de conteudo para @mcasei.mz.
---

# mCasei Triplet — Instagram Generator

Gera 3 posts coordenados (triplet) para @mcasei.mz.
Todos os posts sao 4:5 — viewport 420x525px — exportar 1080x1350px.

---

## Contexto de Marca

```
Instagram:   @mcasei.mz  |  Website: mCasei.co.mz
Tom:         Elegante, sofisticado, romantico. Editorial premium.
Idioma:      Portugues PT-MZ ("vosso/a", nunca "seu/sua")
Proibido:    Revelar URL, pedir cadastro, linguagem de flyer

Font display:  Parisienne (Google Fonts)
Font heading:  Lora 700
Font body:     Nunito Sans 400/600
```

Escala tipografica OBRIGATORIA (viewport 420px):
- Titulo h1:     40-44px, Lora 700, uppercase
- Subtitulo:     28-32px, Parisienne
- Lema/quote:    28-32px, Lora italic
- Assinatura:    32-36px, Parisienne
- Body/bullets:  15-17px, Nunito Sans
- Tags/labels:   11-12px, Nunito Sans 700, uppercase, letter-spacing 3px
- Handle:        11px, Nunito Sans 600
NUNCA usar fontes abaixo de 11px.

---

## Paleta de Rotacao

| Dia | Nome           | PRIMARY | BG      | TEXT    | ACCENT  |
|-----|----------------|---------|---------|---------|---------|
| 1   | Champagne gold | #C8A97E | #F7F3EE | #1A1A1A | #8A7563 |
| 2   | Ivory          | #F7F3EE | #FFFFFF | #1A1A1A | #C8A97E |
| 3   | Warm beige     | #DCCBB8 | #F7F3EE | #1A1A1A | #8A7563 |
| 4   | Nude rose      | #D8B7A3 | #F7F3EE | #1A1A1A | #C8A97E |
| 5   | Taupe          | #8A7563 | #F7F3EE | #1A1A1A | #C8A97E |
| 6   | Black          | #1A1A1A | #F7F3EE | #F7F3EE | #C8A97E |

Rotacao ciclica (dia 1 = primeira entrada do arquivo de estrategia).

---

## Passo 1 - Ler o arquivo de estrategia

### Opcao A - Local (Claude Code)
```powershell
$src = Get-ChildItem "C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot\" -Filter "*.docx" | Select-Object -First 1 -ExpandProperty FullName
$zip = "$env:TEMP\mcasei-strat.zip"; $dst = "$env:TEMP\mcasei-strat"
Copy-Item $src $zip -Force
Expand-Archive $zip $dst -Force
$xml = Get-Content "$dst\word\document.xml" -Raw -Encoding UTF8
($xml -replace '<[^>]+>',' ') -replace '\s+',' '
```

### Opcao B - Remoto (Cowork / agente sem acesso local)
```powershell
$url = "https://1drv.ms/w/c/44e7cfb63db0a40b/IQCALW-u-zSYTJMLFQmjyypsAa9i5A2lA8LYAjeNCCYNLVM?e=eRAz3j&download=1"
$zip = "$env:TEMP\mcasei-strat.zip"; $dst = "$env:TEMP\mcasei-strat"
Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
Expand-Archive $zip $dst -Force
$xml = Get-Content "$dst\word\document.xml" -Raw -Encoding UTF8
($xml -replace '<[^>]+>',' ') -replace '\s+',' '
```

Extrair do texto: tipo, tema, objetivo, texto_na_imagem, legenda, cta,
estrutura_carrossel (lista de slides), lema_semana.
Se nao encontrar o dia de hoje, perguntar: "Qual o tema de hoje?"

---

## Passo 2 - Paleta do dia

Contar posicao do dia no plano (1a entrada = dia 1).
Seleccionar linha da tabela de rotacao acima.

---

## Passo 3 - Gerar os 3 HTMLs

Output: C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot\Posts\{YYYY-MM-DD}\

### Post 1 - Impacto (420x525)
- Cantos decorativos {PRIMARY}, borda interna fina opacity 0.4
- Tag: Nunito Sans 11-12px, uppercase, letter-spacing 3.5px, {ACCENT}
- Titulo: Lora 700, 40-44px, uppercase, {TEXT}
- Subtitulo: Parisienne 28-32px, {PRIMARY}
- Separador: linha 1.5px {PRIMARY}
- "Em breve": Nunito Sans 13px, letter-spacing 5px, {ACCENT}
- Logo bottom-left: Parisienne 20px
- Handle bottom-right: Nunito Sans 11px

### Post 2 - Carrossel (420x525 por slide, 5-8 slides)
Progress bar + swipe arrow em todos os slides exceto o ultimo.
Alternancia claro/escuro. Slide 1 = hook. Ultimo = CTA com logo.
Sem URL se fase pre-lancamento.

### Post 3 - Lema (420x525)
- Fundo escuro (#1A1A1A) com circulos decorativos {PRIMARY} opacity 0.06
- Ornamento central + linhas decorativas {PRIMARY}
- Tag: Nunito Sans 11px, uppercase, {PRIMARY} opacity 0.6
- Lema: Lora italic 28-32px, #F7F3EE, line-height 1.5
- Assinatura: Parisienne 32-36px, {PRIMARY}
- Subtexto: Nunito Sans 11px, "Casamentos modernos - Mocambique"
- Handle bottom-left: 11px

---

## Passo 4 - Exportar via Playwright

```
python3 scripts/export_triplet.py \
  --date {YYYY-MM-DD} \
  --output-dir "C:\Users\igorm\OneDrive\Documentos\Claude\Projects\mCaseiBot\Posts" \
  --html-dir "C:\Users\igorm\AppData\Local\Temp\mcasei-{YYYY-MM-DD}" \
  --slides {N}
```

---

## Passo 5 - Buffer

Org ID:     6a1ef40e0664a6201cec451e
Channel ID: 6a1ef4abc687a22dd451bf84  (mcasei.mz, Instagram Business)
Timezone:   Africa/Maputo (UTC+2)

Drafts em ordem inversa:
- Post 3 Lema      -> 19:30
- Post 2 Carrossel -> 19:32
- Post 1 Impacto   -> 19:34

Caption PT-MZ, hashtags: #CasamentoMocambique #NoivosMocambique #MaputoWeddings

---

## Passo 6 - Email de aprovacao

Para:    mCaseiBot@mcasei.co.mz
Assunto: [mCasei] Triplet {data} ({paleta}) - Aguardando aprovacao

Preview dos 3 posts + captions + links Buffer.
"Responda OK para confirmar ou EDITAR [instrucao] para ajustar."

---

## Links OneDrive

- Estrategia: https://1drv.ms/w/c/44e7cfb63db0a40b/IQCALW-u-zSYTJMLFQmjyypsAa9i5A2lA8LYAjeNCCYNLVM?e=eRAz3j
- Assets:     https://1drv.ms/f/c/44e7cfb63db0a40b/IgB7KO5CqT1nQI2Z4PMzid0kARiAd97aQRAOnWUwQhw38-c?e=ioQ5pd
- Logos:      https://1drv.ms/f/c/44e7cfb63db0a40b/IgBk1jO6gzUzQqec3qLSnhN0AaTYJySPtdPmZnGh08SYCCU?e=ofchZl
- Templates:  https://1drv.ms/f/c/44e7cfb63db0a40b/IgA5OzwZ6oGETrqQHSyoVCTIAcLjVqPvlOzeBssZ4fYqf3Y?e=ljEupy

