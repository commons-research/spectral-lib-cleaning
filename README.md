# Spectral libraries cleaning

[![License](https://img.shields.io/github/license/commons-research/spectral-lib-cleaning)](https://github.com/commons-research/spectral-lib-cleaning/blob/main/LICENSE)
[![Dataset](https://zenodo.org/badge/DOI/10.5281/zenodo.19217442.svg)](https://doi.org/10.5281/zenodo.19217442)

## Setup

```bash
git clone git@github.com:commons-research/spectral-lib-cleaning.git
cd spectral-lib-cleaning
uv sync
```

## Download and merge the data
Files will be downloded to `data/downloads` and the merged file will be in `data/raw`

```bash
uv run spectral-clean download_merge
```

## Clean

```bash
uv run spectral-clean clean ./data/raw/merged_libraries.mgf clean_spectra.mgf
```

The `clean_spectra.mgf` will be saved in `data/processed`

## Publish 
To publish you will need to set `ZENODO_TOKEN` environment variable into a `.env` file. You can create one directly from [Zenodo](https://zenodo.org/account/settings/applications/).

Then you can run :
```bash
uv run spectral-clean publish ./data/processed/clean_spectra.mgf --title "Full GNPS library cleaned with matchms" --description "Full GNPS (GNPS, GNPS-PROPOGATED and IMPORT) cleaned with matchms"
```