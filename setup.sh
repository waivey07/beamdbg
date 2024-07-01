#!/bin/sh

echo "[+] setting up beamdbg.."

echo "${PWD}/main.py" > ~/.local/bin/beamdbg
chmod 755 ~/.local/bin/beamdbg
echo "[+] Done!"