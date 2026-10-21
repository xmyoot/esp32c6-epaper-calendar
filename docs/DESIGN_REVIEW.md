# Revision A engineering review

**Date:** 2026-10-20. **Design:** EPD_C6_RevA, KiCad 10.0.7, single schematic sheet, two-layer 60×50mm carrier. **Disposition:** digital design/package complete for an engineering prototype; physical validation and assembly-quote preflight remain. No prototype has been powered or certified.

## Findings that affect release confidence

| Priority | Finding / decision | Basis and closure |
|---|---|---|
| Prototype test | Shared 3V3 loading, inrush, switching overshoot and actual rail ripple remain unmeasured. | Keep radio and refresh separated. Measure the limits in BRING_UP.md before declaring a working product. No extra regulator was added merely to avoid analysis. |
| Prototype test | Exact panel lot, flex pin-1 orientation and RF relationship to the display backplate need a physical dry-fit. | Documentation and native pad mapping checked; cannot substitute a mechanical fit test with DRC. |
| Electrical characterization | Exact effective MLCC capacitance under DC bias is not established by the generic cached catalogs. | 50V X7R parts and larger 0805/1206/1210 bodies follow the reference nominal values. Ripple/startup testing and manufacturer bias curves remain necessary before production substitution/freeze. Do not claim the nominal 10µF remains 10µF at 20V. |
| Manufacturing | J3 is deliberately close to the cable-entry edge. | Native outline/copper clearance is clean; the analyzer's edge warning uses its courtyard bounds. Use supported panelization and a routed entry edge; confirm the latch with the assembly shop. |
| Procurement | LCSC stock and JLC line-side availability differ; API lifecycle results are unknown. | Exact part IDs and dated responses are saved. Recheck stock, MPN matching, rotations and quote/panelization before purchasing. |

No unresolved native ERC/DRC error, unconnected pad, or pin-map mismatch remains. These findings limit prototype/production claims, not the existence of the delivered design files.

## Verification basis

- **Raw-file checks:** native netlist and pcbnew pad export, full 40-footprint set and schematic UUID paths. `analysis/pin-audit.json`: 37 independent critical pin assertions and all 94 declared pins pass. `scripts/audit_design.py` independently transcribes the critical physical tables; it does not simply compare two copies of the same design JSON.
- **Datasheet/manual checks:** Good Display rev1.0 pp7–10/40; Hirose FH12 catalog pp4–5; Vishay Si1308EDL p1; JSCJ MBR0530 pp1–2; Bourns SRN4018 pp1–2; Yageo RL series pp2/5; cached passive data; Seeed official native module project and SGM6029 datasheet. No structured-extraction claim is made for missing DC-bias curves.
- **Native checks:** `analysis/erc.rpt` has 0 errors/0 warnings. `analysis/drc.rpt` has 0 violations/0 unconnected pads/0 footprint errors. Factory ignored advisory categories are printed in those reports; no board-specific error exclusions or severity suppressions were added.
- **Firmware:** Arduino-ESP32 3.3.12, GxEPD2 1.6.9, Adafruit GFX 1.12.6 / BusIO 1.17.4. Successful compile: 1,010,166 bytes flash (77% of selected app partition), 51,200 bytes global RAM (15%). This is compilation, not a panel test.
- **Export consistency:** BOM/CPL both contain the same 25 fitted SMT references in 13 groups. Native source/output hashes and `analysis/release-check.json` pass. Through-hole sockets/final assembly parts are separate.

## Component summary and power tree

40 board features: 12 capacitors, 7 resistors, 3 diodes, 1 MOSFET, 1 inductor, 3 connectors, 6 test pads, 4 NPTH mounting holes and 3 optical fiducials. The carrier has no separate controller IC, USB circuit, battery, RTC or additional regulator. The display controller is inside the panel; the MCU/regulator/USB live on the removable module.

```text
USB-C 5V -> XIAO ESP32C6 on-module buck -> 3V3_MODULE
                                              |
                                           R1 0R
                                              |
                                           3V3_EPD -> VCI/VDDIO + local bypass
                                              |
                                   L1/Q1/D1-D3/C2 -> PREVGH/PREVGL
                                         ^
                                  panel GDR / RESE
```

Seeed's downloaded 2026 native module project identifies SGM6029CYG/TR. Its manufacturer describes up to 1A under specified conditions; retain the more conservative 700mA shared planning budget rather than treating that as unconditional spare carrier current. Allocations 500mA module + 150mA carrier leave 50mA. They are not observed maxima. Another purchased XIAO revision must be checked against its own regulator implementation.

## Pin-level and physical review

