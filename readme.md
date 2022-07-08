# Readme

###### "If you can't lick 'em, jine 'em" - James Eli Watson

A bot to mint avax NFT contracts, which can be triggered either by allowlist timer (Joepegs) or a contract function boolean changing. 

## Docker

**Docker build not currently working, clone the CLI branch and run without docker as described bellow to accesss the new features**

There is a docker build of the CLI branch.  This includes GUI like command line config for wallets and contracts. I would suggest running on a digital ocean vps, their $4 cheapest option works well with ubuntu/the image linked below.  The commands would be:

```docker pull xpkea/joepegs_sniper:latest```

```docker run -i -t xpkea/joepegs_sniper:latest wallets```

```docker run -i -t xpkea/joepegs_sniper:latest contracts```

```docker run xpkea/joepegs_sniper:latest start```

Useful image: https://marketplace.digitalocean.com/apps/docker

Referal link:

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=2a880223ed17&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## Without docker
From the CLI branch can config with ```python3 main.py wallets``` and ```python3 main.py contracts```. At the moment you would have to create a .env first.

## ENV File Example:
keys = '["KEY", "KEY2"]'

wallet_addresses = '["MATCHING_ADDRESS", "MATCHING_ADDRESS2"]'
