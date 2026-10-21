# Revision A assembly and bring-up

This is a designed and digitally checked prototype. No physical board, display refresh, supply-current measurement or EMC test has been performed.

## Assembly

1. Assemble the top SMT BOM. Inspect Q1 pin 1 and D1–D3 cathode bars against the assembly drawing. Inspect the 0.5mm FPC contacts for bridges.
2. Hand solder J1 and J2, two Samtec SSW-107-01-G-S female sockets. Maintain 15.24mm row spacing and use the removable XIAO with matching 2.54mm male strips as an unpowered alignment fixture. Remove it before cleaning or rework. J1 and J2 pin 1 are both at the USB end; their numbering is deliberately independent of the module's DIP numbering.
3. With USB facing the top board edge: J1 left top-to-bottom = D0,D1,D2,D3,D4,D5,D6. J2 right top-to-bottom = 5V,GND,3V3,D10,D9,D8,D7. The carrier does not connect 5V.
4. J3 accepts a **0.3mm-thick, 24-contact, 0.5mm-pitch flex with exposed contacts facing the carrier PCB**. With USB up, J3 pin 1 is the rightmost signal contact at approximately x=149.75,y=106.85mm in native coordinates. Match the panel's marked pin 1; do not infer it from the screen's front appearance. Open the latch, insert fully and squarely, then close. Dry-fit the exact panel lot before committing an enclosure. Never insert or remove the flex with power applied.
5. Use the GDEY075T7 bare panel only; a random 24-pin panel is not interchangeable. Mount the panel independently so its flex carries no mechanical load. The four carrier mounting holes are 2.7mm NPTH for M2.5 screws/standoffs.
6. Keep the XIAO antenna end (opposite USB) outside the display's conductive backplane shadow and away from metal hardware. The enforced carrier keepout spans x=112–123mm,y=118–133mm on both copper layers. A useful arrangement places the carrier below the display edge with the flex entering from above; do not sandwich its antenna against the panel backplate.

## Unpowered inspection

- Verify BOM, solder joints, connector orientation and no shorts between adjacent FPC pins.
- Verify continuity against `analysis/pin-audit.json`. Pin 18 is an internal regulator output, not a 3V3 input; pins 4 and 5 must not be connected to PREVGL/PREVGH just because the reference drawing reuses names.
- Remove R1 and check that the two 3V3 branches are isolated. Check resistance from each branch to GND, accounting for capacitor charging. Bias outputs must not be shorted to GND. Use a DMM, not a high-voltage insulation tester.
- Initial optional carrier-only test: panel and XIAO absent, R1 removed, 3.3V current-limited to 20mA at TP1 with GND at TP2. No boost should operate because the gate pull-down holds Q1 off. Remove that supply before continuing. Refit R1 for normal USB operation.

## First powered test

Use a regulated USB-C 5V supply rated at least 1A. Connect the panel only while all power is off. Program the XIAO with `firmware/EPDCalendar`; no firmware has been uploaded as part of this project.

Begin with the offline demo. For initial testing set `RUN_PANEL_TESTS=true`, then return it to false. The sketch uses the exact GDEY075T7 driver at 1MHz, full refresh, a paged buffer and hibernate after each frame. Wi-Fi credentials are optional; a fixed-date frame is visibly marked OFFLINE DEMO. Wi-Fi is turned off before refresh.

| Measurement | Expected / initial acceptance target |
|---|---|
| TP1 to TP2 | 3.3V nominal; inspect transients. Aim ±5%; investigate any trough below 3.0V or MCU reset. |
| TP3 PREVGH | About +20V while active, from the pinned driver initialization. |
| TP4 PREVGL | About −20V while active. |
| VSH1 / VSL | About +15V / −15V while active, measured at C7/C8. |
| VSHR | About +4.2V while active, at C4. |
| VCOM | Controller/OTP-dependent; record the actual panel lot's setting. Do not set it by guesswork. |
| TP5 BUSY | Low during controller work; high when idle. |
| TP6 RESET | Low during safe start, then driven reset sequence. |
| R7 voltage | Current = V(R7)/0.47Ω. Measure peak and RMS; initial design targets ≤1A peak and ≤0.5A RMS during boost activity. |
| Q1 drain-source | Nominal roughly the positive boost rail; inspect switching overshoot with a short ground connection. Investigate peaks above 25V before approaching the 30V absolute maximum. |

The voltage values come from GxEPD2 1.6.9's `gdey/GxEPD2_750_GDEY075T7.cpp`, which programs VGH/VGL = ±20V, VDH/VDL = ±15V and VDHR = 4.2V. They are expected active values, not measured results or guaranteed panel tolerances. Stop and investigate rail magnitudes beyond approximately 24V, sustained over-current, heating, or unstable supply behavior. Hibernate discharges/powers down rails; do not expect active bias levels after completion.

Measure the carrier branch separately across the removable R1 link; do not compare whole-module Wi-Fi current with the carrier's 150mA allocation. Use a short scope ground/spring for switching measurements. Do not attach a grounded scope clip to a negative bias rail. Observe capacitance/ripple/startup before accepting substitutions.

## Functional and fault tests to record

- White, black, checkerboard, text and calendar frames; all 800×480 pixels correctly addressed.
- Display retains its last image after USB removal.
- Offline mode is labeled as a demo; a real NTP date appears only after successful synchronization.
- USB reset/removal/reconnection; startup with the panel attached; recovery from a brief brownout.
- Lost Wi-Fi and a deliberate BUSY-low fault: at 8s the sketch holds reset low and retries once; a second failure latches reset through NVS. Clear `epd-c6` NVS only after correcting the fault.
- Worst-case refresh with radio overlap, despite the normal scheduling separation; record 3V3 troughs, branch peak/average current, all bias rails and component temperatures.
- Compare SPI edges with/without the fitted 33Ω resistors only if measurements justify a change.

Record hardware revisions/lot IDs, firmware hash, instrument setup, screenshots and results. A successful compile and ERC/DRC pass do not demonstrate a working display. Add those measurements before presenting this as a tested product.
