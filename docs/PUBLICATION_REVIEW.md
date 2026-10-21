# Revision A publication review — 2026-10-21

## Verdict

No confirmed board-stopping connectivity, footprint-pin mapping, or native design-rule defect was found in this review. Revision A is suitable for presentation as a designed and digitally checked engineering prototype. It is **not physically validated**. The open risks below must be closed during prototype assembly/bring-up before claiming a working display or production readiness.

This review supplements [the detailed R2 review](DESIGN_REVIEW_R2.md), whose pin tables, power calculations, source-page references, and analyzer dispositions remain applicable. The native electrical design and fabrication package were not changed. Evidence is in `analysis/review-2026-10-21/` and the refreshed root ERC/DRC/netlist/pin audit reports.

## Corrections made

- The verification/export script now invokes both native ERC and DRC with `--exit-code-violations`. Previously those commands could return success after reporting violations, allowing exports to proceed. With `set -e`, the first failing check now stops the release sequence. The selected `KICAD_CLI` is exported so the subsequent exporter uses the same executable.
- Gave the exported board-layout SVG an explicit `.svg` filename and linked it from the README so public viewers can recognize it.
- Added the missing Python dependency declaration and replaced firmware instructions that depended on absent local tool binaries with pinned dependency/setup commands.
- Added original-work licensing and the upstream KiCad library license/exception for redistributed library assets. Tool and AI assistance attribution are explicit.
- Excluded supplied client screenshots and local credentials/tooling from publication. Public requirements remain transcribed in ARCHITECTURE.md. Updated the main README to link the latest reviews.

## Fresh verification

| Check | Result / limit |
|---|---|
| Native KiCad ERC | 0 errors / 0 warnings under saved project settings |
| Native KiCad DRC | 0 violations / 0 unconnected pads / 0 footprint errors |
| Fresh exported netlist + pcbnew pin audit | PASS: 94 declared pins, 37 critical assertions, 40 footprints |
| Release consistency | PASS: 16 hashes; 25 SMT placements in 13 BOM groups |
| kicad-happy schematic | 4 warnings / 15 information findings; same as R2 |
| PCB full + proximity | 1 error / 1 warning / 15 information findings; same as R2 |
| Cross analysis | 0 findings |
| Gerber/drill analysis | 0 findings |
| EMC analysis | 4 errors / 15 warnings / 3 information findings; heuristic score 58, five categories produced findings |
| Thermal analysis | 0 components assessed; unavailable loss/extraction data, not a thermal pass |
| LCSC-only lifecycle | 14 MPNs; all unknown by construction, not active-status certification |
| Prior-review delta | Schematic, PCB and EMC findings unchanged |

The full 94-pin check compares current native exported data against the construction record and independently transcribed critical physical pin tables. It proves the declared mapping, not physical assembly. The saved hardware, project and fabrication hashes match the previous release. There are no DRC exclusions; the native reports explicitly list ignored advisory categories. No severity/rule was weakened for this review.

The panel p40 reference, Vishay Si1308EDL p1 top-view pinout, and Hirose FH12 p4 bottom-contact drawing were visually reread. The boost topology, source/shunt pickup and connector pin-1 location agree with the current native mapping. Other component ratings and passive-source conclusions are carried forward from the detailed R2 review, not represented as newly measured or exhaustively re-extracted here. The latest Seeed wiki also confirms GPIO3 low enables RF-switch control and GPIO14 low selects the built-in antenna, matching the sketch.

## Open engineering risks

| Risk | Assessment / required closure |
|---|---|
| Gate drive and sense routing | GDR totals 18.466 mm / two vias; RESE 15.905 mm branched / two vias. Probe Q1 gate-to-source and RESE at both shunt and controller during startup/refresh. Shorten routing in a subsequent revision if waveforms require it. This is a real layout risk, not proof of failure. |
| Shared 3.3 V supply | Only 50 mA planning margin in the conservative allocation. Measure rail droop, inrush and accidental radio/refresh overlap; firmware scheduling alone is insufficient evidence. |
| MLCC effective capacitance | Nominal ratings match the panel reference; exact capacitance at DC bias remains unknown. Obtain manufacturer curves or measure startup/ripple before production freeze. |
| Panel/FPC and RF mechanics | Exact panel-lot dry-fit, pin-1/contact-side confirmation, latch access and antenna/backplate spacing still need physical inspection. |
| Connector edge | J3 courtyard is 0.10 mm from the top edge. Native copper-edge clearance passes. Arrange panel support and depaneling clear of the latch with the assembler. |
| Measurement coverage | Six dedicated probe pads cover 6/22 connected nets. Other nets require component-pad probing; no production fixture claim. |

Analyzer source/ground warnings are explained by the passive two-socket module representation and internally generated VDD node. Do not add an external supply to panel pin 18. EMC transition/return-path findings remain bench items; low SPI repetition rate is not evidence of slow edges or quiet gate drive. The antenna keepout must remain clear on both copper layers.

## Limits and release framing

No physical board, rail/current/temperature measurement, display refresh, RF/EMC test, or panel mating test has been performed. No SPICE executable (`ngspice`, `ltspice`, `xyce`) is installed on PATH and no validated UC8179 loop model is available; no simulation result is claimed. The prior successful firmware compile is retained in `analysis/firmware-build.log`; fresh build validation, if available, is recorded separately. Supplier prices, availability and assembly rotation acceptance were not requalified by this publication review.

The R2 five-record deep-review evidence gate is retained as historical evidence; this publication pass does not claim a new gate run. The fresh analyzer delta, raw native pin audit, source drawings and unchanged release hashes support the narrower verdict above. See [BRING_UP.md](BRING_UP.md) for physical acceptance measurements and stop conditions.

Portfolio wording: **“Designed, routed, and digitally checked; prototype hardware testing pending.”** Renderings are labeled as renderings. The public entry explains module tradeoffs, panel substitution, critical-copper routing, verification coverage, and outstanding measurements. It attributes AI assistance and automation.

Sources: [Seeed RF-switch guidance](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/), [panel specification](https://www.laskakit.cz/user/related_files/gdey075t7.pdf), [Vishay MOSFET](https://www.vishay.com/docs/63399/si1308edl.pdf), and the cached Hirose drawing. See [ATTRIBUTION.md](ATTRIBUTION.md) for tool commits and reference provenance.

## Publication validation

The verification script was exercised with a simulated ERC process returning exit code 5; the release stopped after that first command, before DRC or export. Normal fresh ERC and release checks then passed again. The original fabrication hashes remain unchanged. The portfolio entry was built locally with Jekyll strict front matter, visually inspected, and checked for its homepage link, image asset and explicit untested-hardware status. GitHub Actions adds future release-consistency and pinned firmware builds; hosted runner results must be read independently from the local results above.
