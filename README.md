# Tarjeta Digital (HTML + GitHub Pages + QR)

Este proyecto es una tarjeta de contacto digital en HTML lista para publicar en GitHub Pages y compartir con un codigo QR personalizado.

## Que incluye este repositorio

- `index.html`: pagina principal de la tarjeta.
- `profile.jpg` / `profile.png`: imagen de perfil.
- `giuliano-aversano.vcf`: archivo de contacto para descarga.
- `scripts/generate_profile_qr.py`: script para generar QR con URL + foto de perfil en el centro.
- `requirements-qr.txt`: dependencias de Python para generar el QR.

## Flujo rapido (desde cero)

1. Clonar este repositorio.
2. Personalizar `index.html`, la foto de perfil y el archivo `.vcf`.
3. Crear un nuevo repo en tu cuenta de GitHub.
4. Subir el codigo a ese repo.
5. Activar GitHub Pages.
6. Generar el QR apuntando a la URL publicada.

La guia completa paso a paso esta en [`GUIA_USUARIOS.md`](./GUIA_USUARIOS.md).

## Vista previa local

```bash
python3 -m http.server 8080
```

Luego abre: `http://localhost:8080`

## Generar QR personalizado

1. Instala dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-qr.txt
```

2. Ejecuta el script (modo interactivo):

```bash
python3 scripts/generate_profile_qr.py
```

Te pedira:

- URL de destino del QR.
- Ruta de la foto de perfil.
- Nombre de archivo de salida.

Ejemplo no interactivo:

```bash
python3 scripts/generate_profile_qr.py \
  --url "https://TU-USUARIO.github.io/TU-REPO/" \
  --image profile.jpg \
  --output mi_qr.png \
  --background transparent
```

