# Achados Inteligentes — Gerador automático de vídeos

Gerador gratuito de vídeos verticais (9:16, 720×1280) com Python, Pillow e FFmpeg. A V2 recebe um roteiro JSON, gera cenas animadas e tenta criar narração em português brasileiro com a voz instalada no Windows. **Não produz filmagens realistas do zero.**

## Começo rápido (Windows)

Pré-requisitos: Python 3.10+, FFmpeg no PATH e Pillow (`python -m pip install Pillow`).

1. Baixe o ZIP do repositório pelo botão **Code > Download ZIP** e extraia numa pasta.
2. Abra PowerShell na pasta extraída e execute `python gerar_video_v2.py`.
3. Abra a pasta `saida_v2` e assista ao arquivo `achados_inteligentes_v2.mp4`.

O programa determina a duração das cenas pela duração real de cada narração, incluindo uma pequena pausa. Isso impede o corte prematuro do áudio na exportação. A versão atual também exibe legendas por cena, faz transições suaves e aplica um zoom discreto nas imagens de produtos.

## Roteiros e materiais

Altere `roteiro.json` para mudar título, subtítulo e fala de cada cena. Use de 1 a 8 cenas. Para usar uma imagem, crie a pasta `materiais`, coloque nela uma foto que você tenha autorização para utilizar e adicione a chave `"imagem": "nome-da-foto.jpg"` à cena desejada. O vídeo não depende de imagens externas.

Para testar sem sintetizador de voz: `python gerar_video_v2.py --sem-voz`.

## Limitações e segurança

- O sintetizador de voz Windows `System.Speech` precisa ter voz compatível com português brasileiro. Sem ela, a V2 exporta vídeo silencioso e avisa no terminal.
- O áudio da voz Windows pode soar artificial. A V2 ainda não usa clonagem de voz nem modelos pagos.
- Vídeos com anúncios e material de terceiros só devem ser publicados depois de conferir exatidão das informações, direitos de imagens, voz e trilha e regras da plataforma.
- Nunca salve senhas, tokens, chaves API, dados de clientes ou credenciais no repositório.
- O protótipo anterior permanece em `gerar_video.py` como V1.

## Atualização do projeto

Se você já baixou a V2 antes, baixe novamente o ZIP do repositório e extraia em uma **pasta nova**. O arquivo `gerar_video_v2.py` foi atualizado com legendas por cena e animação das imagens. Não é necessário reinstalar Python ou FFmpeg.

## Voz neural gratuita opcional (Piper)

A voz padrão do Windows continua disponível. Para usar um sintetizador neural offline em português brasileiro:

```powershell
python -m pip install piper-tts
mkdir vozes
python -m piper.download_voices --data-dir vozes pt_BR-faber-medium
python gerar_video_v2.py --voz piper
```

O download da voz pesa aproximadamente 63 MB. Após a instalação inicial, o Piper processa as falas localmente sem cobrança por caracteres. O suporte no Windows com Python 3.14 depende das versões atuais de piper-tts e onnxruntime, por isso execute primeiro o teste e envie o erro se houver. A voz pode não soar natural o suficiente; compare com a versão Windows antes de publicar. Verifique a licença do modelo de voz escolhido e a licença GPL do mecanismo Piper.

Outras opções: `python gerar_video_v2.py --voz windows` ou `python gerar_video_v2.py --sem-voz`.
