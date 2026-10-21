"""Illustrative stress calculations, not measured or controller-limit results."""
import json
r={'assumptions':{'carrier_allocation_A':.15,'radio_module_allocation_A':.5,'conservative_shared_budget_A':.7,'switch_rms_target_A':.5,'switch_peak_target_A':1,'switch_rds_at_2V5_ohm':.185,'inductor_dcr_max_ohm':.18,'shunt_ohm':.47,'shunt_rating_W':.5},'shared_budget_margin_A':.7-.5-.15,'shunt_loss_at_RMS_target_W':.5**2*.47,'MOSFET_conduction_only_W':.5**2*.185,'inductor_copper_loss_W':.5**2*.18,'VDS_rating_to_nominal_rail_ratio':30/20,'capacitor_rating_to_max_nominal_rail_ratio':50/20,'shunt_voltage_at_peak_target_V':1*.47,'local_3V3_nominal_uF':4.7+10+1+.1}
print(json.dumps(r,indent=2))
