# Revision A — kicad-happy re-review

Date: 2026-10-20. Scope: current native schematic, PCB, project rules and fabrication package. Tool: aklofas/kicad-happy at `6a91aaaea124152b2923326c1cf77278e0999cd4` (see ATTRIBUTION.md for repository pin). Review artifacts: `analysis/review-2026-10-20-r2/`. This review does not modify the electrical design or fabrication outputs.

## Verdict and significant findings

**Suitable for a controlled engineering prototype build, subject to connector dry-fit and assembly preflight. No new confirmed connectivity or native design-rule defect found. Physical operation and production readiness remain unproven.**

| ID | Severity / confidence | Finding | Required closure |
|---|---|---|---|
| R2-01 | Warning / medium | GDR switching-gate route is 18.466mm with two vias; RESE contains 15.905mm total branched routing with two vias. These are switching-control/sense connections, not slow DC bias signals. | Measure Q1 gate-to-source waveform and RESE at both controller and shunt during startup/refresh. Check ringing, false turn-on and sense pickup. Shorter same-layer control routing is a candidate improvement if measurements show trouble. |
| R2-02 | Warning / high | Shared 3V3 budget has only 50mA planning margin; transient demand remains unknown. | Measure startup, refresh and accidental radio-overlap current/voltage. Preserve Wi-Fi-off refresh scheduling; follow BRING_UP.md. |
| R2-03 | Warning / high | Selected MLCCs have nominal voltage margin, but effective capacitance at operating DC bias is unestablished. | Obtain exact manufacturer bias curves or characterize startup/ripple on the assembled board before production freeze. |
| R2-04 | Warning / high | Physical panel lot, contact orientation and antenna clearance to its conductive backplate have not been tested. | Unpowered mating dry-fit, panel pin-1 check and assembled RF evaluation. |
| R2-05 | Warning / high | J3 courtyard is 0.10mm from the top board edge; no native copper-edge violation exists. | Confirm latch access and supported panelization/depaneling with the assembler. |

R2-01 is newly emphasized review risk, not a demonstrated failure or a newly introduced layout change. A 1MHz SPI clock does not make GPIO edge rates slow, and SPI scheduling does not determine panel boost-gate edge rates. Do not dismiss GDR/RESE return-path findings on that basis. No additional gate resistor or sense filter is prescribed without checking the panel controller's requirements and actual waveforms.

## Overview, component summary and power tree

USB-powered socketed XIAO ESP32C6 carrier for a GDEY075T7 800×480 monochrome panel with integrated UC8179. The carrier implements the panel reference boost/charge pump. USB, radio, MCU and buck regulator are on the removable module.

40 board features: 12 capacitors, 7 resistors, 3 diodes, 1 MOSFET, 1 inductor, 3 connectors, 6 test pads, 4 mounting holes and 3 fiducials. There are 25 fitted SMT components in 13 assembly groups and two hand-fitted sockets. Schematic analyzer counts 33 nets including 11 intentionally unconnected pin nets; the PCB has 22 connected nets. These different counts do not indicate missing routing.

```text
USB 5V -> XIAO module buck -> J2.3 / 3V3_MODULE
                                -> R1 0R -> 3V3_EPD -> panel VCI/VDDIO
                                                    -> L1/Q1/diodes/charge pump
Panel GDR -> Q1 gate; panel RESE -> Q1 source / R7 sense
Boost/charge pump -> PREVGH / PREVGL -> panel bias circuits
```

No carrier USB data pair, crystal, RF matching network, additional regulator, battery charger, op-amp or mains isolation circuit exists. Their corresponding checks are not applicable to this carrier.

## Fresh checks and verification basis

