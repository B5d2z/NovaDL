<div align="center">
  <h1>NovaDL</h1>
  <p><strong>أداة تحميل فيديوهات وصوت من الإنترنت</strong></p>
  <p>
    <a href="https://github.com/B5d2z/NovaDL/releases"><img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-%3E%3D3.8-green" alt="Python"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
    <a href="https://github.com/B5d2z/NovaDL"><img src="https://img.shields.io/github/stars/B5d2z/NovaDL?style=social" alt="Stars"></a>
  </p>
  <p>YouTube · TikTok · Instagram · Facebook · X · Vimeo · Reddit · Twitch · SoundCloud · <a href="SUPPORTED_SITES.md">1000+</a></p>
</div>

---

### لماذا NovaDL؟

بساطة **yt-dlp** مع قوة واجهة تفاعلية — بدون حفظ أوامر أو بحث.

| المشكلة | الحل |
|---------|------|
| تبي تحمل من يوتيوب، تيك توك، انستا... | قائمة اختيار — تختار المنصة وتلصق الرابط |
| تبي صوت بس أو فيديو بجودة معينة | اختيار جودة تفاعلي |
| مو عارف الـ FFmpeg مركب ولا لا | `doctor` يشخص لك النظام |
| ودك تتابع تحميلاتك | سجل تحميلات + إعدادات محفوظة |

---

### المميزات

- **قائمة تفاعلية** — اختر platform، الصق الرابط، اختر الجودة، خلاص
- **تحميل فيديو وصوت** — MP3, M4A, Opus, FLAC, WAV
- **قوائم تشغيل** — قنوات وقوائم كاملة
- **ترجمة + صور مصغرة** — تحميل ودمج
- **استكمال التحميل** — لو انقطع يكمل
- **كوكيز + بروكسي** — فيديوهات خاصة
- **شريط تقدم** — سرعة، وقت متبقي، حجم
- **يدعم 1000+ موقع** — يوتيوب، تيك توك، انستا، فيسبوك، X، Vimeo، Reddit، Twitch، SoundCloud...
- **Windows, macOS, Linux**

### التشغيل السريع

```bash
git clone https://github.com/B5d2z/NovaDL.git
cd novadl
python run.py
```
> **Windows:** انقر مرتين على `NovaDL.bat`

### ساعد في نشر المشروع ✨

> ⭐ **نجمة على GitHub** — تفرق وتوسع الانتشار.
> 🍴 **Fork** — طور وأضف ميزات.
> 💬 **شارك** المشروع مع المهتمين.

### المتطلبات

- Python ≥ 3.8
- [FFmpeg](https://ffmpeg.org/) للصوت — شغّل `python run.py doctor`

### الإعدادات

```bash
python run.py config                          # عرض الكل
python run.py config output_dir "~/Videos"    # تغيير مسار الحفظ
```

تتحفظ في `~/.config/novadl/config.json`.

### الأوامر

| الأمر | الوظيفة |
|-------|---------|
| `download URL` | تحميل فيديو |
| `audio URL` | استخراج صوت |
| `info URL` | معلومات الرابط |
| `config [key] [value]` | إعدادات |
| `update` | تحديث yt-dlp |
| `history` | سجل التحميلات |
| `doctor` | تشخيص النظام |

### الترخيص

MIT — [B5t Alanzi](https://github.com/B5d2z) · [@B5d2z](https://x.com/B5d2z)
