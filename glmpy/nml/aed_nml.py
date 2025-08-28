from typing import Union, List
from glmpy.nml.nml import NML_REGISTER, NMLParam, NMLBlock, NML


@NML_REGISTER.register_block()
class ModelsBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_models"

    def __init__(
        self,
        models: Union[List[str], None] = None,
    ):
        """ """
        super().__init__()
        self.init_params(NMLParam("models", str, models, is_list=True))
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class TracerBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_tracer"

    def __init__(
        self,
        retention_time: Union[bool, None] = None,
        num_tracers: Union[int, None] = None,
        decay: Union[List[float], None] = None,
        fsed: Union[List[float], None] = None,
    ):
        """ """
        super().__init__()
        self.init_params(
            NMLParam("retention_time", bool, retention_time),
            NMLParam("num_tracers", int, num_tracers),
            NMLParam("decay", float, decay, is_list=True, units="day^{-1}"),
            NMLParam(
                "fsed", float, fsed, is_list=True, units="g (m^{2}*s)^{-1}"
            )
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class NonCohesiveBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_noncohesive"

    def __init__(
        self,
        num_ss: Union[int, None] = None,
        ss_initial: Union[List[int], None] = None,
        ke_ss: Union[List[float], None] = None,
        settling: Union[int, None] = None,
        w_ss: Union[List[float], None] = None,
        d_ss: Union[List[float], None] = None,
        rho_ss: Union[List[float], None] = None,
        resuspension: Union[int, None] = None,
        epsilon: Union[float, None] = None,
        tau_0: Union[List[float], None] = None,
        tau_r: Union[float, None] = None,
        ktau_0: Union[float, None] = None,
        macrophyte_link_var: Union[str, None] = None,
        simsedimentmass: Union[bool, None] = None,
        fs: Union[List[float], None] = None,
        sed_porosity: Union[float, None] = None,
    ):
        """ """
        super().__init__()
        self.init_params(
            NMLParam("num_ss", int, num_ss),
            NMLParam("ss_initial", int, ss_initial, is_list=True),
            NMLParam("ke_ss", float, ke_ss, is_list=True),
            NMLParam("settling", int, settling),
            NMLParam("w_ss", float, w_ss, is_list=True),
            NMLParam("d_ss", float, d_ss, is_list=True),
            NMLParam("rho_ss", float, rho_ss, is_list=True),
            NMLParam("resuspension", int, resuspension),
            NMLParam("epsilon", float, epsilon),
            NMLParam("tau_0", float, tau_0, is_list=True),
            NMLParam("tau_r", float, tau_r),
            NMLParam("ktau_0", float, ktau_0),
            NMLParam("macrophyte_link_var", float, macrophyte_link_var),
            NMLParam("simsedimentmass", bool, simsedimentmass),
            NMLParam("fs", float, fs, is_list=True),
            NMLParam("sed_porosity", float, sed_porosity, is_list=True),
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class OxygenBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_oxygen"

    def __init__(
        self,
        oxy_initial: Union[float, None] = None,
        fsed_oxy: Union[float, None] = None,
        ksed_oxy: Union[float, None] = None,
        theta_sed_oxy: Union[float, None] = None,
        fsed_oxy_variable: Union[str, None] = None,
        oxy_min: Union[float, None] = None,
        oxy_max: Union[float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("oxy_initial", float, oxy_initial, units="mmol m^{-3}"),
            NMLParam(
                "fsed_oxy", float, fsed_oxy, units="mmol m^{-2} day^{-1}"
            ),
            NMLParam("ksed_oxy", float, ksed_oxy, units="mmol m^{-3}"),
            NMLParam("theta_sed_oxy", float, theta_sed_oxy),
            NMLParam("fsed_oxy_variable", str, fsed_oxy_variable),
            NMLParam("oxy_min", float, oxy_min, units="mmol m^{-3}"),
            NMLParam("oxy_max", float, oxy_max, units="mmol m^{-3}"),
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class SedFluxBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_sedflux"

    def __init__(self, sedflux_model: Union[str, None] = None):
        super().__init__()
        self.init_params(
            NMLParam(
                "sedflux_model",
                str,
                sedflux_model,
                val_switch=["Constant", "Constant2d", "Dynamic", "Dynamic2d"],
            )
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class SedConst2DBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_sed_const2d"

    def __init__(
        self,
        n_zones: Union[int, None] = None,
        active_zones: Union[List[int], None] = None,
        fsed_oxy: Union[List[float], None] = None,
        fsed_ch4: Union[List[float], None] = None,
        fsed_amm: Union[List[float], None] = None,
        fsed_nit: Union[List[float], None] = None,
        fsed_frp: Union[List[float], None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("n_zones", int, n_zones),
            NMLParam("active_zones", int, active_zones, is_list=True),
            NMLParam("fsed_oxy", float, fsed_oxy, is_list=True),
            NMLParam("fsed_ch4", float, fsed_ch4, is_list=True),
            NMLParam("fsed_amm", float, fsed_amm, is_list=True),
            NMLParam("fsed_nit", float, fsed_nit, is_list=True),
            NMLParam("fsed_frp", float, fsed_frp, is_list=True),
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("n_zones", "active_zones")
        self.val_list_len_params("n_zones", "fsed_oxy")
        self.val_list_len_params("n_zones", "fsed_ch4")
        self.val_list_len_params("n_zones", "fsed_amm")
        self.val_list_len_params("n_zones", "fsed_nit")
        self.val_list_len_params("n_zones", "fsed_frp")


@NML_REGISTER.register_block()
class CarbonBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_carbon"
    
    def __init__(
        self,
        dic_initial: Union[float, None] = None,
        ph_initial: Union[float, None] = None,
        ch4_initial: Union[float, None] = None,
        co2_model: Union[int, None] = None,
        alk_mode: Union[int, None] = None,
        ionic: Union[float, None] = None,
        atm_co2: Union[float, None] = None,
        atm_ch4: Union[float, None] = None,
        co2_piston_model: Union[int, None] = None,
        ch4_piston_model: Union[int, None] = None,
        rch4ox: Union[float, None] = None,
        kch4ox: Union[float, None] = None,
        vtch4ox: Union[float, None] = None,
        methane_reactant_variable: Union[str, None] = None,
        fsed_dic: Union[float, None] = None,
        ksed_dic: Union[float, None] = None,
        theta_sed_dic: Union[float, None] = None,
        fsed_dic_variable: Union[str, None] = None,
        fsed_ch4: Union[float, None] = None,
        ksed_ch4: Union[float, None] = None,
        theta_sed_ch4: Union[float, None] = None,
        fsed_ch4_variable: Union[str, None] = None,
        ebb_model: Union[int, None] = None,
        fsed_ebb_variable: Union[str, None] = None,
        fsed_ch4_ebb: Union[float, None] = None,
        ch4_bub_all: Union[float, None] = None,
        ch4_bub_cll: Union[float, None] = None,
        ch4_bub_kll: Union[float, None] = None,
        ch4_bub_disf1: Union[float, None] = None,
        ch4_bub_disf2: Union[float, None] = None,
        ch4_bub_disdp: Union[float, None] = None,
    ):
        """
        Parameters
        ----------
        dic_initial : Union[float, None]
            Initial DIC cooncentrations.
        ph_initial : Union[float, None]
            Initial pH values.
        ch4_initial : Union[float, None] 
            Initial CH4 values.
        co2_model : Union[int, None]
            Selection of pCO2 model algorithms. `0` for aed_geochem,
            `1` for CO2SYS, and `2` for Butler.
        alk_mode : Union[int, None]
            Selection of total alkalinity model algorithms.
        ionic : Union[float, None] 
            Average ionic strength of the water column.
        atm_co2 : Union[float, None] 
            Atmospheric CO2 concentration.
        atm_ch4 : Union[float, None] 
            Atmospheric CH4 concentration.
        co2_piston_model : Union[int, None]
            Selection of air-water Co2 flux velocity method.
        ch4_piston_model : Union[int, None]
            Selection of air-water CH4 flux velocity method.
        rch4ox : Union[float, None] 
            Maximum reaction rate of CH4 oxidation at 20C.
        kch4ox : Union[float, None] 
            Half-saturation oxygen concentration for CH4 oxidation.
        vtch4ox : Union[float, None] 
            Arrhenius temperature multiplier for CH4 oxidation.
        methane_reactant_variable : Union[str, None]
            State variable to be consumed during CH4 oxidation.
        fsed_dic : Union[float, None]
            Sediment CO2 flux.
        ksed_dic : Union[float, None]
            Half-saturation oxygen concentration controlling CO2 flux.
        theta_sed_dic : Union[float, None]
            Arrhenius temperature multiplier for sediment CO2 flux.
        fsed_dic_variable : Union[str, None]
            Variable name to link to for spatially resolved sediment 
            zones.
        fsed_ch4 : Union[float, None] 
            Sediment CH4 flux.
        ksed_ch4 : Union[float, None] 
            Half-saturation oxygen concentration controlling CH4 flux.
        theta_sed_ch4 : Union[float, None]
            Arrhenius temperature multiplier for sediment CH4 flux.
        fsed_ch4_variable : Union[str, None]
            Variable name to link to for spatially resolved sediment 
            zone.
        ebb_model : Union[int, None]
            Option to activate CH4 ebullition. `0` for no ebullition, 
            `1` for simple release model.
        fsed_ebb_variable : Union[str, None]
            Variable name to link to for spatially resolved sediment 
            zones.
        fsed_ch4_ebb : Union[float, None]
            Undocumented parameter.
        ch4_bub_all : Union[float, None] 
            Mean water depth.
        ch4_bub_cll : Union[float, None] 
            Normalising constant.
        ch4_bub_kll : Union[float, None] 
            Exponential factor from the depth-ebullition regression 
            relation.
        ch4_bub_disf1 : Union[float, None] 
            Bubble dissolution fraction (surface).
        ch4_bub_disf1 : Union[float, None] 
            Bubble dissolution fraction (deep).
        ch4_bub_disdp : Union[float, None] 
            Bubble dissolution fraction depth interface.
        """
        super().__init__()
        self.init_params(
            NMLParam("dic_initial", float, dic_initial, units="mmol m^{-3}"),
            NMLParam("ph_initial", float, ph_initial),
            NMLParam(
                "ch4_initial", float, ch4_initial, units="mmol m^{-3}"
            ),
            NMLParam("co2_model", int, co2_model, val_switch=[0, 1, 2]),
            NMLParam(
                "alk_mode", int, alk_mode, val_switch=[0, 1, 2, 3, 4, 5]
            ),
            NMLParam("ionic", float, ionic, units="meq"),
            NMLParam("atm_co2", float, atm_co2, units="atm"),
            NMLParam("atm_ch4", float, atm_ch4, units="atm"),
            NMLParam(
                "co2_piston_model",
                int,
                co2_piston_model,
                val_switch=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,]
            ),
            NMLParam(
                "ch4_piston_model",
                int,
                ch4_piston_model,
                val_switch=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,]
            ),
            NMLParam("rch4ox", float, rch4ox),
            NMLParam("kch4ox", float, kch4ox, units="mmol m^{-3}"),
            NMLParam("vtch4ox", float, vtch4ox),
            NMLParam(
                "methane_reactant_variable", str, methane_reactant_variable
            ),
            NMLParam(
                "fsed_dic", float, fsed_dic, units="mmol m^{-2} day^{-1}"
            ),
            NMLParam(
                "ksed_dic", float, ksed_dic, units="mmol m^{-3}"
            ),
            NMLParam("theta_sed_dic", float, theta_sed_dic),
            NMLParam("fsed_dic_variable", str, fsed_dic_variable),
            NMLParam(
                "fsed_ch4", float, fsed_ch4, units="mmol m^{-2} day^{-1}"
            ),
            NMLParam("ksed_ch4", float, ksed_ch4, units="mmol m^{-3}"),
            NMLParam("theta_sed_ch4", float, theta_sed_ch4),
            NMLParam("fsed_ch4_variable", str, fsed_ch4_variable),
            NMLParam("ebb_model", int, ebb_model, val_switch=[0, 1]),
            NMLParam("fsed_ebb_variable", str, fsed_ebb_variable),
            NMLParam("fsed_ch4_ebb", float, fsed_ch4_ebb),
            NMLParam("ch4_bub_all", float, ch4_bub_all, units="m"),
            NMLParam("ch4_bub_cll", float, ch4_bub_cll),
            NMLParam("ch4_bub_kll", float, ch4_bub_kll),
            NMLParam("ch4_bub_disf1", float, ch4_bub_disf1),
            NMLParam("ch4_bub_disf2", float, ch4_bub_disf2),
            NMLParam("ch4_bub_disdp", float, ch4_bub_disdp, units="m"),
        )
    
    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class SilicaBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_silica"

    def __init__(
        self,
        rsi_initial: Union[float, None] = None,
        rsi_min: Union[float, None] = None,
        rsi_max: Union[float, None] = None,
        fsed_rsi: Union[float, None] = None,
        ksed_rsi: Union[float, None] = None,
        theta_sed_rsi: Union[float, None] = None,
        fsed_rsi_variable: Union[str, None] = None,
        silica_reactant_variable: Union[str, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam(
                "rsi_initial", float, rsi_initial, units="mmol Si m^{-3}"
            ),
            NMLParam("rsi_min", float, rsi_min, units="mmol Si m^{-3}"),
            NMLParam("rsi_max", float, rsi_max, units="mmol Si m^{-3}"),
            NMLParam(
                "fsed_rsi", float, fsed_rsi, units="mmol Si m^{-2} d^{-1}"
            ),
            NMLParam("ksed_rsi", float, ksed_rsi, units="mmol Si m^{-3}"),
            NMLParam(
                "theta_sed_rsi", float, theta_sed_rsi, units="mmol Si m^{-3}"
            ),
            NMLParam("fsed_rsi_variable", str, fsed_rsi_variable),
            NMLParam(
                "silica_reactant_variable", str, silica_reactant_variable
            ),
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class NitrogenBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_nitrogen"

    def __init__(
        self,
        amm_initial: Union[float, None] = None,
        nit_initial: Union[float, None] = None,
        n2o_initial: Union[float, None] = None,
        no2_initial: Union[float, None] = None,
        rnitrif: Union[float, None] = None,
        knitrif: Union[float, None] = None,
        theta_nitrif: Union[float, None] = None,
        nitrif_reactant_variable: Union[str, None] = None,
        nitrif_ph_variable: Union[str, None] = None,
        simnitrfph: Union[bool, None] = None,
        rnh4o2: Union[float, None] = None,
        rno2o2: Union[float, None] = None,
        simn2o: Union[int, None] = None,
        rn2o: Union[float, None] = None,
        kpart_ammox: Union[float, None] = None,
        kin_deamm: Union[float, None] = None,
        atm_n2o: Union[float, None] = None,
        n2o_piston_model: Union[int, None] = None,
        rnh4no2: Union[float, None] = None,
        kanammox: Union[float, None] = None,
        kanmx_nit: Union[float, None] = None,
        kanmx_amm: Union[float, None] = None,
        rdenit: Union[float, None] = None,
        kdenit: Union[float, None] = None,
        theta_denit: Union[float, None] = None,
        rdnra: Union[float, None] = None,
        kdnra_oxy: Union[float, None] = None,
        simdrydeposition: Union[bool, None] = None,
        atm_din_dd: Union[float, None] = None,
        simwetdeposition: Union[bool, None] = None,
        atm_din_conc: Union[float, None] = None,
        ksed_amm: Union[float, None] = None,
        ksed_nit: Union[float, None] = None,
        fsed_n2o: Union[float, None] = None,
        ksed_n2o: Union[float, None] = None,
        theta_sed_amm: Union[float, None] = None,
        theta_sed_nit: Union[float, None] = None,
        fsed_amm: Union[float, None] = None,
        fsed_nit: Union[float, None] = None,
        fsed_amm_variable: Union[str, None] = None,
        fsed_nit_variable: Union[str, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("amm_initial", float, amm_initial),
            NMLParam("nit_initial", float, nit_initial),
            NMLParam("n2o_initial", float, n2o_initial),
            NMLParam("no2_initial", float, no2_initial),
            NMLParam("rnitrif", float, rnitrif, units="day^{-1}"),
            NMLParam("knitrif", float, knitrif),
            NMLParam("theta_nitrif", float, theta_nitrif),
            NMLParam(
                "nitrif_reactant_variable", str, nitrif_reactant_variable
            ),
            NMLParam("nitrif_ph_variable", str, nitrif_ph_variable),
            NMLParam("simnitrfph", bool, simnitrfph),
            NMLParam("rnh4o2", float, rnh4o2, units="mmol^{-1} m^{3} s^{-1}"),
            NMLParam("rno2o2", float, rno2o2, units="mmol^{-1} m^{3} s^{-1}"),
            NMLParam("simn2o", int, simn2o),
            NMLParam("rn2o", float, rn2o, units="s^{-1}"),
            NMLParam("kpart_ammox", float, kpart_ammox, units="mmol m^{-3}"),
            NMLParam("kin_deamm", float, kin_deamm, units="mmol m^{-3}"),
            NMLParam("atm_n2o", float, atm_n2o, units="mmol m^{-3}"),
            NMLParam("n2o_piston_model", int, n2o_piston_model),
            NMLParam(
                "rnh4no2", float, rnh4no2, units="mmol^{-1} m^{3} s^{-1}"
            ),
            NMLParam("kanammox", float, kanammox),
            NMLParam("kanmx_nit", float, kanmx_nit),
            NMLParam("kanmx_amm", float, kanmx_amm),
            NMLParam("rdenit", float, rdenit),
            NMLParam("kdenit", float, kdenit, units="mmol m^{-3}"),
            NMLParam("theta_denit", float, theta_denit),
            NMLParam("rdnra", float, rdnra),
            NMLParam("kdnra_oxy", float, kdnra_oxy),
            NMLParam("simdrydeposition", bool, simdrydeposition),
            NMLParam(
                "atm_din_dd", float, atm_din_dd, units="mmol m^{-2} d^{-1}"
            ),
            NMLParam("simwetdeposition", bool, simwetdeposition),
            NMLParam("atm_din_conc", float, atm_din_conc, units="mmol m^{-3}"),
            NMLParam("ksed_amm", float, ksed_amm, units="mmol m^{-2} d^{-1}"),
            NMLParam("ksed_nit", float, ksed_nit, units="mmol m^{-2} d^{-1}"),
            NMLParam("fsed_n2o", float, fsed_n2o, units="mmol m^{-2} y^{-1}"),
            NMLParam("ksed_n2o", float, ksed_n2o, units="mmol m^{-2} y^{-1}"),
            NMLParam("theta_sed_amm", float, theta_sed_amm),
            NMLParam("theta_sed_nit", float, theta_sed_nit),
            NMLParam("fsed_amm", float, fsed_amm),
            NMLParam("fsed_nit", float, fsed_nit),
            NMLParam("fsed_amm_variable", str, fsed_amm_variable),
            NMLParam("fsed_nit_variable", str, fsed_nit_variable),
        )

        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class PhosphorusBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_phosphorus"

    def __init__(
        self,
        frp_initial: Union[float, None] = None,
        frp_min: Union[float, None] = None,
        frp_max: Union[float, None] = None,
        fsed_frp: Union[float, None] = None,
        ksed_frp: Union[float, None] = None,
        theta_sed_frp: Union[float, None] = None,
        phosphorus_reactant_variable: Union[str, None] = None,
        fsed_frp_variable: Union[str, None] = None,
        simpo4adsorption: Union[bool, None] = None,
        ads_use_external_tss: Union[bool, None] = None,
        po4sorption_target_variable: Union[str, None] = None,
        po4adsorptionmodel: Union[int, None] = None,
        kpo4p: Union[float, None] = None,
        kadsratio: Union[float, None] = None,
        qmax: Union[float, None] = None,
        w_po4ads: Union[float, None] = None,
        ads_use_ph: Union[bool, None] = None,
        ph_variable: Union[str, None] = None,
        simdrydeposition: Union[bool, None] = None,
        atm_pip_dd: Union[float, None] = None,
        simwetdeposition: Union[bool, None] = None,
        atm_frp_conc: Union[float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("frp_initial", float, frp_initial, units="mmol P m^{-3}"),
            NMLParam("frp_min", float, frp_min, units="mmol P m^{-3}"),
            NMLParam("frp_max", float, frp_max, units="mmol P m^{-3}"),
            NMLParam(
                "fsed_frp", float, fsed_frp, units="mmol P m^{-3} d^{-1}"
            ),
            NMLParam("ksed_frp", float, ksed_frp, units="mmol O_{2} m^{-3}"),
            NMLParam("theta_sed_frp", float, theta_sed_frp),
            NMLParam(
                "phosphorus_reactant_variable",
                str,
                phosphorus_reactant_variable,
            ),
            NMLParam("fsed_frp_variable", str, fsed_frp_variable),
            NMLParam("simpo4adsorption", bool, simpo4adsorption),
            NMLParam("ads_use_external_tss", bool, ads_use_external_tss),
            NMLParam(
                "po4sorption_target_variable", str, po4sorption_target_variable
            ),
            NMLParam("po4adsorptionmodel", int, po4adsorptionmodel),
            NMLParam("kpo4p", float, kpo4p, units="m^{3} g^{-1}"),
            NMLParam("kadsratio", float, kadsratio, units="l mg^{-1}"),
            NMLParam("qmax", float, qmax, units="mg mgSS^{-1}"),
            NMLParam("w_po4ads", float, w_po4ads, units="m d^{-1}"),
            NMLParam("ads_use_ph", bool, ads_use_ph),
            NMLParam("ph_variable", str, ph_variable),
            NMLParam("simdrydeposition", bool, simdrydeposition),
            NMLParam(
                "atm_pip_dd", float, atm_pip_dd, units="mmol P m^{-2} d^{-1}"
            ),
            NMLParam("simwetdeposition", bool, simwetdeposition),
            NMLParam(
                "atm_frp_conc", float, atm_frp_conc, units="mmol P m^{-3}"
            ),
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class OrganicMatterBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_organic_matter"

    def __init__(
        self,
        poc_initial: Union[float, None] = None,
        doc_initial: Union[float, None] = None,
        pon_initial: Union[float, None] = None,
        don_initial: Union[float, None] = None,
        pop_initial: Union[float, None] = None,
        dop_initial: Union[float, None] = None,
        docr_initial: Union[float, None] = None,
        donr_initial: Union[float, None] = None,
        dopr_initial: Union[float, None] = None,
        cpom_initial: Union[float, None] = None,
        rdom_minerl: Union[float, None] = None,
        rpoc_hydrol: Union[float, None] = None,
        rpon_hydrol: Union[float, None] = None,
        rpop_hydrol: Union[float, None] = None,
        theta_hydrol: Union[float, None] = None,
        theta_minerl: Union[float, None] = None,
        kpom_hydrol: Union[float, None] = None,
        kdom_minerl: Union[float, None] = None,
        simdenitrification: Union[int, None] = None,
        dom_miner_oxy_reactant_var: Union[str, None] = None,
        dom_miner_nit_reactant_var: Union[str, None] = None,
        dom_miner_no2_reactant_var: Union[str, None] = None,
        dom_miner_n2o_reactant_var: Union[str, None] = None,
        dom_miner_fe3_reactant_var: Union[str, None] = None,
        dom_miner_so4_reactant_var: Union[str, None] = None,
        dom_miner_ch4_reactant_var: Union[str, None] = None,
        doc_miner_product_variable: Union[str, None] = None,
        don_miner_product_variable: Union[str, None] = None,
        dop_miner_product_variable: Union[str, None] = None,
        f_an: Union[float, None] = None,
        k_nit: Union[float, None] = None,
        simrpools: Union[bool, None] = None,
        rdomr_minerl: Union[float, None] = None,
        rcpom_bdown: Union[float, None] = None,
        x_cpom_n: Union[float, None] = None,
        x_cpom_p: Union[float, None] = None,
        kedom: Union[float, None] = None,
        kepom: Union[float, None] = None,
        kedomr: Union[float, None] = None,
        kecpom: Union[float, None] = None,
        simphotolysis: Union[bool, None] = None,
        photo_c: Union[float, None] = None,
        settling: Union[int, None] = None,
        w_pom: Union[float, None] = None,
        d_pom: Union[float, None] = None,
        rho_pom: Union[float, None] = None,
        w_cpom: Union[float, None] = None,
        d_cpom: Union[float, None] = None,
        rho_cpom: Union[float, None] = None,
        resuspension: Union[int, None] = None,
        resus_link: Union[str, None] = None,
        sedimentomfrac: Union[float, None] = None,
        xsc: Union[float, None] = None,
        xsn: Union[float, None] = None,
        xsp: Union[float, None] = None,
        fsed_doc: Union[float, None] = None,
        fsed_don: Union[float, None] = None,
        fsed_dop: Union[float, None] = None,
        ksed_dom: Union[float, None] = None,
        theta_sed_dom: Union[float, None] = None,
        fsed_doc_variable: Union[str, None] = None,
        fsed_don_variable: Union[str, None] = None,
        fsed_dop_variable: Union[str, None] = None,
        diag_level: Union[int, None] = None,
        extra_diag: Union[bool, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("poc_initial", float, poc_initial, units="mmol C m^{-3}"),
            NMLParam("doc_initial", float, doc_initial, units="mmol C m^{-3}"),
            NMLParam("pon_initial", float, pon_initial, units="mmol N m^{-3}"),
            NMLParam("don_initial", float, don_initial, units="mmol C m^{-3}"),
            NMLParam("pop_initial", float, pop_initial, units="mmol P m^{-3}"),
            NMLParam("dop_initial", float, dop_initial, units="mmol P m^{-3}"),
            NMLParam("docr_initial", float, docr_initial),
            NMLParam("donr_initial", float, donr_initial),
            NMLParam("dopr_initial", float, dopr_initial),
            NMLParam(
                "cpom_initial", float, cpom_initial, units="mmol C m^{-3}"
            ),
            NMLParam("rdom_minerl", float, rdom_minerl, units="d^{-1}"),
            NMLParam("rpoc_hydrol", float, rpoc_hydrol, units="d^{-1}"),
            NMLParam("rpon_hydrol", float, rpon_hydrol, units="d^{-1}"),
            NMLParam("rpop_hydrol", float, rpop_hydrol, units="d^{-1}"),
            NMLParam("theta_hydrol", float, theta_hydrol),
            NMLParam("theta_minerl", float, theta_minerl),
            NMLParam(
                "kpom_hydrol", float, kpom_hydrol, units="mmol O_{2} m^{-3}"
            ),
            
            
            NMLParam(
                "kdom_minerl", float, kdom_minerl, units="mmol O_{2} m^{-3}"
            ),
            NMLParam("simdenitrification", int, simdenitrification),
            NMLParam(
                "dom_miner_oxy_reactant_var", str, dom_miner_oxy_reactant_var
            ),
            NMLParam(
                "dom_miner_nit_reactant_var", str, dom_miner_nit_reactant_var
            ),
            NMLParam(
                "dom_miner_no2_reactant_var", str, dom_miner_no2_reactant_var
            ),
            NMLParam(
                "dom_miner_n2o_reactant_var", str, dom_miner_n2o_reactant_var
            ),
            NMLParam(
                "dom_miner_fe3_reactant_var", str, dom_miner_fe3_reactant_var
            ),
            NMLParam(
                "dom_miner_so4_reactant_var", str, dom_miner_so4_reactant_var
            ),
            NMLParam(
                "dom_miner_ch4_reactant_var", str, dom_miner_ch4_reactant_var
            ),
            NMLParam(
                "doc_miner_product_variable", str, doc_miner_product_variable
            ),
            NMLParam(
                "don_miner_product_variable", str, don_miner_product_variable
            ),
            NMLParam(
                "dop_miner_product_variable", str, dop_miner_product_variable
            ),
            NMLParam("f_an", float, f_an),
            NMLParam("k_nit", float, k_nit, units="mmol N m^{-3}"),
            NMLParam("simrpools", bool, simrpools),
            NMLParam("rdomr_minerl", float, rdomr_minerl, units="d^{-1}"),
            NMLParam("rcpom_bdown", float, rcpom_bdown, units="d^{-1}"),
            NMLParam(
                "x_cpom_n", float, x_cpom_n, units="(mmol N) (mmol C^{-1})"
            ),
            NMLParam(
                "x_cpom_p", float, x_cpom_p, units="(mmol P) (mmol C^{-1})"
            ),
            NMLParam(
                "kedom", float, kedom, units="m^{-1} ((mmol C) m^{-2})^{-1}"
            ),
            NMLParam(
                "kepom", float, kepom, units="m^{-1} ((mmol C) m^{-2})^{-1}"
            ),
            NMLParam(
                "kedomr", float, kedomr, units="m^{-1} ((mmol C) m^{-2})^{-1}"
            ),
            NMLParam(
                "kecpom", float, kecpom, units="m^{-1} ((mmol C) m^{-2})^{-1}"
            ),
            NMLParam("simphotolysis", bool, simphotolysis),
            NMLParam("photo_c", float, photo_c),
            NMLParam("settling", int, settling),
            NMLParam("w_pom", float, w_pom, units="m d^{-1}"),
            NMLParam("d_pom", float, d_pom, units="m"),
            NMLParam("rho_pom", float, rho_pom, units="kg m^{-3}"),
            NMLParam("w_cpom", float, w_cpom, units="m d^{-1}"),
            NMLParam("d_cpom", float, d_cpom, units="m"),
            NMLParam("rho_cpom", float, rho_cpom, units="kg d^{-3}"),
            NMLParam("resuspension", int, resuspension),
            NMLParam("resus_link", str, resus_link),
            NMLParam(
                "sedimentomfrac",
                float,
                sedimentomfrac,
                units="(g OM) (g sediment)^{-1}",
            ),
            NMLParam("xsc", float, xsc, units="(mmol C) (g OM)^{-1}"),
            NMLParam("xsn", float, xsn, units="(mmol N) (g OM)^{-1}"),
            NMLParam("xsp", float, xsp, units="(mmol P) (g OM)^{-1}"),
            NMLParam(
                "fsed_doc", float, fsed_doc, units="(mmol C) m^{-2} day^{-1}"
            ),
            NMLParam(
                "fsed_don", float, fsed_don, units="(mmol N) m^{-2} day^{-1}"
            ),
            NMLParam(
                "fsed_dop", float, fsed_dop, units="(mmol P) m^{-2} day^{-1}"
            ),
            NMLParam("ksed_dom", float, ksed_dom, units="(mmol O_{2}) m^{-3}"),
            NMLParam("theta_sed_dom", float, theta_sed_dom),
            NMLParam(
                "fsed_doc_variable",
                str,
                fsed_doc_variable,
                units="(mmol C) m^{-2} day^{-1}",
            ),
            NMLParam(
                "fsed_don_variable",
                str,
                fsed_don_variable,
                units="(mmol N) m^{-2} day^{-1}",
            ),
            NMLParam(
                "fsed_dop_variable",
                str,
                fsed_dop_variable,
                units="(mmol P) m^{-2} day^{-1}",
            ),
            NMLParam("diag_level", int, diag_level),
            NMLParam("extra_diag", bool, extra_diag),
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class PhytoplanktonBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_phytoplankton"

    def __init__(
        self,
        num_phytos: Union[int, None] = None,
        the_phytos: Union[List[int], None] = None,
        settling: Union[List[int], None] = None,
        do_mpb: Union[int, None] = None,
        r_mpbg: Union[float, None] = None,
        r_mpbr: Union[float, None] = None,
        i_kmpb: Union[float, None] = None,
        mpb_max: Union[float, None] = None,
        resuspension: Union[float, None] = None,
        n_zones: Union[int, None] = None,
        active_zones: Union[int, None] = None,
        resus_link: Union[str, None] = None,
        p_excretion_target_variable: Union[str, None] = None,
        n_excretion_target_variable: Union[str, None] = None,
        c_excretion_target_variable: Union[str, None] = None,
        si_excretion_target_variable: Union[str, None] = None,
        p_mortality_target_variable: Union[str, None] = None,
        n_mortality_target_variable: Union[str, None] = None,
        c_mortality_target_variable: Union[str, None] = None,
        si_mortality_target_variable: Union[str, None] = None,
        p1_uptake_target_variable: Union[str, None] = None,
        n1_uptake_target_variable: Union[str, None] = None,
        n2_uptake_target_variable: Union[str, None] = None,
        si_uptake_target_variable: Union[str, None] = None,
        do_uptake_target_variable: Union[str, None] = None,
        c_uptake_target_variable: Union[str, None] = None,
        dbase: Union[str, None] = None,
        min_rho: Union[float, None] = None,
        max_rho: Union[float, None] = None,
        diag_level: Union[int, None] = None,
        extra_diag: Union[bool, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("num_phytos", int, num_phytos),
            NMLParam("the_phytos", int, the_phytos, is_list=True),
            NMLParam("settling", int, settling, is_list=True),
            NMLParam("do_mpb", int, do_mpb),
            NMLParam("r_mpbg", float, r_mpbg),
            NMLParam("r_mpbr", float, r_mpbr),
            NMLParam("i_kmpb", float, i_kmpb, units="W m^{-2}"),
            NMLParam("mpb_max", float, mpb_max, units="mmol C m^{-2}"),
            NMLParam("resuspension", float, resuspension),
            NMLParam("n_zones", int, n_zones),
            NMLParam("active_zones", int, active_zones),
            NMLParam("resus_link", str, resus_link),
            NMLParam(
                "p_excretion_target_variable", str, p_excretion_target_variable
            ),
            NMLParam(
                "n_excretion_target_variable", str, n_excretion_target_variable
            ),
            NMLParam(
                "c_excretion_target_variable", str, c_excretion_target_variable
            ),
            NMLParam(
                "si_excretion_target_variable",
                str,
                si_excretion_target_variable,
            ),
            NMLParam(
                "p_mortality_target_variable", str, p_mortality_target_variable
            ),
            NMLParam(
                "n_mortality_target_variable", str, n_mortality_target_variable
            ),
            NMLParam(
                "c_mortality_target_variable", str, c_mortality_target_variable
            ),
            NMLParam(
                "si_mortality_target_variable",
                str,
                si_mortality_target_variable,
            ),
            NMLParam(
                "p1_uptake_target_variable", str, p1_uptake_target_variable
            ),
            NMLParam(
                "n1_uptake_target_variable", str, n1_uptake_target_variable
            ),
            NMLParam(
                "n2_uptake_target_variable", str, n2_uptake_target_variable
            ),
            NMLParam(
                "si_uptake_target_variable", str, si_uptake_target_variable
            ),
            NMLParam(
                "do_uptake_target_variable", str, do_uptake_target_variable
            ),
            NMLParam(
                "c_uptake_target_variable", str, c_uptake_target_variable
            ),
            NMLParam("dbase", str, dbase, is_dbase_fl=True),
            NMLParam("min_rho", float, min_rho),
            NMLParam("max_rho", float, max_rho),
            NMLParam("diag_level", int, diag_level),
            NMLParam("extra_diag", bool, extra_diag),
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("num_phytos", "the_phytos")
        self.val_list_len_params("num_phytos", "settling")


@NML_REGISTER.register_block()
class ZooplanktonBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_zooplankton"

    def __init__(
        self,
        num_zoops: Union[int, None] = None,
        the_zoops: Union[List[int], None] = None,
        dn_target_variable: Union[str, None] = None,
        pn_target_variable: Union[str, None] = None,
        dp_target_variable: Union[str, None] = None,
        pp_target_variable: Union[str, None] = None,
        dc_target_variable: Union[str, None] = None,
        pc_target_variable: Union[str, None] = None,
        dbase: Union[str, None] = None,
        simzoopfeedback: Union[bool, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("num_zoops", int, num_zoops),
            NMLParam("the_zoops", int, the_zoops, is_list=True),
            NMLParam("dn_target_variable", str, dn_target_variable),
            NMLParam("pn_target_variable", str, pn_target_variable),
            NMLParam("dp_target_variable", str, dp_target_variable),
            NMLParam("pp_target_variable", str, pp_target_variable),
            NMLParam("dc_target_variable", str, dc_target_variable),
            NMLParam("pc_target_variable", str, pc_target_variable),
            NMLParam("dbase", str, dbase, is_dbase_fl=True),
            NMLParam("simzoopfeedback", bool, simzoopfeedback),
        )
        self.strict = True

    def validate(self):
        self.params.validate()


@NML_REGISTER.register_block()
class MacrophyteBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_macrophyte"

    def __init__(
        self,
        num_mphy: Union[int, None] = None,
        the_mphy: Union[List[int], None] = None,
        n_zones: Union[int, None] = None,
        active_zones: Union[List[int], None] = None,
        simstaticbiomass: Union[bool, None] = None,
        simmacfeedback: Union[bool, None] = None,
        dbase: Union[str, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("num_mphy", int, num_mphy),
            NMLParam("the_mphy", int, the_mphy, is_list=True),
            NMLParam("n_zones", int, n_zones),
            NMLParam("active_zones", int, active_zones, is_list=True),
            NMLParam("simstaticbiomass", bool, simstaticbiomass),
            NMLParam("simmacfeedback", bool, simmacfeedback),
            NMLParam("dbase", str, dbase, is_dbase_fl=True),
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("num_mphy", "the_mphy")
        self.val_list_len_params("n_zones", "active_zones")

@NML_REGISTER.register_block()
class TotalsBlock(NMLBlock):
    nml_name = "aed"
    block_name = "aed_totals"

    def __init__(
        self,
        outputlight: Union[bool, None] = None,
        tn_vars: Union[List[str], str, None] = None,
        tn_varscale: Union[List[float], float, None] = None,
        tp_vars: Union[List[str], str, None] = None,
        tp_varscale: Union[List[float], float, None] = None,
        toc_vars: Union[List[str], str, None] = None,
        toc_varscale: Union[List[float], float, None] = None,
        tss_vars: Union[List[str], str, None] = None,
        tss_varscale: Union[List[float], float, None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("outputlight", bool, outputlight),
            NMLParam("tn_vars", str, tn_vars, is_list=True),
            NMLParam("tn_varscale", float, tn_varscale, is_list=True),
            NMLParam("tp_vars", str, tp_vars, is_list=True),
            NMLParam("tp_varscale", float, tp_varscale, is_list=True),
            NMLParam("toc_vars", str, toc_vars, is_list=True),
            NMLParam("toc_varscale", float, toc_varscale, is_list=True),
            NMLParam("tss_vars", str, tss_vars, is_list=True),
            NMLParam("tss_varscale", float, tss_varscale, is_list=True),
        )
        self.strict = True
    
    def validate(self):
        self.params.validate()


@NML_REGISTER.register_nml()
class AEDNML(NML):
    nml_name = "aed"

    def __init__(
        self,
        aed_models: ModelsBlock = ModelsBlock(),
        aed_tracer: TracerBlock = TracerBlock(),
        aed_noncohesive: NonCohesiveBlock = NonCohesiveBlock(),
        aed_oxygen: OxygenBlock = OxygenBlock(),
        aed_carbon: CarbonBlock = CarbonBlock(),
        aed_sedflux: SedFluxBlock = SedFluxBlock(),
        aed_sed_const2d: SedConst2DBlock = SedConst2DBlock(),
        aed_silica: SilicaBlock = SilicaBlock(),
        aed_nitrogen: NitrogenBlock = NitrogenBlock(),
        aed_phosphorus: PhosphorusBlock = PhosphorusBlock(),
        aed_organic_matter: OrganicMatterBlock = OrganicMatterBlock(),
        aed_phytoplankton: PhytoplanktonBlock = PhytoplanktonBlock(),
        aed_zooplankton: ZooplanktonBlock = ZooplanktonBlock(),
        aed_macrophyte: MacrophyteBlock = MacrophyteBlock(),
        aed_totals: TotalsBlock = TotalsBlock(),
    ):
        super().__init__()
        self.init_blocks(
            aed_models,
            aed_sedflux,
            aed_sed_const2d,
            aed_tracer,
            aed_noncohesive,
            aed_oxygen,
            aed_carbon,
            aed_silica,
            aed_nitrogen,
            aed_phosphorus,
            aed_organic_matter,
            aed_phytoplankton,
            aed_totals,
            aed_zooplankton,
            aed_macrophyte,
            
        )
        self.strict = True

    def validate(self):
        self.blocks.validate()