| Check actually rerun | Result | Evidence / limits |
|---|---|---|
| Native KiCad 10.0.7 ERC | 0 errors, 0 warnings | `erc.rpt`; ignored advisory checks remain printed in report. |
| Native KiCad DRC | 0 violations, 0 unconnected pads, 0 footprint errors | `drc.rpt`; existing ignored categories disclosed there. |
| `analyze_schematic.py` | 4 warnings, 15 information findings | Supply-source and socket-ground warnings triaged below. |
| `analyze_pcb.py --full --proximity` | 1 error, 1 warning, 15 information findings | J3 courtyard edge and limited dedicated test-point coverage. |
| `cross_analysis.py` | 0 findings | Supplemented by native pin/pad audit. |
| `analyze_gerbers.py` | 0 findings | Eight Gerber files, two drill files, 70 holes. |
| `analyze_emc.py` | 4 errors, 15 warnings, 3 information findings | All 22 retained; heuristic score 58 is not a compliance margin. Only five check categories generated results for this design. |
| `analyze_thermal.py` | 0 components assessed | No quantifiable device-power extraction data; no thermal clearance claim. |
| `lifecycle_audit.py --only lcsc` | 14 unique MPNs checked; all unknown | This source does not supply lifecycle status; not evidence that all parts are active. |
| Fresh native netlist and pcbnew export + independent audit | PASS: 37 critical assertions, 94 declared pin checks, 40 footprints | `pin-audit.json`; current data, not previous audit reused. |
| Release consistency check | PASS: 25 SMT placements, 13 groups, 16/16 hashes | `release-hash-check.json` and existing release-check script; no stale exports detected. |
| Deep-review evidence gate | 5 accepted, 0 partial, 0 quarantined | `deep_review.json`, `deep-review-gate.log`. Gate acceptance checks evidence links, not hardware operation. |

The current source hashes are saved in `review-source-hashes.json`. Prior review and manufacturing instructions were read. Fresh independent pin audit uses the original review script with input/output paths redirected by `recheck_native.py`; it does not regenerate the board.

### Raw files, rules and physical pin checks

Native PCB and schematic agree across the complete declared component/pin set. Direct project JSON inspection finds no DRC exclusions. Minimum track/clearance are 0.20mm, copper-to-edge 0.30mm, via diameter/drill 0.60/0.30mm and minimum annular ring 0.15mm. Existing ignored categories include missing courtyard, track endpoint centering, footprint-filter/type and tuning advisories; this review changed no rule or severity. Saved front/back ground fills are present, with analyzer area ratios 0.722/0.875; the unfilled rule area is a keepout, not an unfilled ground pour.

Critical sources were checked against actual source documents, rather than treating symbol/PCB agreement as physical proof:

| Parts | Pin / endpoint review | Evidence basis |
|---|---|---|
| Q1 | 1 gate/GDR, 2 source/RESE, 3 drain/SW; matches top-view package drawing. | Datasheet-manual: Vishay Si1308EDL PDF p1, visually reread; native pin/pad audit. GE3 ordering suffix appears on that page. |
| J3 | Bottom-contact FH12, 24 contacts, 0.5mm pitch; pad 1 rightmost with board USB up. Pads 15/16 3V3, 17 GND, 18 internal VDD bypass only. Pins 1/4/6/7/19 remain unused. | Datasheet-manual: Hirose catalog p4 drawing visually reread; panel reference p40 visually reread; prior panel table pp7–10 and native audit retained. Actual mating still untested. |
| D1–D3 | Pad 1 cathode: D1 PREVGH, D2 GND, D3 PUMP. Anodes SW, PUMP, PREVGL respectively. | JSCJ MBR0530 source PDF pp1–2 reread for cathode marking and ratings; raw pin audit and panel p40 topology. |
| J1/J2 | USB-end pin 1, 15.24mm socket-row spacing, J2.2 GND/J2.3 3V3; GPIO order matches independently transcribed source table. | Fresh native audit; prior official Seeed native module geometry retained as source basis. Physical module/headers not remeasured. |
| L1 | 10µH; two-pin nonpolar, boost input to SW. | Panel p40 reference reread; Bourns ratings carried from prior datasheet review. |
| R1–R7 | All endpoints pass. 0R branch isolation; 33Ω clock/data damping; 100k CS/reset pulls; 1M gate pull; 0.47Ω sense. | Fresh raw-file audit. Pinout verification skipped for nonpolar two-terminal parts. R7 0.5W 7W variant rationale remains in original review. |
| C1–C12 | All endpoints pass; nominal values match the replacement panel reference. Internal VDD has only its required bypass. | Fresh raw-file audit and visually reread panel p40; nonpolar pinout check not meaningful. DC-bias curves unavailable. |
| TP1–TP6 | Probe nets match declared 3V3/GND/PREVGH/PREVGL/BUSY/RESET. | Raw-file audit; not capacitive-touch electrodes. |
| H1–H4 / FID1–3 | Mechanical and optical features, excluded from fitted SMT BOM. | Raw inventory; electrical pinout not applicable. Missing MPN on optical fiducials is expected. |

