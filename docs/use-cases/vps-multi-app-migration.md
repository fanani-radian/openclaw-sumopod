# Use Case: Multi-App VPS Migration with Security Hardening

> **Scenario:** Migrate multiple applications from Replit/cloud to self-hosted VPS with production-grade security.

```mermaid
flowchart TB
    subgraph Source["☁️ Source: Replit/Cloud"]
        R1[App 1: Radian Portal]
        R2[App 2: Survey Generator]
        R3[App 3: RFM Gold Inventory]
        DB1[(PostgreSQL<br/>Neon/Replit)]
    end
    
    subgraph Process["🔧 Migration Process"]
        P1[Code Clone]
        P2[Database Export]
        P3[Database Import]
        P4[PM2 Process Setup]
        P5[Nginx Config]
    end
    
    subgraph Target["🖥️ Target: VPS"]
        A1[Radian Portal<br/>Port 5000]
        A2[Survey Generator<br/>Port 5001]
        A3[RFM Gold<br/>Port 5002]
        DB2[(PostgreSQL<br/>Local)]
    end
    
    R1 --> P1 --> A1
    R2 --> P1 --> A2
    R3 --> P1 --> A3
    DB1 --> P2 --> P3 --> DB2
    A1 --> P4
    A2 --> P4
    A3 --> P4
    A1 --> P5
    A2 --> P5
    A3 --> P5
```

---

## Architecture Overview

```mermaid
flowchart LR
    subgraph User["👤 User"]
        Browser[Browser/Client]
    end
    
    subgraph Security["🔒 Security Layer"]
        DNS[DNS<br/>fanani.co]
        CF[Cloudflare/Namecheap]
        SSL[SSL Certificate<br/>Let's Encrypt]
    end
    
    subgraph VPS["🖥️ VPS (Tencent Cloud)"]
        UFW[UFW Firewall]
        Nginx[Nginx Reverse Proxy]
        
        subgraph Apps["Node.js Apps (PM2)"]
            A1[Port 5000<br/>Radian Portal]
            A2[Port 5001<br/>Survey Generator]
            A3[Port 5002<br/>RFM Gold]
        end
        
        subgraph Database["Database Layer"]
            PG[(PostgreSQL<br/>Localhost:5432)]
            SQLite[(SQLite<br/>File-based)]
        end
    end
    
    Browser -->|HTTPS| DNS
    DNS -->|SSL| CF
    CF -->|443| UFW
    UFW -->|Allow| Nginx
    Nginx -->|Proxy| A1
    Nginx -->|Proxy| A2
    Nginx -->|Proxy| A3
    A1 -->|Local| PG
    A2 -->|Local| SQLite
    A3 -->|Local| PG
```

---

## Step 1: Pre-Migration Checklist

```mermaid
flowchart TD
    A[Start Migration] --> B{Source Code Ready?}
    B -->|Yes| C[Clone to /var/www/]
    B -->|No| D[Export from Replit]
    D --> C
    
    C --> E{Database?
    PostgreSQL/SQLite}
    E -->|PostgreSQL| F[pg_dump export]
    E -->|SQLite| G[Copy .db file]
    
    F --> H[VPS PostgreSQL Setup]
    G --> I[Place in data/ folder]
    
    H --> J[Install Dependencies]
    I --> J
    J --> K[Build Apps]
    K --> L[Ready for PM2]
```

### Commands:
```bash
# 1. Clone apps
sudo mkdir -p /var/www
cd /var/www
git clone <repo> app-name

# 2. Install dependencies
cd app-name
npm install
npm run build

# 3. Environment setup
cp .env.example .env
# Edit .env with production values
```

---

## Step 2: Database Migration

### PostgreSQL Migration

```mermaid
sequenceDiagram
    participant Source as Source DB
    participant VPS as VPS PostgreSQL
    participant App as Application
    
    Source->>Source: pg_dump > backup.sql
    Source->>VPS: Transfer backup.sql
    VPS->>VPS: createdb app_database
    VPS->>VPS: psql < backup.sql
    VPS->>App: Update DATABASE_URL
    App->>VPS: Connect & Verify
```

```bash
# Export from source
pg_dump -h source-host -U user -d database > backup.sql

# Import to VPS
sudo -u postgres createdb app_database
sudo -u postgres psql app_database < backup.sql

# Verify
sudo -u postgres psql app_database -c "\dt"
```

### SQLite Migration

```bash
# Simply copy the database file
cp source/data/app.db /var/www/app-name/data/

# Ensure permissions
chmod 644 /var/www/app-name/data/app.db
```

---

## Step 3: PM2 Process Management

```mermaid
flowchart LR
    A[App 1] -->|PM2| P[PM2 Daemon]
    B[App 2] -->|PM2| P
    C[App 3] -->|PM2| P
    P -->|Auto-restart| A
    P -->|Auto-restart| B
    P -->|Auto-restart| C
    P -->|Logs| L[Log Files]
    P -->|Save| S[dump.pm2]
```

