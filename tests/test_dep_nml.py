import pytest
from glmpy import nml

def test_nml_bool():
    assert nml.NML.nml_bool(True) == ".true."
    assert nml.NML.nml_bool(False) == ".false."

def test_nml_str():
    python_str = 'temp'
    assert nml.NML.nml_str(python_str) == f"'{python_str}'"

@pytest.mark.parametrize("python_syntax, nml_syntax, syntax_func", [
    ([True], ".true.", nml.NML.nml_bool),
    ([True, False, True], ".true.,.false.,.true.", nml.NML.nml_bool),
    (['temp'], f"'{'temp'}'", nml.NML.nml_str),
    (
        ['temp', 'salt', 'oxy'], 
        f"'{'temp'}','{'salt'}','{'oxy'}'", 
        nml.NML.nml_str
    ),
    ([12.3], "12.3", None),
    ([12.3, 32.4, 64.2], "12.3,32.4,64.2", None)
])

def test_nml_list(python_syntax, nml_syntax, syntax_func):
    assert nml.NML.nml_list(
        python_list=python_syntax,
        syntax_func=syntax_func
    ) == nml_syntax

@pytest.fixture
def example_glmpy_parameters():
    return {
        "param1": True,
        "param2": [True],
        "param3": [True, False, True],
        "param4": 'temp',
        "param5": ['temp'],
        "param6": ['temp', 'salt', 'oxy'],
        "param7": 12.3,
        "param8": [12.3],
        "param9": [12.3, 32.4, 64.2],
        "param10": None
    }

def test_nml_param_val(example_glmpy_parameters):
    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param1",
        syntax_func=nml.NML.nml_bool
    ) == "   param1 = .true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param2",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_bool)
    ) == "   param2 = .true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param3",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_bool)
    ) == "   param3 = .true.,.false.,.true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param4",
        syntax_func=nml.NML.nml_str
    ) == "   param4 = 'temp'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param5",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_str)
    ) == "   param5 = 'temp'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param6",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_str)
    ) == "   param6 = 'temp','salt','oxy'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param7",
        syntax_func=None
    ) == "   param7 = 12.3\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param8",
        syntax_func=nml.NML.nml_list
    ) == "   param8 = 12.3\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param9",
        syntax_func=nml.NML.nml_list
    ) == "   param9 = 12.3,32.4,64.2\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param10",
        syntax_func=None
    ) == ""

@pytest.fixture
def example_glm_setup_parameters():
    return {
        "sim_name": "Example Simulation #1",
        "max_layers": 500,
        "min_layer_thick": 0.15,
        "max_layer_thick": 1.50,
        "min_layer_vol": 0.025,
        "density_model": 1,
        "non_avg": False
    }

@pytest.fixture
def example_mixing_parameters():
    return {
        "surface_mixing": 1,
        "coef_mix_conv": 0.125,
        "coef_wind_stir": 0.23,
        "coef_mix_shear":0.2,
        "coef_mix_turb": 0.51,
        "coef_mix_KH": 0.3,
        "deep_mixing": 2,
        "coef_mix_hyp": 0.5,
        "diff": 0.0
    }

@pytest.fixture
def example_wq_setup_parameters():
    return {
        "wq_lib":"aed2",
        "wq_nml_file": "aed2/aed2.nml",
        "ode_method": 1,
        "split_factor": 1,
        "bioshade_feedback": True,
        "repair_state": True,
        "mobility_off": False
    }

@pytest.fixture
def example_morphometry_parameters():
    return {
        "lake_name":'Example Lake',
        "latitude": 32.0,
        "longitude": 35.0,
        "base_elev": -252.9,
        "crest_elev": -203.9,
        "bsn_len": 21000.0,
        "bsn_wid": 13000.0,
        "bsn_vals": 45,
        "H": [
            -252.9, -251.9, -250.9, -249.9, -248.9, -247.9, -246.9, -245.9, 
            -244.9, -243.9, -242.9, -241.9, -240.9, -239.9, -238.9, -237.9, 
            -236.9, -235.9, -234.9, -233.9, -232.9, -231.9, -230.9, -229.9,  
            -228.9, -227.9, -226.9, -225.9, -224.9, -223.9, -222.9, -221.9,  
            -220.9, -219.9, -218.9, -217.9, -216.9, -215.9, -214.9, -213.9,  
            -212.9, -211.9, -208.9, -207.9, -203.9
        ],
        "A": [
            0, 9250000, 15200000, 17875000, 21975000, 26625000, 31700000, 
            33950000, 38250000, 41100000, 46800000, 51675000, 55725000, 
            60200000, 64675000, 69600000, 74475000, 79850000, 85400000, 
            90975000, 96400000, 102000000, 107000000, 113000000, 118000000, 
            123000000, 128000000, 132000000, 136000000, 139000000, 143000000, 
            146000000, 148000000, 150000000, 151000000, 153000000, 155000000, 
            157000000, 158000000, 160000000, 161000000, 162000000, 167000000, 
            170000000, 173000000
        ]
    }