Complete connector tables and original source-page citations remain in ARCHITECTURE.md and DESIGN_REVIEW.md. In particular, panel p40's misleading pin-4/pin-5 rail aliases must not be used to short those contacts to the positive/negative boost outputs.

## Signal, power and deep review

The reference topology is retained: L1 from 3V3 to SW; Q1 drain SW/source RESE; R7 RESE to GND; positive rectifier SW to PREVGH; flying capacitor SW–PUMP; clamp PUMP to GND; negative rectifier PREVGL to PUMP. Its polarity agrees with the visually inspected panel p40. The short local source/shunt current route and near-source sense branch are beneficial, but they do not guarantee quiet sensing over the return to the panel.

Fresh geometry extraction (`review_geometry.py`) reports SW 9.750mm / no vias, PUMP 9.557mm / no vias, GDR 18.466mm / two vias and RESE 15.905mm / two vias. These are total copper lengths, including branches, not necessarily end-to-end path lengths. R2-to-panel SCK is 28.155mm / no vias; R3-to-panel MOSI is 18.932mm / two vias. Source stubs are 2.540mm SCK and 2.150mm MOSI. No differential-pair or length-matching requirement follows from this interface.

At the illustrative 0.5A switch RMS target, rerun calculations give R7 0.1175W, Q1 conduction 0.04625W and L1 copper 0.045W. These omit diode/switching loss, temperature-dependent resistance and board thermal behavior. Local 3V3 bypass is 15.8µF nominal. Planned 0.50A module + 0.15A carrier against 0.70A leaves 0.05A; these are allocations, not measured worst cases or proof of regulator margin.

50V capacitors versus a nominal 20V bias rail give a 2.5× nominal voltage ratio; 30V Q1/diode ratings have less transient headroom. Check actual overshoot and all diode reverse voltages during boost operation. The panel driver controls conversion; no reliable startup-peak bound is established by average panel consumption. Measure with appropriate differential/short-ground probing, following BRING_UP.md. No new numerical controller current limit is inferred here.

The thermal script assessed zero components. The preceding loss calculation is the available preliminary thermal basis; no junction-temperature or safe-temperature prediction is claimed. No carrier exposed-pad IC requires a thermal-via array. Module regulator and radio heating require assembly-level testing.

## EMC and analyzer dispositions

