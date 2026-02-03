MONA = "https://mona.fiehnlab.ucdavis.edu/rest/downloads/retrieve/024f4ef5-924f-4f2b-a86d-a23f8013e695"
MASS_BANK = "https://github.com/MassBank/MassBank-data/releases/download/2025.10/MassBank_NISTformat.msp"

GNPS_ENDPOINT = "https://external.gnps2.org/gnpslibrary/"
GNPS_LIBS = [
    "BERKELEY-LAB.mgf",
    "BILELIB19.mgf",
    "BIRMINGHAM-UHPLC-MS-NEG.mgf",
    "BIRMINGHAM-UHPLC-MS-POS.mgf",
    "BMDMS-NP.mgf",
    "CASMI.mgf",
    "DRUGS-OF-ABUSE-LIBRARY.mgf",
    "ECG-ACYL-AMIDES-C4-C24-LIBRARY.mgf",
    "ECG-ACYL-ESTERS-C4-C24-LIBRARY.mgf",
    "GNPS-COLLECTIONS-MISC.mgf",
    "GNPS-COLLECTIONS-PESTICIDES-NEGATIVE.mgf",
    "GNPS-COLLECTIONS-PESTICIDES-POSITIVE.mgf",
    "GNPS-D2-AMINO-LIPID-LIBRARY.mgf",
    "GNPS-EMBL-MCF.mgf",
    "GNPS-FAULKNERLEGACY.mgf",
    "GNPS-IOBA-NHC.mgf",
    "GNPS-LIBRARY.mgf",
    "GNPS-MSMLS.mgf",
    "GNPS-NIH-CLINICALCOLLECTION1.mgf",
    "GNPS-NIH-CLINICALCOLLECTION2.mgf",
    "GNPS-NIH-NATURALPRODUCTSLIBRARY.mgf",
    "GNPS-NIH-NATURALPRODUCTSLIBRARY_ROUND2_NEGATIVE.mgf",
    "GNPS-NIH-NATURALPRODUCTSLIBRARY_ROUND2_POSITIVE.mgf",
    "GNPS-NIH-SMALLMOLECULEPHARMACOLOGICALLYACTIVE.mgf",
    "GNPS-NIST14-MATCHES.mgf",
    "GNPS-NUTRI-METAB-FEM-NEG.mgf",
    "GNPS-NUTRI-METAB-FEM-POS.mgf",
    "GNPS-PRESTWICKPHYTOCHEM.mgf",
    "GNPS-SAM-SIK-KANG-LEGACY-LIBRARY.mgf",
    "GNPS-SCIEX-LIBRARY.mgf",
    "GNPS-SELLECKCHEM-FDA-PART1.mgf",
    "GNPS-SELLECKCHEM-FDA-PART2.mgf",
    "HCE-CELL-LYSATE-LIPIDS.mgf",
    "HMDB.mgf",
    "IQAMDB.mgf",
    "LDB_NEGATIVE.mgf",
    "LDB_POSITIVE.mgf",
    "MIADB.mgf",
    "MMV_NEGATIVE.mgf",
    "MMV_POSITIVE.mgf",
    "PNNL-LIPIDS-NEGATIVE.mgf",
    "PNNL-LIPIDS-POSITIVE.mgf",
    "PSU-MSMLS.mgf",
    "RESPECT.mgf",
    "SUMNER.mgf",
    "UM-NPDC.mgf",
]


GNPS_URLS = [GNPS_ENDPOINT + i for i in GNPS_LIBS]


MSNLIB_ZENODO_ENDPOINT = "https://zenodo.org/records/16984129/files/"

MSNLIB = [
    "20241003_enamdisc_neg_msn.mgf",
    "20241003_enamdisc_pos_msn.mgf",
    "20241003_enammol_neg_msn.mgf",
    "20241003_enammol_pos_msn.mgf",
    "20241003_mcebio_neg_msn.mgf",
    "20241003_mcebio_pos_msn.mgf",
    "20241003_mcedrug_neg_msn.mgf",
    "20241003_mcedrug_pos_msn.mgf",
    "20241003_mcescaf_neg_msn.mgf",
    "20241003_mcescaf_pos_msn.mgf",
    "20241003_nihnp_neg_msn.mgf",
    "20241003_nihnp_pos_msn.mgf",
    "20241003_otavapep_neg_msn.mgf",
    "20241003_otavapep_pos_msn.mgf",
    "20250828_mcediv_50k_sub_neg_msn.mgf",
    "20250828_mcediv_50k_sub_pos_msn.mgf",
    "20250828_targetmol_hts_np_neg_msn.mgf",
    "20250828_targetmol_hts_np_pos_msn.mgf",
]

MSNLIB_URLS = [MSNLIB_ZENODO_ENDPOINT + i for i in MSNLIB]
