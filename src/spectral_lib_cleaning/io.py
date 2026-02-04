import re
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from .definitions import (
    ADDUCT,
    CHARGE,
    FEATURE_ID,
    FILE_NAME,
    IONMODE,
    NAME,
    PRECURSOR_MZ,
    RT,
    SCAN_NUMBER,
    SMILES,
    SPECTRUM,
)


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def read_mgf(pth: Path | str, **kwargs) -> pd.DataFrame:
    return read_textual_ms_format(
        pth=pth,
        spectrum_end_line="END IONS",
        name_value_sep="=",
        ignore_line_prefixes=("#",),
        spectrum_start_line="BEGIN IONS",
        **kwargs,
    )


def read_textual_ms_format(
    pth: Path | str,
    spectrum_end_line,
    name_value_sep,
    spectrum_start_line=None,  # If None, first not ignored line is considered to be the start of the first spectrum
    prec_mz_name=["PEPMASS", "PRECURSORMZ", "PRECURSOR_MZ"],
    charge_name=["CHARGE"],
    adduct_name=["ADDUCT"],
    smiles_name=["SMILES"],
    rt_name=["RTINSECONDS", "RETENTION_TIME", "RTINMINUTES", "RT"],
    ionmode_name=["IONMODE"],
    feature_id_name=["FEATURE_ID"],
    scan_number_name=["SCAN_NUMBER"],
    name_name=["NAME"],
    ignore_line_prefixes=(),
    encoding="utf-8",
) -> pd.DataFrame:
    if isinstance(pth, str):
        pth = Path(pth)
    # TODO: this is very raw and dirty.

    # Two numbers separated with a white space
    peak_pattern = re.compile(
        r"\b([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\s([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)\b"
    )

    # A word followed by an arbitrary string separated with `name_value_sep`
    attr_pattern = re.compile(rf"^\s*([A-Z_]+){name_value_sep}(.*)\s*$")
    attr_mapping = {}
    if prec_mz_name:
        for prec_mz_name_i in prec_mz_name:
            attr_mapping[prec_mz_name_i] = PRECURSOR_MZ
    if charge_name:
        for charge_name_i in charge_name:
            attr_mapping[charge_name_i] = CHARGE
    if adduct_name:
        for adduct_name_i in adduct_name:
            attr_mapping[adduct_name_i] = ADDUCT
    if smiles_name:
        for smiles_name_i in smiles_name:
            attr_mapping[smiles_name_i] = SMILES
    if scan_number_name:
        for scan_number_name_i in scan_number_name:
            attr_mapping[scan_number_name_i] = SCAN_NUMBER
    if ionmode_name:
        for ionmode_name_i in ionmode_name:
            attr_mapping[ionmode_name_i] = IONMODE
    if name_name:
        for name_name_i in name_name:
            attr_mapping[name_name_i] = NAME
    if rt_name:
        for rt_name_i in rt_name:
            attr_mapping[rt_name_i] = RT
    if feature_id_name:
        for feature_id_name_i in feature_id_name:
            attr_mapping[feature_id_name_i] = FEATURE_ID

    data = []
    with open(pth, "r", encoding=encoding) as f:
        lines = f.readlines()

        # TODO for msp?
        # if lines[-1] != spectrum_end_line:
        #     lines.append(spectrum_end_line)

    started_reading_spectra = False
    for i, line in enumerate(
        tqdm(
            lines,
            desc="Reading lines",
            leave=False,
        )
    ):

        # Potentially mgf files can start with some metadata before the first spectrum
        if (spectrum_start_line is None and i == 0) or (
            spectrum_start_line is not None and line.startswith(spectrum_start_line)
        ):
            started_reading_spectra = True
            spec = {SPECTRUM: [[], []]}

        # Skip lines that are not part of the spectrum or comments
        if not started_reading_spectra or any(
            [line.startswith(p) for p in ignore_line_prefixes]
        ):
            continue

        # End of spectrum
        if line.rstrip() == spectrum_end_line:
            spec[SPECTRUM] = np.array(spec[SPECTRUM])
            data.append(spec)
            spec = {SPECTRUM: [[], []]}
            continue

        # Attributes parsing
        match = attr_pattern.match(line)
        if match:
            k, v = match.group(1), match.group(2)
            if is_float(v):
                v = float(v)
                if v.is_integer():
                    v = int(v)
            if k in attr_mapping:
                k = attr_mapping[k]

            # If numberic attribute was not parsed to float, try to parse the first number in its space-separated string
            if k in [PRECURSOR_MZ, RT] and isinstance(v, str):
                v = v.split(" ")[0]
                if not is_float(v):
                    raise ValueError(f"Invalid value for {k}: {v}")
                v = float(v)

            # Parse ionization mode
            if k == IONMODE:
                v = v.lower()
                if "pos" in v:
                    v = "+"
                elif "neg" in v:
                    v = "-"
                else:
                    raise ValueError(f"Invalid value for {k}: {v}")

            # Parse charge
            if k == CHARGE:
                try:
                    if isinstance(v, str):
                        sign = 1
                        if "-" in v:
                            sign = -1
                        v = sign * int(v.replace("-", "").replace("+", ""))
                        v = int(v)
                except ValueError:
                    raise ValueError(f"Invalid value for {k}: {v}")

            spec[k] = v
            continue

        # Peaks parsing
        match = peak_pattern.match(line)
        if match:
            mz, intensity = float(match.group(1)), float(match.group(2))
            spec[SPECTRUM][0].append(mz)
            spec[SPECTRUM][1].append(intensity)
            continue

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Add file name column
    df[FILE_NAME] = pth.name

    return df