@pytest.fixture
def example_time_parameters():
    return {
        "timefmt": 3,
        "start": "1997-01-01 00:00:00",
        "stop": "1999-01-01 00:00:00",
        "dt": 3600.0,
        "num_days": 730,
        "timezone": 7.0
    }

@pytest.fixture
def example_output_parameters():
    return {
        'out_dir': 'output',
        'out_fn': 'output',
        'nsave': 6,
        'csv_lake_fname': 'lake',
        'csv_point_nlevs': 2,
        'csv_point_fname': 'WQ_' ,
        "csv_point_frombot": [1], 
        'csv_point_at': [5, 30],    
        'csv_point_nvars': 7,
        'csv_point_vars': [
            'temp', 'salt', 'OXY_oxy', 'SIL_rsi', 
            'NIT_amm', 'NIT_nit', 'PHS_frp'
        ],
        'csv_outlet_allinone': False,
        'csv_outlet_fname': 'outlet_',
        'csv_outlet_nvars': 4,
        'csv_outlet_vars': ['flow', 'temp', 'salt', 'OXY_oxy'],
        'csv_ovrflw_fname': "overflow"
    }

@pytest.fixture
def example_init_profiles_parameters():
    return {
        "lake_depth": 43,
        "num_depths": 3,
        "the_depths": [1, 20, 40],
        "the_temps": [18.0, 18.0, 18.0],
        "the_sals": [ 0.5, 0.5, 0.5],
        "num_wq_vars": 6,
        "wq_names": [
            'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc','OGM_poc'
        ],
        "wq_init_vals": [
            [1.1, 1.2, 1.3, 1.2, 1.3],
            [2.1, 2.2, 2.3, 1.2, 1.3],
            [3.1, 3.2, 3.3, 1.2, 1.3],
            [4.1, 4.2, 4.3, 1.2, 1.3],
            [5.1, 5.2, 5.3, 1.2, 1.3],
            [6.1, 6.2, 6.3, 1.2, 1.3]
        ]
    }

@pytest.fixture
def example_light_parameters():
    return {
        "light_mode": 0,
        "Kw": 0.4,
        "n_bands": 4,
        "light_extc": [1.0, 0.5, 2.0, 4.0],
        "energy_frac": [0.51, 0.45, 0.035, 0.005],
        "Benthic_Imin": 10
    }

@pytest.fixture
def example_bird_model_parameters():
    return {
        "AP": 973,
        "Oz": 0.279,
        "WatVap": 1.1,
        "AOD500": 0.033,
        "AOD380": 0.038,
        "Albedo": 0.2
    }

@pytest.fixture
def example_sediment_parameters():
    return {
        "sed_heat_Ksoil":0.0,
        "sed_temp_depth": 0.2,
        "sed_temp_mean": [5, 10, 20],
        "sed_temp_amplitude": [6, 8, 10],
        "sed_temp_peak_doy": [80, 70, 60],
        "benthic_mode": 1,
        "n_zones": 3,
        "zone_heights": [10.0, 20.0, 50.0],
        "sed_reflectivity": [0.1, 0.01, 0.01],
        "sed_roughness": [0.1, 0.01, 0.01]
    }


@pytest.fixture
def example_snow_ice_parameters():
    return {
        "snow_albedo_factor":1.0,
        "snow_rho_min": 50,
        "snow_rho_max": 300
    }

@pytest.fixture
def example_meteorology_parameters():
    return {
        "met_sw": True,
        "lw_type": "LW_IN",
        "rain_sw": False,
        "atm_stab": 0,
        "fetch_mode": 0,
        "rad_mode": 1,
        "albedo_mode": 1,
        "cloud_mode": 4,
        "subdaily": True,
        "meteo_fl": 'bcs/met_hourly.csv',
        "wind_factor": 0.9,
        "ce": 0.0013,
        "ch": 0.0013,
        "cd": 0.0013,
        "catchrain": True,
        "rain_threshold": 0.001,
        "runoff_coef": 0.0,
    }

