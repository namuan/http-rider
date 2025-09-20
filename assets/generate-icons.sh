#!/usr/bin/env bash
set -euo pipefail

# Generate macOS .icns and Windows .ico from a source PNG.
# Usage: bash assets/generate-icons.sh path/to/source.png
# Outputs: assets/icon.icns and assets/icon.ico

# Resolve script directory (assets)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR"

# Input validation
if [[ $# -lt 1 ]]; then
  echo "Usage: bash assets/generate-icons.sh path/to/source.png" >&2
  exit 2
fi
SRC_PNG="$1"
if [[ ! -f "$SRC_PNG" ]]; then
  # Try relative to assets directory if not found
  if [[ -f "$ASSETS_DIR/$SRC_PNG" ]]; then
    SRC_PNG="$ASSETS_DIR/$SRC_PNG"
  else
    echo "Source PNG not found: $1" >&2
    exit 2
  fi
fi

# Dependency checks
if ! command -v magick >/dev/null 2>&1; then
  echo "Error: ImageMagick 'magick' command not found. Please install ImageMagick." >&2
  exit 3
fi
if ! command -v iconutil >/dev/null 2>&1; then
  echo "Error: 'iconutil' not found (required on macOS to build .icns)." >&2
  exit 3
fi

ICONSET_DIR="$ASSETS_DIR/icons.iconset"
ICNS_OUT="$ASSETS_DIR/icon.icns"
ICO_OUT="$ASSETS_DIR/icon.ico"

echo "🛠️  Generating application icons from: $SRC_PNG"

# Clean/create iconset folder
rm -rf "$ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

# Generate ICNS sizes (ensure exact squares using ^ and extent) and preserve transparency
magick "$SRC_PNG" -background none -alpha on -resize 16x16^  -gravity center -extent 16x16   -strip "$ICONSET_DIR/icon_16x16.png"
magick "$SRC_PNG" -background none -alpha on -resize 32x32^  -gravity center -extent 32x32   -strip "$ICONSET_DIR/icon_16x16@2x.png"
magick "$SRC_PNG" -background none -alpha on -resize 32x32^  -gravity center -extent 32x32   -strip "$ICONSET_DIR/icon_32x32.png"
magick "$SRC_PNG" -background none -alpha on -resize 64x64^  -gravity center -extent 64x64   -strip "$ICONSET_DIR/icon_32x32@2x.png"
magick "$SRC_PNG" -background none -alpha on -resize 128x128^ -gravity center -extent 128x128 -strip "$ICONSET_DIR/icon_128x128.png"
magick "$SRC_PNG" -background none -alpha on -resize 256x256^ -gravity center -extent 256x256 -strip "$ICONSET_DIR/icon_128x128@2x.png"
magick "$SRC_PNG" -background none -alpha on -resize 256x256^ -gravity center -extent 256x256 -strip "$ICONSET_DIR/icon_256x256.png"
magick "$SRC_PNG" -background none -alpha on -resize 512x512^ -gravity center -extent 512x512 -strip "$ICONSET_DIR/icon_256x256@2x.png"
magick "$SRC_PNG" -background none -alpha on -resize 512x512^ -gravity center -extent 512x512 -strip "$ICONSET_DIR/icon_512x512.png"
magick "$SRC_PNG" -background none -alpha on -resize 1024x1024^ -gravity center -extent 1024x1024 -strip "$ICONSET_DIR/icon_512x512@2x.png"

# Build ICNS
iconutil -c icns "$ICONSET_DIR" -o "$ICNS_OUT"

# Generate ICO sizes with high-quality resampling; sharpen small sizes
TMP16="$ASSETS_DIR/icon-16.png"
TMP24="$ASSETS_DIR/icon-24.png"
TMP32="$ASSETS_DIR/icon-32.png"
TMP48="$ASSETS_DIR/icon-48.png"
TMP64="$ASSETS_DIR/icon-64.png"
TMP128="$ASSETS_DIR/icon-128.png"
TMP256="$ASSETS_DIR/icon-256.png"

magick "$SRC_PNG" -background none -alpha on -filter Lanczos -define filter:lobes=3 -resize 16x16^  -gravity center -extent 16x16  -unsharp 0x0.75+0.75+0.008 -strip "$TMP16"
magick "$SRC_PNG" -background none -alpha on -filter Lanczos -define filter:lobes=3 -resize 24x24^  -gravity center -extent 24x24  -unsharp 0x0.75+0.75+0.008 -strip "$TMP24"
magick "$SRC_PNG" -background none -alpha on -filter Lanczos -define filter:lobes=3 -resize 32x32^  -gravity center -extent 32x32  -unsharp 0x0.75+0.75+0.008 -strip "$TMP32"
magick "$SRC_PNG" -background none -alpha on -filter Lanczos -define filter:lobes=3 -resize 48x48^  -gravity center -extent 48x48  -unsharp 0x0.75+0.75+0.008 -strip "$TMP48"
magick "$SRC_PNG" -background none -alpha on -filter Lanczos -define filter:lobes=3 -resize 64x64^  -gravity center -extent 64x64  -unsharp 0x0.75+0.75+0.008 -strip "$TMP64"
magick "$SRC_PNG" -background none -alpha on -filter Lanczos -define filter:lobes=3 -resize 128x128^ -gravity center -extent 128x128 -strip "$TMP128"
magick "$SRC_PNG" -background none -alpha on -filter Lanczos -define filter:lobes=3 -resize 256x256^ -gravity center -extent 256x256 -strip "$TMP256"

# Compose multi-size ICO
magick "$TMP128" "$TMP256" "$ICO_OUT"

# Cleanup
rm -rf "$ICONSET_DIR"
rm -f "$ASSETS_DIR"/icon-*.png

echo "✅ Icons generated: $ICNS_OUT and $ICO_OUT"
