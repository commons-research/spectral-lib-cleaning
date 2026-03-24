from pathlib import Path

import click

from .config import Config


@click.group()
@click.option("--root", type=click.Path(), default=".", help="Project root directory")
@click.pass_context
def main(ctx, root):
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config(project_root=Path(root).resolve())


@main.command()
@click.pass_context
def download_merge(ctx):
    """Download PubChem SMILES data from FTP."""
    from .data.download import run_download

    run_download(ctx.obj["config"])


@main.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("ouput", type=click.Path())
@click.pass_context
def clean(ctx, input, output):
    """"""
    from .clean import run_clean

    run_clean(ctx.obj["config"], input, output)


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--title", required=True, help="Zenodo deposit title")
@click.option("--description", required=True, help="Zenodo deposit description")
@click.option("--sandbox", is_flag=True, help="Use Zenodo sandbox (for testing)")
@click.pass_context
def publish(ctx, file_path, title, description, sandbox):
    """Upload a merged dataset to Zenodo and get a DOI."""
    from .postprocess.publish import run_publish

    run_publish(file_path, title=title, description=description, sandbox=sandbox)
