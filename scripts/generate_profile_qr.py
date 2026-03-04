#!/usr/bin/env python3
"""Generate a QR code with a circular profile image in the center."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import qrcode
    from PIL import Image, ImageDraw
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Faltan dependencias. Ejecuta: pip install -r requirements-qr.txt"
    ) from exc


def _prompt(text: str, default: str | None = None) -> str:
    label = f"{text} [{default}]: " if default else f"{text}: "
    value = input(label).strip()
    if value:
        return value
    if default is not None:
        return default
    return ""


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a QR code with a circular profile image in the center."
    )
    parser.add_argument("--url", help="URL target for the QR code.")
    parser.add_argument("--image", help="Path to profile image file.")
    parser.add_argument(
        "--output",
        default="contact_qr.png",
        help="Output PNG file path (default: contact_qr.png).",
    )
    parser.add_argument(
        "--background",
        choices=("transparent", "white"),
        default="transparent",
        help="QR background style (default: transparent).",
    )
    parser.add_argument(
        "--photo-scale",
        type=float,
        default=0.27,
        help="Center photo scale vs QR width, usually 0.22-0.30 (default: 0.27).",
    )
    parser.add_argument(
        "--box-size",
        type=int,
        default=16,
        help="Pixel size of each QR module (default: 16).",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="QR quiet-zone border in modules (default: 4).",
    )
    return parser


def _circular_image(image_path: Path, size: int) -> Image.Image:
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    cropped = img.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.Resampling.LANCZOS
    )

    mask = Image.new("L", (size * 2, size * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size * 2, size * 2), fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)

    circular = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circular.paste(cropped, (0, 0), mask)
    return circular


def _build_center_badge(profile_img: Image.Image) -> Image.Image:
    size = profile_img.width
    white_ring = max(6, size // 20)
    dark_ring = max(3, size // 36)
    badge_size = size + 2 * (white_ring + dark_ring)

    badge = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    draw.ellipse((0, 0, badge_size - 1, badge_size - 1), fill=(0, 0, 0, 255))
    draw.ellipse(
        (
            dark_ring,
            dark_ring,
            badge_size - dark_ring - 1,
            badge_size - dark_ring - 1,
        ),
        fill=(255, 255, 255, 255),
    )

    photo_xy = dark_ring + white_ring
    badge.paste(profile_img, (photo_xy, photo_xy), profile_img)
    return badge


def generate_qr_with_photo(
    url: str,
    image_path: Path,
    output_path: Path,
    background: str,
    photo_scale: float,
    box_size: int,
    border: int,
) -> Path:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    bg_color = (0, 0, 0, 0) if background == "transparent" else (255, 255, 255, 255)
    qr_img = qr.make_image(fill_color=(0, 0, 0, 255), back_color=bg_color).convert(
        "RGBA"
    )

    photo_size = max(90, int(qr_img.width * photo_scale))
    profile = _circular_image(image_path, photo_size)
    badge = _build_center_badge(profile)

    x = (qr_img.width - badge.width) // 2
    y = (qr_img.height - badge.height) // 2
    qr_img.alpha_composite(badge, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    qr_img.save(output_path, format="PNG")
    return output_path.resolve()


def main() -> None:
    args = _build_parser().parse_args()

    url = args.url or _prompt("Ingresa la URL destino del QR")
    while not url:
        url = _prompt("La URL es obligatoria. Ingresa la URL destino del QR")

    image_input = args.image or _prompt("Ruta de la foto de perfil", "profile.jpg")
    image_path = Path(image_input).expanduser()
    while not image_path.exists():
        image_input = _prompt("No se encontro la imagen. Ingresa una ruta valida")
        image_path = Path(image_input).expanduser()

    output_input = args.output or _prompt("Nombre del archivo de salida", "contact_qr.png")
    output_path = Path(output_input).expanduser()

    photo_scale = max(0.18, min(args.photo_scale, 0.34))

    result_path = generate_qr_with_photo(
        url=url,
        image_path=image_path,
        output_path=output_path,
        background=args.background,
        photo_scale=photo_scale,
        box_size=max(6, args.box_size),
        border=max(2, args.border),
    )
    print(f"QR generado correctamente: {result_path}")


if __name__ == "__main__":
    main()
