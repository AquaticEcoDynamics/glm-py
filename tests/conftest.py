import json
import pytest

@pytest.fixture
def json_nml_sparkling():
    json_nml_sparkling = {
        "&glm_setup": {
            "sim_name": "Sparkling Lake",
            "max_layers": 500,
            "min_layer_vol": 0.5,
            "min_layer_thick": 0.15,
            "max_layer_thick": 0.5,
            "density_model": 1,
            "non_avg": True,
        },
        "&mixing": {
            "surface_mixing": 1,
            "coef_mix_conv": 0.2,
            "coef_wind_stir": 0.402,
            "coef_mix_shear": 0.2,
            "coef_mix_turb": 0.51,
            "coef_mix_KH": 0.3,
            "deep_mixing": 2,
            "coef_mix_hyp": 0.5,
            "diff": 0.0,
        },
        "&morphometry": {
            "lake_name": "Sparkling",
            "latitude": 46.00881,
            "longitude": -89.69953,
            "crest_elev": 320.0,
            "bsn_len": 901.0385,
            "bsn_wid": 901.0385,
            "bsn_vals": 15,
            "H": [301.712, 303.018285714286, 304.324571428571, 305.630857142857, 306.937142857143, 308.243428571429, 309.549714285714, 310.856, 312.162285714286, 313.468571428571, 314.774857142857, 316.081142857143, 317.387428571429, 318.693714285714, 320, 321],
            "A": [0, 45545.8263571429, 91091.6527142857, 136637.479071429, 182183.305428571, 227729.131785714, 273274.958142857, 318820.7845, 364366.610857143, 409912.437214286, 455458.263571429, 501004.089928571, 546549.916285714, 592095.742642857, 637641.569, 687641.569],
        },
        "&time": {
            "timefmt": 3,
            "start": "1980-04-15",
            "stop": "2012-12-10",
            "dt": 3600,
            "timezone": -6,
            "num_days": 730,
        },
        "&wq_setup": {
            "wq_lib": "aed",
            "wq_nml_file": "aed/aed.nml",
            "ode_method": 1,
            "split_factor": 1,
            "bioshade_feedback": True,
            "repair_state": True,
        },
        "&output": {
            "out_dir": "output",
            "out_fn": "output",
            "nsave": 24,
            "csv_lake_fname": "lake",
            "csv_point_nlevs": 0,
            "csv_point_fname": "WQ_",
            "csv_point_at": [17],
            "csv_point_nvars": 2,
            "csv_point_vars": ["temp", "salt", "OXY_oxy"],
            "csv_outlet_allinone": False,
            "csv_outlet_fname": "outlet_",
            "csv_outlet_nvars": 3,
            "csv_outlet_vars": ["flow", "temp", "salt", "OXY_oxy"],
            "csv_ovrflw_fname": "overflow",
        },
        "&init_profiles": {
            "lake_depth": 18.288,
            "num_depths": 3,
            "the_depths": [0, 0.2, 18.288],
            "the_temps": [3, 4, 4],
            "the_sals": [0, 0, 0],
            "num_wq_vars": 6,
            "wq_names": ["OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc"],
            "wq_init_vals": [1.1, 1.2, 1.3, 1.2, 1.3, 2.1, 2.2, 2.3, 1.2, 1.3, 3.1, 3.2, 3.3, 1.2, 1.3, 4.1, 4.2, 4.3, 1.2, 1.3, 5.1, 5.2, 5.3, 1.2, 1.3, 6.1, 6.2, 6.3, 1.2, 1.3],
        },
        "&meteorology": {
            "met_sw": True,
            "lw_type": "LW_IN",
            "rain_sw": False,
            "atm_stab": 0,
            "catchrain": False,
            "rad_mode": 1,
            "albedo_mode": 1,
            "cloud_mode": 4,
            "fetch_mode": 0,
            "subdaily": False,
            "meteo_fl": "bcs/nldas_driver.csv",
            "wind_factor": 1,
            "sw_factor": 1.08,
            "lw_factor": 1,
            "at_factor": 1,
            "rh_factor": 1,
            "rain_factor": 1,
            "ce": 0.00132,
            "ch": 0.0014,
            "cd": 0.0013,
            "rain_threshold": 0.01,
            "runoff_coef": 0.3,
        },
        "&bird_model": {
            "AP": 973,
            "Oz": 0.279,
            "WatVap": 1.1,
            "AOD500": 0.033,
            "AOD380": 0.038,
            "Albedo": 0.2,
        },
        "&light": {
            "light_mode": 0,
            "n_bands": 4,
            "light_extc": [1.0, 0.5, 2.0, 4.0],
            "energy_frac": [0.51, 0.45, 0.035, 0.005],
            "Benthic_Imin": 10,
            "Kw": 0.331,
        },
        "&inflows": {
            "num_inflows": 0,
            "names_of_strms": ["Riv1", "Riv2"],
            "subm_flag": [False],
            "strm_hf_angle": [65, 65],
            "strmbd_slope": [2, 2],
            "strmbd_drag": [0.016, 0.016],
            "inflow_factor": [1, 1],
            "inflow_fl": ["bcs/inflow_1.csv", "bcs/inflow_2.csv"],
            "inflow_varnum": 4,
            "inflow_vars": ["FLOW", "TEMP", "SALT", "OXY_oxy", "SIL_rsi", "NIT_amm", "NIT_nit", "PHS_frp", "OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc", "PHY_green", "PHY_crypto", "PHY_diatom"],
        },
        "&outflows": {
            "num_outlet": 0,
            "flt_off_sw": [False],
            "outl_elvs": [1],
            "bsn_len_outl": [5],
            "bsn_wid_outl": [5],
            "outflow_fl": "bcs/outflow.csv",
            "outflow_factor": [0.8],
            "crest_width": 100,
            "crest_factor": 0.61,
        },
        "&sediment": {
            "sed_heat_Ksoil": 2.0,
            "sed_temp_depth": 0.2,
            "sed_temp_mean": [4.5, 5, 6],
            "sed_temp_amplitude": [1, 1, 1],
            "sed_temp_peak_doy": [242, 242, 242],
            "benthic_mode": 2,
            "n_zones": 3,
            "zone_heights": [10.0, 20.0, 30.0],
            "sed_reflectivity": [0.1, 0.01, 0.01],
            "sed_roughness": [0.1, 0.01, 0.01],
        }
    }
    return json_nml_sparkling


