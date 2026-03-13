# OpenClaw + n8n Integration Tutorial

Connect OpenClaw to 400+ apps via n8n workflow automation. No coding required.

## Why n8n + OpenClaw?

### The Problem

![Without n8n](images/n8n-architecture.png)
*Without n8n: Each integration needs custom code and separate OAuth setup*

**Problems:**
- ❌ Each integration needs custom code
- ❌ OAuth setup for every service
- ❌ Maintenance nightmare
- ❌ Hard to modify workflows

### The Solution

![n8n Solution](images/n8n-architecture.png)
*With n8n: One connection, unlimited integrations via visual workflow builder*

**Benefits:**
- ✅ One connection, unlimited integrations
- ✅ Visual drag-and-drop builder
- ✅ No code required
- ✅ Easy to modify

## Example Workflow: Email to Slack

![Email Workflow](images/n8n-email-workflow.png)
*Example: Gmail → Filter → Slack → OpenClaw Summary*

## Architecture: Who's Backend, Who's Frontend?

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e3f2fd', 'primaryTextColor': '#1565c0'}}}%%
flowchart TB
    subgraph User["👤 User Layer"]
        TG["💬 Telegram"]
        WEB["🌐 Web UI"]
        MOB["📱 Mobile"]
    end
    
    subgraph Frontend["🎭 Frontend: OpenClaw"]
        OC["🤖 OpenClaw Agent"]
        NL["💬 Natural Language"]
        INT["🎯 Intent Routing"]
    end
    
    subgraph Orchestrator["⚙️ Orchestrator: n8n"]
        N8N["🔄 n8n Workflow Engine"]
        TRIG["⚡ Triggers"]
        ACT["🔧 Actions"]
        LOGIC["🧩 Logic/Conditions"]
    end
    
    subgraph Backend["☁️ Backend Services"]
        GM["📧 Gmail API"]
        GD["☁️ Google Drive"]
        SL["💬 Slack API"]
        NT["📝 Notion API"]
        AT["📊 Airtable"]
    end
    
    TG --> OC
    WEB --> OC
    MOB --> OC
    
    OC -->|API/Webhook| N8N
    
    N8N --> TRIG
    N8N --> ACT
    N8N --> LOGIC
    
    ACT --> GM
    ACT --> GD
    ACT --> SL
    ACT --> NT
    ACT --> AT
    
    style User fill:#e3f2fd,stroke:#1976d2
    style Frontend fill:#fff3e0,stroke:#f57c00
    style Orchestrator fill:#c8e6c9,stroke:#388e3c
    style Backend fill:#f3e5f5,stroke:#9c27b0
```

**Summary:**
| Layer | Role | Example |
|-------|------|---------|
| **User Layer** | Interface | Telegram chat |
| **Frontend** | AI Assistant | OpenClaw/Radit |
| **Orchestrator** | Workflow Engine | n8n |
| **Backend** | Service APIs | Gmail, Slack, Notion |

## What You Can Build

### 🔄 Two-Way Communication Flow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e8f5e9', 'primaryTextColor': '#2e7d32'}}}%%
flowchart LR
    subgraph Request["📤 Outgoing Request"]
        U1["👤 User Request"]
        OC1["🤖 OpenClaw"]
        N8N1["🔄 n8n"]
        API1["☁️ External API"]
    end
    
    subgraph Response["📥 Incoming Response"]
        API2["☁️ API Result"]
        N8N2["🔄 n8n Process"]
        OC2["🤖 OpenClaw Format"]
        U2["👤 User Gets Answer"]
    end
    
    U1 -->|"Send email"| OC1
    OC1 -->|Webhook| N8N1
    N8N1 -->|Call| API1
    
    API1 -->|Result| API2
    API2 -->|Parse| N8N2
    N8N2 -->|JSON| OC2
    OC2 -->|💬 Message| U2
    
    style Request fill:#e3f2fd,stroke:#1976d2
    style Response fill:#c8e6c9,stroke:#388e3c
```

### Example 1: Email to Slack Notification

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Gmail   │────▶│    n8n   │────▶│  Filter  │────▶│  Slack   │
│  (New    │     │  Trigger │     │ (AI/Key  │     │ (Notify  │
│   Email) │     │          │     │  words)  │     │  Team)   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                        │
                    ┌───────────────────────────────────┘
                    ▼
            ┌──────────────┐
            │  OpenClaw    │
            │  (Summary    │
            │   Report)    │
            └──────────────┘
```

**Flow:**
1. New email arrives in Gmail
2. n8n detects it (trigger)
3. Filter: Only urgent emails (from boss, contains "ASAP")
4. Send Slack notification to team
5. OpenClaw generates daily summary

### Example 2: Form to Database to Notification

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Google  │────▶│    n8n   │────▶│  Google  │────▶│  Email   │
│  Form    │     │  (Parse  │     │  Sheets  │     │ (Confirm │
│(Response)│     │   Data)  │     │ (Store)  │     │  User)   │
└──────────┘     └────┬─────┘     └──────────┘     └──────────┘
                      │
                      ▼
               ┌────────────┐
               │  OpenClaw  │
               │ (Process   │
               │   Request) │
               └────────────┘
```

