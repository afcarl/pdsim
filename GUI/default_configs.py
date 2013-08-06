# -*- coding: latin-1 -*-

import yaml

recip_yaml = (
"""
family = recip

[GeometryPanel]
piston_diameter = float,0.02,Piston diameter [m]
piston_length = float,0.02,Piston length [m]
crank_length = float,0.01,Crank length [m]
connecting_rod_length = float,0.04,Connecting rod length [m]
dead_volume_perc = float,4.0,Dead volume percentage [%%]
x_TDC = float,0.005,Distance to piston at TDC [m]
shell_volume = float,100e-6,Shell volume [m�]

[MassFlowPanel]
d_discharge = float,0.0059,Discharge port diameter [m]
d_suction = float,0.0059,Suction port diameter [m]
valve_E = float,1.93e+11,Youngs Modulus [Pa]
valve_d = float,0.007,Valve diameter [m]
valve_h = float,0.0001532,Valve thickness [m]
valve_l = float,0.018,Valve length [m]
valve_a = float,0.014,Valve distance from anchor [m]
valve_x_stopper = float,0.0018,Valve distance to stopper [m]
valve_rho = float,8000.0,Valve metal density [kg/m�]
valve_C_D = float,1.17,Valve drag coefficient [-]

[MechanicalLossesPanel]
eta_motor = float,0.95,Motor efficiency [-]
h_shell = float,0.01,Shell air-side heat transfer coefficient [kW/m�/K]
A_shell = float,0.040536,Shell Area [m�]
Tamb = float,298.0,Ambient temperature [K]
mu_oil = float,0.0086,Oil viscosity [Pa-s]
delta_gap = float,2e-05,Gap width [m]

[StatePanel]
omega = float,377.0,Rotational speed [rad/s]
inletState = State,R404A,283.15,5.75
discharge = Discharge,2.0,Pressure ratio [-]

[ParametricPanel]
Term1 = Term,Rotational speed [rad/s],250.0;300.0

[SolverInputsPanel]
Cycle = Cycle,Euler,7000

[OutputDataPanel]
selected  = selected,['run_index'; 'mdot'; 'eta_v'; 'eta_oi'; 'Td']
"""
)

scroll_yaml=(
"""
family : scroll

GeometryPanel:
  Vdisp : 104.8e-6 # Displacement volume / revolution [m^3/rev]
  Vratio : 2.2 # Built-in volume ratio [-]
  ro : 0.005 # Orbiting radius [m]
  t : 0.004 # Scroll wrap thickness [m]
  use_offset : False
  delta_offset : 1e-3 # Offset scroll portion gap width [m]
  phi_fi0 : 0.0 # Inner wrap initial involute angle [rad]
  phi_fis : 3.141 # Inner wrap starting involute angle [rad]
  phi_fos : 0.3 # Outer wrap starting involute angle [rad]
  delta_flank : 15e-6 # Flank gap width [m]
  delta_radial : 15e-6 # Radial gap width [m]
  d_discharge : 0.01 # Discharge port diameter [m]
  inlet_tube_length : 0.3 # Inlet tube length [m]
  inlet_tube_ID : 0.02 # Inlet tube inner diameter [m]
  outlet_tube_length : 0.3 # Outlet tube length [m]
  outlet_tube_ID : 0.02 # Outlet tube inner diameter [m]
  disc_curves:
      type : 2Arc
      r2 : 0

MassFlowPanel:
  sa-s1:
      model : IsentropicNozzle
      options : {Xd : 0.8}
  sa-s2:
      model : IsentropicNozzle
      options : {Xd : 0.8}
  inlet.2-sa:
      model : IsentropicNozzle
      options : {Xd : 0.8}
  d1-dd:
      model : IsentropicNozzle
      options : {Xd : 0.8}
  d2-dd:
      model : IsentropicNozzle
      options : {Xd : 0.8}      

MechanicalLossesPanel:
  eta_motor : 0.95 # Motor efficiency [-]
  h_shell : 0.01 # Shell air-side heat transfer coefficient [kW/m^2/K]
  A_shell : 0.040536 # Shell Area [m^2]
  Tamb : 298.0 # Ambient temperature [K]
  mu_oil : 0.0086 # Oil viscosity [Pa-s]
  D_upper_bearing : 0.025 # Upper bearing diameter [m]
  L_upper_bearing : 0.025 # Upper bearing length [m]
  c_upper_bearing : 20e-6 # Upper bearing gap [m]
  D_crank_bearing : 0.025 # Crank bearing diameter [m]
  L_crank_bearing : 0.025 # Crank bearing length [m]
  c_crank_bearing : 20e-6 # Crank bearing gap [m]
  D_lower_bearing : 0.025 # Lower bearing diameter [m]
  L_lower_bearing : 0.025 # Lower bearing length [m]
  c_lower_bearing : 20e-6 # Lower bearing gap [m]
  thrust_friction_coefficient : 0.03 # Thrust bearing friction coefficient [-]
  thrust_ID : 0.08 # Thrust bearing inner diameter [m]
  thrust_OD : 0.3 # Thrust bearing outer diameter [m]
  L_ratio_bearings : 3.0 # Ratio of lengths for bearings [-]
  HTC : 0.0 # Heat transfer coefficient in scrolls [-]
  journal_tune_factor : 1.0 # Journal loss tune factor [-]
  scroll_plate_thickness : 0.008

StatePanel:
  omega : 377.0 # Rotational speed [rad/s]
  inletState: 
      Fluid : R410A
      T : 283.15 #[K]
      rho : 5.75 #[kg/m^3]
  discharge:
      pratio : 2.0

ParametricPanel:
  structured : True

SolverInputsPanel:
  cycle_integrator: RK45
  integrator_options: {epsRK45 : 1e-7}
  eps_cycle : 0.001 # Cycle-Cycle convergence tolerance (RSSE) [-]
  
Plugin:ScrollInjectionPlugin:
    - Length : 1.1
      ID : 0.0000001
      inletState: 
          Fluid : R410A
          T : 283.15 #[K]
          rho : 5.75 #[kg/m^3]
      ports:
      - phi : 7.2
        D : 0.0025
        check_valve : True
        inner_outer : 'i'
        symmetric : None
      - phi : 10.1
        D : 0.0025
        check_valve : True
        inner_outer : 'o'
        symmetric : 1

"""
)

def get_defaults(family):
    if family == 'scroll':
        return yaml.load(scroll_yaml)
    elif family == 'recip':
        return yaml.load(recip_yaml)
    else:
        raise ValueError('Your machine family [{f:s}] was not found'.format(f=family))
    