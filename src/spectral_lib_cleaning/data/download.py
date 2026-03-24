from pathlib import Path
from typing import Tuple

import pandas as pd
from downloaders import BaseDownloader
from matchms.exporting import save_as_mgf
from matchms.importing import load_spectra
from tqdm.auto import tqdm

from ..config import Config
from ..urls import GNPS_LIBS, GNPS_URLS, MASS_BANK, MONA, MSNLIB, MSNLIB_URLS


def download_mona(
    download_dir: Path = Path("downloads"),
) -> Tuple[pd.DataFrame, Path]:

    df = BaseDownloader(
        auto_extract=True,
    ).download(MONA, [str(download_dir / "mona.zip")])
    mona_file_name = [i for i in Path(df["extraction_destination"][0]).iterdir()]
    mona_file_name = mona_file_name[0]
    return (df, mona_file_name)


def download_all_libs_except_mona(
    download_dir: Path = Path("downloads"),
) -> pd.DataFrame:

    all_urls = MASS_BANK + MSNLIB_URLS + GNPS_URLS
    download_path = [download_dir / "MassBank.msp"]
    download_path = download_path + [download_dir / i for i in MSNLIB + GNPS_LIBS]

    df = BaseDownloader(
        process_number=1,
        auto_extract=True,
        delete_original_after_extraction=True,
        verbose=2,
    ).download(all_urls, [str(i) for i in download_path])
    return df


def run_download(config: Config) -> None:
    config.raw_dir.mkdir(parents=True, exist_ok=True)
    _, mona_dir = download_mona(config.download_dir)
    libs_db = download_all_libs_except_mona(config.download_dir)

    spectra = []
    for i in tqdm(
        load_spectra(str(mona_dir), metadata_harmonization=False),
        desc="Loading MoNA",
        leave=False,
    ):
        spectra.append(i)

    for file_name in tqdm(
        libs_db["destination"],
        desc="Loading spectra",
        leave=False,
    ):
        for i in tqdm(
            load_spectra(file_name, metadata_harmonization=False),
            desc=f"Loading {file_name}",
            leave=False,
        ):
            spectra.append(i)

    save_as_mgf(spectra=spectra, filename=str(config.raw_dir / "merged_libraries.mgf"))
