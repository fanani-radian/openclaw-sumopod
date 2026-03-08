# Visual Data Alert

Transform spreadsheet data into beautiful charts delivered to Telegram.

## Overview

Tired of staring at raw numbers in Google Sheets? This automation:
- Generates charts from your spreadsheet data
- Detects anomalies and trends automatically
- Delivers visual reports to Telegram
- Alerts on significant changes

**Perfect for:** Sales tracking, website analytics, expense monitoring, KPI dashboards.

## Architecture

```
[Google Sheets data]
         ↓
[Fetch & process]
         ↓
[Generate charts]
  - Line charts (trends)
  - Bar charts (comparisons)
  - Pie charts (distributions)
         ↓
[Anomaly detection]
  - % change alerts
  - Threshold triggers
         ↓
[Send to Telegram]
  - Chart images
  - Summary text
  - Action items
```

## Prerequisites

- OpenClaw installed
- gog CLI (Google Workspace)
- matplotlib/seaborn (Python charting)
- Telegram bot

## Step 1: Install Dependencies

```bash
pip install matplotlib seaborn pandas numpy gspread
```

## Step 2: Chart Generator

`scripts/visual-alert/chart-generator.py`:

```python
#!/usr/bin/env python3
"""
Generate charts from spreadsheet data
Usage: python3 chart-generator.py <sheet_id> <range> <chart_type>
"""

import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import subprocess

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100

def fetch_sheet_data(sheet_id, range_name):
    """Fetch data from Google Sheets using gog CLI"""
    result = subprocess.run(
        ["gog", "sheets", "get", sheet_id, range_name, "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def generate_line_chart(data, title, x_label, y_label):
    """Generate line chart for trends"""
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Convert date column if exists
    if 'Date' in df.columns or 'date' in df.columns:
        date_col = 'Date' if 'Date' in df.columns else 'date'
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
    
    fig, ax = plt.subplots()
    
    # Plot numeric columns
    for col in df.columns:
        if col not in ['Date', 'date'] and pd.api.types.is_numeric_dtype(df[col]):
            ax.plot(df[date_col] if 'Date' in df.columns or 'date' in df.columns else range(len(df)), 
                   df[col], marker='o', label=col, linewidth=2)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = f"/tmp/chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    
    return output_path

def generate_bar_chart(data, title, x_label, y_label):
    """Generate bar chart for comparisons"""
    df = pd.DataFrame(data[1:], columns=data[0])
    
    fig, ax = plt.subplots()
    
    # Find label and value columns
    label_col = df.columns[0]
    value_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
    
    if len(value_cols) == 1:
        # Simple bar chart
        ax.bar(df[label_col], df[value_cols[0]], color='steelblue')
        ax.set_ylabel(value_cols[0])
    else:
        # Grouped bar chart
        x = range(len(df))
        width = 0.8 / len(value_cols)
        
        for i, col in enumerate(value_cols):
            ax.bar([p + width*i for p in x], df[col], width, label=col)
        
        ax.set_xticks([p + width*(len(value_cols)-1)/2 for p in x])
        ax.set_xticklabels(df[label_col])
        ax.legend()
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_label)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    output_path = f"/tmp/chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    
    return output_path

def generate_pie_chart(data, title):
    """Generate pie chart for distributions"""
    df = pd.DataFrame(data[1:], columns=data[0])
    
    label_col = df.columns[0]
    value_col = df.columns[1]
    
    fig, ax = plt.subplots()
    
    colors = plt.cm.Set3(range(len(df)))
    wedges, texts, autotexts = ax.pie(
        df[value_col], 
        labels=df[label_col],
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    output_path = f"/tmp/chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    
    return output_path

def generate_kpi_cards(data):
    """Generate KPI summary cards"""
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # Calculate KPIs
    kpis = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            kpis[col] = {
                'current': df[col].iloc[-1],
                'previous': df[col].iloc[-2] if len(df) > 1 else 0,
                'change_pct': ((df[col].iloc[-1] - df[col].iloc[-2]) / df[col].iloc[-2] * 100) if len(df) > 1 and df[col].iloc[-2] != 0 else 0,
                'avg': df[col].mean(),
                'max': df[col].max(),
                'min': df[col].min()
            }
    
    return kpis

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 chart-generator.py <sheet_id> <range> <chart_type> [title]")
        print("Chart types: line, bar, pie, kpi")
        sys.exit(1)
    
    sheet_id = sys.argv[1]
    range_name = sys.argv[2]
    chart_type = sys.argv[3]
    title = sys.argv[4] if len(sys.argv) > 4 else "Data Chart"
    
    print(f"📊 Fetching data from sheet...")
    data = fetch_sheet_data(sheet_id, range_name)
    
    print(f"📈 Generating {chart_type} chart...")
    
    if chart_type == "line":
        chart_path = generate_line_chart(data, title, "Date", "Value")
    elif chart_type == "bar":
        chart_path = generate_bar_chart(data, title, "Category", "Value")
    elif chart_type == "pie":
        chart_path = generate_pie_chart(data, title)
    elif chart_type == "kpi":
        kpis = generate_kpi_cards(data)
        print(json.dumps(kpis, indent=2))
        return
    else:
        print(f"Unknown chart type: {chart_type}")
        sys.exit(1)
    
    print(f"✅ Chart saved: {chart_path}")
    print(chart_path)  # Output path for next script

if __name__ == "__main__":
    main()
```

