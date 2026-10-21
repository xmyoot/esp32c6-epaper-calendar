# ESP32-C6 e-paper calendar carrier

A 60×50mm, two-layer carrier for a removable XIAO ESP32C6 and a 7.5-inch 800×480 monochrome e-paper panel. USB supplies the product. A small external boost/charge-pump stage follows the panel manufacturer's reference circuit; the controller itself is integrated into the display.

The design deliberately delegates USB, wireless and low-voltage regulation to a documented module. It includes a real bare-panel interface, source damping, safe reset/deselect defaults, accessible bias/current measurements, antenna exclusion and a simple assembly strategy. A clearly labeled offline calendar works without an account; optional Wi-Fi time sync is scheduled before refresh.

Key engineering decisions:

- Replaced an undocumented requested panel with GDEY075T7, preserving size, resolution and product function, and used its own circuit and firmware driver.
- Resolved conflicting panel reference names by physical FPC pin number, preventing accidental joins between NC, VSHR and PREVGH/PREVGL.
- Kept the switching/sense-current loop explicit and protected during routing, then used KiCadRoutingTools for remaining connections with size escalation disabled.
- Verified all 94 declared connections against native exported netlist/PCB data; independently checked critical pin tables against source documents.
- Delivered native editable sources, fabrication/assembly exports, buildable firmware, review evidence and a measured bring-up plan.

Current evidence: clean native ERC/DRC, zero unconnected pads, passing pin audit and a successful ESP32-C6 firmware compile. **No physical prototype has been tested.** Present this as a designed and digitally checked engineering prototype; add actual rail/current measurements, fault tests and display photographs before claiming a working product.

Useful interview discussion: requirements traceability, reference-circuit pin ambiguity, module-vs-discrete tradeoffs, inrush and supply overlap, MLCC DC bias, manufacturing rotation review, RF/backplane clearance and the limits of automated checks.
