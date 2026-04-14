# OpenClaw MCP Server Setup
## Connect Your AI Assistant to Google Workspace, Notion, GitHub, and 100+ Other Tools

> **Reading Time:** 20 minutes
> **Difficulty:** Intermediate
> **Prerequisite:** OpenClaw Gateway installed and running
> **Version:** OpenClaw v2025+

---

## What is an MCP Server

Think of MCP (Model Context Protocol) as a universal adapter for your AI assistant. Instead of your AI assistant talking directly to every single app you use, it talks to one central hub, and that hub connects to all your other apps.

This is a massive improvement over the old way of doing things. Before MCP, integrating a new tool meant writing custom code every single time. With MCP, you just install a server and your AI assistant can immediately use it.

```mermaid
flowchart TD
    subgraph Traditional["Traditional Setup (Messy)"]
        A1[AI Assistant] --> G1[Google Calendar]
        A1 --> G2[Gmail]
        A1 --> G3[Notion]
        A1 --> G4[GitHub]
        A1 --> G5[Slack]
    end
    
    subgraph MCP["With MCP (Clean)"]
        A2[AI Assistant] --> M[MCP Hub]
        M --> C1[Google Calendar]
        M --> C2[Gmail]
        M --> C3[Notion]
        M --> C4[GitHub]
        M --> C5[Slack]
    end
    
    style A1 fill:#ef9a9a,stroke:#c62828
    style A2 fill:#e8f5e9,stroke:#2e7d32
    style M fill:#1565c0,stroke:#0d47a1,color:#fff
```

OpenClaw already acts as an MCP server. When you run `openclaw mcp serve`, your AI assistant becomes available to any MCP-compatible client like Claude Code or Codex.

But this guide is about the other direction: connecting external MCP servers TO your OpenClaw assistant, so your assistant can use tools from Google Workspace, Notion, GitHub, and hundreds of other platforms.

---

## Why MCP Changes Everything

Here is what makes MCP special.

**Standardized connections.** Before MCP, every AI tool integration was custom work. Companies would spend months building integrations that barely worked. MCP standardizes how AI assistants connect to external tools. One integration works across every MCP-compatible AI.

**Tool calling made reliable.** MCP gives your AI assistant structured tool definitions with clear input schemas. Instead of the AI guessing how to call an API, MCP tells it exactly what tools exist, what arguments they need, and what they return.

**Session isolation.** Each MCP server connection is isolated. If one integration breaks, it does not take down your entire assistant. You can hot-swap servers without restarting everything.

**No more API gymnastics.** You do not need to write code to connect your calendar. You install the Google Calendar MCP server, configure it once, and your AI assistant can read and write to your calendar immediately.

---

## How MCP Works in OpenClaw

OpenClaw supports MCP servers in two directions.

```mermaid
flowchart LR
    subgraph outbound["OpenClaw as MCP Client"]
        A[OpenClaw<br/>Gateway] -->|uses| B[MCP Servers]
        B --> C1[Google Calendar]
        B --> C2[Notion]
        B --> C3[GitHub]
        B --> C4[Slack]
    end
    
    subgraph inbound["OpenClaw as MCP Server"]
        D[Claude Code] -->|connects to| E[openclaw mcp serve]
        F[Codex] -->|connects to| E
    end
    
    style A fill:#1565c0,stroke:#0d47a1,color:#fff
    style E fill:#1565c0,stroke:#0d47a1,color:#fff
```

**Outbound (MCP Client):** Your OpenClaw Gateway connects to external MCP servers and uses their tools. This is what this guide covers.

**Inbound (MCP Server):** Your OpenClaw Gateway runs as an MCP server that Claude Code or Codex can connect to. This is covered in the OpenClaw Gateway Setup guide.

---

## Step 1: Check Your Gateway Version

Before you start, make sure your OpenClaw installation supports MCP servers.

```bash
openclaw --version
```

You need version 2025.1 or later for full MCP support. If you have an older version:

```bash
npm update -g openclaw
```

Verify MCP is available:

```bash
openclaw mcp --help
```

If you see a list of MCP commands, you are good to go.

---

## Step 2: Install Your First MCP Server

The easiest first MCP server to install is the filesystem server. It lets your AI assistant read and write files on your machine.

### Install via openclaw mcp Command

```bash
openclaw mcp add filesystem -- npx @modelcontextprotocol/server-filesystem /path/to/directory
```

This installs the official MCP filesystem server and grants it access to a specific directory.

For Google Workspace access, you would install the Google Calendar MCP server:

```bash
openclaw mcp add google-calendar -- npx @modelcontextprotocol/server-google-calendar
```

### Understanding the Command Structure

The `openclaw mcp add` command follows this pattern:

```bash
openclaw mcp add [name] -- [command to run]
```

