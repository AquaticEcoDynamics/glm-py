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
        fsed_amm: Union[List[float], None] = None,
        fsed_nit: Union[List[float], None] = None,
        fsed_frp: Union[List[float], None] = None,
    ):
        super().__init__()
        self.init_params(
            NMLParam("n_zones", int, n_zones),
            NMLParam("active_zones", int, active_zones, is_list=True),
            NMLParam("fsed_oxy", float, fsed_oxy, is_list=True),
            NMLParam("fsed_amm", float, fsed_amm, is_list=True),
            NMLParam("fsed_nit", float, fsed_nit, is_list=True),
            NMLParam("fsed_frp", float, fsed_frp, is_list=True),
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("n_zones", "active_zones")
        self.val_list_len_params("n_zones", "fsed_oxy")
        self.val_list_len_params("n_zones", "fsed_oxy")
        self.val_list_len_params("n_zones", "fsed_amm")
        self.val_list_len_params("n_zones", "fsed_nit")
        self.val_list_len_params("n_zones", "fsed_frp")


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
        rpoc_hydrol: Union[float, None] = None,
        rpon_hydrol: Union[float, None] = None,
        rpop_hydrol: Union[float, None] = None,
        theta_hydrol: Union[float, None] = None,
        kpom_hydrol: Union[float, None] = None,
        rdom_minerl: Union[float, None] = None,
        theta_minerl: Union[float, None] = None,
        kdom_minerl: Union[float, None] = None,
        simdenitrification: Union[int, None] = None,
        f_an: Union[float, None] = None,
        k_nit: Union[float, None] = None,
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
            NMLParam("rpoc_hydrol", float, rpoc_hydrol, units="d^{-1}"),
            NMLParam("rpon_hydrol", float, rpon_hydrol, units="d^{-1}"),
            NMLParam("rpop_hydrol", float, rpop_hydrol, units="d^{-1}"),
            NMLParam("theta_hydrol", float, theta_hydrol),
            NMLParam(
                "kpom_hydrol", float, kpom_hydrol, units="mmol O_{2} m^{-3}"
            ),
            NMLParam("rdom_minerl", float, rdom_minerl, units="d^{-1}"),
            NMLParam("theta_minerl", float, theta_minerl),
            NMLParam(
                "kdom_minerl", float, kdom_minerl, units="mmol O_{2} m^{-3}"
            ),
            NMLParam("simdenitrification", int, simdenitrification),
            NMLParam("f_an", float, f_an),
            NMLParam("k_nit", float, k_nit, units="mmol N m^{-3}"),
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
    ):
        super().__init__()
        self.init_params(
            NMLParam("num_phytos", int, num_phytos),
            NMLParam("the_phytos", int, the_phytos, is_list=True),
            NMLParam("settling", int, settling, is_list=True),
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
            NMLParam("dbase", str, dbase),
            NMLParam("min_rho", float, min_rho),
            NMLParam("max_rho", float, max_rho),
            NMLParam("diag_level", int, diag_level),
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
            NMLParam("dbase", str, dbase),
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
            NMLParam("dbase", str, dbase),
        )
        self.strict = True

    def validate(self):
        self.params.validate()
        self.val_list_len_params("num_mphy", "the_mphy")
        self.val_list_len_params("n_zones", "active_zones")


@NML_REGISTER.register_nml()
class AEDNML(NML):
    nml_name = "aed"

    def __init__(
        self,
        aed_models: ModelsBlock = ModelsBlock(),
        aed_sedflux: SedFluxBlock = SedFluxBlock(),
        aed_sed_const2d: SedConst2DBlock = SedConst2DBlock(),
        aed_oxygen: OxygenBlock = OxygenBlock(),
        aed_silica: SilicaBlock = SilicaBlock(),
        aed_nitrogen: NitrogenBlock = NitrogenBlock(),
        aed_phosphorus: PhosphorusBlock = PhosphorusBlock(),
        aed_organic_matter: OrganicMatterBlock = OrganicMatterBlock(),
        aed_phytoplankton: PhytoplanktonBlock = PhytoplanktonBlock(),
        aed_zooplankton: ZooplanktonBlock = ZooplanktonBlock(),
        aed_macrophyte: MacrophyteBlock = MacrophyteBlock(),
    ):
        super().__init__()
        self.init_blocks(
            aed_models,
            aed_sedflux,
            aed_sed_const2d,
            aed_oxygen,
            aed_silica,
            aed_nitrogen,
            aed_phosphorus,
            aed_organic_matter,
            aed_phytoplankton,
            aed_zooplankton,
            aed_macrophyte,
        )
        self.strict = True

    def validate(self):
        self.blocks.validate()