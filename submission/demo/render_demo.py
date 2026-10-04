"""Render a captioned walkthrough from actual browser screenshots.

Requires Pillow and imageio-ffmpeg (video tooling only, not app dependencies).
Run: python submission/demo/render_demo.py
"""
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "render-work"
WORK.mkdir(exist_ok=True)
SIZE = (1600, 1000)
BLUE = "#295bc4"
INK = "#153047"
FONT = Path("C:/Windows/Fonts")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT / ("segoeuib.ttf" if bold else "segoeui.ttf")), size)


def wrapped(draw, text, position, width, size=30, color=INK, bold=False):
    words = text.split()
    line = ""
    x, y = position
    face = font(size, bold)
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and draw.textlength(candidate, font=face) > width:
            draw.text((x, y), line, font=face, fill=color)
            y += size * 1.45
            line = word
        else:
            line = candidate
    draw.text((x, y), line, font=face, fill=color)
    return y + size * 1.45


SCENES = [
    (7, "Know the concept. Find your words.", "One question. Four ways to understand it.",
     "01-home.jpg", (20, 110, 710, 1170), "Local Qwen3 4B · React + FastAPI + Ollama"),
    (9, "01 / Explain", "Start with a clear explanation of database indexing.",
     "02-explain.jpg", (610, 390, 1220, 1050), "Real browser response · 66.13 seconds"),
    (9, "02 / Explain simpler", "Connect the same concept to a familiar library catalogue.",
     "03-simpler.jpg", (20, 1183, 710, 1730), "Real browser response · 70.36 seconds"),
    (10, "03 / Show example", "See a small SQL example and what each step does.",
     "04-example.jpg", None, "Real browser response · about 66 seconds"),
    (10, "04 / Interview answer", "Rehearse a concise explanation and its tradeoff.",
     "05-interview.jpg", None, "Real browser response · 223.08 seconds"),
    (8, "05 / Java in practice", "Ask for a focused HashMap example. This snippet was also compiled and checked.",
     "07-java-example.jpg", None, "Real browser response · 82.17 seconds"),
    (7, "Now make it yours.", "Look away. Explain the idea in your own words. Then try another mode.",
     "05-interview.jpg", None, "Local inference · No account · No saved conversations"),
]

manifest = {"width": SIZE[0], "height": SIZE[1], "fps": 24, "duration": sum(s[0] for s in SCENES),
            "format": "captioned still-image walkthrough", "audio": "none",
            "disclosure": "Actual app screenshots. Generation waiting time is omitted. No simulated clicks.",
            "scenes": []}
frames = []
start = 0
for number, (duration, title, caption, asset, crop, receipt) in enumerate(SCENES, 1):
    if crop is None:
        rect = json.loads((ROOT / asset.replace(".jpg", "-rect.json")).read_text())
        crop = (round(rect["x"]), round(rect["y"]), round(rect["x"] + rect["width"]),
                round(rect["y"] + rect["height"]))
    canvas = Image.new("RGB", SIZE, "#edf3fa")
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((52, 52, 126, 126), 20, fill=BLUE)
    draw.text((67, 65), "ib", font=font(38, True), fill="white")
    draw.text((148, 70), "interview buddy", font=font(32, True), fill=INK)
    draw.line((52, 154, 1548, 154), fill="#ccd7e4", width=2)
    y = wrapped(draw, title, (52, 232), 430, 52, bold=True)
    wrapped(draw, caption, (52, y + 32), 430, 31)
    wrapped(draw, receipt, (52, 762), 430, 24, BLUE)
    screenshot = Image.open(ROOT / asset).convert("RGB").crop(crop)
    screenshot = ImageOps.contain(screenshot, (980, 735), Image.Resampling.LANCZOS)
    canvas.paste(screenshot, (548 + (980 - screenshot.width) // 2,
                              183 + (735 - screenshot.height) // 2))
    draw.text((52, 940), "Actual app captures · waiting time edited out · AI answers can contain errors",
              font=font(22), fill="#526b82")
    draw.text((1460, 940), f"{number}/{len(SCENES)}", font=font(22, True), fill=BLUE)
    output = WORK / f"scene-{number:02}.png"
    canvas.save(output)
    frames.append(canvas)
    manifest["scenes"].append({"start": start, "duration": duration, "asset": asset,
                               "crop": list(crop), "title": title, "receipt": receipt})
    start += duration

(ROOT / "demo-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
concat = WORK / "scenes.txt"
lines = []
for i, scene in enumerate(SCENES, 1):
    lines += [f"file 'scene-{i:02}.png'", f"duration {scene[0]}"]
lines.append(f"file 'scene-{len(SCENES):02}.png'")
concat.write_text("\n".join(lines), encoding="utf-8")
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", str(concat), "-t", str(manifest["duration"]), "-r", "24", "-c:v", "libx264",
                "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                str(ROOT / "interview-buddy-demo.mp4")], check=True)
sheet = Image.new("RGB", (1200, ((len(frames) + 1) // 2) * 375), "white")
for i, frame in enumerate(frames):
    sheet.paste(frame.resize((600, 375), Image.Resampling.LANCZOS), ((i % 2) * 600, (i // 2) * 375))
sheet.save(ROOT / "contact-sheet.jpg", quality=95)
print(f"Rendered {manifest['duration']} seconds, {len(SCENES)} scenes, no audio.")