@pytest.fixture
def ellenbrook_nml(tmp_path):
    nml = '''!-------------------------------------------------------------------------------
! general model setup
!-------------------------------------------------------------------------------
!
! sim_name         [string]  title of simulation
! max_layers       [integer] maximum number of layers
! min_layer_vol    [real]    minimum layer volume (m3 * 1000)
! min_layer_thick  [real]    minimum layer thickness (m)
! max_layer_thick  [real]    maximum layer thickness (m)
! Kw               [real]    background light attenuation (m**-1)
! coef_mix_conv    [real]    mixing efficiency - convective overturn
! coef_wind_stir   [real]    mixing efficiency - wind stirring
! coef_mix_turb    [real]    mixing efficiency - unsteady turbulence effects
! coef_mix_shear   [real]    mixing efficiency - shear production
! coef_mix_KH      [real]    mixing efficiency - hypolimnetic Kelvin-Helmholtz turbulent billows
! coef_mix_hyp     [real]    mixing efficiency - hypolimnetic turbulence
! deep_mixing      [bool]    flag to disable deep-mixing
!-------------------------------------------------------------------------------
&glm_setup
   sim_name = 'GLM Simulation'
   max_layers = 60
   min_layer_vol = 0.0005
   min_layer_thick = 0.05
   max_layer_thick = 0.1
   non_avg = .true.
   !  mobility_off = .true.
/

&mixing
   !-- Mixing Parameters
   coef_mix_conv = 0.125
   coef_wind_stir = 0.23
   coef_mix_shear = 0.00
   coef_mix_turb = 0.51
   coef_mix_KH = 0.30
   coef_mix_hyp = 0.5
  deep_mixing = 0
  surface_mixing = 1
/
&light
!-- Light Parameters
light_mode = 0
Kw = 3.5
/

!-------------------------------------------------------------------------------
! water quality setup
! if this block is read, water quality functionality will be enabled
!-------------------------------------------------------------------------------
! wq_lib            [string]
!                     selection of the WQ model library to engage - 'fabm' or 'aed2'
! ode_method        [integer]
!                     ODE numerical scheme for source and sink dynamics
!                     1: first-order explicit (not positive)
!                     2: second-order explicit Runge-Kutta (not positive)
!                     3: fourth-order explicit Runge-Kutta (not positive)
!                     4: Patankar (first-order, not conservative)
!                     5: Patankar-RK (second-order, not conservative)
!                     6: Patankar-RK (does not work, not conservative)
!                     7: Modified Patankar (1st-order, conservat., posit.)
!                     8: Modified Patankar-RK (2nd-order, conservat., posit.)
!                     9: Modified Patankar-RK (does not work, conservat.,
!                       posit.)
!                     10: Extended Modified Patankar (1st-order, conservat.,
!                       posit.)
!                     11: Extended Modified Patankar-RK (2nd-order, conservat.,
!                       posit.)
!                     This variable is used only if bio_calc = True
! split_factor      [integer, minimum = 1]
!                     number of biogeochemical time steps per physical time step
! bioshade_feedback [bool]
!                     feedback of bio-turbidity to temperature equation
! repair_state      [bool]
!                     option to repair state variables that have -ve's
! wq_nml_file       [string]
!                     name of .nml file to be passed to wq_lib
! mobility_off      [bool]
!                     flag to turn off settling/rising
! multi_ben         [bool]
!                     GLM specific option for FABM to do benthic fluxes only
!                     in bottom layer, or on flanks of all layers (.true.)
!-------------------------------------------------------------------------------

!-------------------------------------------------------------------------------
! lake details
!-------------------------------------------------------------------------------
!
! name             [string]
!                    name of the lake
! latitude         [float, minimum = -90, maximum = 90, unit = deg North]
!                    latitude
! longitude        [float, minimum = -360, maximum = 360, unit = deg East]
!                    longitude
! base_elev        [float]
!                    base elevation (m)
! crest_elev       [float]
!                    crest elevation (m)
! bsn_len          [float]
!                    basin length at crest (m)
! bsn_wid          [float]
!                    basin width at crest (m)
! bsn_vals         [integer]
!                    number of depth points on height-area relationship
! H                [float]
!                    elevations (m)   (comma separated list, len=bsn_vals)
! A                [float]
!                    area (m2 * 1000) (comma separated list, len=bsn_vals)
!
!-------------------------------------------------------------------------------
&morphometry
   lake_name  = 'EBNR'
   latitude   = -32
   longitude  = 35
   crest_elev = 16.45000
   bsn_len    = 761.4900
   bsn_wid    = 1015.9130
   bsn_vals   = 11
 A = 100,3600,5600,9200,11200,15600,25600,46800,64800,86400,108400,130800,154800,182800,211600,245200,273200,303200,320000,336800,345200
 H = 16.0000,16.1000,16.2000,16.3000,16.4000,16.5000,16.6000,16.7000,16.8000,16.9000,17.0000,17.1000,17.2000,17.3000,17.4000,17.5000,17.6000,17.7000,17.8000,17.9000,18.0000
/

!-------------------------------------------------------------------------------
! duration of run
!-------------------------------------------------------------------------------
!
! timefmt [integer]
!           method to specify start and duration of model run
!           1: duration computed from number of time steps, MaxN (bogus start
!             date used) [no longer implemented!!]
!           2: duration computed from given start and stop dates (number of time
!             steps MaxN computed)
!           3: duration computed from number of time steps, MaxN (start date as
!             specified, stop date computed)
! start   [string, format = "yyyy-mm-dd hh:mm:ss"]
!           nominal start date
!           This variable is used only if timefmt != 1
! stop    [string, format = "yyyy-mm-dd hh:mm:ss"]
!           nominal stop date
!           This variable is used only if timefmt = 2
! dt        [float, minimum = 0.001, maximum = 86400, unit = s]
!               Time step for integration
! numb_days [number of days to run the simulation ]
!           This variable is used only if timefmt != 2
!
!-------------------------------------------------------------------------------
&time
   timefmt  = 2
   start    = '2007-01-01 00:00:00'
   stop     = '2009-01-01 00:00:00'
   dt       = 3600.0
   num_days = 730
   timezone = 8.0
/

!-------------------------------------------------------------------------------
! format for output and filename(s)
!-------------------------------------------------------------------------------
!
! out_dir           [string]
!                     path to output directory (set permissions)
! out_fn            [string]
!                     name of output netcdf file
! nsave             [integer, minimum = 1, maximum = 86400]
!                     save results every 'nsave' timesteps
! csv_lake_fname    [string]
!                     name of lake.csv lake simulation daily summary information
! csv_point_nlevs   [integer]
!                     number of depths at which to dump a csv time-series file
! csv_point_at      [real]
!                     height from bottom for point csv file(s) (comma separated list)
! csv_point_fname   [string]
!                     name of csv output file(s) (comma separated list)
! csv_point_nvars   [integer]
!                     number of variables to output into csv
! csv_point_vars    [string]
!                     list of names of variables to output, - order IS important
! csv_outlet_allinone [bool]
!                     put all outflow data into the same csv file
! csv_outlet_fname  [string]
!                     name of csv output file(s) (comma separated list)
! csv_outlet_nvars  [integer]
!                     number of variables to output into outlet csv
! csv_outlet_vars   [string]
!                     list of names of variables to output
! csv_ovrflw_fname  [string]
!                     name of csv file to record amount and quality of overflow
!
!-------------------------------------------------------------------------------
&output
   out_dir = 'output'
   out_fn = 'output'
   nsave = 1
   ! General summary file
   csv_lake_fname = 'lake'
   ! Depth specific outputs
   csv_point_nlevs = 1
   csv_point_fname = 'WQ_'
   csv_point_at = 0.1
   csv_point_nvars = 2
   csv_point_vars = 'temp',
                    'salt'
   ! Combined outlet file & overflow
   csv_outlet_allinone = .false.
   csv_outlet_fname = 'outlet_'
   csv_outlet_nvars = 3
   csv_outlet_vars = 'flow',
                     'temp',
                     'salt'
   csv_ovrflw_fname = "overflow"
/

!-------------------------------------------------------------------------------
! initial condition profiles
!-------------------------------------------------------------------------------
!
!   lake_depth     [float]   initial lake depth (m)
!   num_depths     [integer] number of depths provided for initial profiles
!   the_depths     [float]   the depths of the initial profile points (m)
!   the_temps      [float]   the temperature of the initial profile points (C)
!   the_sals       [float]   the salinity of the initial profile points (psu)
!   num_wq_vars    [integer] number of non GLM (ie FABM) vars to be initialised
!   wq_names       [string]  names of non GLM (ie FABM) vars to be initialised
!   wq_init_vals   [float]   array of FABM vars (rows = vars; cols = depths)
!
!-------------------------------------------------------------------------------
&init_profiles
    lake_depth  = 0.15 !m
    num_depths  = 2
    the_depths  = 0.01,0.1
    ! GLM
    the_temps   = 18.00,10.00     
    the_sals    = 0.5, 1.5
    bar = 1, 2, 3
    ! WQ
    num_wq_vars = 1
    wq_names =     'OGM_don',
                   'OGM_pon',
                   'OGM_dop',
                   'OGM_pop',
                   'OGM_doc',
                   'OGM_poc'
    wq_init_vals =  1.1, 1.2, 1.3, 1.2, 1.3,  
                    2.1, 2.2, 2.3, 1.2, 1.3,   
                    3.1, 3.2, 3.3, 1.2, 1.3,  
                    4.1, 4.2, 4.3, 1.2, 1.3,
                    5.1, 5.2, 5.3, 1.2, 1.3,
                    6.1, 6.2, 6.3, 1.2, 1.3  
    foo = 'foo'
/

!-------------------------------------------------------------------------------
! meteorology
!-------------------------------------------------------------------------------
!
!   met_sw         [bool]   switch to include surface meteorological forcing
!   lw_type        [string] type of longwave data supplied (LW_IN/LW_CC/LW_NET)
!   rain_sw        [bool]   include rainfall nutrient composition
!   atm_stab       [bool]   account for non-neutral atmospheric stability
!   catchrain      [bool]   flag that enables runoff from exposed banks of lake area
!   rad_mode       [integer] short and long wave radation model configuration (see manual)
!   albedo_mode    [integer] shortwave albedo calculation method
!   cloud_mode     [integer] atmospheric emmisivity calculation method
!
!   subdaily       [bool]   .true. if met data is provided at the model (sub-daily) time-step
!   meteo_fl       [string] name of file with meteorology input data
!   wind_factor    [float]  wind multiplication factor (-)
!   rain_factor    [float]  wind multiplication factor (-)
!   sw_factor      [float]  wind multiplication factor (-)
!   lw_factor      [float]  wind multiplication factor (-)
!   at_factor      [float]  wind multiplication factor (-)
!   rh_factor      [float]  wind multiplication factor (-)
!
!   ce             [float]  bulk aerodynamic coefficient for latent heat transfer
!   ch             [float]  bulk aerodynamic coefficient for sensible heat transfer
!   cd             [float]  bulk aerodynamic coefficient for transfer of momentum
!   rain_threshold [float]  rainfall amount (m) required before runoff from exposed banks
!   runoff_coef    [float]  conversion of rainfall to runoff in exposed lake banks
!
!-------------------------------------------------------------------------------
&meteorology
   met_sw      = .true.
   lw_type     = 'LW_IN'
   rain_sw     = .false.
   atm_stab    = 0
   catchrain   = .true.
   rad_mode    = 2
   albedo_mode = 2
   cloud_mode  = 4
   fetch_mode  = 0
   !-- BC file details
   subdaily    = .true.
   meteo_fl    = 'bcs/met_hourly.csv'
   wind_factor = 0.5
   sw_factor = 0.9
   lw_factor = 1.0
   at_factor = 1.0
   rh_factor = 1.0
   rain_factor = 1.0
   !-- Parameters
   ce          = 0.0013
   ch          = 0.0013
   cd          = 0.0013
   rain_threshold = 0.025
   runoff_coef    = 0.080
/


!-------------------------------------------------------------------------------
! bird_model
!-------------------------------------------------------------------------------
!
!   AP = 973           Atmospheric Pressure in milibars
!   Oz = 0.279         Ozone concentration in atm-cm
!   WatVap = 1.1       Total Precipitable water vapor in atm-cm
!   AOD500 = 0.033     Dimensionless Aerosol Optical Depth at wavelength 500 nm
!   AOD380 = 0.038     Dimensionless Aerosol Optical Depth at wavelength 380 nm
!   Albedo = 0.2       Default Albedo value
!
!-------------------------------------------------------------------------------
&bird_model
  AP = 973
  Oz = 0.279
  WatVap = 1.1
  AOD500 = 0.033
  AOD380 = 0.038
  Albedo = 0.2
/


!-------------------------------------------------------------------------------
! inflows
!-------------------------------------------------------------------------------
!
!  num_inflows       [integer]   number of inflowing streams (0+)
!  subm_flag         [bool]      flag is true if inflow is submerged (non-plunging)
!  names_of_strms    [string]    names of streams (comma separated list)
!  strm_hf_angle     [float]     stream half angle (degrees)
!  strmbd_slope      [float]     streambed slope (degrees)
!  strmbd_drag       [float]     streambed drag coefficient (-)
!  inflow_factor     [float]     inflow flow rate multiplier (-)
!  inflow_fl         [string]    inflow data filename(s) (comma separated list)
!  inflow_varnum     [integer]   number of columns (excluding date) to be read
!  inflow_vars       [string]    variable names of inflow file columns
!                                This should be a comma separated list, and must
!                                include FLOW, SALT & TEMP (for GLM), and
!                                optionally can include FABM var names.
! coef_inf_entrain   [real]      entrainment coefficient for inflows
!
!-------------------------------------------------------------------------------
&inflow
   num_inflows    = 0
   names_of_strms = 'Riv1','Riv2'
   subm_flag      = .false.,.false.
   strm_hf_angle  = 65.0,   65.0
   strmbd_slope   = 2.0,    2.0
   strmbd_drag    = 0.0160, 0.0160
   inflow_factor  = 1.0,    1.0
   inflow_fl      = 'inflow_1.csv', 'inflow_2.csv'
   inflow_varnum  = 4
   inflow_vars    =   'FLOW',
                      'TEMP',
                      'SALT',
                      'OXY_oxy',
                      'SIL_rsi',
                      'NIT_amm',
                      'NIT_nit',
                      'PHS_frp',
                      'OGM_don',
                      'OGM_pon',
                      'OGM_dop',
                      'OGM_pop',
                      'OGM_doc',
                      'OGM_poc',
                      'PHY_green',
                      'PHY_crypto',
                      'PHY_diatom'
   coef_inf_entrain = 0.
!  time_fmt = 'YYYY-MM-DD hh:mm:ss'
/

!-------------------------------------------------------------------------------
! outflows
!-------------------------------------------------------------------------------
!
!  num_outlet      [integer]  no. of outlets
!  flt_off_sw      [bool]     floating offtake switches
!  outl_elvs       [float]    outlet elevations (comma separated list)
!  bsn_len_outl    [float]    basin length at outlets (m)
!  bsn_wid_outl    [float]    basin width at outlets (m)
!  outflow_fl      [string]   outflow data file
!  outflow_factor  [float]    outflow flow rate multiplier (-)
!  seepage         [bool]     do seepage processing [default is off - ie no seepage]
!  seepage_rate    [float]    seepage rate of water (m/day) from bottom layer
!
!-------------------------------------------------------------------------------
&outflow
   num_outlet   = 0
   flt_off_sw   = .false.
  !outlet_type  = 1, 1, 1, 1, 1, 1, 1
   outl_elvs    = 0.1
   bsn_len_outl = 100
   bsn_wid_outl = 100
   outflow_fl   = 'outflow.csv'
   outflow_factor = 0.8
   seepage  = .true.
   seepage_rate   = 0.011
   crest_width = 3
   crest_factor = 0.62
/
!-------------------------------------------------------------------------------
&snowice
   snow_albedo_factor = 1.0
   snow_rho_max       = 300
   snow_rho_min       = 50
/
!-------------------------------------------------------------------------------
&debugging
disable_evap = .false.
/

&sediment
  sed_heat_Ksoil = 2.0
  sed_temp_depth = 0.2
  sed_temp_mean = 15,17,20
  sed_temp_amplitude = 6,8,10
  sed_temp_peak_doy = 80, 70, 60
  benthic_mode = 2
  n_zones = 3
  zone_heights = 0.35, 0.6, 1.0
  sed_reflectivity = 0.1, 0.01, 0.01
  sed_roughness = 0.1, 0.01, 0.01
/
'''
    nml_file = tmp_path / "glm3_nml.nml"
    nml_file.write_text(nml)
    return nml_file

