#!/usr/bin/env python3

import sys
import click
import logging
import threading

from .lib.akamai import Akamai
from .lib.aws import Aws
from .lib.azure import Azure
from .lib.cloudflare import Cloudflare
from .lib.fastly import Fastly
from .lib.google import Google
from .lib.sucuri import Sucuri
from .lib.incapsula import Incapsula

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import track
from ipaddress import ip_address, ip_network

# Dealing with SSL Warnings
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass

# Setting up logging with rich
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

# Initializing console for rich
console = Console()

# Setting context settings for click
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


def process(p, v, target, output):
    """
    Function to process IPs as a thread.
    """
    try:
        for i in v:
            if ip_address(target) in ip_network(i):
                log.info(f'Found {target} in {i} for provider {p.upper()}')

                # Writing output to file
                with open(output, "a") as f:
                    f.write(f'{target},{p.upper()},{i}\n')
    except ValueError:
        pass


def spawn_process(res, targets, output):
    """
    Creating threads to process IPs.
    """
    for target in targets:
        for p, v in res.items():
            t = threading.Thread(target=process, args=(p, v, target, output))
            t.start()


@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.argument("kind", type=click.Choice(["cloud"]), default="cloud")
@click.argument("provider", type=click.Choice(["all"]), default="all")
@click.argument("targets", type=click.File("r"))
@click.argument("output", type=click.Path(file_okay=True, writable=True))
def main(kind, provider, targets, output):
    """
    Tool to check if a list of IPs are associated with a cloud provider. \n
    Currently only supports the checking of all providers at once. \n
    Usage: cloudcheck [kind] [provider] [targets] [output]
    """

    target_file = [line.strip() for line in open(targets)]

    # Pre-defined providers
    providers = ["aws", "azure", "google", "akamai",
                 "cloudflare", "fastly", "sucuri"]

    # Pre-defined results
    res = {}

    # Instantiating modules from providers
    for p in providers:
        try:
            module = p.title()
            mod_name = getattr(sys.modules[__name__], module)
            module = mod_name()
        except Exception as err:
            log.error(f"Unable to run module: {err}")
            exit(1)

        # Getting IP ranges from module and inserting into res
        try:
            ranges = module._get_ranges()
            results = module._process_ranges(ranges)
            res[p] = results
        except Exception as err:
            log.error(f"Unable to get and process ranges: {err}")
            exit(1)

    # Spawning threads for each module to check IPs
    spawn_process(res, target_file, output)


if __name__ == "__main__":
    main()