## Step 3: Anomaly Detection

`scripts/visual-alert/anomaly-detector.py`:

```python
#!/usr/bin/env python3
"""
Detect anomalies in data
Usage: python3 anomaly-detector.py <sheet_id> <range>
"""

import sys
import json
import subprocess
import pandas as pd
import numpy as np

def fetch_data(sheet_id, range_name):
    """Fetch data from Google Sheets"""
    result = subprocess.run(
        ["gog", "sheets", "get", sheet_id, range_name, "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def detect_anomalies(data, threshold_pct=20):
    """Detect significant changes"""
    df = pd.DataFrame(data[1:], columns=data[0])
    
    alerts = []
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            values = pd.to_numeric(df[col], errors='coerce').dropna()
            
            if len(values) < 2:
                continue
            
            current = values.iloc[-1]
            previous = values.iloc[-2]
            
            if previous == 0:
                continue
            
            change_pct = ((current - previous) / previous) * 100
            
            # Alert on significant changes
            if abs(change_pct) >= threshold_pct:
                direction = "📈 UP" if change_pct > 0 else "📉 DOWN"
                alerts.append({
                    "metric": col,
                    "current": current,
                    "previous": previous,
                    "change_pct": round(change_pct, 2),
                    "direction": direction,
                    "severity": "high" if abs(change_pct) > 50 else "medium"
                })
            
            # Detect outliers (values beyond 2 std dev)
            mean = values.mean()
            std = values.std()
            z_score = abs((current - mean) / std) if std > 0 else 0
            
            if z_score > 2:
                alerts.append({
                    "metric": col,
                    "current": current,
                    "mean": round(mean, 2),
                    "z_score": round(z_score, 2),
                    "type": "outlier",
                    "severity": "medium"
                })
    
    return alerts

def generate_summary(data):
    """Generate text summary of data"""
    df = pd.DataFrame(data[1:], columns=data[0])
    
    summaries = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            values = pd.to_numeric(df[col], errors='coerce').dropna()
            if len(values) > 0:
                trend = "increasing" if values.iloc[-1] > values.iloc[0] else "decreasing"
                summaries.append(f"{col}: {trend} from {values.iloc[0]:.0f} to {values.iloc[-1]:.0f}")
    
    return summaries

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 anomaly-detector.py <sheet_id> <range>")
        sys.exit(1)
    
    sheet_id = sys.argv[1]
    range_name = sys.argv[2]
    
    print("🔍 Analyzing data...")
    data = fetch_data(sheet_id, range_name)
    
    # Detect anomalies
    alerts = detect_anomalies(data)
    
    # Generate summary
    summaries = generate_summary(data)
    
    result = {
        "alerts": alerts,
        "summaries": summaries,
        "alert_count": len(alerts)
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

## Step 4: Telegram Integration

`scripts/visual-alert/send-report.py`:

```python
#!/usr/bin/env python3
"""
Send chart and report to Telegram
Usage: python3 send-report.py <chart_path> <message>
"""

import sys
import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_photo(photo_path, caption):
    """Send photo to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    with open(photo_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
        
        response = requests.post(url, files=files, data=data)
        return response.json()

def send_message(text):
    """Send text message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, data=data)
    return response.json()

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send-report.py <chart_path> '<message>'")
        sys.exit(1)
    
    chart_path = sys.argv[1]
    message = sys.argv[2]
    
    # Send chart with caption
    if os.path.exists(chart_path):
        result = send_photo(chart_path, message)
        if result.get('ok'):
            print("✅ Chart sent to Telegram")
        else:
            print(f"❌ Failed: {result}")
    else:
        # Send text only
        result = send_message(message)
        if result.get('ok'):
            print("✅ Message sent to Telegram")
        else:
            print(f"❌ Failed: {result}")