```bash
# Start apps with PM2
cd /var/www/app1 && pm2 start npm --name "app1" -- start
cd /var/www/app2 && pm2 start dist/index.cjs --name "app2"
cd /var/www/app3 && pm2 start npm --name "app3" -- start

# Save PM2 config
pm2 save
pm2 startup systemd
```

---

## Step 4: Nginx Reverse Proxy

```mermaid
flowchart LR
    A[User] -->|HTTP/HTTPS| N[Nginx :80/:443]
    N -->|/| A1[App1 :5000]
    N -->|/api| A2[App2 :5001]
    N -->|/gold| A3[App3 :5002]
```

```nginx
# /etc/nginx/conf.d/app1.conf
server {
    listen 80;
    server_name app1.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## Step 5: Security Hardening

### Firewall Configuration

```mermaid
flowchart TD
    A[Internet] -->|All Ports| F{UFW Firewall}
    F -->|Port 2222| SSH[SSH Access ✅]
    F -->|Port 80| HTTP[HTTP ✅]
    F -->|Port 443| HTTPS[HTTPS ✅]
    F -->|Port 5432| DB[PostgreSQL ❌ BLOCKED]
    F -->|Other| DENY[Deny All]
```

```bash
# Install UFW
sudo dnf install -y ufw

# Configure rules
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp comment 'SSH'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
sudo ufw deny 5432/tcp comment 'Block PostgreSQL external'

# Enable
sudo ufw enable
```

### PostgreSQL Security

```bash
# Edit postgresql.conf
sudo nano /var/lib/pgsql/data/postgresql.conf

# Change:
# listen_addresses = '*'     # ❌ Dangerous
listen_addresses = '127.0.0.1'  # ✅ Safe (localhost only)

# Restart
sudo systemctl restart postgresql
```

### File Permissions

```bash
# Secure .env files
sudo chmod 600 /var/www/*/ .env

# Verify
ls -la /var/www/*/ .env
# Should show: -rw------- (owner read/write only)
```

---

## Step 6: SSL with Let's Encrypt

```mermaid
flowchart LR
    A[Certbot] -->|Request| B[Let's Encrypt]
    B -->|Challenge| C[DNS Verification]
    C -->|Success| D[SSL Certificate]
    D -->|Install| E[Nginx]
    E -->|HTTPS| F[Users]
    
    G[Auto-renew Timer] -->|Every 60 days| A
```

```bash
# Install Certbot
sudo dnf install -y certbot python3-certbot-nginx

# Generate certificates
sudo certbot --nginx \
  -d yourdomain.com \
  -d app1.yourdomain.com \
  -d app2.yourdomain.com \
  --agree-tos \
  --email admin@yourdomain.com \
  --redirect

# Auto-renewal
sudo systemctl enable certbot-renew.timer
```

---

## Troubleshooting

### Common Issues

```mermaid
flowchart TD
    A[App not accessible] --> B{Check PM2}
    B -->|Stopped| C[pm2 restart app]
    B -->|Running| D{Check Port}
    
    D -->|Not listening| E[Check logs: pm2 logs]
    D -->|Listening| F{Check Firewall}
    
    F -->|Blocked| G[ufw allow port]
    F -->|Allowed| H{Check Nginx}
    
    H -->|Error| I[nginx -t && systemctl restart nginx]
    H -->|OK| J[Check DNS propagation]
```

### Database Connection Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ECONNREFUSED` | Wrong host/port | Check DATABASE_URL |
| `password authentication failed` | Wrong credentials | Verify .env |
| `database does not exist` | DB not created | Run createdb |
| `role does not exist` | User missing | Create PostgreSQL user |

---

## Production Checklist

```mermaid
flowchart TD
    A[Production Ready?] --> B[✅ Apps Running]
    A --> C[✅ Database Connected]
    A --> D[✅ Firewall Active]
    A --> E[✅ SSL Enabled]
    A --> F[✅ Auto-restart PM2]
    A --> G[✅ Auto-renew SSL]
    A --> H[✅ Backups Configured]
    
    B --> I[🚀 LAUNCH]
    C --> I
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
```

- [ ] Apps running under PM2
- [ ] Databases migrated and verified
- [ ] Firewall active (UFW/iptables)
- [ ] SSL certificates installed
- [ ] Auto-renewal configured
- [ ] .env files secured (chmod 600)
- [ ] PostgreSQL localhost-only
- [ ] Log rotation configured
- [ ] Monitoring/alerts setup
- [ ] Backup strategy implemented

---

## Files Generated

| File | Purpose |
|------|---------|
| `/tmp/secure-vps.sh` | Security hardening script |
| `/tmp/setup-ssl.sh` | SSL automation script |
| `/tmp/sqlite_import.sql` | Database conversion |

---

## References

- [PM2 Documentation](https://pm2.keymetrics.io/)
- [Nginx Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Let's Encrypt Certbot](https://certbot.eff.org/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)

---

*Generated from real-world migration: Replit → VPS (March 13, 2026)*
