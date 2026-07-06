# NovaDL

أداة تحميل فيديوهات وصوت من الإنترنت تعمل من سطر الأوامر. تدعم YouTube، TikTok، Instagram، Facebook، X (Twitter)، Vimeo، Reddit، Twitch، SoundCloud، ومئات المواقع الأخرى.

مبنية على [yt-dlp](https://github.com/yt-dlp/yt-dlp) بهيكل نظيف وقابل للتوسع.

## المميزات

- **تحميل الفيديو** — من جميع المواقع التي يدعمها yt-dlp
- **استخراج الصوت** — بصيغ MP3، M4A، Opus، FLAC، WAV
- **اختيار الجودة** — أفضل جودة، 1080p، 720p، 480p، 360p، أسوأ جودة
- **اختيار الصيغة** — mp4، mkv، webm، إلخ
- **قائمة تشغيل** — تحميل قوائم تشغيل كاملة
- **ترجمة** — تحميل ودمج الترجمة داخل الفيديو
- **صورة مصغرة** — تحميل ودمج الصورة المصغرة
- **معلومات الوسائط** — عرض معلومات وتفاصيل الفيديو
- **استكمال التحميل** — عند انقطاع الاتصال
- **تحميل دفعة واحدة** — عدة روابط من ملف
- **الكوكيز** — استخدام ملفات الكوكيز للتحميل من حسابات خاصة
- **بروكسي** — توجيه التحميل عبر بروكسي
- **إعدادات** — حفظ الإعدادات بشكل دائم
- **سجل التحميل** — تتبع التحميلات السابقة
- **تحديث yt-dlp** — تحديث محرك التحميل مباشرة من الأداة
- **فحص FFmpeg** — التحقق من وجود FFmpeg وإرشادك لتثبيته
- **واجهة تفاعلية** — قائمة اختيار بالأرقام
- **شريط تقدم** — نسبة التحميل، السرعة، الوقت المتبقي، حجم الملف

## التنصيب

### المتطلبات

- Python 3.8 أو أحدث
- [FFmpeg](https://ffmpeg.org/) (مطلوب لاستخراج الصوت وتحويل الصيغ)

### تحميل سريع (ملف واحد)

```bash
git clone https://github.com/Badr1Alanzi/novadl.git
cd novadl
python novadl.py
```

### عبر Poetry

```bash
pip install poetry
git clone https://github.com/Badr1Alanzi/novadl.git
cd novadl
poetry install
poetry run novadl
```

## الاستخدام

### الواجهة التفاعلية

شغّل الملف بدون أي أمر لفتح القائمة التفاعلية:

```bash
python novadl.py
```

ستظهر لك قائمة اختار منها رقم المنصة، ثم نوع التحميل (فيديو أو صوت)، أدخل الرابط، واختر الجودة.

### أوامر سطر الأوامر المباشرة

```bash
# تحميل فيديو
python novadl.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# تحميل صوت فقط
python novadl.py audio "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# عرض معلومات
python novadl.py info "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# تحديث yt-dlp
python novadl.py update

# عرض الإعدادات
python novadl.py config

# عرض سجل التحميل
python novadl.py history

# مسح السجل
python novadl.py clear-history

# تشخيص النظام
python novadl.py doctor
```

> **ملاحظة:** بعد تنصيب الأداة عبر Poetry، استخدم `novadl` بدل `python novadl.py`.

### خيارات التحميل

| الخيار | الاختصار | الوصف |
|--------|----------|-------|
| `--output-dir` | `-o` | مجلد الحفظ |
| `--quality` | `-q` | جودة الفيديو |
| `--format` | `-f` | صيغة المخرج |
| `--audio-only` | `-a` | تحميل الصوت فقط |
| `--audio-format` | | صيغة الصوت |
| `--audio-quality` | | جودة الصوت |
| `--subtitles` | `-s` | تحميل الترجمة |
| `--sub-langs` | | رموز لغات الترجمة |
| `--embed-subs` | | دمج الترجمة |
| `--thumbnail` | `-t` | حفظ الصورة المصغرة |
| `--cookies` | `-c` | مسار ملف الكوكيز |
| `--proxy` | `-p` | رابط البروكسي |

## الأوامر

| الأمر | الوصف |
|-------|-------|
| `python novadl.py download <url>` | تحميل فيديو مع خيارات الجودة والصيغة والترجمة |
| `python novadl.py audio <url>` | تحميل صوت فقط (MP3, M4A, Opus, FLAC, WAV) |
| `python novadl.py info <url>` | عرض معلومات مفصلة عن رابط وسائط |
| `python novadl.py update` | تحديث yt-dlp لأحدث إصدار |
| `python novadl.py config [key] [value]` | عرض أو تعديل الإعدادات |
| `python novadl.py version` | عرض معلومات الإصدار |
| `python novadl.py history` | عرض سجل التحميل |
| `python novadl.py clear-history` | مسح سجل التحميل |
| `python novadl.py doctor` | تشخيص النظام (yt-dlp, FFmpeg) |

## المنصات المدعومة

- Windows 10 / 11
- macOS 12+
- Linux (أي توزيعة مع Python 3.12+)

## المواقع المدعومة

جميع المواقع التي يدعمها yt-dlp، ومنها:

YouTube، YouTube Music، YouTube Shorts، TikTok، Instagram، Facebook، X (Twitter)، Vimeo، Reddit، Twitch، SoundCloud، Dailymotion، Bilibili، Niconico، والمئات غيرها.

للقائمة الكاملة: [مواقع yt-dlp المدعومة](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## الإعدادات

تُحفظ الإعدادات في `~/.config/novadl/config.json`.

### عرض جميع الإعدادات

```bash
python novadl.py config
```

### عرض إعداد معين

```bash
python novadl.py config output_dir
```

### تعيين قيمة

```bash
python novadl.py config output_dir "~/Videos/NovaDL"
```

### مفاتيح الإعدادات

| المفتاح | الوصف | القيمة الافتراضية |
|---------|-------|-------------------|
| `output_dir` | مسار الحفظ الافتراضي | `~/Downloads/NovaDL` |
| `proxy` | رابط البروكسي الافتراضي | — |
| `cookies` | مسار ملف الكوكيز الافتراضي | — |
| `audio_format` | صيغة الصوت الافتراضية | `mp3` |
| `audio_quality` | جودة الصوت الافتراضية | `192` |

## الأسئلة الشائعة

**س: هل أحتاج FFmpeg؟**

ج: FFmpeg مطلوب لاستخراج الصوت وتحويل الصيغ. إذا كنت تحمّل فيديو بصيغته الأصلية فقط، فهو اختياري.

**س: كيف أثبت FFmpeg؟**

ج: شغّل `python novadl.py doctor` لتعليمات التنصيب حسب نظامك.

**س: هل يعمل على Windows؟**

ج: نعم. NovaDL مدعوم بالكامل على Windows وmacOS وLinux.

**س: هل يمكن تحميل فيديوهات يوتيوب خاصة؟**

ج: نعم، بتوفير ملف كوكيز عبر الخيار `--cookies`.

**س: كيف أحدث yt-dlp؟**

ج: شغّل `python novadl.py update`.

## هيكل المشروع

```
src/novadl/
├── cli/              # أوامر Typer والقائمة التفاعلية
├── core/             # منطق المجال (كيانات، حالات استخدام، واجهات)
│   ├── entities/     # نماذج البيانات
│   ├── use_cases/    # منطق الأعمال
│   └── interfaces/   # واجهات مجردة
├── infrastructure/   # التكامل مع الخارج
│   ├── downloader/   # تكامل yt-dlp
│   ├── config/       # إدارة الإعدادات
│   ├── history/      # سجل التحميل
│   └── system/       # أدوات النظام
├── presentation/     # واجهة المستخدم (Rich)
└── utils/            # أدوات مشتركة
```

## التطوير

```bash
# تنصيب الاعتماديات
poetry install

# تشغيل الفحص
poetry run ruff check src/

# تشغيل التنسيق
poetry run black src/ tests/

# تشغيل فحص الأنواع
poetry run mypy src/

# تشغيل الاختبارات
poetry run pytest
```

## المساهمة

اقرأ [CONTRIBUTING.md](CONTRIBUTING.md) للتفاصيل عن كيفية المساهمة.

## الترخيص

هذا المشروع مرخص تحت رخصة MIT — راجع [LICENSE](LICENSE) للمزيد.

## المطور

**بدر العنزي**

- GitHub: [@Badr1Alanzi](https://github.com/Badr1Alanzi)
- X: [@B5d2z](https://x.com/B5d2z)

## الشكر

NovaDL يعتمد على [yt-dlp](https://github.com/yt-dlp/yt-dlp) وجميع المساهمين فيه.
