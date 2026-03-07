# Daily OpenClaw Tips

A curated collection of hidden features, best practices, and pro tips for getting the most out of OpenClaw.

> **New tips added daily!**  
> Last updated: March 7, 2026  
> Total tips: 2

---

## Tip #2: The MCP Context Trap (March 7, 2026)

### The Problem
When using MCP (Model Context Protocol) servers, there's a hidden gotcha: **MCP tools consume your context window aggressively** but don't always show up in the conversation history.

### What Happens
```
You: "Check my email and calendar"
→ MCP calls happen (invisible to you)
→ Context fills up with tool results
→ Later messages start getting truncated
```

### The Fix
**After MCP-heavy operations, always compact:**
```
"Check email, calendar, and tasks. Then /compact."
```

Or break into chunks:
```
"Check email" → wait → /compact
"Check calendar" → wait → /compact
```

### Why It Matters
MCP results can be 10-20K tokens each. Three MCP calls = potentially 60K tokens gone. Your 128K window just became 68K.

---

## Tip #1: The Memory Pressure Pattern (March 7, 2026)

### The Problem
Context windows are finite (128K-200K tokens depending on model). After ~50 messages or heavy file operations, the AI starts losing early context.

### Symptoms of Memory Pressure
- Repeating explanations
- Forgetting constraints you mentioned earlier
- "As I mentioned before..." (when it wasn't mentioned)
- Circular conversations

### Strategic Compaction

**Compact BEFORE:**
- Complex multi-step tasks
- Code refactoring sessions
- Long debugging sessions
- After reading 5+ files

**Compact AFTER:**
- File exploration (directory listings, searches)
- Large output processing
- MCP tool batches

**The Checkpoint Pattern:**
```
"Remember these key requirements: [list]. 
Now /compact, then implement."
```

This forces critical info into the compressed summary.

### Pro Tips

1. **Don't compact randomly** — You'll lose useful context
2. **Compact when switching topics** — Clean slate for new domain
3. **Use /compact not restart** — Maintains system memory files

---

## Coming Tomorrow

**Tip #3: The Silent Truncation Problem**  
*Why your `exec` outputs get cut off and how to prevent it*

---

## Contributing

Have a tip? Submit a PR to `docs/tips/daily-tips.md`!

---

*Powered by OpenClaw 🦞*  
*For more tutorials: [github.com/openclaw/openclaw-sumopod](https://github.com/openclaw/openclaw-sumopod)*
