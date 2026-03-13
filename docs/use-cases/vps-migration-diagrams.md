# Migration Workflow Visual Guide

## Complete Migration Flow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e1f5fe', 'primaryTextColor': '#01579b', 'primaryBorderColor': '#0288d1', 'lineColor': '#0288d1', 'secondaryColor': '#fff3e0', 'tertiaryColor': '#e8f5e9'}}}%%
flowchart TB
    subgraph Phase1["📦 Phase 1: Preparation"]
        P1A[Export Source Code] ==> P1B[Export Database]
        P1B ==> P1C[Document Environment Variables]
    end
    
    subgraph Phase2["🚚 Phase 2: Transfer"]
        P2A[Clone to VPS /var/www/] ==> P2B[Transfer Database Backup]
        P2B ==> P2C[Install Dependencies]
    end
    
    subgraph Phase3["⚙️ Phase 3: Configuration"]
        P3A[Configure .env Files] ==> P3B[Import Database]
        P3B ==> P3C[Build Applications]
    end
    
    subgraph Phase4["🚀 Phase 4: Deployment"]
        P4A[Start with PM2] ==> P4B[Configure Nginx]
        P4B ==> P4C[Setup SSL]
    end
    
    subgraph Phase5["🔒 Phase 5: Security"]
        P5A[Enable Firewall] ==> P5B[Secure .env Files]
        P5B ==> P5C[Database Localhost Only]
        P5C ==> P5D[Auto-renew SSL]
    end
    
    Phase1 ==> Phase2 ==> Phase3 ==> Phase4 ==> Phase5
    
    style Phase1 fill:#e3f2fd
    style Phase2 fill:#fff3e0
    style Phase3 fill:#e8f5e9
    style Phase4 fill:#fce4ec
    style Phase5 fill:#f3e5f5
```

---

## Security Architecture

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TB
    subgraph Internet["🌐 Internet"]
        User[User Browser]
        Attacker[❌ Potential Attacker]
    end
    
    subgraph Perimeter["🛡️ Security Perimeter"]
        DNS[DNS Records]
        SSL[SSL/TLS Encryption]
        UFW[UFW Firewall]
    end
    
    subgraph DMZ["📡 DMZ (Services)"]
        Nginx[Nginx Reverse Proxy]
    end
    
    subgraph Internal["🔐 Internal Network"]
        subgraph Apps["Applications (PM2)"]
            A1[App 1 :5000]
            A2[App 2 :5001]
            A3[App 3 :5002]
        end
        
        subgraph Data["Data Layer"]
            PG[PostgreSQL :5432]
            SQLite[SQLite Files]
        end
    end
    
    User -->|HTTPS 443| DNS
    DNS -->|SSL Termination| UFW
    UFW -->|Allow 80/443| Nginx
    Nginx -->|Proxy| A1
    Nginx -->|Proxy| A2
    Nginx -->|Proxy| A3
    A1 -->|Localhost| PG
    A2 -->|Localhost| SQLite
    A3 -->|Localhost| PG
    
    Attacker -->|Port 5432| UFW
    UFW -->|❌ DENY| Attacker
    
    style Attacker fill:#ffcdd2
    style UFW fill:#c8e6c9
    style PG fill:#fff9c4
```

---

## Database Migration Strategies

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    subgraph SourceDB["Source Database"]
        PG1[(PostgreSQL)]
        SQL1[(SQLite)]
    end
    
    subgraph Method["Migration Method"]
        M1[pg_dump & psql]
        M2[File Copy]
        M3[Python Converter]
    end
    
    subgraph TargetDB["Target Database"]
        PG2[(PostgreSQL)]
        SQL2[(SQLite)]
    end
    
    PG1 -->|pg_dump| M1 -->|psql| PG2
    SQL1 -->|cp| M2 -->|direct| SQL2
    PG1 -->|Python script| M3 -->|INSERT| SQL2
    
    style M1 fill:#e3f2fd
    style M2 fill:#fff3e0
    style M3 fill:#e8f5e9
