"""Achados Inteligentes V2: roteiro JSON -> video automatico em MP4.
Requisitos: Python 3.10+, Pillow, FFmpeg e (para voz) Windows com voz pt-BR.
"""
import argparse
import json
import math
import shutil
import subprocess
import sys
import wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H, FPS = 720, 1280, 24

def font(size, bold=True):
    name = 'arialbd.ttf' if bold else 'arial.ttf'
    paths = [Path('C:/Windows/Fonts') / name,
             Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    for p in paths:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

def center(d, text, y, size, fill, bold=True):
    text = str(text).strip()
    if not text:
        return
    f = font(size, bold)
    while size > 22 and d.textbbox((0, 0), text, font=f)[2] > 610:
        size -= 2
        f = font(size, bold)
    b = d.textbbox((0, 0), text, font=f)
    d.text(((W - (b[2] - b[0])) / 2, y), text, font=f, fill=fill)

def speech(text, path, rate=1):
    script = path.with_suffix('.ps1')
    escaped_text = text.replace("'", "''")
    escaped_path = str(path.resolve()).replace("'", "''")
    script.write_text(
        'Add-Type -AssemblyName System.Speech\n'
        '$s = New-Object System.Speech.Synthesis.SpeechSynthesizer\n'
        '$v = @($s.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -eq "pt-BR" })\n'
        'if ($v.Count -eq 0) { $s.Dispose(); exit 3 }\n'
        '$s.SelectVoice($v[0].VoiceInfo.Name)\n'
        f'$s.Rate = {int(rate)}\n'
        f"$s.SetOutputToWaveFile('{escaped_path}')\n"
        f"$s.Speak('{escaped_text}')\n"
        '$s.Dispose()\n', encoding='utf-8-sig')
    result = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script)],
                            capture_output=True, text=True)
    script.unlink(missing_ok=True)
    if result.returncode != 0:
        print('AVISO: voz pt-BR indisponivel no System.Speech:', result.stderr.strip())
        return False
    return path.exists() and path.stat().st_size > 44

def combine_audio(wavs, target, pause=0.28):
    lengths = []
    with wave.open(str(wavs[0]), 'rb') as first:
        rate, ch, width = first.getframerate(), first.getnchannels(), first.getsampwidth()
    with wave.open(str(target), 'wb') as out:
        out.setnchannels(ch)
        out.setsampwidth(width)
        out.setframerate(rate)
        for src in wavs:
            with wave.open(str(src), 'rb') as wf:
                if (wf.getframerate(), wf.getnchannels(), wf.getsampwidth()) != (rate, ch, width):
                    raise ValueError('Formatos WAV incompativeis')
                frames = wf.readframes(wf.getnframes())
                length = wf.getnframes() / rate
            out.writeframes(frames)
            out.writeframes(b'\x00' * int(rate * pause) * ch * width)
            lengths.append(length + pause + 0.35)
    return lengths

