# Revision A handoff — implementation complete

The requested pause/architecture handoff was resumed. Revision A now has native KiCad schematic/PCB, local libraries, routed/filled copper, source/assembly exports, a compiled calendar demonstration and engineering/bring-up documentation. Do not restart architecture planning or overwrite the accepted PCB with an intermediate routing board.

## Authoritative state

- `hardware/EPD_C6_RevA.kicad_pro`, `.kicad_sch`, `.kicad_pcb` are the editable design.
- Architecture: socketed XIAO ESP32C6, USB power, GDEY075T7 bare panel, custom reference boost/charge pump, 60×50mm two-layer carrier, 4 M2.5 holes.
- Q1 final MPN SI1308EDL-T1-GE3 / C469327. The initial BE3 suffix has a manufacturer obsolescence notice recommending GE3; this was resolved in the BOM.
- R7 final RL1206FR-7W0R47L / C859932, 0.47Ω/0.5W.
- 25 fitted SMT components, 13 BOM groups; 2 socket strips hand fitted. 40 total board features including test pads/holes/fiducials.
- J3 bottom contacts, 24×0.5mm, 0.3mm flex; pin1 rightmost with USB up. Mounting tabs explicitly grounded. Native names use the schematic root `/` prefix.
- Final ERC 0/0; DRC 0 violations/0 unconnected/0 footprint errors; independent 94-pin audit passes. See `analysis/release-check.json` and current reports rather than stale exploratory logs.
- Firmware compiles for `esp32:esp32:XIAO_ESP32C6`, core 3.3.12, GxEPD2 1.6.9. Default is a fixed-date OFFLINE DEMO, optional Wi-Fi NTP, 1MHz SPI, full refresh, hibernate and bounded BUSY recovery.

## Files to read next

1. `docs/DESIGN_REVIEW.md`: decisions, evidence, triage and limits.
2. `docs/BRING_UP.md`: physical acceptance sequence and measurement targets.
3. `manufacturing/README.md`: origin, rotation/panelization and final quote preflight.
4. `docs/PORTFOLIO.md`: accurate interview/presentation framing.

No physical prototype, fabrication order, assembly upload or firmware flash occurred. Remaining real-world work is a prototype build/measurement; do not claim working hardware based on compile/DRC alone. Exact flex lot fit, rail/current/thermal behavior, DC-bias capacitance, RF/backplane geometry and assembly quote/rotation acceptance remain documented limits. Make routine decisions autonomously; ask the user only for actual blockers, as already authorized.

## Tools and reproduction

Requested repos remain under `tools/kicad-happy` and `tools/KiCadRoutingTools`, pinned in `docs/ATTRIBUTION.md`. Accepted routing commands/logs are under `analysis/routing/strict-power.log`, `clock-first.log`, `remaining-signals.log`, `ground.log`. Default fab-size escalation produced an exploratory result that was rejected. Use explicit net lists, no rip of protected copper, no settings relaxation, escalation off, 0.20mm clearance and 0.60/0.30mm vias. Fine-pitch power entry has a reviewed 0.2mm neck; it is not a clearance exception.

`./scripts/verify_and_export.sh` repeats checks and exports from the native design without rerouting. The generation scripts/design JSON record construction history; native files are authoritative after any future manual edits. The Arduino/host dependencies are project-local and can be large; `tools/` and `.venv/` are disposable setup rather than portfolio deliverables. The local ctags compatibility patch and exact versions are recorded in ATTRIBUTION.md. No global tool installation or OS permission change was needed.