- `[name]` is what you call this MCP server inside OpenClaw
- `--` separates the name from the actual server command
- The command is usually `npx` followed by the MCP server package name
- Some servers take additional arguments like directory paths

### Verify the Server is Installed

```bash
openclaw mcp list
```

You should see your new server listed. It should show as disconnected until you restart the gateway.

---

## Step 3: Configure MCP Servers in Your Config File

For more control, add MCP servers directly to your Openclaw config file.

Open your config file at `~/.openclaw/openclaw.json`:

```json5
{
  mcp: {
    servers: {
      filesystem: {
        command: "npx",
        args: ["@modelcontextprotocol/server-filesystem", "/path/to/directory"],
        env: {}
      },
      google-calendar: {
        command: "npx",
        args: ["@modelcontextprotocol/server-google-calendar"],
        env: {
          GOOGLECALENDAR_CREDENTIALS_PATH: "/path/to/credentials.json"
        }
      }
    }
  }
}
```

The config file approach gives you more control over environment variables and arguments.

```mermaid
flowchart TD
    A[Add MCP Server to Config] --> B[Restart Gateway]
    B --> C[Server Connects]
    C --> D[Tools Available to AI]
    D --> E[Use in Chat or Code]
    
    style D fill:#e8f5e9,stroke:#2e7d32
```

---

## Step 4: Connect Google Workspace (Gmail + Calendar)

This is the integration most people want first. Here is how to connect Gmail and Google Calendar.

### Google Calendar MCP Server

First, you need Google Cloud credentials.

1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Go to **Credentials** and create an **OAuth 2.0 Client ID**
5. Download the JSON credentials file
6. Save it somewhere safe on your machine

Install and configure the server:

```bash
openclaw mcp add google-calendar -- npx @modelcontextprotocol/server-google-calendar
```

Set the credentials path in your environment or config:

```json5
{
  mcp: {
    servers: {
      google-calendar: {
        command: "npx",
        args: ["@modelcontextprotocol/server-google-calendar"],
        env: {
          GOOGLECALENDAR_CREDENTIALS_PATH: "/home/user/.config/google-calendar-credentials.json"
        }
      }
    }
  }
}
```

### Gmail MCP Server

For Gmail access, install the Gmail MCP server:

```bash
openclaw mcp add gmail -- npx @modelcontextprotocol/server-gmail
```

Gmail requires a similar OAuth setup through Google Cloud Console. You need to enable the Gmail API and download credentials.

```json5
{
  mcp: {
    servers: {
      gmail: {
        command: "npx",
        args: ["@modelcontextprotocol/server-gmail"],
        env: {
          GMAIL_CREDENTIALS_PATH: "/home/user/.config/gmail-credentials.json"
        }
      }
    }
  }
}
```

### Restart and Test

After adding the servers to your config, restart the gateway:

```bash
openclaw gateway restart
```

Test by asking your assistant: "What meetings do I have today?" or "Send an email to John saying hello."

---

## Step 5: Connect Notion

Notion is a popular workspace for notes, databases, and project management. Here is how to connect it.

### Create a Notion Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **New integration**
3. Give it a name (this is what Notion shows when asking for permission)
4. Select the workspace
5. Under **Capabilities**, check what you need (Read content, Update content, Insert content)
6. Click **Submit** and copy the **Internal Integration Token**

### Install the Notion MCP Server

```bash
openclaw mcp add notion -- npx @modelcontextprotocol/server-notion
```

Configure with your token:

```json5
{
  mcp: {
    servers: {
      notion: {
        command: "npx",
        args: ["@modelcontextprotocol/server-notion"],
        env: {
          NOTION_API_KEY: "secret_xxxxxxxxxxxxxx"
        }
      }
    }
  }
}
```

### Link Your Notion Pages

After starting the gateway, you need to share specific Notion pages with your integration.

Open Notion, go to any page you want the assistant to access, click the **three dots menu**, then **Add connections**, and select your integration name.

---

## Step 6: Connect GitHub

For code-related work, GitHub integration is essential.

### Create a GitHub Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Give it a name and set an expiration
4. Select these scopes:
   - `repo` (full repository access)
   - `workflow` (if you need to manage GitHub Actions)
   - `read:user` (profile info)

Copy the generated token.

### Install the GitHub MCP Server

```bash
openclaw mcp add github -- npx @modelcontextprotocol/server-github
```

Configure:

```json5
{
  mcp: {
    servers: {
      github: {
        command: "npx",
        args: ["@modelcontextprotocol/server-github"],
        env: {
          GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"
        }
      }
    }
  }
}
```

Now your AI assistant can read repositories, create issues, manage pull requests, and more.

---

## Step 7: Connect Slack

For team communication, Slack integration lets your AI assistant post messages and respond to commands.

### Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and click **Create New App**
2. Choose **From scratch**
3. Give it a name and pick your workspace
4. Under **OAuth & Permissions**, scroll to **Bot Token Scopes**
5. Add these scopes:
   - `chat:write` (post messages)
   - `channels:history` (read channel history)
   - `channels:read` (list channels)
   - `groups:history` (private channel history)
   - `im:history` (DM history)
6. Scroll up and click **Install to Workspace**
7. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### Install the Slack MCP Server

```bash
openclaw mcp add slack -- npx @modelcontextprotocol/server-slack
```

Configure:

```json5
{
  mcp: {
    servers: {
      slack: {
        command: "npx",
        args: ["@modelcontextprotocol/server-slack"],
        env: {
          SLACK_BOT_TOKEN: "xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
          SLACK_TEAM_ID: "TXXXXXXXXX"
        }
      }
    }
  }
}
```

---

## Popular MCP Servers You Can Install

Here is a list of popular MCP servers and what they do:

```mermaid
flowchart LR
    subgraph productivity["Productivity"]
        GCal[Google Calendar]
        Gmail[Gmail]
        Notion[Notion]
        Slack[Slack]
    end
    
    subgraph code["Development"]
        GitHub[GitHub]
        GitLab[GitLab]
        Postgres[PostgreSQL]
        Redis[Redis]
    end
    
    subgraph storage["Storage"]
        Drive[Google Drive]
        Dropbox[Dropbox]
        S3[AWS S3]
    end
    
    subgraph ai["AI & Automation"]
        Puppeteer[Puppeteer]
        Brave[Brave Search]
        Fetch[Fetch / HTTP]
    end
    
    A[OpenClaw MCP Hub] --> productivity
    A --> code
    A --> storage
    A --> ai
    
    style A fill:#1565c0,stroke:#0d47a1,color:#fff
```

| Server | Package | What It Does |
|--------|---------|-------------|
| Google Calendar | `@modelcontextprotocol/server-google-calendar` | Read/write calendar events |
| Gmail | `@modelcontextprotocol/server-gmail` | Send and search emails |
| Notion | `@modelcontextprotocol/server-notion` | Read/write Notion pages and databases |
| GitHub | `@modelcontextprotocol/server-github` | Manage repos, issues, PRs |
| Slack | `@modelcontextprotocol/server-slack` | Post messages to channels |
| Google Drive | `@modelcontextprotocol/server-gdrive` | Access Drive files |
| Puppeteer | `@modelcontextprotocol/server-puppeteer` | Browser automation |
| Brave Search | `@modelcontextprotocol/server-brave-search` | Web search |
| PostgreSQL | `@modelcontextprotocol/server-postgres` | Database queries |
| Filesystem | `@modelcontextprotocol/server-filesystem` | Read/write local files |

You can install multiple MCP servers simultaneously. Your AI assistant picks which one to use based on what you ask for.

---

## Step 8: Run OpenClaw as an MCP Server

Now that your Gateway can use external MCP servers, you might also want to expose OpenClaw itself as an MCP server. This lets Claude Code or Codex connect to your running Gateway.

### Start the MCP Server

```bash
openclaw mcp serve
```

This starts OpenClaw as a stdio MCP server. The MCP client (Claude Code or Codex) owns this process.

### Connect from Claude Code

In your Claude Code session, configure the MCP server:

```bash
claude --mcp "openclaw,mcp,serve" --mcp-server openclaw
```

Or add it to your Claude Code config file:

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "openclaw",
      "args": ["mcp", "serve"]
    }
  }
}
```

### What Gets Exposed

When OpenClaw runs as an MCP server, it exposes:

- `conversations_list` - List recent conversations across all channels
- `messages_read` - Read transcript history for a conversation
- `events_poll` - Wait for new inbound messages
- `events_wait` - Block until the next event arrives
- `messages_send` - Send a reply through the same channel
- Approval tools - See and respond to approval requests

This means Claude Code can read your Telegram messages, WhatsApp conversations, and Discord DMs, then send responses back through those same channels.

---

## Security: Keep Your Tokens Safe

MCP servers often need API tokens and credentials. Treat these like passwords.

**Never commit credentials to git.** Add your config file to `.gitignore`:

```
~/.openclaw/openclaw.json
```

**Use environment variables for tokens.** Instead of putting tokens directly in the config file:

```json5
{
  mcp: {
    servers: {
      github: {
        command: "npx",
        args: ["@modelcontextprotocol/server-github"],
        env: {
          GITHUB_PERSONAL_ACCESS_TOKEN: {
            fromEnv: "GITHUB_TOKEN"
          }
        }
      }
    }
  }
}
```

Then set the token in your shell profile:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

**Limit filesystem access.** Only grant the filesystem MCP server access to specific directories, not your entire home folder.

**Review MCP server permissions.** Each MCP server asks for specific permissions. Read what they are before installing. A calendar server should not need access to your GitHub repos.

---

## Troubleshooting MCP Server Issues

### Server Shows as Disconnected

1. Restart the gateway: `openclaw gateway restart`
2. Check the server command is correct: `openclaw mcp list`
3. Look at gateway logs: `openclaw logs`
4. Verify the npm package exists: `npm info @modelcontextprotocol/server-filesystem`

### Authentication Errors

1. Check credential file paths are correct
2. Verify tokens have not expired
3. For Google Workspace, make sure you enabled the correct APIs in Google Cloud Console
4. For Notion, make sure you shared the specific pages with your integration

### Tools Not Appearing in Chat

1. Make sure the gateway fully restarted after adding the server
2. Ask your assistant explicitly: "What tools do you have access to?"
3. Check the MCP server documentation for any required environment variables

### npx Command Not Found

If you get "npx command not found", install Node.js:

```bash
# macOS with Homebrew
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows - download from nodejs.org
```

OpenClaw needs Node.js to run MCP servers that are distributed as npm packages.

---

## Keeping MCP Servers Updated

MCP servers are npm packages and get updated regularly. Update them to get new features and security fixes.

```bash
# Update all MCP server packages
npx npm-check-updates -g

