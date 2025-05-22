#!/usr/bin/python3

try:
    import rich_click as click
    RICH_CLICK = True
except ImportError:
    import click

from enum import Enum, unique
import os
import sys

if RICH_CLICK:
    program_name = sys.argv[0]
    
    click.rich_click.OPTION_GROUPS = {
        f"{sys.argv[0]}": [
            {
                "name": "Standard output logging",
                "options": ["--stdout-log-level"],
            },
            {
                "name": "Logfile",
                "options": ["--logfile", "--logfile-log-level"],
            },
        ],
        f"{sys.argv[0]} install": [
            {
                "name": "Basic Usage",
                "options": ["--recommended", "--sources", "--package-list"],
            },
            {
                "name": "Graphics drivers",
                "options": ["--gpgpu", "--include-dkms"],
            },
            {
                "name": "OEM packages",
                "options": ["--no-oem"],
            },
        ],
    }

@unique
class LogLevel(Enum):
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"

@unique
class PackageSources(Enum):
    FREE = "FREE"
    NONFREE = "NONFREE"

@click.group(invoke_without_command=True)
@click.option("--stdout-log-level", type=click.Choice(LogLevel._member_names_), default="ERROR")
@click.option("--logfile-log-level", type=click.Choice(LogLevel._member_names_), default="INFO")
@click.option("--logfile", type=click.Path(), default=None)
@click.pass_context
def cli(ctx, stdout_log_level: LogLevel, logfile_log_level: LogLevel, logfile: os.PathLike):
    if ctx.invoked_subcommand is None:
        click.echo("Devices:")
        click.echo("")
        click.echo("For more information about usage, try `ubuntu-drivers --help`.")

@cli.command()
def debug():
    click.echo("debug")

@cli.command()
@click.argument("package-name", type=click.STRING, default=None, required=False)
@click.option("--recommended", is_flag=True, help="Automatically select the most compatible version of a driver in case there is multiple options.")
@click.option("--gpgpu", is_flag=True, help="Select packages intended for server environments with GPGPUs and no graphical environment.")
@click.option("--include-dkms/--no-dkms", default=False, help="Add DKMS packages to the selection.")
@click.option("--oem/--no-oem", default=True, help="Include OEM packages.")
@click.option("--sources", type=click.Choice(PackageSources._member_names_), default="NONFREE")
@click.option("--package-list", type=click.Path(), default=None, help="File where the list of explicitely installed packages will be stored.")
def install(package_name: str | None, recommended: bool, gpgpu: bool, include_dkms: bool, oem: bool, sources: PackageSources, package_list: os.PathLike):
    click.echo("install")

@cli.command()
@click.option("--recommended", is_flag=True)
@click.option("--gpgpu", is_flag=True)
@click.option("--include-dkms/--no-dkms", default=False)
@click.option("--oem/--no-oem", default=True)
@click.option("--sources", type=click.Choice(PackageSources._member_names_), default="NONFREE")
def list(recommended: bool, gpgpu: bool, include_dkms: bool, oem: bool, sources: PackageSources):
    click.echo("list")

if __name__ == '__main__':
    cli()
