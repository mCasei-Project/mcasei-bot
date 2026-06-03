# mCasei — Brand Context

## Identidade
- **Marca:** mCasei
- **Instagram:** @mcasei.mz
- **Website:** mCasei.co.mz
- **Segmento:** Plataforma de casamentos (Moçambique)
- **Tom:** Elegante, sofisticado, romântico
- **Idioma dos posts:** Português (PT-MZ)

## Paleta de Cores

### Versão Principal (Vinho/Bordô)
| Token         | Hex       | Uso                             |
|---------------|-----------|---------------------------------|
| BRAND_PRIMARY | `#6c000f` | Cor principal                   |
| BRAND_DARK    | `#410000` | Fundo escuro / near-black       |
| BRAND_ACCENT  | `#c76a67` | Destaque rosé                   |
| LIGHT_BG      | `#fdf8f5` | Fundo claro (off-white quente)  |
| LIGHT_BORDER  | `#ede6df` | Divisores em slides claros      |
| DARK_BG       | `#1a0a0b` | Near-black com tint vinho       |

**Gradiente principal:** `linear-gradient(165deg, #410000 0%, #6c000f 50%, #c76a67 100%)`

### Versão Gold (logos recentes)
- Gradiente: `#905e26` → `#f5ec9b` → `#905e26`
- Texto tagline: `#f1deab`

## Paleta Pré-Lançamento (rotação diária)

Todos os posts são **4:5 — 1080×1350px**.
A paleta rota diariamente (cíclica após dia 6):

| Dia | Nome           | PRIMARY   | BG        | TEXT      | ACCENT    |
|-----|----------------|-----------|-----------|-----------|-----------|
| 1   | Champagne gold | `#C8A97E` | `#F7F3EE` | `#1A1A1A` | `#8A7563` |
| 2   | Ivory          | `#F7F3EE` | `#FFFFFF` | `#1A1A1A` | `#C8A97E` |
| 3   | Warm beige     | `#DCCBB8` | `#F7F3EE` | `#1A1A1A` | `#8A7563` |
| 4   | Nude rose      | `#D8B7A3` | `#F7F3EE` | `#1A1A1A` | `#C8A97E` |
| 5   | Taupe          | `#8A7563` | `#F7F3EE` | `#1A1A1A` | `#C8A97E` |
| 6   | Black          | `#1A1A1A` | `#F7F3EE` | `#F7F3EE` | `#C8A97E` |

## Tipografia (fontes oficiais da marca)

| Elemento              | Fonte             | Peso       |
|-----------------------|-------------------|------------|
| Título / heading (h1,h2) | **Playfair Display** | 600/700 |
| Lema / quote          | Playfair Display  | italic 500 |
| Assinatura "mCasei"   | **Parisienne**    | 400        |
| Body / bullets / labels | **DM Sans**     | 400/500/600|

Google Fonts: `Playfair+Display`, `DM+Sans`, `Parisienne`.
(As antigas Lora/Nunito Sans foram substituídas — usar SEMPRE Playfair + DM Sans + Parisienne.)

## Cores reais em uso (vinho/rosé)
- Rosé claro: `#c76a67` `#d98a87` · Vinho: `#6c000f` `#a04f4c` · Escuro: `#1a1210`
- Claro: `#faf5f2` `#fdf8f5` · Dourado: `#dbc078` `#c2a06a`
- Gradiente vinho: `linear-gradient(165deg,#410000,#6c000f,#a04f4c)`

## Estrutura de Publicação — Triplet

3 posts por linha da grade (todos 4:5 — 1080×1350px):

```
POST 1 (Impacto)  │  POST 2 (Carrossel)  │  POST 3 (Lema)
19h34             │  19h32               │  19h30
```
Ordem de publicação inversa (Instagram mostra mais recente à esquerda).

## Automação

### Buffer
- **Organization ID:** `6a1ef40e0664a6201cec451e`
- **Channel ID:** `6a1ef4abc687a22dd451bf84` (mcasei.mz, Instagram Business)
- **Timezone:** Africa/Maputo (UTC+2)

### Gmail / Notificações
- **E-mail:** mCaseiBot@mcasei.co.mz
- **Aprovação:** resposta "OK" ou "EDITAR [instrução]"

### Horários
- **Geração:** 13h00 | **Verificação:** 16h00 | **Publicação:** 19h30/32/34

## Links OneDrive (acesso remoto — agentes Cowork)

| Recurso | Link | Tipo |
|---|---|---|
| **Estratégia semanal** | `https://1drv.ms/w/c/44e7cfb63db0a40b/IQCALW-u-zSYTJMLFQmjyypsAa9i5A2lA8LYAjeNCCYNLVM?e=eRAz3j` | .docx (Word) |
| **Assets / Imagens** | `https://1drv.ms/f/c/44e7cfb63db0a40b/IgB7KO5CqT1nQI2Z4PMzid0kARiAd97aQRAOnWUwQhw38-c?e=ioQ5pd` | Pasta |
| **Logos** | `https://1drv.ms/f/c/44e7cfb63db0a40b/IgBk1jO6gzUzQqec3qLSnhN0AaTYJySPtdPmZnGh08SYCCU?e=ofchZl` | Pasta |
| **Templates** | `https://1drv.ms/f/c/44e7cfb63db0a40b/IgA5OzwZ6oGETrqQHSyoVCTIAcLjVqPvlOzeBssZ4fYqf3Y?e=ljEupy` | Pasta |

**Download do .docx para agente remoto:**
```powershell
$docxUrl = "https://1drv.ms/w/c/44e7cfb63db0a40b/IQCALW-u-zSYTJMLFQmjyypsAa9i5A2lA8LYAjeNCCYNLVM?e=eRAz3j&download=1"
Invoke-WebRequest -Uri $docxUrl -OutFile "$env:TEMP\mcasei-strategy.docx" -UseBasicParsing
```

## Caminhos Locais (acesso directo — Claude Code)

```
OneDrive\Documentos\Claude\Projects\mCaseiBot\
  estrategia-semanal.docx          → estratégia da semana (nome genérico)
  Posts\{YYYY-MM-DD}\              → outputs do triplet

OneDrive\Documentos\Empresa MZ\mCasei\
  Identidade Visual\Logos Antigos\svg\       → logos vinho
  Identidade Visual\Logo Pink and Gold\      → logos gold
  Claude\brand-context.md                    → este arquivo
```

## Regras Pré-Lançamento
- Não revelar URL do site
- Não pedir cadastro directo
- Sem linguagem de panfleto / flyer
- Foco: curiosidade, educação, posicionamento premium
- Falar de Moçambique / Maputo

