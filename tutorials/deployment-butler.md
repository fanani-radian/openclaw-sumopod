# Deployment Butler

Automated deployment pipeline: GitHub → VPS with zero-downtime and instant rollback.

## Overview

Manual deployments are error-prone. This automation:
- Triggers on GitHub webhook (push to main)
- Auto-pulls latest code
- Runs health checks
- Rolls back if deployment fails
- Notifies status via Telegram

**Perfect for:** Web apps, APIs, microservices, static sites.

## Architecture

```
[GitHub push]
     ↓
[Webhook triggered]
     ↓
[Deployment pipeline]
  1. Pull latest code
  2. Install dependencies
  3. Build (if needed)
  4. Health check
     ↓
[If healthy]
  → Switch to new version
  → Notify success
     ↓
[If failed]
  → Automatic rollback
  → Notify failure
  → Keep previous version
```

## Prerequisites

- OpenClaw installed
- VPS with systemd
- GitHub webhook setup
- Telegram bot
- Docker (optional but recommended)

## Step 1: Webhook Handler

`scripts/deployment/webhook-server.py`:

```python
#!/usr/bin/env python3
"""
GitHub webhook handler for auto-deployment
Usage: python3 webhook-server.py
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import hmac
import hashlib
import subprocess
import os

# Config
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
REPO_PATH = "/var/www/app"
SERVICE_NAME = "myapp"
BRANCH = "main"

def verify_signature(payload, signature):
    """Verify GitHub webhook signature"""
    if not signature:
        return False
    
    sha_name, signature = signature.split('=')
    mac = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Verify signature
        signature = self.headers.get('X-Hub-Signature-256')
        if not verify_signature(post_data, signature):
            self.send_response(401)
            self.end_headers()
            return
        
        # Parse payload
        payload = json.loads(post_data)
        
        # Check if push to main
        if payload.get('ref') == f'refs/heads/{BRANCH}':
            print(f"🚀 Deployment triggered by {payload['pusher']['name']}")
            
            # Run deployment
            result = subprocess.run(
                ["bash", "scripts/deployment/deploy.sh"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status": "deployed"}')
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'{"status": "failed"}')
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ignored"}')
    
    def log_message(self, format, *args):
        print(f"[Webhook] {format % args}")

def run_server():
    server = HTTPServer(('0.0.0.0', 9000), WebhookHandler)
    print("🌐 Webhook server running on port 9000")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
```

## Step 2: Deployment Script

`scripts/deployment/deploy.sh`:

```bash
#!/bin/bash
# Zero-downtime deployment with rollback

set -e

APP_DIR="/var/www/app"
BACKUP_DIR="/var/www/backups"
SERVICE_NAME="myapp"
HEALTH_URL="http://localhost:3000/health"
MAX_RETRIES=5
RETRY_DELAY=5

LOG_FILE="/var/log/deployment.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

notify() {
    local status="$1"
    local message="$2"
    
    # Telegram notification
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${message}" \
        -d "parse_mode=Markdown" > /dev/null
}

pre_deploy() {
    log "📦 Starting deployment..."
    
    # Create backup
    backup_name="backup_$(date +%Y%m%d_%H%M%S)"
    cp -r "$APP_DIR" "$BACKUP_DIR/$backup_name"
    log "💾 Backup created: $backup_name"
    
    # Store current commit
    cd "$APP_DIR"
    git rev-parse HEAD > "$BACKUP_DIR/$backup_name.commit"
}

deploy() {
    log "🔄 Pulling latest code..."
    
    cd "$APP_DIR"
    git fetch origin
    git reset --hard origin/main
    
    log "📦 Installing dependencies..."
    
    # Install based on project type
    if [ -f "package.json" ]; then
        npm ci --production
    elif [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    elif [ -f "Dockerfile" ]; then
        docker build -t "$SERVICE_NAME:latest" .
    fi
    
    log "🔧 Running build (if needed)..."
    
    if [ -f "package.json" ] && grep -q '"build"' package.json; then
        npm run build
    fi
}

health_check() {
    log "🏥 Running health check..."
    
    # Restart service
    systemctl restart "$SERVICE_NAME"
    
    # Wait for service to start
    sleep 3
    
    # Health check with retries
    for i in $(seq 1 $MAX_RETRIES); do
        if curl -sf "$HEALTH_URL" > /dev/null; then
            log "✅ Health check passed"
            return 0
        fi
        
        log "⏳ Retry $i/$MAX_RETRIES..."
        sleep $RETRY_DELAY
    done
    
    log "❌ Health check failed"
    return 1
}

rollback() {
    log "🚨 Deployment failed! Rolling back..."
    
    # Find latest backup
    latest_backup=$(ls -t "$BACKUP_DIR" | grep "backup_" | head -1)
    
    if [ -z "$latest_backup" ]; then
        log "❌ No backup found! Manual intervention needed."
        notify "error" "🚨 *Deployment Failed*\nNo backup available!"
        exit 1
    fi
    
    # Restore from backup
    rm -rf "$APP_DIR"
    cp -r "$BACKUP_DIR/$latest_backup" "$APP_DIR"
    
    # Restart service
    systemctl restart "$SERVICE_NAME"
    
    log "✅ Rollback complete: $latest_backup"
    notify "error" "🚨 *Deployment Failed*\nRolled back to: $latest_backup"
}

cleanup() {
    # Keep only last 10 backups
    cd "$BACKUP_DIR"
    ls -t | grep "backup_" | tail -n +11 | xargs -r rm -rf
    log "🧹 Old backups cleaned up"
}

# Main deployment flow
main() {
    pre_deploy
    
    if deploy; then
        if health_check; then
            log "✅ Deployment successful!"
            notify "success" "✅ *Deployment Successful*\nApp updated to latest version"
            cleanup
        else
            rollback
            exit 1
        fi
    else
        rollback
        exit 1
    fi
}

main
```

