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
    ) == f"   param1 = .true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param2",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_bool)
    ) == f"   param2 = .true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param3",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_bool)
    ) == f"   param3 = .true.,.false.,.true.\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param4",
        syntax_func=nml.NML.nml_str
    ) == f"   param4 = 'temp'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param5",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_str)
    ) == f"   param5 = 'temp'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param6",
        syntax_func=lambda x: nml.NML.nml_list(x, nml.NML.nml_str)
    ) == f"   param6 = 'temp','salt','oxy'\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param7",
        syntax_func=None
    ) == f"   param7 = 12.3\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param8",
        syntax_func=nml.NML.nml_list
    ) == f"   param8 = 12.3\n"

    assert nml.NML.nml_param_val(
        param_dict=example_glmpy_parameters,
        param="param9",
        syntax_func=nml.NML.nml_list
    ) == f"   param9 = 12.3,32.4,64.2\n"

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

def test_write_nml_glm_setup(example_glm_setup_parameters):
    glm_setup = nml.NMLGLMSetup()
    glm_setup.set_attributes(example_glm_setup_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    glm_setup_str = my_nml._write_nml_glm_setup(glm_setup())
    expected = (
        "&glm_setup\n" +
        f"   sim_name = 'Example Simulation #1'\n" +
        f"   max_layers = 500\n" +
        f"   min_layer_vol = 0.025\n" +
        f"   min_layer_thick = 0.15\n" +
        f"   max_layer_thick = 1.5\n" +
        f"   density_model = 1\n" +
        f"   non_avg = .false.\n" +
        "/"
    )
    assert glm_setup_str == expected


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

def test_write_nml_mixing(example_mixing_parameters):
    mixing = nml.NMLMixing()
    mixing.set_attributes(example_mixing_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    mixing_str = my_nml._write_nml_mixing(mixing())
    expected = (
        "&mixing\n" +
        f"   surface_mixing = 1\n" +
        f"   coef_mix_conv = 0.125\n" +
        f"   coef_wind_stir = 0.23\n" +
        f"   coef_mix_shear = 0.2\n" +
        f"   coef_mix_turb = 0.51\n" +
        f"   coef_mix_KH = 0.3\n" +
        f"   deep_mixing = 2\n" +
        f"   coef_mix_hyp = 0.5\n" +
        f"   diff = 0.0\n" +
        "/"
    )
    assert mixing_str == expected

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

def test_write_wq_setup(example_wq_setup_parameters):
    wq_setup = nml.NMLWQSetup()
    wq_setup.set_attributes(example_wq_setup_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    wq_setup_str = my_nml._write_nml_wq_setup(wq_setup())
    expected = (
        "&wq_setup\n" +
        f"   wq_lib = 'aed2'\n" +
        f"   wq_nml_file = 'aed2/aed2.nml'\n" +
        f"   bioshade_feedback = .true.\n" +
        f"   mobility_off = .false.\n" +
        f"   ode_method = 1\n" +
        f"   split_factor = 1\n" +
        f"   repair_state = .true.\n" +
        "/"
    )
    assert wq_setup_str == expected

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

def test_write_morphometry(example_morphometry_parameters):
    morphometry = nml.NMLMorphometry()
    morphometry.set_attributes(example_morphometry_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    morphometry_str = my_nml._write_nml_morphometry(morphometry())
    expected = (
        "&morphometry\n" +
        f"   lake_name = 'Example Lake'\n" +
        f"   latitude = 32.0\n" +
        f"   longitude = 35.0\n" +
        f"   base_elev = -252.9\n" +
        f"   crest_elev = -203.9\n" +
        f"   bsn_len = 21000.0\n" +
        f"   bsn_wid = 13000.0\n" +
        f"   bsn_vals = 45\n" +
        f"   H = -252.9,-251.9,-250.9,-249.9,-248.9,-247.9,-246.9,-245.9," +
        "-244.9,-243.9,-242.9,-241.9,-240.9,-239.9,-238.9,-237.9," +
        "-236.9,-235.9,-234.9,-233.9,-232.9,-231.9,-230.9,-229.9," + 
        "-228.9,-227.9,-226.9,-225.9,-224.9,-223.9,-222.9,-221.9," + 
        "-220.9,-219.9,-218.9,-217.9,-216.9,-215.9,-214.9,-213.9," + 
        "-212.9,-211.9,-208.9,-207.9,-203.9\n"
        f"   A = 0,9250000,15200000,17875000,21975000,26625000,31700000," +
            "33950000,38250000,41100000,46800000,51675000,55725000," +
            "60200000,64675000,69600000,74475000,79850000,85400000," +
            "90975000,96400000,102000000,107000000,113000000,118000000," +
            "123000000,128000000,132000000,136000000,139000000,143000000," +
            "146000000,148000000,150000000,151000000,153000000,155000000," +
            "157000000,158000000,160000000,161000000,162000000,167000000," +
            "170000000,173000000\n" +
        "/"
    )
    assert morphometry_str == expected


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

def test_write_time(example_time_parameters):
    time = nml.NMLTime()
    time.set_attributes(example_time_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    time_str = my_nml._write_nml_time(time())
    expected = (
        "&time\n" +
        f"   timefmt = 3\n" +
        f"   start = '1997-01-01 00:00:00'\n" +
        f"   stop = '1999-01-01 00:00:00'\n" +
        f"   dt = 3600.0\n" +
        f"   num_days = 730\n" +
        f"   timezone = 7.0\n" +
        "/"
    )
    assert time_str == expected

@pytest.fixture
def example_output_parameters():
    return {
        'out_dir': 'output',
        'out_fn': 'output',
        'nsave': 6,
        'csv_lake_fname': 'lake',
        'csv_point_nlevs': 2,
        'csv_point_fname': 'WQ_' ,
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

def test_write_output(example_output_parameters):
    output = nml.NMLOutput()
    output.set_attributes(example_output_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    output_str = my_nml._write_nml_output(output())
    expected = (
        "&output\n" +
        f"   out_dir = 'output'\n" +
        f"   out_fn = 'output'\n" +
        f"   nsave = 6\n" +
        f"   csv_lake_fname = 'lake'\n" +
        f"   csv_point_nlevs = 2\n" +
        f"   csv_point_fname = 'WQ_'\n" +
        f"   csv_point_at = 5,30\n" +
        f"   csv_point_nvars = 7\n" +
        f"   csv_point_vars = 'temp','salt','OXY_oxy','SIL_rsi','NIT_amm'," +
        "'NIT_nit','PHS_frp'\n" +
        f"   csv_outlet_allinone = .false.\n" +
        f"   csv_outlet_fname = 'outlet_'\n" +
        f"   csv_outlet_nvars = 4\n" +
        f"   csv_outlet_vars = 'flow','temp','salt','OXY_oxy'\n" +
        f"   csv_ovrflw_fname = 'overflow'\n" + 
        "/"
    )
    assert output_str == expected


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
            1.1, 1.2, 1.3, 1.2, 1.3,
            2.1, 2.2, 2.3, 1.2, 1.3,
            3.1, 3.2, 3.3, 1.2, 1.3,
            4.1, 4.2, 4.3, 1.2, 1.3,
            5.1, 5.2, 5.3, 1.2, 1.3,
            6.1, 6.2, 6.3, 1.2, 1.3
        ]
    }

def test_write_init_profiles(example_init_profiles_parameters):
    init_profiles = nml.NMLInitProfiles()
    init_profiles.set_attributes(example_init_profiles_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    init_profiles_str = my_nml._write_nml_init_profiles(init_profiles())
    expected = (
        "&init_profiles\n" +
        f"   lake_depth = 43\n" +
        f"   num_depths = 3\n" +
        f"   the_depths = 1,20,40\n" +
        f"   the_temps = 18.0,18.0,18.0\n" +
        f"   the_sals = 0.5,0.5,0.5\n" +
        f"   num_wq_vars = 6\n" +
        f"   wq_names = 'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc'," +
        "'OGM_poc'\n" +
        f"   wq_init_vals = 1.1,1.2,1.3,1.2,1.3," +
        "2.1,2.2,2.3,1.2,1.3," +
        "3.1,3.2,3.3,1.2,1.3," +
        "4.1,4.2,4.3,1.2,1.3," +
        "5.1,5.2,5.3,1.2,1.3," +
        "6.1,6.2,6.3,1.2,1.3\n" +
        "/"
    )
    assert init_profiles_str == expected

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

def test_write_light(example_light_parameters):
    light = nml.NMLLight()
    light.set_attributes(example_light_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    light_str = my_nml._write_nml_light(light())
    expected = (
        "&light\n" +
        f"   light_mode = 0\n" +
        f"   Kw = 0.4\n" +
        f"   n_bands = 4\n" +
        f"   light_extc = 1.0,0.5,2.0,4.0\n" +
        f"   energy_frac = 0.51,0.45,0.035,0.005\n" +
        f"   Benthic_Imin = 10\n" +
        "/"
    )
    assert light_str == expected

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

def test_write_bird_model(example_bird_model_parameters):
    bird_model = nml.NMLBirdModel()
    bird_model.set_attributes(example_bird_model_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    bird_model_str = my_nml._write_nml_bird_model(bird_model())
    expected = (
        "&bird_model\n" +
        f"   AP = 973\n" +
        f"   Oz = 0.279\n" +
        f"   WatVap = 1.1\n" +
        f"   AOD500 = 0.033\n" +
        f"   AOD380 = 0.038\n" +
        f"   Albedo = 0.2\n" +
        "/"
    )
    assert bird_model_str == expected

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

def test_write_sediment(example_sediment_parameters):
    sediment = nml.NMLSediment()
    sediment.set_attributes(example_sediment_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    sediment_str = my_nml._write_nml_sediment(sediment())
    expected = (
        "&sediment\n" +
        f"   sed_heat_Ksoil = 0.0\n" +
        f"   sed_temp_depth = 0.2\n" +
        f"   sed_temp_mean = 5,10,20\n" +
        f"   sed_temp_amplitude = 6,8,10\n" +
        f"   sed_temp_peak_doy = 80,70,60\n" +
        f"   benthic_mode = 1\n" +
        f"   n_zones = 3\n" +
        f"   zone_heights = 10.0,20.0,50.0\n" +
        f"   sed_reflectivity = 0.1,0.01,0.01\n" +
        f"   sed_roughness = 0.1,0.01,0.01\n" +
        "/"
    )
    assert sediment_str == expected

@pytest.fixture
def example_snow_ice_parameters():
    return {
        "snow_albedo_factor":1.0,
        "snow_rho_min": 50,
        "snow_rho_max": 300
    }

def test_write_snow_ice(example_snow_ice_parameters):
    snow_ice = nml.NMLSnowIce()
    snow_ice.set_attributes(example_snow_ice_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    snow_ice_str = my_nml._write_nml_snow_ice(snow_ice())
    expected = (
        "&snowice\n" +
        f"   snow_albedo_factor = 1.0\n" +
        f"   snow_rho_min = 50\n" +
        f"   snow_rho_max = 300\n" +
        "/"
    )
    assert snow_ice_str == expected

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

def test_write_meteorology(example_meteorology_parameters):
    meteorology = nml.NMLMeteorology()
    meteorology.set_attributes(example_meteorology_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    meteorology_str = my_nml._write_nml_meteorology(meteorology())
    expected = (
        "&meteorology\n" +
        f"   met_sw = .true.\n" +
        f"   meteo_fl = 'bcs/met_hourly.csv'\n" +
        f"   subdaily = .true.\n" +
        f"   rad_mode = 1\n" +
        f"   albedo_mode = 1\n" +
        f"   lw_type = 'LW_IN'\n" +
        f"   cloud_mode = 4\n" +
        f"   atm_stab = 0\n" +
        f"   ce = 0.0013\n" +
        f"   ch = 0.0013\n" +
        f"   rain_sw = .false.\n" +
        f"   catchrain = .true.\n" +
        f"   rain_threshold = 0.001\n" +
        f"   runoff_coef = 0.0\n" +
        f"   cd = 0.0013\n" +
        f"   wind_factor = 0.9\n" +
        f"   fetch_mode = 0\n" +
        "/"
    )
    assert meteorology_str == expected

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

def test_write_inflow(example_inflow_parameters):
    inflow = nml.NMLInflow()
    inflow.set_attributes(example_inflow_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    inflow_str = my_nml._write_nml_inflow(inflow())
    expected = (
        "&inflow\n" +
        f"   num_inflows = 6\n" +
        f"   names_of_strms = 'Inflow1','Inflow2','Inflow3','Inflow4',"+
        "'Inflow5','Inflow6'\n" +
        f"   subm_flag = .false.,.false.,.false.,.true.,.false.,.false.\n" +
        f"   strm_hf_angle = 85.0,85.0,85.0,85.0,85.0,85.0\n" +
        f"   strmbd_slope = 4.0,4.0,4.0,4.0,4.0,4.0\n" +
        f"   strmbd_drag = 0.016,0.016,0.016,0.016,0.016,0.016\n" +
        f"   coef_inf_entrain = 0.0\n" +
        f"   inflow_factor = 1.0,1.0,1.0,1.0,1.0,1.0\n" +
        f"   inflow_fl = 'bcs/inflow_1.csv','bcs/inflow_2.csv'," +
        "'bcs/inflow_3.csv','bcs/inflow_4.csv','bcs/inflow_5.csv'," + 
        "'bcs/inflow_6.csv'\n" +
        f"   inflow_varnum = 3\n" +
        f"   inflow_vars = 'FLOW','TEMP','SALT'\n" +
        f"   time_fmt = 'YYYY-MM-DD hh:mm:ss'\n" +
        "/"
    )
    assert inflow_str == expected

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


def test_write_outflow(example_outflow_parameters):
    outflow = nml.NMLOutflow()
    outflow.set_attributes(example_outflow_parameters)
    my_nml = nml.NML(
        glm_setup={},
        morphometry={},
        time={},
        init_profiles={}
    )
    outflow_str = my_nml._write_nml_outflow(outflow())
    expected = (
        "&outflow\n" +
        f"   num_outlet = 1\n" +
        f"   outflow_fl = 'bcs/outflow.csv'\n" +
        f"   outflow_factor = 1.0\n" +
        f"   flt_off_sw = .false.\n" +
        f"   outlet_type = 1\n" +
        f"   outl_elvs = -215.5\n" +
        f"   bsn_len_outl = 18000\n" +
        f"   bsn_wid_outl = 11000\n" +
        f"   seepage = .true.\n" +
        f"   seepage_rate = 0.01\n" +
        "/"
    )
    assert outflow_str == expected


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
        wq_setup=wq_setup(),
        check_errors=False
    )
    file_path = tmp_path / "test.nml"
    nml_file.write_nml(file_path)

    with open(file_path, "r") as file:
        content = file.read()
    
    expected = (
        "&glm_setup\n" +
        f"   sim_name = 'Example Simulation #1'\n" +
        f"   max_layers = 500\n" +
        f"   min_layer_vol = 0.025\n" +
        f"   min_layer_thick = 0.15\n" +
        f"   max_layer_thick = 1.5\n" +
        f"   density_model = 1\n" +
        f"   non_avg = .false.\n" +
        "/" + 
        "\n" +
        "&mixing\n" +
        f"   surface_mixing = 1\n" +
        f"   coef_mix_conv = 0.125\n" +
        f"   coef_wind_stir = 0.23\n" +
        f"   coef_mix_shear = 0.2\n" +
        f"   coef_mix_turb = 0.51\n" +
        f"   coef_mix_KH = 0.3\n" +
        f"   deep_mixing = 2\n" +
        f"   coef_mix_hyp = 0.5\n" +
        f"   diff = 0.0\n" +
        "/" +
        "\n" +
        "&wq_setup\n" +
        f"   wq_lib = 'aed2'\n" +
        f"   wq_nml_file = 'aed2/aed2.nml'\n" +
        f"   bioshade_feedback = .true.\n" +
        f"   mobility_off = .false.\n" +
        f"   ode_method = 1\n" +
        f"   split_factor = 1\n" +
        f"   repair_state = .true.\n" +
        "/" +
        "\n" +
        "&morphometry\n" +
        f"   lake_name = 'Example Lake'\n" +
        f"   latitude = 32.0\n" +
        f"   longitude = 35.0\n" +
        f"   base_elev = -252.9\n" +
        f"   crest_elev = -203.9\n" +
        f"   bsn_len = 21000.0\n" +
        f"   bsn_wid = 13000.0\n" +
        f"   bsn_vals = 45\n" +
        f"   H = -252.9,-251.9,-250.9,-249.9,-248.9,-247.9,-246.9,-245.9," +
        "-244.9,-243.9,-242.9,-241.9,-240.9,-239.9,-238.9,-237.9," +
        "-236.9,-235.9,-234.9,-233.9,-232.9,-231.9,-230.9,-229.9," + 
        "-228.9,-227.9,-226.9,-225.9,-224.9,-223.9,-222.9,-221.9," + 
        "-220.9,-219.9,-218.9,-217.9,-216.9,-215.9,-214.9,-213.9," + 
        "-212.9,-211.9,-208.9,-207.9,-203.9\n"
        f"   A = 0,9250000,15200000,17875000,21975000,26625000,31700000," +
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
        f"   timefmt = 3\n" +
        f"   start = '1997-01-01 00:00:00'\n" +
        f"   stop = '1999-01-01 00:00:00'\n" +
        f"   dt = 3600.0\n" +
        f"   num_days = 730\n" +
        f"   timezone = 7.0\n" +
        "/" +
        "\n" +
        "&output\n" +
        f"   out_dir = 'output'\n" +
        f"   out_fn = 'output'\n" +
        f"   nsave = 6\n" +
        f"   csv_lake_fname = 'lake'\n" +
        f"   csv_point_nlevs = 2\n" +
        f"   csv_point_fname = 'WQ_'\n" +
        f"   csv_point_at = 5,30\n" +
        f"   csv_point_nvars = 7\n" +
        f"   csv_point_vars = 'temp','salt','OXY_oxy','SIL_rsi','NIT_amm'," +
        "'NIT_nit','PHS_frp'\n" +
        f"   csv_outlet_allinone = .false.\n" +
        f"   csv_outlet_fname = 'outlet_'\n" +
        f"   csv_outlet_nvars = 4\n" +
        f"   csv_outlet_vars = 'flow','temp','salt','OXY_oxy'\n" +
        f"   csv_ovrflw_fname = 'overflow'\n" + 
        "/" + 
        "\n"
        +
        "&init_profiles\n" +
        f"   lake_depth = 43\n" +
        f"   num_depths = 3\n" +
        f"   the_depths = 1,20,40\n" +
        f"   the_temps = 18.0,18.0,18.0\n" +
        f"   the_sals = 0.5,0.5,0.5\n" +
        f"   num_wq_vars = 6\n" +
        f"   wq_names = 'OGM_don','OGM_pon','OGM_dop','OGM_pop','OGM_doc'," +
        "'OGM_poc'\n" +
        f"   wq_init_vals = 1.1,1.2,1.3,1.2,1.3," +
        "2.1,2.2,2.3,1.2,1.3," +
        "3.1,3.2,3.3,1.2,1.3," +
        "4.1,4.2,4.3,1.2,1.3," +
        "5.1,5.2,5.3,1.2,1.3," +
        "6.1,6.2,6.3,1.2,1.3\n" +
        "/" +
        "\n" +
        "&light\n" +
        f"   light_mode = 0\n" +
        f"   Kw = 0.4\n" +
        f"   n_bands = 4\n" +
        f"   light_extc = 1.0,0.5,2.0,4.0\n" +
        f"   energy_frac = 0.51,0.45,0.035,0.005\n" +
        f"   Benthic_Imin = 10\n" +
        "/" +
        "\n" +
        "&bird_model\n" +
        f"   AP = 973\n" +
        f"   Oz = 0.279\n" +
        f"   WatVap = 1.1\n" +
        f"   AOD500 = 0.033\n" +
        f"   AOD380 = 0.038\n" +
        f"   Albedo = 0.2\n" +
        "/" +
        "\n" +
        "&sediment\n" +
        f"   sed_heat_Ksoil = 0.0\n" +
        f"   sed_temp_depth = 0.2\n" +
        f"   sed_temp_mean = 5,10,20\n" +
        f"   sed_temp_amplitude = 6,8,10\n" +
        f"   sed_temp_peak_doy = 80,70,60\n" +
        f"   benthic_mode = 1\n" +
        f"   n_zones = 3\n" +
        f"   zone_heights = 10.0,20.0,50.0\n" +
        f"   sed_reflectivity = 0.1,0.01,0.01\n" +
        f"   sed_roughness = 0.1,0.01,0.01\n" +
        "/" +
        "\n" +
        "&snowice\n" +
        f"   snow_albedo_factor = 1.0\n" +
        f"   snow_rho_min = 50\n" +
        f"   snow_rho_max = 300\n" +
        "/" +
        "\n" +
        "&meteorology\n" +
        f"   met_sw = .true.\n" +
        f"   meteo_fl = 'bcs/met_hourly.csv'\n" +
        f"   subdaily = .true.\n" +
        f"   rad_mode = 1\n" +
        f"   albedo_mode = 1\n" +
        f"   lw_type = 'LW_IN'\n" +
        f"   cloud_mode = 4\n" +
        f"   atm_stab = 0\n" +
        f"   ce = 0.0013\n" +
        f"   ch = 0.0013\n" +
        f"   rain_sw = .false.\n" +
        f"   catchrain = .true.\n" +
        f"   rain_threshold = 0.001\n" +
        f"   runoff_coef = 0.0\n" +
        f"   cd = 0.0013\n" +
        f"   wind_factor = 0.9\n" +
        f"   fetch_mode = 0\n" +
        "/" +
        "\n" +
        "&inflow\n" +
        f"   num_inflows = 6\n" +
        f"   names_of_strms = 'Inflow1','Inflow2','Inflow3','Inflow4',"+
        "'Inflow5','Inflow6'\n" +
        f"   subm_flag = .false.,.false.,.false.,.true.,.false.,.false.\n" +
        f"   strm_hf_angle = 85.0,85.0,85.0,85.0,85.0,85.0\n" +
        f"   strmbd_slope = 4.0,4.0,4.0,4.0,4.0,4.0\n" +
        f"   strmbd_drag = 0.016,0.016,0.016,0.016,0.016,0.016\n" +
        f"   coef_inf_entrain = 0.0\n" +
        f"   inflow_factor = 1.0,1.0,1.0,1.0,1.0,1.0\n" +
        f"   inflow_fl = 'bcs/inflow_1.csv','bcs/inflow_2.csv'," +
        "'bcs/inflow_3.csv','bcs/inflow_4.csv','bcs/inflow_5.csv'," + 
        "'bcs/inflow_6.csv'\n" +
        f"   inflow_varnum = 3\n" +
        f"   inflow_vars = 'FLOW','TEMP','SALT'\n" +
        f"   time_fmt = 'YYYY-MM-DD hh:mm:ss'\n" +
        "/" +
        "\n" +
        "&outflow\n" +
        f"   num_outlet = 1\n" +
        f"   outflow_fl = 'bcs/outflow.csv'\n" +
        f"   outflow_factor = 1.0\n" +
        f"   flt_off_sw = .false.\n" +
        f"   outlet_type = 1\n" +
        f"   outl_elvs = -215.5\n" +
        f"   bsn_len_outl = 18000\n" +
        f"   bsn_wid_outl = 11000\n" +
        f"   seepage = .true.\n" +
        f"   seepage_rate = 0.01\n" +
        "/" +
        "\n"
    )
    assert content == expected

