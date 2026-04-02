# Setup Custom Email dengan Domain di Namecheap + Google Workspace — Gratis

> Tutorial lengkap setup email profesional pakai domain sendiri (contoh: `inquiry@fanani.co`) tanpa biaya bulanan, menggunakan Namecheap + Google Workspace.

**📅 Dibuat:** 3 April 2026  
**🏷️ Tags:** email, google-workspace, namecheap, tutorial, dns  
**⏱️ Estimasi waktu:** 15–20 menit

---

## 🏗️ Arsitektur

```mermaid
graph LR
    A[👤 Pengirim Email] -->|DNS lookup| B[Namecheap DNS]
    B -->|MX records| C[Google Workspace]
    C -->|fanani@cvrfm.com| D[Inbox Utama]
    C -->|inquiry@fanani.co| D
    C -->|newsletters@fanani.co| D
    C -->|dm@fanani.co| D
    C -->|japri@fanani.co| D
    
    E[OpenClaw AI] -.->|Research & Docs| F[Tutorial & Guide]
    E -.->|Automated| G[Documentation Pipeline]
```

**Flow:** Semua email yang dikirim ke alias (`inquiry@`, `newsletters@`, `dm@`, `japri@`) → masuk ke inbox utama `fanani@cvrfm.com` lewat Google Workspace.

---

## 1. 📋 Persiapan

Yang kamu butuhkan sebelum mulai:

- [ ] **Domain** yang sudah aktif di Namecheap (contoh: `fanani.co`)
- [ ] **Akun Google Workspace** (Business Starter atau trial — gratis 14 hari)
- [ ] **Akses Google Admin Console** (`admin.google.com`)
- [ ] **Akses Namecheap Domain List** (`namecheap.com/domains`)

> 💡 **Tips:** Google Workspace Business Starter trial 14 hari — lebih dari cukup buat setup. Setelah itu ~$6/bulan, tapi worth it untuk email profesional.

---

## 2. ➕ Add Domain ke Google Workspace

