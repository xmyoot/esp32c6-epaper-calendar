# Revision A manufacturing package

**Prototype package; digital checks complete, physical validation pending.** Nothing has been ordered or uploaded to an assembly service.

- `EPD_C6_RevA-fabrication.zip`: two copper layers, front paste, both masks/silks, outline and separate plated/non-plated Excellon drills.
- `BOM-JLCPCB.csv`: 13 exact SMT part groups, 25 fitted SMT components, LCSC identifiers and MPNs.
- `CPL-JLCPCB.csv`: top SMT placements only; same native board revision as the Gerbers.
- `SHA256.json`: source and output hashes for this export.
- `drill-report.txt`: drill summary. Four 2.7mm NPTH mounting holes plus socket plated holes and 0.3mm via drills.

Specify standard 2-layer FR-4, 1.6mm finished thickness, 1oz copper, solder mask both sides. ENIG is a reasonable finish for the optical fiducials and FPC pads. Minimum project clearance/trace = 0.20mm; through vias = 0.60/0.30mm with 0.15mm annular ring. There are no microvias or intentionally open via-in-pad features. Three 1mm fiducials have 2mm mask openings. Keep tooling/panel tabs clear of J3's entry edge; arrange a supported breakaway rail or route out that edge after reflow rather than stressing the latch.

Placement origin is the board's lower-left bounding corner: native (100,150)mm. CPL X increases right; Y increases upward. Gerber/drill exports use the same auxiliary origin. CPL rotations are the native KiCad footprint angles, not guessed blanket package corrections. Check JLC's part matching and placement preview against the assembly drawing before ordering. Specifically check D1–D3 cathode pad 1, Q1 gate pad 1, and J3 pin 1. Do not accept an automatic substitute without checking its electrical ratings and land pattern.

J1/J2 sockets, the XIAO, the panel, male headers and mounting hardware are final assembly items, excluded from SMT CPL/BOM. See `../bom/BOM-final-assembly.csv` and `../docs/BRING_UP.md`.

LCSC IDs/MPNs and dated stock responses are recorded under `../analysis/`; LCSC warehouse stock is not a reservation or proof of JLC line-side stock. Extended/basic classification, current JLC quantity, feeder fees, exact rotation mapping and panelization must be rechecked in the actual assembly quote. No pricing or availability guarantee is implied.