| Analyzer findings | Disposition and remaining risk |
|---|---|
| GP-001: MOSI_SRC 50%, SCK_SRC 75% opposite-plane coverage | Raw routes are short source-to-resistor stubs at through-hole module sockets. Percentage sampling is not proof of a whole-interface split plane. Retain an edge/return-path measurement item; low SPI repetition rate alone does not close it. |
| IO-001/002: J1/J2 filtering and ground count | These two sockets form one internal module interface with ground on J2; independent external-cable assumptions overstate risk. No arbitrary ferrite/choke addition justified. |
| RS-001: 3V3_MODULE, 3V3_EPD no source | Actual source is on the removable module, represented by passive sockets; R1 bridges display supply. Native connectivity establishes the intended source path. |
| RS-001: VDD_INT no source | Controller internal regulator output, externally bypassed only. Do not tie it to external 3V3. |
| CK-003: SCK near J2/J3 | Source/destination connectors necessarily nearby. Keep source damping and inspect edges. |
| RP-001: missing ground stitching within 1mm of transitions | Preserve as layout risk, especially GDR, RESE and MOSI. Dense escape geometry and low refresh frequency do not prove immunity. Bias output nets have different edge behavior from logic but still need ripple/return evaluation. |
| PM-002: J3 0.1mm from edge | This distance is to the courtyard, not copper; native copper-edge rule passes. Mechanical depaneling/latch risk remains. |
| TE-001: 6/22 nets with dedicated test points | 27% dedicated coverage is limited but reasonable for prototype probing with exposed resistor/capacitor pads. No production test-fixture coverage claim. |

The antenna exclusion is an explicit F.Cu+B.Cu rule area at x112–123mm, y118–133mm, prohibiting tracks/vias/pads/pours/footprints. Presence and restrictions are raw-file verified; module RF performance near the eventual display/enclosure is unmeasured. Do not add stitching inside that area to silence EMC findings. EMC scores and generic geometry rules cannot establish regulatory compliance.

## Manufacturing and lifecycle

Board: 60×50mm, two layers, specified 1.6mm FR4 / 1oz copper. Front fitted SMT, hand-fitted sockets; 52 through vias. Gerbers include both copper, front paste, both masks/silks and outline, with separate plated/non-plated drills. Hole total 70 agrees with 52 vias + 14 socket contacts + 4 mounting holes. Release hashes establish identity with the prior checked native design/exports. BOM and CPL fitted reference sets match. J3 is the main fine-pitch assembly feature; arrange a stencil and supported entry-edge panelization. ENIG is a documented manufacturing recommendation, not a newly confirmed order setting.

Current supplier quote, placement rotations/part matching, feeder availability, panelization and latch handling remain assembler preflight items. No ordering/upload occurred. The freshly executed LCSC-only lifecycle audit reports all 14 statuses unknown by construction. The earlier manufacturer notice resolving BE3 to GE3 remains documented; this rerun does not establish the lifecycle of every selected part or reserve stock.

## Previous review delta

Automated `diff_analysis.py` comparisons against `analysis/final/` show **zero changes** for schematic, PCB and EMC. No native design change was made in this review. Existing warnings remain open; zero automated delta does not close them.

Deep-review delta: three previous records persist (pin consistency information, current-dependent losses warning, shared supply-margin warning). Added one warning R2-01 and one explicit Q1 source-document evidence record. No previous warning was fixed by a hardware change. All five records passed the evidence gate after schema validation; none remain quarantined. The new GDR/RESE concern refines the previous review's broad treatment of slow control/bias transitions.

## Not performed / limits

- SPICE was not run: fresh PATH check found no ngspice, LTspice or Xyce executable. KiCad's shared simulator library was not exercised, and no UC8179 control-loop model was available.
- No thermal model with validated device losses or board thermal resistance; zero analyzer assessments is a coverage gap.
- No physical prototype power-up, gate/sense waveform measurement, rail-ripple/overshoot characterization, RF/EMC test, connector dry-fit or display update test.
- No new exhaustive reread of every passive manufacturer's catalog or exact MLCC DC-bias extraction. Critical diagrams were manually reread; remaining source conclusions are identified above as carried from the prior review.
- No fresh firmware compilation/flash: this hardware re-review checks existing release consistency and retains the previous successful build as historical evidence.
- No manufacturer-wide active/EOL certification, latest panel-lot approval, live assembly quote or supplier reservation.

Proceed to a small prototype after the documented mechanical/assembly checks. Acceptance still requires measured bring-up. For portfolio presentation, describe the result as designed, routed and reviewed until a real panel has passed those tests.