| Parts | Complete review result |
|---|---|
| J1/J2 | Physical two-row header order checked against Seeed U2 drilled contacts: 15.24mm row spacing, 2.54mm pitch. J2 numbers top-to-bottom are 5V,GND,3V3,D10,D9,D8,D7, not the module DIP numbering. USB points toward the board top. Samtec SSW series catalog documents the pitch and mating family; exact assembly engagement still needs dry-fit. |
| J3 | All 24 contacts plus mounting-tab ground reviewed. Pin 4 NC, pin 5 VSHR independent of pin 21; pin 18 only bypassed to GND; BS1 grounded; TSCL/TSDA/VPP unused. Hirose bottom contacts, 0.3mm flex, 0.5mm pitch and land geometry compared with the vendored footprint. Pin 1 is the rightmost contact with USB up. |
| Q1 | Pad 1 gate/GDR, 2 source/RESE, 3 drain/SW. SC70/SOT323 geometry and top-view diagram compared with Vishay p1. Selected SI1308EDL-T1-GE3, 30V, 0.185Ω maximum at VGS=2.5V, typical 1.4nC gate charge. No pin-order assumption from a generic MOSFET alone. |
| D1 | Cathode pad 1 PREVGH, anode pad 2 SW. |
| D2 | Cathode pad 1 GND, anode pad 2 PUMP. |
| D3 | Cathode pad 1 PUMP, anode pad 2 PREVGL. All three use JSCJ MBR0530 SOD123; cathode marking and package checked. |
| L1 | 10µH SRN4018-100M: 1.3A RMS, 1.4A saturation at specified 30% inductance loss, ≤0.180Ω DCR. Same reference inductance; no mixing with the original client's 22µH panel circuit. |
| R1–R7 | All endpoints checked. R1 isolates the display branch; R2/R3 33Ω source damping; R4 100k CS pull-up; R5 100k reset pull-down; R6 1M gate pull-down; R7 0.47Ω/0.5W sense. R7's final RL1206FR-7W0R47L is the high-power 7W packing/power variant, not the ordinary 0.25W 07 variant. |
| C1–C12 | All endpoints checked; nonpolar parts. C1/C2 4.7µF50V; C3/C7/C8/C9/C12 10µF50V; C4/C5/C6/C10 1µF50V; C11 100nF16V. Two-pin polarity checking is not meaningful; value, dielectric, voltage/package and endpoint checks were performed. Bias capacitance is an explicit characterization gap. |
| TP1–TP6 | 3V3, GND, PREVGH, PREVGL, BUSY, RESET match the probe table. Other rail capacitor pads remain accessible. |
| H1–H4 / FID1–3 | Mechanical/optical features; no electrical pin mapping. Excluded from fitted SMT BOM. |

The complete panel net table is in ARCHITECTURE.md. The independently audited table is in `scripts/audit_design.py`. Native net names include the root-sheet `/` prefix; logical tables omit it for readability.

## Switching, supply and thermal reasoning

The topology reproduces the panel-controlled reference, not MCU PWM. The short Q1/L1/D1/C2 switching copper and Q1-to-R7 sense-current path were explicitly routed and locked. The router completed other connections; native DRC and source checks decide acceptance.

The exact GxEPD2 initialization programs ±20V gate boost, ±15V source drive and 4.2V red/source auxiliary drive. VCOM is panel/OTP dependent. Thus 50V capacitors have 2.5× nominal voltage ratio against a 20V rail. Q1/diodes have 30V ratings against nominal ~20V switching stress; overshoot must be measured. These ratios do not prove transient safety.

`analysis/helpers/power_budget.py` records illustrative calculations at 0.5A switch RMS / 1A peak: R7 loss 0.1175W (24% of 0.5W), Q1 conduction 0.04625W at 0.185Ω, L1 copper loss 0.045W. These omit switching loss, pulse heating and actual board thermal resistance. The initial bench limits are below L1's saturation rating and Q1's 2.5V-drive current rating; controller current-limit behavior still needs measurement.

Local 3V3 capacitance is 15.8µF nominal. Stored energy in the four nominal 10µF bias capacitors at ±20/±15V is about 6.25mJ, before other nodes and losses. Even this small energy can create input transients; the panel's average-current specification is not a startup-current bound. Use the R1 link and scope 3V3 during startup. The controlled default reset/deselect states, Wi-Fi separation and finite BUSY recovery support bring-up but do not replace those tests.

The thermal analyzer ran but assessed zero components because it lacks structured device dissipation data. It must not be read as “zero heat.” The manual losses above are the current thermal basis. No carrier QFN or exposed-pad IC requires a thermal-via array; Q1 is a three-lead discrete. Module thermal behavior is outside the carrier analyzer's device coverage.

## Layout, manufacturing and signal review

60×50mm, 1.6mm board; 1oz copper specified; 2mm corner radii; all fitted SMT on front, two hand-soldered socket strips. Minimum track 0.20mm, minimum clearance 0.20mm, all 52 through vias 0.60/0.30mm, 0.15mm annular ring. No impedance-controlled or differential routes are needed because USB stays on the XIAO. Clock starts at 1MHz; 33Ω source resistors are fitted. No length tuning was added.