# Update a specific package
npm update -g @modelcontextprotocol/server-github
```

After updating, restart the gateway.

---

## MCP Server Setup Checklist

| Step | Task | Done? |
|------|------|-------|
| 1 | Check OpenClaw version (need 2025.1+) | [ ] |
| 2 | Install filesystem MCP server as test | [ ] |
| 2 | Verify with `openclaw mcp list` | [ ] |
| 3 | Add MCP servers to config file | [ ] |
| 3 | Restart gateway | [ ] |
| 4 | Set up Google Cloud credentials | [ ] |
| 4 | Install Google Calendar MCP server | [ ] |
| 4 | Test calendar read | [ ] |
| 4 | Install Gmail MCP server | [ ] |
| 4 | Test email send | [ ] |
| 5 | Create Notion integration | [ ] |
| 5 | Install Notion MCP server | [ ] |
| 5 | Share a Notion page with integration | [ ] |
| 5 | Test Notion read/write | [ ] |
| 6 | Create GitHub personal access token | [ ] |
| 6 | Install GitHub MCP server | [ ] |
| 6 | Test repository access | [ ] |
| 7 | Create Slack app with bot token | [ ] |
| 7 | Install Slack MCP server | [ ] |
| 7 | Test channel message | [ ] |
| 8 | Run `openclaw mcp serve` | [ ] |
| 8 | Connect from Claude Code | [ ] |
| Security | Add credentials to environment variables | [ ] |
| Security | Add openclaw.json to .gitignore | [ ] |

---

## For More Information

- [Official OpenClaw MCP Documentation](https://docs.openclaw.ai/mcp)
- [OpenClaw CLI MCP Command Reference](https://docs.openclaw.ai/cli/mcp)
- [Official MCP Server Repository](https://github.com/modelcontextprotocol/servers)
- [Google Workspace MCP Servers](https://github.com/modelcontextprotocol/servers/tree/main/src/google-workspace)
- [Notion MCP Server](https://github.com/makenotion/notion-sdk-js)
- [Slack MCP Server Documentation](https://github.com/modelcontextprotocol/servers/tree/main/src/slack)

Want to run your OpenClaw Gateway 24/7 on a VPS so your MCP-connected assistant is always available?

**[Get SumoPod VPS](https://blog.fanani.co/sumopod)** - Reliable, affordable VPS hosting perfect for keeping your AI assistant online around the clock with all your MCP integrations connected.

For the easy-to-follow version of this guide in mixed Indonesian and English:

**[Baca versi Bahasa Indonesia](https://blog.fanani.co/tech/openclaw-mcp-server-setup/)** - Same content, casual Indonesian style, easier to follow.

---

## Related Tutorials

- [OpenClaw Gateway Setup From Scratch](/tutorials/openclaw-gateway-setup-from-scratch.md) - Get your gateway running first, then add MCP servers
- [OpenClaw Channel Integration Guide](/tutorials/openclaw-channel-integration-guide.md) - Connect Telegram, WhatsApp, and Discord alongside your MCP tools
- [OpenClaw Security Hardening Checklist](/tutorials/openclaw-security-hardening.md) - Secure your MCP connections and API tokens
- [OpenClaw Session Maintenance Guide](/tutorials/openclaw-session-maintenance.md) - Keep your gateway running smoothly with many integrations

---

*This guide is verified against the official OpenClaw documentation at docs.openclaw.ai and the official MCP server repository at github.com/modelcontextprotocol/servers.*

**Last Updated:** April 2026
**Version:** 1.0
**Author:** Radian IT Team
