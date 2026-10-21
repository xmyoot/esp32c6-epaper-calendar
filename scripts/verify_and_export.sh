#!/bin/zsh
set -euo pipefail
mkdir -p "$(dirname "$0")/../analysis"
cd "$(dirname "$0")/.."
KICAD_CLI=${KICAD_CLI:-/Users/hector/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
export KICAD_CLI
KICAD_PYTHON=${KICAD_PYTHON:-/Users/hector/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3}
"$KICAD_CLI" sch erc hardware/EPD_C6_RevA.kicad_sch --exit-code-violations -o analysis/erc.rpt > analysis/erc-cli.log 2>&1
"$KICAD_CLI" pcb drc hardware/EPD_C6_RevA.kicad_pcb --exit-code-violations -o analysis/drc.rpt > analysis/drc-cli.log 2>&1
"$KICAD_CLI" sch export netlist hardware/EPD_C6_RevA.kicad_sch -o analysis/schematic.net > analysis/netlist.log 2>&1
"$KICAD_PYTHON" scripts/native_board.py > analysis/native-board.log 2>&1
.venv/bin/python scripts/audit_design.py
.venv/bin/python scripts/export_release.py
.venv/bin/python scripts/check_release.py