if __name__ == "__main__":
    main()
```

## Step 5: Complete Pipeline

`scripts/visual-alert/generate-report.sh`:

```bash
#!/bin/bash
# Generate visual report and send to Telegram
# Usage: ./generate-report.sh <sheet_id> <range> <chart_type> <title>

SHEET_ID="$1"
RANGE="$2"
CHART_TYPE="$3"
TITLE="$4"

if [ -z "$SHEET_ID" ] || [ -z "$RANGE" ]; then
    echo "Usage: ./generate-report.sh <sheet_id> <range> [chart_type] [title]"
    exit 1
fi

CHART_TYPE="${CHART_TYPE:-line}"
TITLE="${TITLE:-Data Report}"

echo "📊 Generating visual report..."
echo "Sheet: $SHEET_ID"
echo "Range: $RANGE"
echo "Type: $CHART_TYPE"

# Generate chart
CHART_PATH=$(python3 scripts/visual-alert/chart-generator.py "$SHEET_ID" "$RANGE" "$CHART_TYPE" "$TITLE")

# Detect anomalies
ANOMALIES=$(python3 scripts/visual-alert/anomaly-detector.py "$SHEET_ID" "$RANGE")
ALERT_COUNT=$(echo "$ANOMALIES" | python3 -c "import sys,json; print(json.load(sys.stdin)['alert_count'])")

# Build message
MESSAGE="📊 *$TITLE*

"

# Add alerts if any
if [ "$ALERT_COUNT" -gt 0 ]; then
    MESSAGE+="🚨 *Alerts Detected:*\n"
    ALERTS=$(echo "$ANOMALIES" | python3 -c "import sys,json; alerts=json.load(sys.stdin)['alerts']; print('\\n'.join([f\"{a['direction']} {a['metric']}: {a['change_pct']}%\" for a in alerts]))")
    MESSAGE+="$ALERTS\n\n"
fi

# Add summary
SUMMARIES=$(echo "$ANOMALIES" | python3 -c "import sys,json; print('\\n'.join(json.load(sys.stdin)['summaries']))")
MESSAGE+="📈 *Summary:*\n$SUMMARIES"

# Send to Telegram
python3 scripts/visual-alert/send-report.py "$CHART_PATH" "$MESSAGE"

# Cleanup
rm -f "$CHART_PATH"

echo "✅ Report complete!"
```

## Step 6: Cron Schedule

```bash
# Daily sales report at 9 AM
0 9 * * * /root/.openclaw/workspace/scripts/visual-alert/generate-report.sh \
    "YOUR_SHEET_ID" "Sales!A1:D30" "line" "Daily Sales Report" \
    >> /var/log/visual-alert.log 2>&1

# Weekly analytics every Monday
0 10 * * 1 /root/.openclaw/workspace/scripts/visual-alert/generate-report.sh \
    "YOUR_SHEET_ID" "Analytics!A1:E52" "bar" "Weekly Analytics" \
    >> /var/log/visual-alert.log 2>&1
```

## Example Output

**Telegram Message:**
```
📊 *Daily Sales Report*

🚨 *Alerts Detected:*
📈 UP Revenue: +23.5%
📉 DOWN Churn: -15.2%

📈 *Summary:*
Revenue: increasing from 45000 to 55575
Orders: increasing from 120 to 142
Churn: decreasing from 5.2 to 4.4
```

**With Chart:** [Visual chart image attached]

## Advanced Features

### Multi-Chart Reports

```python
def generate_dashboard(data_dict):
    """Generate multiple charts in one report"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    # Generate different chart types in subplots
    pass
```

### Predictive Alerts

```python
def predict_trend(data, days_ahead=7):
    """Simple linear prediction"""
    from sklearn.linear_model import LinearRegression
    # Predict future values
    pass
```

## Conclusion

You now have automated visual reporting that:
- ✅ Generates charts from spreadsheet data
- ✅ Detects anomalies automatically
- ✅ Delivers reports to Telegram
- ✅ Runs on schedule

**Next Steps:**
- Add more chart types (heatmap, area chart)
- Build interactive web dashboard
- Integrate with more data sources (database, API)

---

*Tutorial created for OpenClaw Sumopod*
