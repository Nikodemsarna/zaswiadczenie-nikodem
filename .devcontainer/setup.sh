#!/usr/bin/env bash
# Instalacja Claude Code w Codespace. Uruchamiane raz, przy tworzeniu środowiska.
set -e

echo "→ Instaluję Claude Code…"
curl -fsSL https://claude.ai/install.sh | bash

# Katalog instalacji natywnej
export PATH="$HOME/.local/bin:$PATH"
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo
echo "→ Weryfikacja:"
git --version
python --version
node --version
claude --version || echo "  (claude: uruchom nowy terminal i sprawdź ponownie)"

echo
echo "=============================================="
echo " Środowisko gotowe."
echo " Następny krok: wpisz  claude  i zaloguj się."
echo "=============================================="
