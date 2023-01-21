#!/usr/bin/env python3

import json
import logging
import sys
import threading
from ipaddress import ip_address, ip_network

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import track

from .lib.akamai import Akamai
from .lib.aws import Aws
from .lib.azure import Azure
from .lib.cloudflare import Cloudflare
from .lib.fastly import Fastly
from .lib.google import Google
from .lib.incapsula import Incapsula
from .lib.sucuri import Sucuri

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
                if not silence:
                    log.info(f"Found {target} in {i} for provider {p.upper()}")

                # Writing output to file
                with open(output, "a") as f:
                    data = {
                        "ip": target,
                        "cdn": True,
                        "provider": p.upper(),
                        "range": i,
                    }
                    f.write(json.dumps(data, indent=4) + "\n")
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
@click.option("-s", "--silent", is_flag=True, help="Silence output")
@click.option("-c", "--cache", is_flag=True, help="Use cached data.")
@click.option("-u", "--update", is_flag=True, help="Update cache.", default=False)
@click.argument("kind", type=click.Choice(["cdn"]), default="cdn")
@click.argument("provider", type=click.Choice(["all"]), default="all")
@click.argument("targets", type=click.Path(file_okay=True, readable=True))
@click.argument("output", type=click.Path(file_okay=True, writable=True))
def main(silent, cache, update, kind, provider, targets, output):
    """
    Tool to check if a list of IPs are associated with a cloud provider. \n
    Currently only supports the checking of all providers at once. \n
    Usage: cloudcheck [kind] [provider] [targets] [output]
    """

    global silence
    silence = silent

    if not update:
        target_file = [line.strip() for line in open(targets)]

    # Pre-defined providers
    providers = [
        "aws",
        "azure",
        "google",
        "akamai",
        "cloudflare",
        "fastly",
        "sucuri",
        "incapsula",
    ]

    # Pre-defined results
    res = {}

    # Instantiating modules from providers
    if not cache or update == True:
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
                with open("cloudcheck/lib/cache/cache.json", "w") as f:
                    json.dump(res, f)
            except Exception as err:
                log.error(f"Unable to get and process ranges: {err}")
                exit(1)
    else:
        # Spawning threads for each module to check IPs
        with open("cloudcheck/lib/cache/cache.json", "r") as f:
            res = json.load(f)

    if not update:
        spawn_process(res, target_file, output)


if __name__ == "__main__":
    main()