def image_crop(path):
    im = Image.open(path).convert('RGB')
    scale = max(630 / im.width, 455 / im.height)
    nw, nh = math.ceil(im.width * scale), math.ceil(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return im.crop(((nw - 630)//2, (nh - 455)//2, (nw + 630)//2, (nh + 455)//2))

def render(scene, i, total, t, progress, photo, brand):
    im = Image.new('RGB', (W, H), (5, 12, 26))
    d = ImageDraw.Draw(im, 'RGBA')
    cx = W//2 + int(100 * math.sin(t * 0.4))
    cy = 430 + int(110 * math.sin(t * 0.22))
    for radius in range(470, 60, -22):
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=(0, 85, 190, 3))
    for k in range(11):
        y = 150 + k*104
        d.line((0, y+int(12*math.sin(t+k)), W, y-30), fill=(16, 49, 89, 32), width=2)
    d.rounded_rectangle((38, 74, 682, 1220), radius=44, outline=(48, 190, 244, 135), width=3)
    d.rounded_rectangle((57, 95, 663, 152), radius=18, fill=(3, 31, 57, 220))
    center(d, brand.upper(), 108, 27, (175, 226, 252))
    if photo is not None:
        py = 265 + int(9 * math.sin(progress * math.pi))
        d.rounded_rectangle((37, py-12, 683, py+475), radius=28, fill=(8, 76, 115, 160))
        im.paste(photo, (45, py))
        d = ImageDraw.Draw(im, 'RGBA')
        d.rectangle((45, py, 675, py+455), outline=(40, 183, 242, 180), width=4)
        title_y, subtitle_y = 820, 950
    else:
        d.ellipse((250, 325, 470, 545), outline=(46, 204, 252, 195), width=6)
        d.line([(295, 445), (330, 410), (360, 438), (422, 375)], fill=(66, 224, 255, 210), width=9)
        title_y, subtitle_y = 630, 798
    center(d, scene.get('titulo', '').upper(), title_y, 65, (255, 255, 255))
    center(d, scene.get('subtitulo', ''), subtitle_y, 35, (122, 224, 255), False)
    d.rounded_rectangle((90, 1110, 630, 1120), radius=5, fill=(33, 66, 92, 240))
    fill_x = max(91, 90 + int(540 * min(1, progress)))
    d.rounded_rectangle((90, 1110, fill_x, 1120), radius=5, fill=(50, 209, 255, 255))
    center(d, f'{i+1:02d} / {total:02d}  -  DESCUBRA. SIMPLIFIQUE. APROVEITE.', 1160, 20, (165, 203, 224), False)
    return im

def main():
    p = argparse.ArgumentParser()
    p.add_argument('roteiro', nargs='?', default='roteiro.json')
    p.add_argument('--sem-voz', action='store_true')
    opts = p.parse_args()
    if not shutil.which('ffmpeg'):
        sys.exit('ERRO: FFmpeg nao encontrado no PATH')
    cfg_path = Path(opts.roteiro)
    if not cfg_path.is_absolute():
        cfg_path = ROOT / cfg_path
    cfg = json.loads(cfg_path.read_text(encoding='utf-8-sig'))
    scenes = cfg.get('cenas', [])
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 8:
        sys.exit('ERRO: roteiro precisa de 1 a 8 cenas')
    out = ROOT / 'saida_v2'
    frames_dir = out / 'quadros'
    frames_dir.mkdir(parents=True, exist_ok=True)
    wavs = []
    has_voice = not opts.sem_voz and sys.platform == 'win32'
    if has_voice:
        for i, scene in enumerate(scenes):
            path = out / f'voz_{i+1:02d}.wav'
            if not speech(scene['fala'], path, cfg.get('velocidade_voz', 1)):
                has_voice = False
                break
            wavs.append(path)
    if has_voice:
        durations = combine_audio(wavs, out / 'narracao_v2.wav')
    else:
        print('AVISO: gerando sem voz; confira a voz pt-BR instalada no Windows')
        durations = [max(3.5, float(s.get('segundos', 4))) for s in scenes]
    photos = []
    assets = ROOT / 'materiais'
    for scene in scenes:
        name = scene.get('imagem', '')
        if name:
            path = (assets / name).resolve()
            if not path.is_relative_to(assets.resolve()) or not path.is_file():
                sys.exit(f'ERRO: imagem nao encontrada na pasta materiais: {name}')
            photos.append(image_crop(path))
        else:
            photos.append(None)
    number, elapsed = 0, 0.0
    for i, (scene, seconds) in enumerate(zip(scenes, durations)):
        count = max(1, math.ceil(seconds * FPS))
        for n in range(count):
            frame = render(scene, i, len(scenes), elapsed+n/FPS, n/count,
                           photos[i], cfg.get('marca', 'Achados Inteligentes'))
            frame.save(frames_dir / f'frame_{number:05d}.jpg', quality=89)
            number += 1
        elapsed += seconds
        print(f'Cena {i+1}/{len(scenes)} pronta ({seconds:.1f} segundos)')
    destination = out / 'achados_inteligentes_v2.mp4'
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
           '-framerate', str(FPS), '-i', str(frames_dir / 'frame_%05d.jpg')]
    if has_voice:
        cmd += ['-i', str(out / 'narracao_v2.wav')]
    cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-preset', 'fast', '-crf', '20', '-movflags', '+faststart']
    if has_voice:
        cmd += ['-c:a', 'aac', '-b:a', '128k']
    cmd += [str(destination)]
    subprocess.run(cmd, check=True)
    print('SUCESSO: Video criado:', destination)

if __name__ == '__main__':
    main()
