---
title: "OpenClaw × Smart Hotel — Integrasi BAS, AI Concierge, dan Green Rewards"
description: "Tutorial lengkap implementasi OpenClaw sebagai smart hotel assistant: integrasi BAS (Building Automation System), AI concierge via WhatsApp, WiFi login automation, dan green hotel reward system. Dari arsitektur sampai kode."
date: "2026-04-04"
image: "images/smart-hotel/smart-hotel-header.jpg"
tags: ["openclaw", "smart-hotel", "bas", "iot", "ai-concierge", "building-automation"]
author: "Zainul Fanani"
readingTime: 18
---

Sebelum masuk ke tutorial, quick disclosure: setup OpenClaw butuh VPS yang solid. Gue pake [Sumopod](https://blog.fanani.co/sumopod) — VPS KVM dengan harga bersahabat dan performa yang nge-gas. Cek link di atas kalau butuh rekomendasi VPS.

---

## 🔥 Masalah Nyata di Industri Hotel

Mari gue gambaran scenario yang sering banget terjadi di hotel-hotel Indonesia:

- Tamu check-in jam 14:00, AC dinyalakan penuh. Tamu keluar jalan-jalan sampai jam 22:00. **8 jam AC nyala buat nganginin kamar kosong.**
- Satu hotel 200 kamar, rata-rata occupancy 70%. Bayangin berapa kWh yang terbuang cuma buat nganginin kamar yang nggak ada orang-nya.
- Tamu baru di kota, pengen cari makan enak dekat hotel. Tanya resepsionis → dapat jawaban generik "Ada mall di sebelah sana". **Zero personalization.**
- Housekeeping schedule tetap, nggak peduli tamu lagi tidur atau nggak.

Menurut data dari Schneider Electric's Building Performance Index, **HVAC (AC) mengonsumsi 40-60% total energi hotel**. Ini bukan angka kecil. Dan sebagian besar pemborosan terjadi karena **manual control** yang nggak adaptif.

Di sisi lain, guest experience juga kurang. Tamu modern pengen instant, personalized, dan seamless. Nggak mau tanya-tanya manual. Mau ketik di WhatsApp, langsung dapet jawaban.

**Nah, di titik inilah OpenClaw masuk sebagai game changer.**

━━━━━━━━━━━━

## 🏗️ Arsitektur Besar — Gimana Caranya Kerja?

Sebelum masuk ke kode, gue mau jelasin big picture-nya dulu. Jadi nggak nyebur ke technical tanpa paham konsep.

```mermaid
flowchart TD
    subgraph Guest["🏨 Guest Layer"]
        WA["WhatsApp / Telegram"]
        APP["Hotel App"]
        WIFI["WiFi Login Portal"]
    end

    subgraph OpenClaw["🤖 OpenClaw AI Engine"]
        ENGINE["NLP Engine<br/>Intent Detection"]
        TOOLS["Tool Registry<br/>Skills & Functions"]
        SCHEDULER["Scheduler<br/>Automation Rules"]
        MEMORY["Context Memory<br/>Guest Profile & History"]
    end

    subgraph BAS["⚡ Building Automation System"]
        HVAC["HVAC Controller<br/>Schneider / Honeywell"]
        LIGHT["Lighting System"]
        SMARTM["Smart Meters<br/>Energy Monitoring"]
    end

    subgraph Hotel["🏢 Hotel Systems"]
        PMS["PMS<br/>Property Management"]
        BOOKING["Booking Engine"]
        WIFI_DB["WiFi Auth DB"]
        CRM["Guest CRM"]
    end

    WA --> ENGINE
    APP --> ENGINE
    WIFI --> WIFI_DB
    WIFI_DB -->|Guest Check-in Event| ENGINE
    ENGINE --> TOOLS
    TOOLS --> HVAC
    TOOLS --> LIGHT
    TOOLS --> SMARTM
    HVAC -->|Energy Data| SMARTM
    ENGINE -->|Recommendations| PMS
    ENGINE -->|Guest Data| CRM
    PMS -->|Room Status| ENGINE
    BOOKING -->|Booking Dates| ENGINE
    SCHEDULER -->|Auto Rules| TOOLS
    MEMORY -->|Context| ENGINE
```

**Alur kerja sederhananya:**

1. Tamu connect WiFi → email tercatat → match booking → kirim WhatsApp welcome
2. Tamu chat di WhatsApp → OpenClaw tangkap intent → eksekusi action
3. BAS kirim data energi ke OpenClaw → OpenClaw analisis → trigger otomasi
4. Semua interaksi tercatat di memory → personalization makin akurat

━━━━━━━━━━━━

## ⚡ BAS Integration — Jangan Ganggu Tamu, Otomasi di Balik Layar

Ini point paling penting dari diskusi tadi, dan gue mau highlight banget:

> **❌ SALAH:** Ngirim WhatsApp ke tamu "Matikan AC Anda untuk hemat energi"
> **✅ BENAR:** BAS otomatis turunkan AC saat tamu keluar kamar, naikkan lagi saat tamu mendekati hotel

Jangan pernah ganggu tamu dengan urusan listrik. Mereka udah bayar. Mereka pengen nyaman. **Otomasi energi harus invisible** — bekerja di background tanpa tamu sadari.

### Gimana cara deteksi tamu keluar/masuk kamar?

Ada beberapa pendekatan:

**▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░ 60% — Smart Door Lock**

Door lock dengan sensor occupancy. Setiap kali pintu dibuka/tutup, event dikirim ke BAS. Logika sederhana:

```python
# BAS Rule: Door lock event handler
async def handle_door_event(room_id: str, event: str):
    if event == "door_opened":
        # Guest entered room → restore comfort settings
        await bas.set_hvac_mode(room_id, "comfort")
        await bas.set_lighting(room_id, "welcome_scene")
        
    elif event == "all_guests_left":
        # Wait 15 minutes, then switch to eco mode
        await asyncio.sleep(900)
        if not await bas.is_room_occupied(room_id):
            await bas.set_hvac_mode(room_id, "eco")
            await bas.set_lighting(room_id, "off")
```

**▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░ 70% — PIR Motion Sensor**

Sensor gerak di dalam kamar. Nggak ada gerakan selama X menit → kamar dianggap kosong.

**▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░ 80% — BLE/WiFi Presence**

Track HP tamu yang konek ke WiFi hotel. Signal strength dari access point bisa tentukan tamu masih di kamar atau nggak.

**▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░ 90% — Hybrid (Recommended)**

Gabungkan semua di atas. Door lock + PIR + WiFi presence = akurasi tinggi dengan false positive minimal.

### Konek OpenClaw ke BAS

Ini bagian yang seru. OpenClaw bisa konek ke BAS lewat beberapa protocol:

| Protocol | Use Case | Konek via |
|----------|----------|-----------|
| **Modbus TCP** | Schneider, Honeywell, Siemens | OpenClaw Skill → TCP socket |
| **BACnet/IP** | Standar industri gedung | OpenClaw Skill → BACnet lib |
| **MQTT** | IoT sensor modern | OpenClaw Skill → MQTT broker |
| **REST API** | Cloud-based BAS | OpenClaw Skill → HTTP calls |
| **KNX** | Smart building standard | OpenClaw Skill → KNX gateway |

Gue sendiri lagi plan konek Schneider BAS dengan OpenClaw. Awalnya plan lewat n8n sebagai middleware, tapi OpenClaw sendiri udah cukup powerful sebagai orchestrator.

Contoh skill OpenClaw untuk BAS control:

```yaml
# skills/bas-control/SKILL.md
name: bas-control
description: Control Building Automation System via Modbus/MQTT
version: 1.0.0

triggers:
  - pattern: "matikan ac kamar {room}"
    action: bas.set_hvac(room, "off")
  
  - pattern: "status kamar {room}"
    action: bas.get_room_status(room)
  
  - pattern: "laporan energi hari ini"
    action: bas.get_daily_energy_report()

endpoints:
  - name: schneider-bas
    protocol: modbus-tcp
    host: 192.168.1.100
    port: 502
```

━━━━━━━━━━━━

## 📱 Layer Tamu — AI Concierge via WhatsApp

Nah, sekarang ke bagian yang tamu rasain. Ini **front-facing** — interaksi langsung antara tamu dan AI assistant.

```mermaid
flowchart LR
    GUEST["🏨 Tamu"] -->|"Ketik pesan"| WA["WhatsApp"]
    WA -->|"Webhook"| OC["OpenClaw"]
    
    OC --> INTENT{"NLP Intent Detection"}
    
    INTENT -->|"makan_recommend"| FOOD["🍽️ Rekomendasi Restoran"]
    INTENT -->|"attraction_recommend"| TOUR["🗺️ Wisata & Attractions"]
    INTENT -->|"room_service"| RS["🛎️ Room Service"]
    INTENT -->|"transport"| TAXI["🚗 Transportasi"]
    INTENT -->|"info"| INFO["ℹ️ Info Hotel"]
    INTENT -->|"complaint"| CS["🎯 Customer Service"]
    
    FOOD --> GUEST
    TOUR --> GUEST
    RS --> GUEST
    TAXI --> GUEST
    INFO --> GUEST
    CS --> GUEST
```

### Apa aja yang bisa dilakukan AI Concierge?

**▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 80% — Fitur Utama:**

| Kategori | Contoh Query | Response |
|----------|-------------|----------|
| 🍽️ Kuliner | "Makan enak dekat sini dong" | Daftar restoran + rating + jarak + rekomendasi berdasarkan preferensi |
| 🗺️ Wisata | "Tempat wisata yang wajib dikunjungi" | Itinerary + transport + estimasi waktu |
| 🛎️ Room Service | "Minta extra towel" | Forward ke housekeeping + tracking |
| 🚗 Transport | "Cari grab ke airport" | Link booking + estimasi harga + jadwal |
| 📋 Info Hotel | "Jam breakfast berapa?" | FAQ instant dari knowledge base |
| 🎯 Komplain | "AC kamar saya rusak" → Forward ke maintenance + real-time tracking |
| 🧖 Spa & Wellness | "Ada pijat dekat hotel?" | Rekomendasi + booking link |
| 🏪 Shopping | "Mau beli oleh-oleh khas" | Rekomendasi toko + peta |

Yang menarik dari OpenClaw: **bisa pake RAG (Retrieval Augmented Generation)**. Hotel upload semua info mereka (menu restoran, brosur spa, peta lokal), dan OpenClaw bisa jawab berdasarkan data real, bukan halusinasi.

### Contoh Conversational Flow

```
Tamu: Selamat malam, ada tempat makan seafood yang enak dekat hotel?

AI Concierge: Selamat malam! 🌊 Ada beberapa rekomendasi seafood dekat hotel:

1. 🦐 Rumah Makan Pantai Indah (800m, 10 min jalan kaki)
   Rating: 4.6⭐ | Harga: 50-150rb/pax | Signature: Ikan Bakar Rica-rica
   
2. 🦀 Seafood 88 (1.2km, 5 min naik grab)
   Rating: 4.4⭐ | Harga: 80-200rb/pax | Signature: Kepiting Saus Padang
   
3. 🐟 Dapur Laut (1.5km, 7 min naik grab)
   Rating: 4.8⭐ | Harga: 100-250rb/pax | Signature: Cumi Goreng Tepung
   
Mau gue bantu reservasi atau pesan grab ke salah satunya?

Tamu: Yang pertama dong, mau reservasi untuk 2 orang jam 8

AI Concierge: Siap! 🎉 Gue reservasikan di Rumah Makan Pantai Indah:
- 👥 2 orang
- 🕗 Jam 20:00 WITA
- 📅 Hari ini, 4 April 2026

Mau pesan dulu juga atau bayar di tempat?

Tamu: Bayar di tempenya aja

AI Concierge: Done! ✅ Konfirmasi reservasi udah dikirim ke WA restoran. 
Kalo mau cancel, bilang aja sebelum jam 19:00 ya. Selamat makan! 🦐
```

Liat bagaimana natural-nya? Nggak kayak bot generik. Ini karena OpenClaw bisa di-set persona dan tone-nya.

━━━━━━━━━━━━

## 📶 WiFi Login → Welcome Automation

Ini salah satu fitur yang paling impactful tapi sering terlewat.

**Alurnya:**

```mermaid
flowchart TD
    A["Tamu Connect WiFi Hotel"] --> B["WiFi Captive Portal<br/>Login dengan Email"]
    B --> C["Email Terdaftar di System"]
    C --> D{"Match dengan<br/>Booking PMS?"}
    D -->|"Ya"| E["✅ Verified Guest"]
    D -->|"Tidak"| F["📱 Tanya Nama & Booking ID"]
    F --> G{"Valid?"}
    G -->|"Ya"| E
    G -->|"Tidak"| H["❌ Akses Terbatas<br/>Basic WiFi Only"]
    
    E --> I["Kirim WhatsApp Welcome"]
    I --> J["Room Number Info"]
    I --> K["Hotel Facilities Guide"]
    I --> L["Promo & Special Offers"]
    I --> M["Emergency Contact"]
```

**Teknis implementasi:**

```python
# WiFi portal handler - ketika tamu login via email
async def handle_wifi_login(email: str, mac_address: str):
    # 1. Query PMS untuk match booking
    booking = await pms.find_booking_by_email(email)
    
    if not booking:
        return {"status": "guest_not_found", "wifi": "basic_access"}
    
    # 2. Set full WiFi access
    await wifi_controller.set_access(mac_address, "full", duration=booking.duration)
    
    # 3. Get guest phone number from booking
    phone = booking.guest_phone
    
    # 4. Create OpenClaw session for this guest
    session = await openclaw.create_session(
        chat_id=phone,
        channel="whatsapp",
        metadata={
            "room_number": booking.room_number,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "guest_name": booking.guest_name,
            "booking_id": booking.id
        }
    )
    
    # 5. Send welcome message
    await openclaw.send_message(session, {
        "template": "hotel_welcome",
        "params": {
            "name": booking.guest_name,
            "room": booking.room_number,
            "wifi_password": "premium_access_enabled",
            "breakfast_time": "06:30 - 10:00",
            "pool_hours": "07:00 - 21:00",
            "gym_hours": "24 hours"
        }
    })
    
    # 6. Schedule eco-mode activation for this room
    await bas.schedule_eco_mode(booking.room_number, booking.check_out)
    
    return {"status": "verified", "session": session.id}
```

**Hasilnya:** Tamu baru aja connect WiFi, langsung dapet WhatsApp welcome lengkap. Nggak perlu repot tanya resepsionis. Seamless. Modern.

━━━━━━━━━━━━

## 🌿 Green Hotel Reward System

Ini ide yang menarik dari diskusi: reward tamu yang hemat energi. Tapi gue mau bikin pendekatan yang lebih realistis.

### Kenapa Reward System Itu Tricky?

Jujur aja, kalau tamu udah bayar full, nanya mereka buat hemat energi itu... challenging. Tapi bisa di-framing secara positif:

**▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 80% — Pendekatan yang Realistis:**

1. **Eco Mode Opt-In** — Tamu PILIH sendiri mau ikut program green hotel
2. **Transparent Energy Dashboard** — Tamu bisa lihat berapa energi yang dihemat
3. **Gamification** — Poin, badge, level
4. **Tangible Rewards** — Voucher F&B, late check-out, spa discount, loyalty points

### Arsitektur Reward System

```mermaid
flowchart TD
    subgraph Data["📊 Energy Data"]
        SMART["Smart Meter<br/>per Room"]
        OCC["Occupancy Sensor<br/>per Room"]
    end
    
    subgraph Calc["🧮 Calculation Engine"]
        BASELINE["Baseline<br/>(kWh per occupied hour)"]
        ACTUAL["Actual<br/>(kWh measured)"]
        SAVE["Saved = Baseline - Actual"]
        POINTS["Points = Saved × Rate"]
    end
    
    subgraph Reward["🎁 Reward Engine"]
        TIER["Tier System<br/>Bronze/Silver/Gold/Platinum"]
        REDEEM["Redeem Catalog"]
        LEADER["Leaderboard<br/>(Opt-in only)"]
    end
    
    subgraph Guest["👤 Guest Experience"]
        DASH["Energy Dashboard<br/>in App/WA"]
        NOTIFY["Daily Summary<br/>via WhatsApp"]
        VOUCHER["Digital Voucher<br/>QR Code"]
    end
    
    SMART --> ACTUAL
    OCC --> BASELINE
    BASELINE --> SAVE
    ACTUAL --> SAVE
    SAVE --> POINTS
    POINTS --> TIER
    TIER --> REDEEM
    POINTS --> LEADER
    
    ACTUAL --> DASH
    SAVE --> NOTIFY
    REDEEM --> VOUCHER
```

### Contoh Implementasi

```python
# Green Hotel Reward Calculator
class GreenRewardEngine:
    BASELINE_KWH_PER_HOUR = {
        "standard": 2.5,    # AC, lights, TV
        "deluxe": 3.5,      # Bigger room, more fixtures
        "suite": 5.0        # Multiple rooms
    }
    
    POINT_RATE = 10  # points per kWh saved
    
    TIERS = {
        "bronze": 0,
        "silver": 100,
        "gold": 500,
        "platinum": 1500
    }
    
    def calculate_stay_rewards(self, room_type: str, hours_occupied: int, 
                                actual_kwh: float) -> dict:
        baseline = self.BASELINE_KWH_PER_HOUR[room_type] * hours_occupied
        saved = max(0, baseline - actual_kwh)
        points = int(saved * self.POINT_RATE)
        
        # Determine tier
        tier = "bronze"
        for name, threshold in self.TIERS.items():
            if points >= threshold:
                tier = name
        
        # Calculate monetary value
        point_value = {
            "bronze": 50,    # Rp 50 per point
            "silver": 75,
            "gold": 100,
            "platinum": 150
        }
        
        return {
            "baseline_kwh": baseline,
            "actual_kwh": actual_kwh,
            "saved_kwh": saved,
            "savings_percent": (saved / baseline * 100) if baseline > 0 else 0,
            "points_earned": points,
            "tier": tier,
            "voucher_value_rp": points * point_value[tier]
        }
```

### WhatsApp Daily Summary

```
🌿 Green Hotel Report — Kamar 204

Kemarin kamu hemat 3.2 kWh listrik! 🎉
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 80% lebih hemat dari rata-rata

📊 Energy Summary:
⚡ Total: 5.1 kWh
🌿 Baseline: 8.3 kWh
✅ Hemat: 3.2 kWh
💰 Setara: Rp 4.800

🏆 Green Points: +32 poin
📊 Total: 156 poin (Silver Tier 🥈)

🎁 Rewards yang bisa kamu redeem:
• Late check-out sampai jam 14:00 (50 poin)
• Diskon 20% spa treatment (80 poin)
• Gratis 1 minuman di lobby bar (30 poin)

Ketik "redeem [nomor]" untuk klaim reward!
```

━━━━━━━━━━━━

## 🔒 Security — Isolasi Kamar & Validasi Tamu

Ini CRITICAL. Hotel harus memastikan:

1. Tamu cuma bisa kontrol kamar sendiri
2. Tamu cuma akses data selama masa booking
3. Cross-room access mustahil

```mermaid
flowchart TD
    MSG["Incoming Message"] --> AUTH{"Authentication"}
    
    subgraph AuthCheck["🔐 Auth Layer"]
        PHONE["Phone Number<br/>Match Booking?"]
        ROOM["Room Number<br/>from Booking"]
        DATE["Current Date<br/>within Booking?"]
        SESSION["Active Session<br/>exists?"]
    end
    
    AUTH --> PHONE
    PHONE -->|Match| ROOM
    PHONE -->|No Match| DENY1["❌ Unknown Guest<br/>Basic FAQ Only"]
    ROOM --> DATE
    DATE -->|Valid| SESSION
    DATE -->|Expired| DENY2["❌ Booking Expired<br/>Thank You Message"]
    SESSION -->|Yes| ALLOW["✅ Full Access"]
    SESSION -->|No| NEW["🔄 Create New Session"]
    NEW --> ALLOW
    
    ALLOW --> TOOLS["BAS Control<br/>Room Service<br/>Recommendations"]
    
    DENY1 --> LIMIT["Limit to:<br/>• Hotel FAQ<br/>• Booking inquiry<br/>• General info"]
```

**Implementasi middleware OpenClaw:**

```python
# Middleware: Hotel guest authentication
async def authenticate_hotel_guest(message, context):
    phone = message.sender
    now = datetime.now()
    
    # 1. Check if phone matches any active booking
    booking = await pms.get_active_booking(phone, now)
    
    if not booking:
        # Unknown guest — limit access
        return {
            "authenticated": False,
            "access_level": "public",
            "allowed_tools": ["hotel_faq", "booking_inquiry", "contact_info"]
        }
    
    # 2. Check if booking is still valid
    if now < booking.check_in or now > booking.check_out + timedelta(hours=12):
        return {
            "authenticated": False,
            "access_level": "expired",
            "allowed_tools": ["hotel_faq", "contact_info"],
            "message": "Terima kasih telah menginap! Semoga perjalanan menyenangkan 🙏"
        }
    
    # 3. Full authentication
    return {
        "authenticated": True,
        "access_level": "full",
        "guest_data": {
            "name": booking.guest_name,
            "room": booking.room_number,
            "room_type": booking.room_type,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "vip": booking.is_vip
        },
        "allowed_tools": ["bas_control", "room_service", "recommendations", 
                         "transport", "complaints", "green_rewards"]
    }
```

━━━━━━━━━━━━

## 💰 Analisis Biaya & ROI

Sebagai orang engineering, gue suka ngitung-ngitung. Ini analisis kasar untuk hotel 200 kamar:

### Biaya Implementasi

| Komponen | Estimasi Biaya | Keterangan |
|----------|---------------|------------|
| OpenClaw Setup (VPS) | Rp 500rb-1jt/bulan | VPS + OpenClaw license |
| BAS Integration | Rp 20-50jt (one-time) | Tergantung brand & scope |
| WhatsApp Business API | Rp 500rb-2jt/bulan | Tergantung volume |
| WiFi Portal Modifikasi | Rp 5-10jt (one-time) | Email capture + API |
| Smart Sensors | Rp 500rb-2jt/kamar | Motion + door + power |
| Custom Development | Rp 15-30jt | Skill development, API, UI |
| **Total Setup** | **Rp 40-90jt** | One-time |
| **Monthly Ops** | **Rp 1-3.5jt** | Recurring |

### Potensi Penghematan Energi

```
📊 Skenario Hotel 200 Kamar, 70% Occupancy

Baseline Energy (tanpa automasi):
  AC: 200 × 70% × 24h × 2.5kWh = 8,400 kWh/hari
  Lighting: 200 × 70% × 12h × 0.5kWh = 840 kWh/hari
  Total: ~9,240 kWh/hari

Dengan BAS + OpenClaw:
  Eco mode saat kamar kosong (est. 8 jam/hari):
  - AC: 200 × 70% × (16h comfort + 8h eco) × avg 1.8kWh = 6,048 kWh/hari
  - Lighting: Auto-off saat kosong → 600 kWh/hari
  Total: ~6,648 kWh/hari

Penghematan: 2,592 kWh/hari (28%)
Biaya listrik: Rp 1,500/kWh
Hemat per hari: Rp 3,888,000
Hemat per bulan: ~Rp 116,640,000
```

▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 80% ROI dalam 1-2 bulan dari sisi energi saja!

Belum termasuk:
- Revenue increase dari better guest experience
- Operational efficiency (less manual work)
- Brand value (green hotel certification)

━━━━━━━━━━━━

## 🛠️ Setup OpenClaw untuk Smart Hotel

Sekarang masuk ke bagian teknis — gimana cara setup OpenClaw untuk use case ini.

### Step 1: Install & Konfigurasi OpenClaw

```bash
# Di VPS khusus hotel (atau shared)
npm install -g openclaw
openclaw init hotel-assistant
cd hotel-assistant

# Setup environment
cat > .env << 'EOF'
OPENCLAW_MODEL=anthropic/claude-sonnet-4-20250514
OPENCLAW_CHANNEL=whatsapp
WHATSAPP_WEBHOOK_URL=https://your-hotel.com/api/whatsapp
BAS_API_URL=http://192.168.1.100:502
PMS_API_URL=https://your-pms.com/api
GREEN_REWARD_ENABLED=true
EOF
```

### Step 2: Buat Hotel-Specific Skills

```
skills/
├── bas-control/
│   ├── SKILL.md
│   └── scripts/
│       ├── hvac-control.py      # AC on/off/eco
│       ├── lighting-control.py  # Lights on/off/dim
│       └── energy-report.py     # Energy usage report
├── hotel-concierge/
│   ├── SKILL.md
│   └── scripts/
│       ├── restaurant-search.py # Local restaurant DB
│       ├── attraction-guide.py  # Tourist attractions
│       ├── transport-booking.py # Grab/Gojek integration
│       └── hotel-faq.py         # FAQ knowledge base
├── green-rewards/
│   ├── SKILL.md
│   └── scripts/
│       ├── reward-calculator.py # Points calculation
│       ├── tier-checker.py      # Tier determination
│       └── daily-report.py      # WhatsApp summary
└── guest-auth/
    ├── SKILL.md
    └── scripts/
        ├── auth-middleware.py    # Guest authentication
        ├── booking-validator.py  # Booking date check
        └── session-manager.py    # Session management
```

### Step 3: Konfigurasi Channel Routing

```yaml
# openclaw.config.yaml
channels:
  whatsapp:
    provider: whatsapp-business-api
    webhook: /api/whatsapp
    
routing:
  # Public: anyone can access
  - match: ".*"
    condition: "!authenticated"
    tools:
      - hotel_faq
      - booking_inquiry
      - emergency_contact
      
  # Guest-only: authenticated hotel guests
  - match: ".*"
    condition: "authenticated"
    tools:
      - bas_control
      - room_service
      - recommendations
      - green_rewards
      - complaint
      - transport
      
  # Admin-only: hotel staff
  - match: ".*"
    condition: "admin"
    tools:
      - bas_control
      - room_service
      - recommendations
      - green_rewards
      - complaint
      - transport
      - energy_dashboard
      - guest_management
      - staff_notifications
```

### Step 4: Heartbeat Automation

OpenClaw heartbeat bisa digunakan untuk monitoring otomatis:

```yaml
# HEARTBEAT.md
## Smart Hotel Daily Checks

### Energy Monitoring (Every 2 hours)
- Run: `python3 skills/bas-control/scripts/energy-report.py --summary`
- Alert if: Any room using >150% baseline
- Alert if: Total hotel energy > 110% of budget

### Guest Welcome (Real-time)
- Trigger: WiFi login event
- Run: `python3 skills/guest-auth/scripts/session-manager.py --welcome`
- Send welcome message + create session

### Room Status Sync (Every 30 min)
- Run: `python3 skills/guest-auth/scripts/booking-validator.py --sync`
- Auto-expire sessions for checked-out guests
- Prepare welcome for expected check-ins

### Green Rewards Summary (Daily 09:00)
- Run: `python3 skills/green-rewards/scripts/daily-report.py --all`
- Send individual summary to participating guests
- Update hotel energy dashboard
```

━━━━━━━━━━━━

## 🏭 Use Cases di Luar Hotel

Konsep ini nggak cuma buat hotel lho. Bisa diterapkan ke banyak vertical:

### 🏢 Serviced Apartments & Co-Living

Sama kayak hotel tapi longer stay. Guest bisa:
- Kontrol apartemen via WhatsApp
- Report maintenance
- Terima notifikasi paket
- Booking fasilitas (gym, meeting room)

### 🏥 Rumah Sakit

- Pasien kontrol kamar (AC, lampu, TV) tanpa bergerak
- Notifikasi jadwal obat
- Request makanan diet khusus
- Info dokter jaga

### 🏭 Office Building

- Tenant kontrol kantor area
- Meeting room booking via chat
- Energy monitoring per tenant
- Facility request & tracking

### 🎓 Kampus / University

- Mahasiswa kontrol asrama
- Info jadwal kelas
- Pemesanan makanan kantin
- Library & facility booking

### 🏘️ Smart Residential

- Penghuni kontrol rumah
- Integrasi dengan smart home
- Community announcements
- Maintenance request

━━━━━━━━━━━━

## 📋 Roadmap Implementasi

Kalau gue jadi project manager untuk implementasi ini, gue bagi jadi fase:

```mermaid
gantt
    title Smart Hotel Implementation Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1 - Foundation (Bulan 1-2)
    OpenClaw Setup & Config           :a1, 2026-04-01, 14d
    BAS API Integration               :a2, after a1, 14d
    WhatsApp Business API Setup       :a3, after a1, 7d
    Guest Auth Middleware              :a4, after a2, 10d
    
    section Phase 2 - Features (Bulan 3-4)
    AI Concierge - FAQ & Info          :b1, 2026-05-01, 14d
    Restaurant Recommendations          :b2, after b1, 10d
    Room Service Integration            :b3, after b1, 14d
    WiFi Login Automation               :b4, after a4, 7d
    
    section Phase 3 - Advanced (Bulan 5-6)
    Green Rewards System                :c1, 2026-06-01, 21d
    Energy Dashboard                    :c2, after c1, 14d
    Advanced BAS Rules                  :c3, after b3, 14d
    Analytics & Reporting               :c4, after c2, 14d
    
    section Phase 4 - Optimization (Bulan 7+)
    Machine Learning for Energy         :d1, 2026-07-01, 30d
    Multi-language Support              :d2, 2026-07-15, 14d
    Loyalty Integration                 :d3, 2026-08-01, 14d
```

**▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 80% Estimasi Total: 5-7 bulan sampai full production.**

━━━━━━━━━━━━

## 🔥 Tips dari Pengalaman

Gue udah main-main dengan OpenClaw untuk beberapa use case, dan ini tips yang bisa gue kasih:

### 1. Mulai dari Simple

Jangan langsung ke BAS integration. Mulai dari:
- ✅ FAQ bot dulu (paling gampang)
- ✅ WiFi → welcome message (quick win, impact besar)
- ✅ Room service request

Setelah basic layer jalan, baru tambah BAS integration dan green rewards.

### 2. Persona Matters

Set AI persona sesuai brand hotel. Luxury hotel beda tone-nya dengan budget hotel:

```yaml
# Luxury hotel persona
persona: |
  Kamu concierge premium di [Hotel Name]. Bahasa formal tapi warm.
  Selalu gunakan "Bapak/Ibu". Rekomendasi harus curated dan eksklusif.
  
# Budget hotel persona  
persona: |
  Kamu asisten seru di [Hotel Name]. Santai, casual, friendly.
  Bisa pake "mas/mbak". Rekomendasi fokus value for money.
```

### 3. Human Handoff

AI nggak bisa handle semua. Pastikan ada escalation path:

```
Tamu: "AC kamar saya bocor!"

AI: Maaf atas ketidaknyamanannya 🙏 Gue langsung forward ke tim maintenance.
     Estimasi mereka datang dalam 10-15 menit. 
     Ada yang lain bisa gue bantu?
     
     [Auto-forward ke maintenance group dengan room number + issue]
```

### 4. Data Privacy

Ini penting banget:
- Jangan simpan chat history tamu setelah check-out
- Clear semua session data setelah 24 jam post check-out
- Comply dengan data protection regulations
- Guest harus opt-in untuk green reward data tracking

### 5. Multi-Language

Indonesia itu turis mancanegara. Minimal support:
- Bahasa Indonesia (default)
- English
- Japanese (optional, tergantung market)
- Mandarin (optional, banyak turis Tiongkok)

OpenClaw bisa auto-detect language dan switch response accordingly.

━━━━━━━━━━━━

## 📊 OpenClaw vs Alternatif

Gue yakin ada yang nanya "kenapa nggak pake [tool lain]?" Jadi gue bikin perbandingan:

| Fitur | OpenClaw | Dialogflow CX | Rasa | Custom Bot |
|-------|----------|---------------|------|------------|
| BAS Integration | ✅ Native via Skills | ⚠️ Perlu custom | ⚠️ Perlu custom | ✅ Full control |
| WhatsApp Integration | ✅ Native | ✅ Native | ✅ Native | ⚠️ Manual |
| Multi-Channel | ✅ WA, TG, Discord, Signal | ✅ WA, TG | ✅ WA, TG | ⚠️ Custom |
| Heartbeat/Automation | ✅ Built-in | ❌ Perlu external | ❌ Perlu external | ❌ Custom |
| RAG/Knowledge Base | ✅ Built-in | ✅ Native | ✅ Native | ⚠️ Custom |
| Self-Evolving | ✅ Auto-improve | ❌ Manual | ❌ Manual | ❌ Manual |
| Cost | 💰 Medium | 💸 Expensive | 💰 Medium | 💸 Dev time |
| Flexibility | ✅✅✅ Maximum | ⚠️ Limited | ⚠️ Limited | ✅✅ Full |

**Bottom line:** OpenClaw menang di flexibility dan automation capability. Untuk hotel yang butuh BAS integration + AI concierge + automation dalam satu platform, OpenClaw jawabannya.

━━━━━━━━━━━━

## 🎯 Saran Penggunaan OpenClaw untuk Hotel

Berdasarkan diskusi dan analisis gue, ini rekomendasi use case OpenClaw untuk hotel:

### Tier 1: Quick Wins (1-2 minggu setup)

| # | Use Case | Impact | Effort |
|---|----------|--------|--------|
| 1 | FAQ Bot via WhatsApp | 🔥🔥🔥 | 💚 Low |
| 2 | WiFi → Welcome Message | 🔥🔥🔥🔥 | 💚 Low |
| 3 | Room Service Request | 🔥🔥🔥 | 💛 Medium |
| 4 | Hotel Info & Directions | 🔥🔥 | 💚 Low |

### Tier 2: Core Features (1-2 bulan setup)

| # | Use Case | Impact | Effort |
|---|----------|--------|--------|
| 5 | BAS Integration (AC/Light) | 🔥🔥🔥🔥🔥 | ❤️ High |
| 6 | Restaurant Recommendations | 🔥🔥🔥🔥 | 💛 Medium |
| 7 | Transport Booking (Grab/Gojek) | 🔥🔥🔥 | 💛 Medium |
| 8 | Guest Auth & Session Management | 🔥🔥🔥🔥 | 💛 Medium |

### Tier 3: Advanced (3-6 bulan setup)

| # | Use Case | Impact | Effort |
|---|----------|--------|--------|
| 9 | Green Rewards System | 🔥🔥🔥🔥 | ❤️ High |
| 10 | Energy Dashboard | 🔥🔥🔥🔥 | ❤️ High |
| 11 | Predictive HVAC (ML) | 🔥🔥🔥🔥🔥 | ❤️❤️ Very High |
| 12 | Multi-language Support | 🔥🔥🔥 | 💛 Medium |

### Tier 4: Nice to Have

| # | Use Case | Impact | Effort |
|---|----------|--------|--------|
| 13 | Loyalty Program Integration | 🔥🔥🔥 | 💛 Medium |
| 14 | Voice Assistant (Room) | 🔥🔥🔥🔥 | ❤️ High |
| 15 | AR Navigation in Hotel | 🔥🔥 | ❤️❤️ Very High |
| 16 | Predictive Maintenance | 🔥🔥🔥🔥 | ❤️❤️ Very High |

━━━━━━━━━━━━

## 🧠 Kesimpulan

Smart hotel bukan konsep baru. Tapi implementasinya sering terhambat oleh:
- Biaya integrasi yang tinggi
- Fragmented systems (BAS, PMS, CRM, Communication)
- Kurangnya AI yang bisa handle multi-domain

OpenClaw mengubah equation ini. Dengan kemampuan:
- **Multi-channel** (WhatsApp, Telegram, Discord)
- **Skill-based architecture** (mudah tambah fitur baru)
- **Heartbeat automation** (proactive monitoring)
- **Self-evolving** (makin pintar seiring waktu)
- **BAS integration** via custom skills

Satu platform bisa handle semuanya: dari energy optimization sampai guest experience, dari maintenance tracking sampai revenue optimization.

Yang paling penting: **mulai dari simple, iterate fast.** Nggak perlu implementasi semuanya sekaligus. FAQ bot aja udah bisa deliver value. WiFi welcome aja udah bikin tamu wow.

Hotel yang pertama adopt AI concierge di Indonesia akan punya competitive advantage yang signifikan. Dan OpenClaw siap jadi engine-nya.

━━━━━━━━━━━━

> **Heads up:** Artikel ini ditulis berdasarkan diskusi di komunitas OpenClaw Indonesia tentang smart hotel use case. Setup OpenClaw butuh VPS — gue rekomendasiin [Sumopod](https://blog.fanani.co/sumopod) untuk hosting yang reliable dan harga bersahabat.

---

**Referensi & Resources:**

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Schneider Electric Building Automation](https://www.se.com/ww/en/work/products-services/building-automation/)
- [WhatsApp Business API](https://business.whatsapp.com/developers/developer-hub)
- [BACnet Protocol](https://www.bacnet.org/)
- [Green Hotel Association](https://www.greenhotels.com/)

**Artikel terkait:**

- [Panduan Lengkap Pilih LLM Provider untuk OpenClaw](/tech/openclaw-llm-provider-guide/)
- [OpenClaw 2026.4.2 — Update Terbaru](/tech/openclaw-2026-4-2/)
