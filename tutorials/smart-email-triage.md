# Smart Email Triage

AI-powered inbox management that auto-sorts, prioritizes, and drafts responses.

## Overview

Inbox overflowing? This automation:
- Classifies emails by urgency (urgent, newsletter, follow-up, spam)
- Auto-archives low-priority mail
- Stars important messages
- Drafts quick replies for common requests
- Sends daily digest of what needs attention

**Before:** 200+ unread emails, important messages buried  
**After:** Inbox zero, urgent items flagged, newsletters archived

## Architecture

```
[New email arrives]
         ↓
[AI classification]
  - Urgent (client, boss, deadline)
  - Newsletter (marketing, updates)
  - Follow-up (waiting for reply)
  - FYI (info only)
  - Spam (unwanted)
         ↓
[Auto-actions]
  - Urgent → Star + Notify
  - Newsletter → Archive + Label
  - Follow-up → Add to task list
  - FYI → Mark read
         ↓
[Draft responses]
  - Common requests
  - Meeting scheduling
  - Status updates
         ↓
[Daily digest]
  - Summary to Telegram
  - Action items highlighted
```

## Prerequisites

- OpenClaw installed
- gog CLI (Gmail access)
- Telegram bot (for notifications)

## Step 1: Email Classifier

`scripts/email-triage/classify.py`:

```python
#!/usr/bin/env python3
"""
Classify emails using AI
Usage: python3 classify.py <email_json>
"""

import json
import sys

def classify_email(email_data):
    """Use AI to classify email"""
    
    prompt = f"""Classify this email into one category:

From: {email_data['from']}
Subject: {email_data['subject']}
Body: {email_data['body'][:500]}

Categories:
1. URGENT - Needs immediate attention (client, boss, deadline, problem)
2. NEWSLETTER - Marketing, updates, subscriptions
3. FOLLOW_UP - Waiting for your reply or follow-up needed
4. FYI - Information only, no action needed
5. SPAM - Unwanted, promotional

Respond in JSON format:
{{
  "category": "urgent|newsletter|follow_up|fyi|spam",
  "confidence": 0-100,
  "reason": "why this category",
  "action": "star|archive|reply|read|delete",
  "priority": "high|medium|low",
  "suggested_response": "draft reply if applicable"
}}"""

    # Call AI model
    result = call_ai_model(prompt)
    return json.loads(result)

def main():
    # Read email from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            email = json.load(f)
    else:
        email = json.load(sys.stdin)
    
    classification = classify_email(email)
    print(json.dumps(classification, indent=2))

if __name__ == "__main__":
    main()
```

## Step 2: Fetch and Process

`scripts/email-triage/process-inbox.sh`:

```bash
#!/bin/bash
# Process inbox and auto-triage emails

LOG_FILE="/var/log/email-triage.log"

log() {
    echo "[$(date)] $1" | tee -a "$LOG_FILE"
}

process_emails() {
    log "🔍 Checking inbox..."
    
    # Fetch unread emails
    emails=$(gog gmail search "is:unread" --max=50 --json)
    
    count=$(echo "$emails" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
    log "📧 Found $count unread emails"
    
    # Process each email
    echo "$emails" | python3 -c "
import sys
import json
import subprocess

emails = json.load(sys.stdin)
results = {'urgent': 0, 'newsletter': 0, 'follow_up': 0, 'fyi': 0, 'spam': 0}

for email in emails:
    # Classify
    result = subprocess.run(
        ['python3', 'scripts/email-triage/classify.py'],
        input=json.dumps(email),
        capture_output=True,
        text=True
    )
    
    classification = json.loads(result.stdout)
    category = classification['category']
    results[category] += 1
    
    # Take action
    msg_id = email['id']
    action = classification['action']
    
    if action == 'star':
        subprocess.run(['gog', 'gmail', 'modify', msg_id, '--add-label', 'STARRED'])
    elif action == 'archive':
        subprocess.run(['gog', 'gmail', 'modify', msg_id, '--remove-label', 'INBOX'])
    elif action == 'read':
        subprocess.run(['gog', 'gmail', 'modify', msg_id, '--remove-label', 'UNREAD'])
    
    print(f'Processed: {email[\"subject\"][:50]}... → {category}')

print(json.dumps(results))
"
}

# Run processing
process_emails
log "✅ Processing complete"
```

## Step 3: Daily Digest

`scripts/email-triage/daily-digest.py`:

```python
#!/usr/bin/env python3
"""
Generate daily email digest
Usage: python3 daily-digest.py
"""

import subprocess
import json
from datetime import datetime

def fetch_important_emails():
    """Fetch starred/important emails"""
    result = subprocess.run(
        ["gog", "gmail", "search", "is:starred OR is:important", "--max=20", "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def fetch_todays_emails():
    """Fetch today's emails"""
    result = subprocess.run(
        ["gog", "gmail", "search", "newer_than:1d", "--max=50", "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def generate_digest():
    """Generate digest message"""
    
    important = fetch_important_emails()
    today = fetch_todays_emails()
    
    message = f"📧 *Email Digest - {datetime.now().strftime('%A, %d %B')}*\n\n"
    
    # Important emails
    if important:
        message += f"⭐ *Important ({len(important)}):*\n"
        for email in important[:5]:
            sender = email['from'].split('<')[0].strip()
            subject = email['subject'][:40]
            message += f"• {subject} - _{sender}_\n"
        message += "\n"
    
    # Today's summary
    message += f"📊 *Today's Summary:*\n"
    message += f"• Total received: {len(today)}\n"
    message += f"• Important: {len(important)}\n"
    message += f"• Need reply: {len([e for e in today if 'Re:' not in e['subject']])}\n"
    
    return message

def send_to_telegram(message):
    """Send digest to Telegram"""
    import os
    import requests
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    })

if __name__ == "__main__":
    digest = generate_digest()
    print(digest)
    send_to_telegram(digest)
```

## Step 4: Auto-Reply Drafts

`scripts/email-triage/draft-replies.py`:

```python
#!/usr/bin/env python3
"""
Draft replies for common email types
"""

import json
import subprocess

def draft_reply(email, classification):
    """Generate draft reply using AI"""
    
    prompt = f"""Draft a professional email reply:

Original email:
From: {email['from']}
Subject: {email['subject']}
Body: {email['body'][:300]}

Category: {classification['category']}

Draft a concise, professional reply. Keep it brief but helpful."""

    reply = call_ai_model(prompt)
    return reply

def create_draft(email_id, reply_body):
    """Create Gmail draft"""
    subprocess.run([
        "gog", "gmail", "draft",
        "--reply-to", email_id,
        "--body", reply_body
    ])

# Usage: Process emails marked for reply
```

## Step 5: Complete Setup

`scripts/email-triage/setup.sh`:

```bash
#!/bin/bash
# Setup email triage automation

echo "📧 Setting up Smart Email Triage..."

# Create directories
mkdir -p scripts/email-triage
mkdir -p /var/log

# Make scripts executable
chmod +x scripts/email-triage/*.py
chmod +x scripts/email-triage/*.sh

# Add cron jobs
echo "Adding cron schedules..."
(
crontab -l 2>/dev/null
cat << 'EOF'

# Email triage - every 30 minutes
*/30 * * * * /root/.openclaw/workspace/scripts/email-triage/process-inbox.sh >> /var/log/email-triage.log 2>&1

# Daily digest - 8 AM
0 8 * * * /usr/bin/python3 /root/.openclaw/workspace/scripts/email-triage/daily-digest.py >> /var/log/email-triage.log 2>&1
EOF
) | crontab -

echo "✅ Setup complete!"
echo "📊 Check logs: tail -f /var/log/email-triage.log"
```

## Example Output

**Telegram Digest:**
```
📧 *Email Digest - Monday, 08 March*

⭐ *Important (3):*
• Project proposal feedback needed - _Client ABC_
• Q1 review meeting tomorrow - _Boss_
• Invoice payment reminder - _Finance_

📊 *Today's Summary:*
• Total received: 23
• Important: 3
• Need reply: 7
```

**Processing Log:**
```
[2026-03-08 09:00:01] 🔍 Checking inbox...
[2026-03-08 09:00:03] 📧 Found 12 unread emails
Processed: Newsletter: March Updates → newsletter
Processed: RE: Project Timeline → follow_up
Processed: 🚨 URGENT: Server Down → urgent
Processed: Your Amazon order... → fyi
[2026-03-08 09:00:15] ✅ Processing complete
```

## Advanced Features

### Sender-based Rules

```python
VIP_SENDERS = ['boss@company.com', 'client@vip.com']

def check_vip(email):
    if any(vip in email['from'] for vip in VIP_SENDERS):
        return {'category': 'urgent', 'action': 'star'}
```

### Thread Tracking

```python
def is_follow_up(email):
    # Check if email is part of existing thread
    if 'Re:' in email['subject'] or email.get('threadId'):
        return True
```

## Conclusion

You now have automated email management that:
- ✅ Classifies emails with AI
- ✅ Auto-archives newsletters
- ✅ Stars urgent messages
- ✅ Sends daily digests

**Next Steps:**
- Add calendar integration for meeting emails
- Build unsubscribe automation
- Create email analytics dashboard

---

*Tutorial created for OpenClaw Sumopod*