@pytest.fixture
def ellenbrook_json(tmp_path):
    ellenbrook_dict = {
        "glm_setup": {
            "sim_name": "GLM Simulation",
            "max_layers": 60,
            "min_layer_vol": 0.0005,
            "min_layer_thick": 0.05,
            "max_layer_thick": 0.1,
            "non_avg": True
        },
        "mixing": {
            "coef_mix_conv": 0.125,
            "coef_wind_stir": 0.23,
            "coef_mix_shear": 0.0,
            "coef_mix_turb": 0.51,
            "coef_mix_KH": 0.3,
            "coef_mix_hyp": 0.5,
            "deep_mixing": 0,
            "surface_mixing": 1
        },
        "light": {
            "light_mode": 0,
            "Kw": 3.5
        },
        "morphometry": {
            "lake_name": "EBNR",
            "latitude": -32.0,
            "longitude": 35.0,
            "crest_elev": 16.45,
            "bsn_len": 761.49,
            "bsn_wid": 1015.913,
            "bsn_vals": 11.0,
        "A": [
            100.0, 3600.0, 5600.0, 9200.0, 11200.0, 15600.0, 25600.0, 46800.0,
            64800.0, 86400.0, 108400.0, 130800.0, 154800.0, 182800.0, 211600.0, 
            245200.0, 273200.0, 303200.0, 320000.0, 336800.0, 345200.0
            ],
        "H": [ 
            16.0, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 16.8, 16.9, 17.0, 
            17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8, 17.9, 18.0
            ]
        },
        "time": {
            "timefmt": 2,
            "start": "2007-01-01 00:00:00",
            "stop": "2009-01-01 00:00:00",
            "dt": 3600.0,
            "num_days": 730,
            "timezone": 8.0
        },
        "output": {
            "out_dir": "output",
            "out_fn": "output",
            "nsave": 1,
            "csv_lake_fname": "lake",
            "csv_point_nlevs": 1.0,
            "csv_point_fname": "WQ_",
            "csv_point_at": [0.1],
            "csv_point_nvars": 2,
            "csv_outlet_allinone": False,
            "csv_outlet_fname": "outlet_",
            "csv_outlet_nvars": 3,
            "csv_ovrflw_fname": "overflow",
            "csv_point_vars": ["temp", "salt"],
            "csv_outlet_vars": ["flow", "temp", "salt"]
        },
        "init_profiles": {
            "lake_depth": 0.15,
            "num_depths": 2,
            "the_depths": [0.01, 0.1],
        "the_temps": [18.0, 10.0],
        "the_sals": [0.5, 1.5],
        "bar": [1, 2, 3],
        "num_wq_vars": 1,
        "foo": "foo",
        "wq_names": [
            "OGM_don", "OGM_pon", "OGM_dop", "OGM_pop", "OGM_doc", "OGM_poc"
            ],
        "wq_init_vals": [
            [1.1, 1.2, 1.3, 1.2, 1.3],
            [2.1, 2.2, 2.3, 1.2, 1.3], 
            [3.1, 3.2, 3.3, 1.2, 1.3], 
            [4.1, 4.2, 4.3, 1.2, 1.3],
            [5.1, 5.2, 5.3, 1.2, 1.3],
            [6.1, 6.2, 6.3, 1.2, 1.3]
            ]
        },
        "meteorology": {
            "met_sw": True,
            "lw_type": "LW_IN",
            "rain_sw": False,
            "atm_stab": 0,
            "catchrain": True,
            "rad_mode": 2,
            "albedo_mode": 2,
            "cloud_mode": 4,
            "fetch_mode": 0,
            "subdaily": True,
            "meteo_fl": "bcs/met_hourly.csv",
            "wind_factor": 0.5,
            "sw_factor": 0.9,
            "lw_factor": 1.0,
            "at_factor": 1.0,
            "rh_factor": 1.0,
            "rain_factor": 1.0,
            "ce": 0.0013,
            "ch": 0.0013,
            "cd": 0.0013,
            "rain_threshold": 0.025,
            "runoff_coef": 0.08
        },
        "bird_model": {
            "AP": 973.0,
            "Oz": 0.279,
            "WatVap": 1.1,
            "AOD500": 0.033,
            "AOD380": 0.038,
            "Albedo": 0.2
        },
        "inflow": {
            "num_inflows": 0,
            "names_of_strms": ["Riv1", "Riv2"],
            "subm_flag": [False, False],
            "strm_hf_angle": [65.0, 65.0],
            "strmbd_slope": [2.0, 2.0],
            "strmbd_drag": [0.016, 0.016],
            "inflow_factor": [1.0, 1.0],
            "inflow_fl": ["inflow_1.csv", "inflow_2.csv"],
            "inflow_varnum": 4,
            "coef_inf_entrain": [0.0],
            "inflow_vars": [
                "FLOW", "TEMP", "SALT", "OXY_oxy", "SIL_rsi", "NIT_amm", 
                "NIT_nit",  "PHS_frp", "OGM_don", "OGM_pon", "OGM_dop", 
                "OGM_pop", "OGM_doc", "OGM_poc", "PHY_green", "PHY_crypto", 
                "PHY_diatom"
                ]
        },
        "outflow": {
            "num_outlet": 0,
            "flt_off_sw": [False],
            "outl_elvs": [0.1],
            "bsn_len_outl": [100.0],
            "bsn_wid_outl": [100.0],
            "outflow_fl": ["outflow.csv"],
            "outflow_factor": [0.8],
            "seepage": True,
            "seepage_rate": 0.011,
            "crest_width": 3.0,
            "crest_factor": 0.62
        },
        "snowice": {
            "snow_albedo_factor": 1.0,
            "snow_rho_max": 300.0,
            "snow_rho_min": 50.0
        },
        "debugging": {
            "disable_evap": False
        },
        "sediment": {
            "sed_heat_Ksoil": 2.0,
            "sed_temp_depth": 0.2,
            "sed_temp_mean": [15.0, 17.0, 20.0],
            "sed_temp_amplitude": [6.0, 8.0, 10.0],
            "sed_temp_peak_doy": [80, 70, 60],
            "benthic_mode": 2,
            "n_zones": 3,
            "zone_heights": [0.35, 0.6, 1.0],
            "sed_reflectivity": [0.1, 0.01, 0.01],
            "sed_roughness": [0.1, 0.01, 0.01 ]
        }
    }
    json_file = tmp_path / "glm3_nml.json"
    with open(json_file, 'w') as file:
        json.dump(ellenbrook_dict, file)
    return json_file
