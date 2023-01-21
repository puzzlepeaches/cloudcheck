<div align="center">

# cloudcheck

cloudcheck is a CLI utility to check if IP addresses in a file are associated with a cloud or CDN network.

<br>

[Installation](#installation) •
[Usage](#usage) •
[Getting Started](#getting-started) •
[Coming Soon](#coming-soon)
[Thanks](#thanks)

</div><br>

</div>
<br>

## Installation

cloudcheck supports all major operating systems and can be installed from PyPi using the following command:

```
pipx install cloudcheck
```

<br>

## Getting Started

The utility supports the following cloud and CDN providers:

- Akamai
- AWS Cloudfront
- Azure FrontDoor
- Cloudflare
- Fastly
- Google
- Succuri
- Incapsula

On run, the tool first requests IP ranges from API endpoints hosted by each provider. These ranges are then stored in a dictionary for processing. With this, the ranges are then searched to determine if the input IP addresses are contained within the stored CIDRs.

<br>

## Usage

To use cloudcheck, execute a command similar to what is shown below:

```
cloudcheck cdn all /tmp/targets.txt /tmp/output.json
```

The tool will request IP ranges from from the supported providers and then search for your target IPs in the requested IP ranges.

<br>

## Coming Soon

Some planned features coming in the next release:

- Support checking all cloud IP ranges
- Support checking only CDN IP ranges (Done)
- Support searching specific providers only
- JSON output support (Done)
- DNS support
- Caching for ranges (Done)
- Support silent mode (Done)

<br>

## Thanks

- 0xdade's tool, [sephiroth](https://github.com/0xdade/sephiroth)

- projectdiscovery's GO library [cdncheck](https://github.com/projectdiscovery/cdncheck)
