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
