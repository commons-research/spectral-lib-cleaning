import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

ZENODO_API = "https://zenodo.org/api"
ZENODO_SANDBOX_API = "https://sandbox.zenodo.org/api"

load_dotenv()


def run_publish(
    file_path: str,
    *,
    title: str,
    description: str,
    sandbox: bool = False,
) -> None:
    dataset_path = Path(file_path)
    token: str | None = os.environ.get("ZENODO_TOKEN")

    if not token:
        raise RuntimeError(
            "Set ZENODO_TOKEN environment variable. "
            "Create one at https://zenodo.org/account/settings/applications/"
        )

    api = ZENODO_SANDBOX_API if sandbox else ZENODO_API
    env_label = "SANDBOX" if sandbox else "PRODUCTION"
    print(f"Publishing to Zenodo ({env_label})")

    # Load metadata.json if present for extra info
    meta_path = dataset_path / "metadata.json"
    extra_meta: dict = {}
    if meta_path.exists():
        with open(meta_path) as meta_file:
            extra_meta = json.load(meta_file)

    # 1. Create deposition
    print("\nCreating deposition...")
    deposition = _api_request(
        f"{api}/deposit/depositions",
        token=token,
        method="POST",
        data=json.dumps({}).encode(),
    )
    dep_id = deposition["id"]
    bucket_url = deposition["links"]["bucket"]
    print(f"  Deposition ID: {dep_id}")

    # 2. Upload file
    _upload_file(bucket_url, dataset_path, token)

    # 3. Set metadata
    print("Setting metadata...")
    metadata = {
        "metadata": {
            "title": title,
            "upload_type": "dataset",
            "description": description,
            "creators": [
                {"name": "Visani, Marco", "affiliation": "University of Fribourg"}
            ],
            "keywords": [
                "matchms",
                "Spectral library",
                "cheminformatics",
            ],
            "related_identifiers": [
                {
                    "identifier": "https://github.com/commons-research/spectral-lib-cleaning",
                    "relation": "isSupplementTo",
                    "scheme": "url",
                },
            ],
            "notes": json.dumps(extra_meta, indent=2) if extra_meta else "",
        }
    }
    _api_request(
        f"{api}/deposit/depositions/{dep_id}",
        token=token,
        method="PUT",
        data=json.dumps(metadata).encode(),
    )

    # 4. Print link — do NOT auto-publish so the user can review
    edit_url = deposition["links"]["html"]
    print("\nDeposition created successfully!")
    print(f"Review and publish at: {edit_url}")
    print(f"Total pairs: {extra_meta.get('total_pairs', 'unknown')}")

    return None


def _api_request(
    url: str, *, token: str, method: str, data: bytes | None = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Zenodo API error {e.code}: {body}") from e


def _upload_file(bucket_url: str, file_path: Path, token: str) -> None:
    url = f"{bucket_url}/{file_path.name}"
    file_size = file_path.stat().st_size
    with open(file_path, "rb") as f:
        req = urllib.request.Request(
            url,
            data=f,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/octet-stream",
                "Content-Length": str(file_size),
            },
            method="PUT",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
                print(f"    -> {result['checksum']} ({file_size / (1024**2):.1f} MB)")
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            raise RuntimeError(
                f"Upload failed for {file_path.name}: {e.code} {body}"
            ) from e
