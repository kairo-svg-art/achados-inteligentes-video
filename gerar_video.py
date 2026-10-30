"""Achados Inteligentes — gerador de video v1 (Windows, sem API paga).

Requisitos: Python 3.10+, Pillow, FFmpeg no PATH.
Uso: python gerar_video.py
"""
from pathlib import Path
import math
import shutil
import subprocess
import sys
import wave

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "saida"
FRAMES = OUT / "quadros"
W, H = 720, 1280
FPS = 24
DURATION = 15
TEXTS = [
    ("ACHADOS", "INTELIGENTES", "Tecnologia e descobertas para seu dia."),
    ("DESCUBRA", "NOVIDADES", "Ideias que voce ainda nao conhece."),
    ("SIMPLIFIQUE", "SUA ROTINA", "Solucoes uteis para o cotidiano."),
    ("APROVEITE", "CADA IDEIA", "Siga Achados Inteligentes."),
]
NARRATION = (
    "Ja imaginou descobrir coisas que facilitam seu dia? "
    "Tecnologia, utilidades e ideias inteligentes para sua rotina. "
    "Bem-vindo ao Achados Inteligentes. Descubra, simplifique, aproveite."
)

def font(size):
    choices = [
        Path("C:/Windows/Fonts/arialbd.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf"),
    ]
    for path in choices:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

def centered(draw, text, y, ft, color):
    box = draw.textbbox((0, 0), text, font=ft)
    x = (W - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=ft, fill=color)

def make_frame(index, t):
    img = Image.new("RGB", (W, H), (5, 12, 26))
    pix = img.load()
    # Fundo escuro com iluminacao azul animada; sem recursos externos.
    cx = W * (0.52 + 0.12 * math.sin(t * 0.55))
    cy = H * (0.42 + 0.08 * math.cos(t * 0.41))
    for y in range(H):
        for x in range(W):
            d = ((x - cx) / 440) ** 2 + ((y - cy) / 570) ** 2
            light = max(0, 1 - d) ** 2
            band = max(0, 1 - abs(x - W * (0.20 + t / 25)) / 180)
            pix[x, y] = (
                int(5 + 8 * light),
                int(12 + 63 * light + 12 * band),
                int(26 + 115 * light + 24 * band),
            )
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((55, 365, W - 55, 880), radius=44, outline=(24, 167, 230), width=4)
    d.rounded_rectangle((76, 385, W - 76, 858), radius=35, outline=(20, 67, 109), width=2)
    for j in range(12):
        xx = (j * 97 + int(t * 42)) % (W + 150) - 75
        yy = 200 + (j * 113) % 850
        d.ellipse((xx, yy, xx + 4, yy + 4), fill=(27, 132, 190))
    head, sub, foot = TEXTS[index]
    centered(d, head, 476, font(75 if len(head) < 12 else 60), (255, 255, 255))
    centered(d, sub, 583, font(57 if len(sub) < 14 else 45), (53, 208, 255))
    centered(d, foot, 735, font(27), (207, 227, 244))
    centered(d, "DESCUBRA  |  SIMPLIFIQUE  |  APROVEITE", 1087, font(23), (161, 198, 220))
    return img

def create_speech(wav_path):
    ps = OUT / "narrar.ps1"
    # Escape de aspas simples para literais do PowerShell.
    literal = NARRATION.replace("'", "''")
    location = str(wav_path).replace("'", "''")
    ps.write_text(
        "Add-Type -AssemblyName System.Speech\n"
        "$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer\n"
        "$voices = @($voice.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like 'pt-*' })\n"
        "if ($voices.Count -gt 0) { $voice.SelectVoice($voices[0].VoiceInfo.Name) }\n"
        "$voice.Rate = 1\n"
        f"$voice.SetOutputToWaveFile('{location}')\n"
        f"$voice.Speak('{literal}')\n"
        "$voice.Dispose()\n",
        encoding="utf-8-sig",
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("Aviso: narracao do Windows indisponivel:", result.stderr.strip())
        return False
    return wav_path.exists() and wav_path.stat().st_size > 44

def main():
    if not shutil.which("ffmpeg"):
        sys.exit("FFmpeg nao encontrado. Instale FFmpeg e adicione ao PATH.")
    OUT.mkdir(exist_ok=True)
    FRAMES.mkdir(exist_ok=True)
    print("Gerando quadros do video...")
    for n in range(DURATION * FPS):
        t = n / FPS
        segment = min(3, int(t / (DURATION / 4)))
        frame = make_frame(segment, t)
        frame.save(FRAMES / f"frame_{n:04d}.jpg", quality=88)
        if n % 48 == 0:
            print(f"  {int(t)} de {DURATION} segundos")
    wav_path = OUT / "narracao.wav"
    has_voice = create_speech(wav_path) if sys.platform == "win32" else False
    output = OUT / "achados_inteligentes_001.mp4"
    command = [
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", str(FRAMES / "frame_%04d.jpg"),
    ]
    if has_voice:
        command += ["-i", str(wav_path)]
    command += [
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "23",
        "-r", str(FPS), "-t", str(DURATION),
        "-movflags", "+faststart",
    ]
    if has_voice:
        command += ["-c:a", "aac", "-b:a", "160k", "-af", "apad", "-shortest"]
    else:
        print("Video sera exportado sem voz. Confira vozes instaladas no Windows.")
    command += [str(output)]
    subprocess.run(command, check=True)
    print("Video criado:", output)

if __name__ == "__main__":
    main()
