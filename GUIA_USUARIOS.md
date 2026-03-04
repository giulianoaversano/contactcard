# Guia para usuarios (replicar desde cero)

Esta guia permite que cualquier usuario tome este proyecto, lo personalice y lo publique en su propia cuenta.

## 1) Descargar el codigo del repositorio original

### Opcion A: con Git (recomendada)

```bash
git clone https://github.com/TU-USUARIO-ORIGEN/TU-REPO-ORIGEN.git
cd TU-REPO-ORIGEN
```

### Opcion B: ZIP

1. Entrar al repo en GitHub.
2. `Code` -> `Download ZIP`.
3. Descomprimir y abrir la carpeta.

## 2) Modificar el contenido del proyecto

Edita estos archivos:

- `index.html`
- `profile.jpg` (o cambia el `src` del `<img class="avatar">` si usas otro nombre)
- `giuliano-aversano.vcf` (reemplazalo por tu propio contacto `.vcf`)

### Que partes cambiar en `index.html`

- Nombre, titulo y empresa.
- Links de WhatsApp, email, scheduler y LinkedIn.
- Texto del boton de contacto si corresponde.
- Copyright del pie.

### Probar localmente

```bash
python3 -m http.server 8080
```

Abrir en navegador: `http://localhost:8080`

## 3) Crear tu propio repositorio en GitHub

En GitHub:

1. `New repository`.
2. Nombre sugerido: `digital-card` (o el que prefieras).
3. Publico (recomendado para GitHub Pages).
4. Crear repo.

## 4) Crear GitHub Pages

Dentro del nuevo repo:

1. `Settings` -> `Pages`.
2. En `Build and deployment`, elegir `Deploy from a branch`.
3. Branch: `main` y folder: `/(root)`.
4. Guardar.

GitHub mostrara una URL como:

- `https://TU-USUARIO.github.io/TU-REPO/`
- o `https://TU-USUARIO.github.io/` si el repo se llama `TU-USUARIO.github.io`

## 5) Subir el codigo a tu repositorio

Si clonaste el repo original y quieres empezar limpio en tu repo:

```bash
rm -rf .git
git init
git add .
git commit -m "Initial commit - my digital card"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-NUEVO-REPO.git
git push -u origin main
```

Si ya tenias Git inicializado, solo cambia el remoto `origin` al nuevo repo y hace push.

## 6) Crear QR personalizado (URL + foto de perfil)

Este proyecto incluye el script:

- `scripts/generate_profile_qr.py`

El script:

- pide la URL destino,
- pide la ruta de la foto de perfil,
- genera un QR con foto circular al centro (estilo similar al ejemplo adjunto).

### Instalar dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-qr.txt
```

### Ejecutar (interactivo)

```bash
python3 scripts/generate_profile_qr.py
```

Te preguntara:

1. URL del QR (ej: URL de GitHub Pages)
2. Ruta de imagen de perfil (ej: `profile.jpg`)
3. Nombre del archivo de salida (ej: `mi_qr.png`)

### Ejecutar (sin preguntas)

```bash
python3 scripts/generate_profile_qr.py \
  --url "https://TU-USUARIO.github.io/TU-REPO/" \
  --image profile.jpg \
  --output mi_qr.png \
  --background transparent
```

## Recomendaciones finales

- Verifica que la URL de GitHub Pages ya responda antes de generar el QR definitivo.
- Prueba el QR con al menos dos apps/camaras distintas.
- Mantene una copia de tu imagen final (`mi_qr.png`) para imprimirla o compartirla.

