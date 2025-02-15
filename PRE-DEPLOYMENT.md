# Pre-deployment for Django (Production Ready)

## Step 1: Register a Domain Name

- [namecheap](https://www.namecheap.com)
- [cloudflare](https://www.cloudflare.com/)
- etc.

### Config DNS records

> Custom digitalocean DNS

```sh
ns1.digitalocean.com
ns2.digitalocean.com
ns3.digitalocean.com
```

## Step 2: Set Up a Cloud Server (VPS)

- Hetzner.
- Digitalocean (We use this).
- Linode.
- etc.

### Details Server

> Droplet

- Spec: `512 MB Memory / 10 GB Disk / SGP1`
- OS: Ubuntu 22.04 LTS or Ubuntu 24.04 (LTS) x64 (Recommended)

## Step 3: Deployment

[Deploy Django](./DEPLOYMENT.md)