```

---

## SSL Certificate Lifecycle

```mermaid
%%{init: {'theme': 'base'}}%%
sequenceDiagram
    participant App as Application
    participant Cert as Certbot
    participant LE as Let's Encrypt
    participant Nginx as Nginx Server
    participant User as User Browser
    
    Note over App,User: Initial Setup
    App->>Cert: Request certificate
    Cert->>LE: Validate domain
    LE->>Cert: Issue certificate
    Cert->>Nginx: Install certificate
    
    Note over App,User: Daily Operation
    User->>Nginx: HTTPS request
    Nginx->>User: Encrypted response
    
    Note over App,User: Auto-Renewal (every 60 days)
    Cert->>Cert: Check expiry
    Cert->>LE: Renew request
    LE->>Cert: New certificate
    Cert->>Nginx: Update certificate
```

---

## Troubleshooting Decision Tree

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[❌ App Not Accessible] --> B{Check PM2 Status}
    B -->|Stopped| C[pm2 restart app]
    B -->|Running| D{Check Port Listening}
    
    D -->|Not Listening| E[Check App Logs]
    E -->|Error| F[Fix Error & Restart]
    E -->|No Error| G[Check Environment]
    
    D -->|Listening| H{Check Firewall}
    H -->|Blocked| I[ufw allow PORT]
    H -->|Allowed| J{Check Nginx}
    
    J -->|Config Error| K[nginx -t & Fix]
    J -->|OK| L{Check SSL}
    
    L -->|Expired| M[certbot renew]
    L -->|OK| N[Check DNS Propagation]
    
    C --> O[✅ Fixed!]
    F --> O
    I --> O
    K --> O
    M --> O
    
    style A fill:#ffcdd2
    style O fill:#c8e6c9
    style C fill:#fff9c4
    style F fill:#fff9c4
    style I fill:#fff9c4
    style K fill:#fff9c4
    style M fill:#fff9c4
```

---

## Complete Infrastructure Map

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '14px'}}}%%
flowchart TB
    subgraph Cloud["☁️ Cloud Infrastructure"]
        subgraph DNS["DNS Layer"]
            D1[example.com]
            D2[app1.example.com]
            D3[app2.example.com]
        end
        
        subgraph CDN["SSL/HTTPS"]
            SSL1[Let's Encrypt]
        end
    end
    
    subgraph VPS["🖥️ VPS (Your Server)"]
        subgraph Network["Network Layer"]
            FW[UFW Firewall
            SSH_PORT, 80, 443 ALLOW
            5432 DENY]
        end
        
        subgraph Proxy["Reverse Proxy"]
            NG[Nginx
            / → :5000
            /app1 → :5001
            /app2 → :5002]
        end
        
        subgraph Runtime["Runtime"]
            PM2[PM2 Process Manager]
            A1[Dashboard App
            Node.js :5000]
            A2[Survey App
            Node.js :5001]
            A3[Inventory App
            Node.js :5002]
        end
        
        subgraph Storage["Storage"]
            DB1[(PostgreSQL
            app1_database)]
            DB2[(PostgreSQL
            app2_database)]
            DB3[(SQLite
            app3.db)]
        end
        
        subgraph Security["Security"]
            ENV[.env files
            chmod 600]
            LOG[Log Rotation]
        end
    end
    
    D1 --> FW
    D2 --> FW
    D3 --> FW
    SSL1 --> NG
    FW --> NG
    NG --> A1
    NG --> A2
    NG --> A3
    PM2 --> A1
    PM2 --> A2
    PM2 --> A3
    A1 --> DB2
    A2 --> DB3
    A3 --> DB1
    
    style FW fill:#ffcdd2
    style NG fill:#e3f2fd
    style PM2 fill:#fff3e0
    style DB1 fill:#e8f5e9
    style DB2 fill:#e8f5e9
    style DB3 fill:#e8f5e9
```

---

*Generated: March 13, 2026*