@pytest.fixture
def example_inflow_parameters():
    return {
        "num_inflows": 6,
        "names_of_strms": [
            'Inflow1','Inflow2','Inflow3','Inflow4','Inflow5','Inflow6'
            ],
        "subm_flag": [False, False, False, True, False, False],
        "strm_hf_angle": [85.0, 85.0, 85.0, 85.0, 85.0, 85.0],
        "strmbd_slope": [4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
        "strmbd_drag": [0.0160, 0.0160, 0.0160, 0.0160, 0.0160, 0.0160],
        "inflow_factor": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        "inflow_fl": [
            'bcs/inflow_1.csv', 'bcs/inflow_2.csv', 'bcs/inflow_3.csv', 
            'bcs/inflow_4.csv', 'bcs/inflow_5.csv', 'bcs/inflow_6.csv'
        ],
        "inflow_varnum": 3,
        "inflow_vars": ['FLOW', 'TEMP', 'SALT'],
        "coef_inf_entrain": 0.0,
        "time_fmt": 'YYYY-MM-DD hh:mm:ss'
    }

@pytest.fixture
def example_outflow_parameters():
    return {
        "num_outlet": 1,
        "flt_off_sw": False,
        "outlet_type": 1,
        "outl_elvs": -215.5,
        "bsn_len_outl": 18000,
        "bsn_wid_outl": 11000,
        "outflow_fl" : 'bcs/outflow.csv',
        "outflow_factor": 1.0,
        "seepage": True,
        "seepage_rate": 0.01,
    }

def test_write_nml(
        tmp_path,
        example_glm_setup_parameters,
        example_mixing_parameters,
        example_morphometry_parameters,
        example_time_parameters,
        example_output_parameters,
        example_init_profiles_parameters,
        example_meteorology_parameters,
        example_light_parameters,
        example_bird_model_parameters,
        example_inflow_parameters,
        example_outflow_parameters,
        example_sediment_parameters,
        example_snow_ice_parameters,
        example_wq_setup_parameters
):
    glm_setup = nml.NMLGLMSetup()
    morphometry = nml.NMLMorphometry()
    time = nml.NMLTime()
    init_profiles = nml.NMLInitProfiles()
    mixing = nml.NMLMixing()
    output = nml.NMLOutput()
    meteorology = nml.NMLMeteorology()
    light = nml.NMLLight()
    bird_model = nml.NMLBirdModel()
    inflow = nml.NMLInflow()
    outflow = nml.NMLOutflow()
    sediment = nml.NMLSediment()
    snow_ice = nml.NMLSnowIce()
    wq_setup = nml.NMLWQSetup()

    glm_setup.set_attributes(example_glm_setup_parameters)
    morphometry.set_attributes(example_morphometry_parameters)
    time.set_attributes(example_time_parameters)
    init_profiles.set_attributes(example_init_profiles_parameters)
    mixing.set_attributes(example_mixing_parameters)
    output.set_attributes(example_output_parameters)
    meteorology.set_attributes(example_meteorology_parameters)
    light.set_attributes(example_light_parameters)
    bird_model.set_attributes(example_bird_model_parameters)
    inflow.set_attributes(example_inflow_parameters)
    outflow.set_attributes(example_outflow_parameters)
    sediment.set_attributes(example_sediment_parameters)
    snow_ice.set_attributes(example_snow_ice_parameters)
    wq_setup.set_attributes(example_wq_setup_parameters)

    nml_file = nml.NML(
        glm_setup=glm_setup(),
        morphometry=morphometry(),
        time=time(),
        init_profiles=init_profiles(),
        mixing=mixing(),
        output=output(),
        meteorology=meteorology(),
        light=light(),
        bird_model=bird_model(),
        inflow=inflow(),
        outflow=outflow(),
        sediment=sediment(),
        snow_ice=snow_ice(),
        wq_setup=wq_setup()
    )
    file_path = tmp_path / "test.nml"
    nml_file.write_nml(file_path)

    with open(file_path, "r") as file:
        content = file.read()
    
    expected = (
        "&glm_setup\n" +
        "   sim_name = 'Example Simulation #1'\n" +
        "   max_layers = 500\n" +
        "   min_layer_vol = 0.025\n" +
        "   min_layer_thick = 0.15\n" +
        "   max_layer_thick = 1.5\n" +
        "   density_model = 1\n" +
        "   non_avg = .false.\n" +
        "/" + 
        "\n" +
        "&mixing\n" +
        "   surface_mixing = 1\n" +
        "   coef_mix_conv = 0.125\n" +
        "   coef_wind_stir = 0.23\n" +
        "   coef_mix_shear = 0.2\n" +
        "   coef_mix_turb = 0.51\n" +
        "   coef_mix_KH = 0.3\n" +
        "   deep_mixing = 2\n" +
        "   coef_mix_hyp = 0.5\n" +
        "   diff = 0.0\n" +
        "/" +
        "\n" +
        "&morphometry\n" +
        "   lake_name = 'Example Lake'\n" +
        "   latitude = 32.0\n" +
        "   longitude = 35.0\n" +
        "   base_elev = -252.9\n" +
        "   crest_elev = -203.9\n" +
        "   bsn_len = 21000.0\n" +
        "   bsn_wid = 13000.0\n" +
        "   bsn_vals = 45\n" +
        "   H = -252.9,-251.9,-250.9,-249.9,-248.9,-247.9,-246.9,-245.9," +
        "-244.9,-243.9,-242.9,-241.9,-240.9,-239.9,-238.9,-237.9," +
        "-236.9,-235.9,-234.9,-233.9,-232.9,-231.9,-230.9,-229.9," + 
        "-228.9,-227.9,-226.9,-225.9,-224.9,-223.9,-222.9,-221.9," + 
        "-220.9,-219.9,-218.9,-217.9,-216.9,-215.9,-214.9,-213.9," + 
        "-212.9,-211.9,-208.9,-207.9,-203.9\n"
        "   A = 0,9250000,15200000,17875000,21975000,26625000,31700000," +
            "33950000,38250000,41100000,46800000,51675000,55725000," +
            "60200000,64675000,69600000,74475000,79850000,85400000," +
            "90975000,96400000,102000000,107000000,113000000,118000000," +
            "123000000,128000000,132000000,136000000,139000000,143000000," +
            "146000000,148000000,150000000,151000000,153000000,155000000," +
            "157000000,158000000,160000000,161000000,162000000,167000000," +
            "170000000,173000000\n" +
        "/" +
        "\n" +
        "&time\n" +
        "   timefmt = 3\n" +
        "   start = '1997-01-01 00:00:00'\n" +
        "   stop = '1999-01-01 00:00:00'\n" +
        "   dt = 3600.0\n" +
        "   num_days = 730\n" +
        "   timezone = 7.0\n" +
        "/" +
        "\n" +
        "&output\n" +
        "   out_dir = 'output'\n" +
        "   out_fn = 'output'\n" +
        "   nsave = 6\n" +
        "   csv_lake_fname = 'lake'\n" +
        "   csv_point_nlevs = 2\n" +
        "   csv_point_fname = 'WQ_'\n" +
        "   csv_point_frombot = 1\n" +
        "   csv_point_at = 5,30\n" +
        "   csv_point_nvars = 7\n" +
        "   csv_point_vars = 'temp','salt','OXY_oxy','SIL_rsi','NIT_amm'," +
        "'NIT_nit','PHS_frp'\n" +
        "   csv_outlet_allinone = .false.\n" +
        "   csv_outlet_fname = 'outlet_'\n" +
        "   csv_outlet_nvars = 4\n" +
        "   csv_outlet_vars = 'flow','temp','salt','OXY_oxy'\n" +
        "   csv_ovrflw_fname = 'overflow'\n" + 
        "/" + 
        "\n"+
        "&init_profiles\n" +
        "   lake_depth = 43\n" +
        "   num_depths = 3\n" +
        "   the_depths = 1,20,40\n" +
        "   the_temps = 18.0,18.0,18.0\n" +
        "   the_sals = 0.5,0.5,0.5\n" +
        "   num_wq_vars = 6\n" +
        "   wq_names = 'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc'," +
        "'OGM_poc'\n" +
        "   wq_init_vals = 1.1,1.2,1.3,1.2,1.3,\n" +
        "                  2.1,2.2,2.3,1.2,1.3,\n" +
        "                  3.1,3.2,3.3,1.2,1.3,\n" +
        "                  4.1,4.2,4.3,1.2,1.3,\n" +
        "                  5.1,5.2,5.3,1.2,1.3,\n" +
        "                  6.1,6.2,6.3,1.2,1.3\n" +
        "/" +
        "\n" +
        "&meteorology\n" +
        "   met_sw = .true.\n" +
        "   meteo_fl = 'bcs/met_hourly.csv'\n" +
        "   subdaily = .true.\n" +
        "   rad_mode = 1\n" +
        "   albedo_mode = 1\n" +
        "   lw_type = 'LW_IN'\n" +
        "   cloud_mode = 4\n" +
        "   atm_stab = 0\n" +
        "   ce = 0.0013\n" +
        "   ch = 0.0013\n" +
        "   rain_sw = .false.\n" +
        "   catchrain = .true.\n" +
        "   rain_threshold = 0.001\n" +
        "   runoff_coef = 0.0\n" +
        "   cd = 0.0013\n" +
        "   wind_factor = 0.9\n" +
        "   fetch_mode = 0\n" +
        "/" +
        "\n" +
        "&light\n" +
        "   light_mode = 0\n" +
        "   Kw = 0.4\n" +
        "   n_bands = 4\n" +
        "   light_extc = 1.0,0.5,2.0,4.0\n" +
        "   energy_frac = 0.51,0.45,0.035,0.005\n" +
        "   Benthic_Imin = 10\n" +
        "/" +
        "\n" +
        "&bird_model\n" +
        "   AP = 973\n" +
        "   Oz = 0.279\n" +
        "   WatVap = 1.1\n" +
        "   AOD500 = 0.033\n" +
        "   AOD380 = 0.038\n" +
        "   Albedo = 0.2\n" +
        "/" +
        "\n" +
        "&inflow\n" +
        "   num_inflows = 6\n" +
        "   names_of_strms = 'Inflow1','Inflow2','Inflow3','Inflow4',"+
        "'Inflow5','Inflow6'\n" +
        "   subm_flag = .false.,.false.,.false.,.true.,.false.,.false.\n" +
        "   strm_hf_angle = 85.0,85.0,85.0,85.0,85.0,85.0\n" +
        "   strmbd_slope = 4.0,4.0,4.0,4.0,4.0,4.0\n" +
        "   strmbd_drag = 0.016,0.016,0.016,0.016,0.016,0.016\n" +
        "   coef_inf_entrain = 0.0\n" +
        "   inflow_factor = 1.0,1.0,1.0,1.0,1.0,1.0\n" +
        "   inflow_fl = 'bcs/inflow_1.csv','bcs/inflow_2.csv'," +
        "'bcs/inflow_3.csv','bcs/inflow_4.csv','bcs/inflow_5.csv'," + 
        "'bcs/inflow_6.csv'\n" +
        "   inflow_varnum = 3\n" +
        "   inflow_vars = 'FLOW','TEMP','SALT'\n" +
        "   time_fmt = 'YYYY-MM-DD hh:mm:ss'\n" +
        "/" +
        "\n" +
        "&outflow\n" +
        "   num_outlet = 1\n" +
        "   outflow_fl = 'bcs/outflow.csv'\n" +
        "   outflow_factor = 1.0\n" +
        "   flt_off_sw = .false.\n" +
        "   outlet_type = 1\n" +
        "   outl_elvs = -215.5\n" +
        "   bsn_len_outl = 18000\n" +
        "   bsn_wid_outl = 11000\n" +
        "   seepage = .true.\n" +
        "   seepage_rate = 0.01\n" +
        "/" +
        "\n" +
        "&sediment\n" +
        "   sed_heat_Ksoil = 0.0\n" +
        "   sed_temp_depth = 0.2\n" +
        "   sed_temp_mean = 5,10,20\n" +
        "   sed_temp_amplitude = 6,8,10\n" +
        "   sed_temp_peak_doy = 80,70,60\n" +
        "   benthic_mode = 1\n" +
        "   n_zones = 3\n" +
        "   zone_heights = 10.0,20.0,50.0\n" +
        "   sed_reflectivity = 0.1,0.01,0.01\n" +
        "   sed_roughness = 0.1,0.01,0.01\n" +
        "/" +
        "\n" +
        "&snowice\n" +
        "   snow_albedo_factor = 1.0\n" +
        "   snow_rho_min = 50\n" +
        "   snow_rho_max = 300\n" +
        "/" +
        "\n" +
        "&wq_setup\n" +
        "   wq_lib = 'aed2'\n" +
        "   wq_nml_file = 'aed2/aed2.nml'\n" +
        "   bioshade_feedback = .true.\n" +
        "   mobility_off = .false.\n" +
        "   ode_method = 1\n" +
        "   split_factor = 1\n" +
        "   repair_state = .true.\n" +
        "/" +
        "\n" 
    )
    assert content == expected