The fixed 0.20mm gap between the connector's 0.30mm pads sets the local minimum. 0.30mm bias spacing is a preferred target outside that escape, not a falsely claimed universal achieved minimum. The power trunk is generally 0.6mm; roughly 1mm of a fine-pitch 3V3 pad entry necks to 0.2mm. That is a reviewed local neck for the 150mA carrier budget, not a wholesale constraint relaxation. Inspect edges/ripple before increasing SPI speed.

Front/back GND pours are filled and stitched; the native zero-unconnected result includes the formerly separate ground islands. The antenna exclusion is an explicit rule area on both copper layers, not an accidental copper gap. Module matching/antenna routing is unchanged on the module. Display backplane/enclosure clearance still needs physical evaluation.

Gerber/drill analysis reports no findings; native board and export dimension is 60×50mm. Three fiducials are included. CPL and drill/Gerber origins are consistent. Library references resolve locally. The 3D rendering is from KiCad and is illustrative: the removable XIAO and display are not shown.

## Automated findings triaged

| Analyzer finding | Engineering disposition |
|---|---|
| J1 has no GND; J1/J2 lack I/O EMC filters | The two sockets jointly form one module interface; GND is on J2. They are not arbitrary external wire-cable connectors. Adding ferrites/chokes to each GPIO would overcomplicate this carrier. No EMC compliance claim follows from this dismissal. |
| 3V3_MODULE / 3V3_EPD have no declared source | Connector symbols are passive, with the real source on the removable XIAO and R1 bridging branches. The native pin trace establishes the DC source. |
| VDD_INT has no source | It is a panel internal regulator node; its only external component is the required bypass. It must not be tied to external 3V3 to silence a detector. |
| J3 edge proximity | Intended edge-facing connector; pad/body/courtyard distinction reviewed. Copper DRC is clean. Supported panelization and physical latch access remain relevant. |
| Short source segments show 50% / 75% plane coverage | MOSI_SRC/SCK_SRC are only 2.2/2.5mm and include the through-hole pad transition. The heuristic percentage is not proof of a split across the whole SPI path. Retain as a local SI/return-path test item, not a reason to split GND or add a bridge capacitor across the RF exclusion. |
| Clock near J2/J3 | These are the source module and destination panel; proximity is inherent. SPI is deliberately slow and source damped. |
| Missing stitching within 1mm of each layer change | Additional ground stitching was added to connect regions. Some dense escapes still exceed this heuristic distance; infrequent bias rails and slow control nets are not equivalent to high-speed clocks. Residual emissions/edge behavior require measurement. |
| Six test points cover 27% of nets | Intended compact prototype coverage; exposed source resistors and capacitor pads provide remaining access. No bed-of-nails production fixture is claimed. |

No automated findings were silently deleted or severity-suppressed to obtain a pass. The EMC analyzer's heuristic score is not a measured emissions margin; its error/warning labels are retained in the JSON with the above dispositions.

## Lifecycle, sources and review limits

The LCSC-only lifecycle audit executed for 14 unique fitted MPNs, but returned unknown for all because that source does not publish lifecycle status. A separate manufacturer notice, Vishay PTN-SIL-029-2026, identifies the initially considered BE3 suffix for last-time-buy and explicitly recommends **SI1308EDL-T1-GE3**. The final BOM uses that GE3 part, LCSC C469327, with a dated stock response; no footprint change is needed. This closes that identified lifecycle issue without claiming every other part has been audited active. [Manufacturer notice, pp1–3](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8919/PTN-SIL-029-2026-REV-0.pdf).

Applicable tools run: `analyze_schematic.py`, `analyze_pcb.py --full`, `cross_analysis.py`, `analyze_emc.py`, `analyze_thermal.py`, `analyze_gerbers.py`, `lifecycle_audit.py`, native KiCad ERC/DRC, independent pin audit and export consistency check. The evidence-linked manual review record `analysis/deep_review.json` passed its gate (3 findings, no quarantined entries).

Not performed / limits:

- No SPICE simulation: no ngspice/LTspice/Xyce executable was installed on PATH. KiCad's shared ngspice library was not used as a standalone simulator; no UC8179 closed-loop model was available. Reference topology and manual calculations are the basis, not simulated control-loop stability.
- No quantified thermal prediction from the analyzer; no measured transient/ripple/current or component temperatures.
- No calibrated EMC/RF test, system enclosure model, USB supply qualification or production fixture validation.
- No manufacturer DC-bias extraction for the selected MLCCs, latest panel-lot approval sheet or physical flex dry-fit.
- No complete active/EOL certification for every passive. No JLC quote/stock reservation or production rotation acceptance.

## Review delta and verdict

This is the first complete review. Exploratory routing with the tool's default fab escalation was rejected; accepted routing disables escalation and keeps native rules. Ground connectivity, signal ordering, reference-text collisions and fiducial placement were corrected and rechecked. The final data is under `hardware/`, `analysis/final/` and `manufacturing/`; exploratory boards under `analysis/routing/` are not fabrication sources.

The digital package is suitable for engineering review and preparation of a prototype build. It is not evidence of a physically working display or a production-qualified design. The next acceptance milestone is the measured bring-up in BRING_UP.md.
