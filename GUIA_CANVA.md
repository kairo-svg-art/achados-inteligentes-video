# Canva + Gerador de Vídeos: integração visual

O Canva pode produzir layouts, fundos e artes de marca. O Python/FFmpeg gera a animação e o MP4. **A conexão do Canva ao ChatGPT não transfere automaticamente um design para a pasta do programa no Windows.** Até existir integração de download automatizado, exporte as imagens de cenas do Canva para a pasta `materiais`.

## Identidade visual recomendada
- Formato: vertical 9:16
- Elementos: navy #071326, ciano #31CEFA, azul #1865B4, branco #F8FBFF
- Estilo: premium, simples, realista, com respiro para textos e recortes de produtos
- Visual do produto: use imagens reais do anúncio e respeite direitos de uso; não invente funcionalidades, avaliações ou descontos.

## Caminho de produção
1. No Canva, prepare fundos ou artes para o vídeo vertical e exporte cada cena em PNG/JPG.
2. Crie a pasta `materiais` ao lado de `gerar_video_v2.py`.
3. Salve as imagens nessa pasta, com nomes como `produto_01.png`.
4. No `roteiro.json`, adicione `"imagem": "produto_01.png"` à cena que deve mostrar a arte.
5. Execute `python gerar_video_v2.py` (ou `--voz piper` após a instalação da voz).
6. Assista e revise o MP4. Não publique material promocional com fatos não confirmados.

## Exemplo de cena no roteiro.json

```json
{
  "titulo": "Organize sua mesa",
  "subtitulo": "Uma ideia para sua rotina",
  "fala": "Este acessório pode ajudar a manter seus objetos ao alcance.",
  "imagem": "produto_01.png"
}
```

## Etapas de automação futuras
- Exportação de imagens diretamente do Canva, se os recursos e permissões disponíveis permitirem.
- Geração de um conjunto de cenas a partir de link e ficha de produto, sempre verificando informações.
- Legendas acompanhando palavras em vez de exibir o parágrafo completo.
- Escolha entre voz local e voz externa conforme licença e orçamento.

## Importante
O Canva é especializado em design. Ele não substitui o motor do MP4 nem garante vídeos realistas gerados por IA sem créditos. É um módulo de visuais, não a solução inteira.
