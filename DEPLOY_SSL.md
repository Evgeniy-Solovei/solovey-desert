# HTTPS and Let's Encrypt

The project uses nginx and certbot as Docker containers. No certbot packages need to be installed on the server.

## First server setup

1. Point DNS records to the server IP:
   - `A solovey-desert.by -> server IPv4`
   - `A www.solovey-desert.by -> server IPv4`

2. Open ports on the server firewall:
   - `80/tcp`
   - `443/tcp`

3. Set a real email in `.env`:

   ```env
   LETSENCRYPT_EMAIL=your-email@example.com
   ```

4. Build and start the containers:

   ```bash
   docker compose up -d --build
   ```

5. Issue the first real certificate:

   ```bash
   sh scripts/issue-letsencrypt.sh
   ```

After that, the `certbot` container checks renewal every 12 hours. The `nginx` container reloads itself periodically so renewed certificates are picked up.

## Important

Run `scripts/issue-letsencrypt.sh` only after DNS already points to the server. Let's Encrypt validates the domain through `http://solovey-desert.by/.well-known/acme-challenge/...`.
