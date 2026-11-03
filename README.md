# Achados Inteligentes — Gerador automático de vídeos

Gerador gratuito de vídeos verticais (9:16, 720×1280) com Python, Pillow e FFmpeg. A V2 recebe um roteiro JSON, gera cenas animadas e tenta criar narração em português brasileiro com a voz instalada no Windows. **Não produz filmagens realistas do zero.**

## Começo rápido (Windows)

Pré-requisitos: Python 3.10+, FFmpeg no PATH e Pillow (`python -m pip install Pillow`).

1. Baixe o ZIP do repositório pelo botão **Code > Download ZIP** e extraia numa pasta.
2. Abra PowerShell na pasta extraída e execute `python gerar_video_v2.py`.
3. Abra a pasta `saida_v2` e assista ao arquivo `achados_inteligentes_v2.mp4`.

O programa determina a duração das cenas pela duração real de cada narração, incluindo uma pequena pausa. Isso impede o corte prematuro do áudio na exportação.

## Roteiros e materiais

Altere `roteiro.json` para mudar título, subtítulo e fala de cada cena. Use de 1 a 8 cenas. Para usar uma imagem, crie a pasta `materiais`, coloque nela uma foto que você tenha autorização para utilizar e adicione a chave `"imagem": "nome-da-foto.jpg"` à cena desejada. O vídeo não depende de imagens externas.

Para testar sem sintetizador de voz: `python gerar_video_v2.py --sem-voz`.

## Limitações e segurança

- O sintetizador de voz Windows `System.Speech` precisa ter voz compatível com português brasileiro. Sem ela, a V2 exporta vídeo silencioso e avisa no terminal.
- O áudio da voz Windows pode soar artificial. A V2 ainda não usa clonagem de voz nem modelos pagos.
- Vídeos com anúncios e material de terceiros só devem ser publicados depois de conferir exatidão das informações, direitos de imagens, voz e trilha e regras da plataforma.
- Nunca salve senhas, tokens, chaves API, dados de clientes ou credenciais no repositório.
- O protótipo anterior permanece em `gerar_video.py` como V1.