**Flow:**
1. User submits Google Form (RFQ/tender)
2. n8n parses form data
3. Store in Google Sheets (CRM)
4. Send confirmation email to user
5. OpenClaw reviews and drafts response

### Example 3: Multi-Step Approval Workflow

```
┌──────────┐
│  Request │
│  Created │
└────┬─────┘
     │
     ▼
┌──────────┐     ┌──────────┐
│   n8n    │────▶│ Manager  │
│  (Route  │     │ Approval │
│   Task)  │     └────┬─────┘
└──────────┘          │
                      ▼
               ┌──────────┐
               │ Approved?│
               └────┬─────┘
                    │
           ┌────────┴────────┐
           │                 │
           ▼                 ▼
     ┌──────────┐      ┌──────────┐
     │   Yes    │      │    No    │
     │          │      │          │
     ▼          │      ▼          │
┌──────────┐   │  ┌──────────┐   │
│ Execute  │   │  │  Notify  │   │
│  Task    │   │  │  User    │   │
└──────────┘   │  └──────────┘   │
               │                 │
               └────────┬────────┘
                        │
                        ▼
                 ┌────────────┐
                 │  OpenClaw  │
                 │  (Final    │
                 │   Report)  │
                 └────────────┘
```

## Step-by-Step Setup

### Step 1: Install n8n

**Option A: Self-Host (Recommended for privacy)**

```bash
# Using Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Option B: Cloud (n8n.io)**
- Sign up at https://n8n.io/cloud
- Free tier: 1,000 executions/month
- No setup required

### Step 2: Create First Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    n8n Editor                            │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │  1. ADD TRIGGER                                  │    │
│  │     Click [+] → Search "Webhook" → Select        │    │
│  │                                                  │    │
│  │     [Webhook] ──────►                            │    │
│  │     URL: https://n8n.yourdomain/webhook/xxx      │    │
│  └─────────────────────────────────────────────────┘    │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │  2. ADD ACTION                                   │    │
│  │     Click [+] → Search "Gmail" → Send Email      │    │
│  │                                                  │    │
│  │     [Webhook] ────► [Gmail]                      │    │
│  │     (Trigger)       (Send Email)                 │    │
│  └─────────────────────────────────────────────────┘    │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │  3. ADD MORE ACTIONS                             │    │
│  │     Keep adding nodes as needed                  │    │
│  │                                                  │    │
│  │     [Webhook] ────► [Gmail] ────► [Slack]       │    │
│  │     (Trigger)       (Email)       (Notify)      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  [💾 Save]  [▶️ Execute]  [🚀 Activate]                   │
└─────────────────────────────────────────────────────────┘
```

### Step 3: Connect OpenClaw to n8n

**Method A: Webhook (Simple)**

```python
# In OpenClaw, call n8n webhook
import requests

n8n_webhook_url = "https://n8n.yourdomain/webhook/abc123"

data = {
    "message": "New task from user",
    "sender": "user@example.com",
    "priority": "high"
}

response = requests.post(n8n_webhook_url, json=data)
```

**Method B: n8n Node (Advanced)**

```
┌─────────────────────────────────────────────────────────┐
│  n8n HTTP Request Node                                   │
│                                                          │
│  Method: POST                                            │
│  URL: https://api.openclaw.ai/v1/execute                │
│  Headers:                                                │
│    Authorization: Bearer YOUR_TOKEN                     │
│  Body:                                                   │
│    {                                                     │
│      "agent": "radit",                                   │
│      "task": "Analyze this email"                       │
│    }                                                     │
└─────────────────────────────────────────────────────────┘
```

### Step 4: Two-Way Communication