## Step 3: Health Check Endpoint

Add to your app:

```javascript
// Express.js example
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version
  });
});
```

```python
# Flask example
@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })
```

## Step 4: Systemd Service

`/etc/systemd/system/myapp.service`:

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/app
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
systemctl daemon-reload
systemctl enable myapp
systemctl start myapp
```

## Step 5: GitHub Webhook Setup

1. Go to GitHub Repo → Settings → Webhooks
2. Add webhook:
   - **Payload URL:** `http://your-vps:9000/webhook`
   - **Content type:** `application/json`
   - **Secret:** Generate random string
   - **Events:** Just the push event

3. Set environment variable on VPS:
```bash
export GITHUB_WEBHOOK_SECRET="your-secret-here"
```

## Step 6: Manual Deployment Command

`scripts/deployment/deploy-manual.sh`:

```bash
#!/bin/bash
# Manual deployment trigger

echo "🚀 Triggering manual deployment..."
bash scripts/deployment/deploy.sh
```

## Deployment Status Check

`scripts/deployment/status.sh`:

```bash
#!/bin/bash
# Check deployment status

echo "📊 Deployment Status"
echo "==================="

# Git info
cd /var/www/app
echo "📦 Current commit: $(git rev-parse --short HEAD)"
echo "📝 Last message: $(git log -1 --pretty=%B)"

# Service status
echo ""
echo "🔧 Service status:"
systemctl status myapp --no-pager -l

# Health check
echo ""
echo "🏥 Health check:"
curl -s http://localhost:3000/health | python3 -m json.tool

# Recent deployments
echo ""
echo "📜 Recent deployments:"
tail -10 /var/log/deployment.log
```

## Example Output

**Successful Deployment:**
```
[2026-03-08 14:30:01] 📦 Starting deployment...
[2026-03-08 14:30:02] 💾 Backup created: backup_20260308_143002
[2026-03-08 14:30:05] 🔄 Pulling latest code...
[2026-03-08 14:30:08] 📦 Installing dependencies...
[2026-03-08 14:30:15] 🔧 Running build...
[2026-03-08 14:30:25] 🏥 Running health check...
[2026-03-08 14:30:28] ✅ Health check passed
[2026-03-08 14:30:28] ✅ Deployment successful!
[2026-03-08 14:30:29] 🧹 Old backups cleaned up
```

**Telegram Notification:**
```
✅ *Deployment Successful*
App updated to latest version
Commit: a1b2c3d
```

**Failed + Rollback:**
```
[2026-03-08 14:35:10] 🏥 Running health check...
[2026-03-08 14:35:40] ❌ Health check failed
[2026-03-08 14:35:41] 🚨 Deployment failed! Rolling back...
[2026-03-08 14:35:45] ✅ Rollback complete: backup_20260308_143002
```

## Advanced Features

### Blue-Green Deployment

```bash
# Deploy to blue instance
# Health check
# Switch nginx to blue
# Keep green as backup
```

### Database Migrations

```bash
# Run migrations before deployment
npm run migrate

# If migration fails → abort deployment
```

### Canary Deployment

```bash
# Deploy to 10% of traffic first
# Monitor for 5 minutes
# If healthy → deploy to 100%
```

## Conclusion

You now have automated deployment that:
- ✅ Deploys on every GitHub push
- ✅ Runs health checks
- ✅ Auto-rollback on failure
- ✅ Sends Telegram notifications
- ✅ Maintains backups

**Next Steps:**
- Add database migration handling
- Implement blue-green deployment
- Build deployment analytics

---

*Tutorial created for OpenClaw Sumopod*