1. Login ke [Google Admin Console](https://admin.google.com)
2. Buka **Account** → **Domains** → **Add domain**
3. Masukkan domain kamu (contoh: `fanani.co`)
4. Google akan generate **verification record** (TXT record)
5. **Jangan tutup tab ini** — kamu butuh info TXT record-nya

---

## 3. ✅ Verify Domain di Namecheap (TXT Record)

Google perlu verifikasi bahwa kamu pemilik domain.

### Langkah:

1. Buka [Namecheap Domain List](https://www.namecheap.com/domains)
2. Klik **Manage** di domain kamu
3. Pilih **Advanced DNS**
4. Scroll ke **TXT Records**
5. Klik **Add New Record**:

| Type | Host | Value | TTL |
|------|------|-------|-----|
| TXT | `@` | `google-site-verification=XXXXXXX` | Auto |

> ⚠️ **Penting:** Nilai `google-site-verification=XXXXXXX` diambil dari Google Admin Console. Copy-paste persis.

6. Tunggu **1–5 menit** (propagasi DNS)
7. Kembali ke Google Admin Console → klik **Verify**

### Troubleshooting:
- Belum ke-verify? Cek [MXToolbox TXT Lookup](https://mxtoolbox.com/TXTLookup.aspx) untuk cek apakah record sudah live
- Pastikan Host = `@` (bukan subdomain)

---

## 4. 📬 Set MX Records di Namecheap

Setelah domain terverifikasi, arahkan email ke Google Workspace.

### Langkah:

1. Masih di **Namecheap Advanced DNS**
2. Scroll ke **MX Records** (atau **Mail Settings**)
3. **Hapus semua MX record lama** (kalau ada dari Namecheap default email)
4. Tambahkan 5 MX record Google:

| Type | Host | Value | Priority |
|------|------|-------|----------|
| MX | `@` | `ASPMX.L.GOOGLE.COM` | 1 |
| MX | `@` | `ALT1.ASPMX.L.GOOGLE.COM` | 5 |
| MX | `@` | `ALT2.ASPMX.L.GOOGLE.COM` | 5 |
| MX | `@` | `ALT3.ASPMX.L.GOOGLE.COM` | 10 |
| MX | `@` | `ALT4.ASPMX.L.GOOGLE.COM` | 10 |

5. Klik **Save All Changes**
6. Tunggu propagasi **15 min – 48 jam** (biasanya < 30 menit)

### Optional — SPF & DKIM Records:

| Type | Host | Value |
|------|------|-------|
| TXT | `@` | `v=spf1 include:_spf.google.com ~all` |
| TXT | `fanani._domainkey` | (Dari Google Admin → Security → DKIM) |

> 💡 SPF & DKIM penting biar email kamu nggak masuk spam folder penerima.

---

## 5. 📧 Add Email Aliases di Google Admin

Setelah MX record aktif, buat email alias yang nanti masuk ke inbox utama.

### Langkah:

1. Buka [Google Admin → Directory → Users](https://admin.google.com/ac/users)
2. Klik user utama (`fanani@cvrfm.com`)
3. Pilih **User** → **Aliases**
4. Klik **Add Alias** untuk setiap alias:

| Alias | Fungsi |
|-------|--------|
| `inquiry@fanani.co` | Email bisnis / pertanyaan |
| `newsletters@fanani.co` | Subscribe newsletter |
| `dm@fanani.co` | Direct message / social media |
| `japri@fanani.co` | Japri (obrolan pribadi) 😅 |

5. Save setelah setiap alias

### Cara Kerja:
- Email ke `inquiry@fanani.co` → otomatis masuk ke inbox `fanani@cvrfm.com`
- Bisa pakai filter di Gmail untuk label otomatis per alias
- Reply bisa dari alias tersebut

---

## 6. 🧪 Test & Verify

### Quick Test:

1. Kirim email dari akun lain ke `inquiry@fanani.co`
2. Cek inbox `fanani@cvrfm.com` — seharusnya masuk
3. Reply email tersebut — cek apakah from address bener

### Gmail Filter (Optional):

```
Settings → Filters → Create new filter
To: inquiry@fanani.co → Apply label "📬 Inquiries"
To: newsletters@fanani.co → Apply label "📰 Newsletters"
To: dm@fanani.co → Apply label "💬 DM"
To: japri@fanani.co → Apply label "🔒 Japri"
```

### Verification Tools:
- [Google Admin Toolbox — Check MX](https://toolbox.googleapps.com/apps/checkmx/)
- [MXToolbox](https://mxtoolbox.com/)

---

## 💡 Tips & Notes

1. **TTL set Auto** — biarkan Namecheap yang manage TTL, kecuali butuh propagasi cepat
2. **Backup DNS** — screenshot DNS records lama sebelum edit
3. **Email forwarding** alternatif: kalau nggak mau pakai Google Workspace, Namecheap punya email forwarding gratis
4. **Multiple domains** — cara ini bisa diulang untuk semua domain (cvrfm.com, uno-st.com, reforel.com, ptrfs.com)
5. **Google Workspace trial** — setelah 14 hari, pilih Business Starter ($6/bulan) atau hapus domain kalau nggak butuh

---

## 🤖 Bagaimana OpenClaw Membantu

Tutorial ini dibuat dan didokumentasikan dengan bantuan **OpenClaw AI**:

| Step | Kontribusi OpenClaw |
|------|-------------------|
| **Research** | Riset provider email hosting & membandingkan opsi (Google Workspace vs Zoho vs Namecheap Email) |
| **Guide Generation** | Generate tutorial lengkap step-by-step dalam bahasa Indonesia |
| **Documentation** | Automasi dokumentasi ke GitHub repo + blog post |
| **DNS Guidance** | Panduan setup MX, TXT, SPF, DKIM records yang akurat |
| **Multi-format Output** | Satu konten → 3 format (tutorial, blog post, checklist guide) |
| **Architecture Diagram** | Mermaid diagram untuk visualisasi flow email |

OpenClaw membantu dari riset awal sampai dokumentasi final — mengubah proses yang biasanya 2-3 jam jadi kurang dari 30 menit.

---

## 📚 Referensi

- [Google Workspace — Add your domain](https://support.google.com/a/answer/9057229)
- [Google Workspace — Set up MX records](https://support.google.com/a/answer/174734)
- [Namecheap — Google Workspace Setup](https://www.namecheap.com/support/knowledgebase/article.aspx/9266/2208/how-do-i-set-up-google-workspace-email/)
- [Namecheap — DNS Management](https://www.namecheap.com/support/knowledgebase/article.aspx/5968/89/how-to-manage-dns-records)

---

**🔗 Repo:** [github.com/fanani-radian/openclaw-sumopod](https://github.com/fanani-radian/openclaw-sumopod)