```
┌─────────────────────────────────────────────────────────┐
│              TWO-WAY INTEGRATION FLOW                    │
│                                                          │
│  ┌─────────┐              ┌─────────┐              ┌────┴────┐ │
│  │  User   │─────────────▶│ OpenClaw│─────────────▶│   n8n   │ │
│  │ Request │  "Send email │ Process │  "Execute   │ Workflow│ │
│  │         │   via n8n"  │ Intent  │   workflow"  │         │ │
│  └─────────┘              └────┬────┘              └────┬────┘ │
│                                │                        │       │
│                                │                        ▼       │
│                                │               ┌─────────────┐  │
│                                │               │  Call APIs  │  │
│                                │               │  (Gmail,    │  │
│                                │               │   Slack...) │  │
│                                │               └──────┬──────┘  │
│                                │                      │         │
│                                │                      ▼         │
│                                │               ┌─────────────┐  │
│                                └───────────────│   Result    │  │
│                                                │   Back      │  │
│                                                └─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Popular Use Cases

### 📊 Use Case Pipeline Overview

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fff3e0', 'primaryTextColor': '#e65100'}}}%%
flowchart TB
    subgraph Email["📧 Email Processing"]
        E1["Gmail Trigger"] --> E2["AI Filter"]
        E2 --> E3{Urgent?}
        E3 -->|Yes| E4["Slack + OpenClaw"]
        E3 -->|No| E5["Archive"]
    end
    
    subgraph Form["📝 Form Automation"]
        F1["Google Form"] --> F2["Validate"]
        F2 --> F3["Save to Sheets"]
        F3 --> F4["Send Email"]
        F4 --> F5["OpenClam Summary"]
    end
    
    subgraph Social["📱 Social Monitoring"]
        S1["Twitter Mention"] --> S2["Analyze"]
        S2 --> S3{Sentiment}
        S3 -->|😊 Positive| S4["Thank You"]
        S3 -->|😐 Neutral| S5["Ignore"]
        S3 -->|😠 Negative| S6["Alert Team"]
    end
    
    style Email fill:#ffcdd2,stroke:#d32f2f
    style Form fill:#c8e6c9,stroke:#388e3c
    style Social fill:#e1f5fe,stroke:#0288d1
```

### 1. Email Processing Pipeline

```
[GMail Trigger] → [AI Filter] → [Classify] → [Route]
                      │              │           │
                      ▼              ▼           ▼
               [Newsletter]   [Urgent]     [Routine]
                    │              │           │
                    ▼              ▼           ▼
               [Mark Read]   [Slack +     [Auto-
                             OpenClaw]    Reply]
```

### 2. Data Entry Automation

```
[Form Submission] → [Validate] → [Save to DB] → [Notify]
                                          │
                                          ▼
                                    [OpenClaw Summary]
```

### 3. Social Media Monitoring

```
[Twitter Mention] → [Analyze] → [Sentiment] → [Action]
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
              [Positive]            [Neutral]            [Negative]
                  │                     │                     │
                  ▼                     ▼                     ▼
            [Thank You]            [Ignore]            [Alert + 
                                                          Response]
```

## Security Best Practices

```
┌─────────────────────────────────────────────────────────┐
│                    SECURITY LAYER                        │
│                                                          │
│  1. API KEYS (n8n Credentials)                          │
│     └─► Encrypted storage                                 │
│     └─► Never expose in workflows                         │
│                                                          │
│  2. WEBHOOK SECURITY                                     │
│     └─► Use random URLs                                   │
│     └─► Add authentication headers                        │
│     └─► IP whitelist                                      │
│                                                          │
│  3. DATA FLOW                                            │
│     └─► Validate all inputs                               │
│     └─► Sanitize before sending to APIs                   │
│     └─► Log for audit                                     │
│                                                          │
│  4. ACCESS CONTROL                                       │
│     └─► Restrict n8n dashboard access                     │
│     └─► Use strong passwords                              │
│     └─► Enable 2FA                                        │
└─────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Webhook Not Triggering?

```
✓ Check URL is correct
✓ Verify workflow is "Active"
✓ Check n8n execution logs
✓ Test with curl:
  curl -X POST https://n8n.yourdomain/webhook/xxx \
    -H "Content-Type: application/json" \
    -d '{"test":"data"}'
```

### Authentication Errors?

```
✓ Re-connect credentials in n8n
✓ Check API scopes/permissions
✓ Verify token not expired
✓ Check service status page
```

### Data Not Passing?

```
✓ Check field names match
✓ Verify data types (string vs number)
✓ Use "Set" node to transform data
✓ Add "Function" node for custom logic
```

## Quick Reference

| Task | n8n Node | OpenClaw Role |
|------|----------|---------------|
| Send Email | Gmail / SendGrid | Trigger / Review |
| Save to Spreadsheet | Google Sheets | Analyze data |
| Post to Slack | Slack | Notify team |
| Create Task | Todoist / Asana | Prioritize |
| Store File | Google Drive / Dropbox | Organize |
| Database Query | PostgreSQL / MySQL | Query builder |
| API Call | HTTP Request | Natural language |
| Schedule Task | Cron / Schedule | Set reminders |

## Next Steps

1. **Install n8n** (self-host or cloud)
2. **Create first workflow** (webhook → email)
3. **Connect OpenClaw** (call webhook from agent)
4. **Build complex flows** (multi-step automations)
5. **Monitor & optimize** (check execution logs)

## Resources

- [n8n Documentation](https://docs.n8n.io)
- [n8n Community](https://community.n8n.io)
- [Workflow Templates](https://n8n.io/workflows)
- [OpenClaw API Docs](https://docs.openclaw.ai)

---

**Tutorial Version:** 1.0  
**Last Updated:** 2026-03-08  
**Compatible With:** OpenClaw 2026.2+, n8n 1.0+
