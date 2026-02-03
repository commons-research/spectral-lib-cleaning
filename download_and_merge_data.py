from matchms.exporting import save_as_mgf
from matchms.importing import load_spectra
from tqdm.auto import tqdm

from spectral_lib_cleaning.download_data import (
    download_all_libs_except_mona,
    download_mona,
)


def main():
    _, mona_dir = download_mona()
    libs_db = download_all_libs_except_mona()

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

    save_as_mgf(spectra=spectra, filename="merged_libraries.mgf")


if __name__ == "__main__":
    main()
