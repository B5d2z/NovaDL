#!/usr/bin/env python
"""NovaDL - أداة تحميل فيديوهات وصوت من الإنترنت.

الاستخدام:
    python run.py                   # القائمة التفاعلية
    python run.py download URL      # تحميل مباشر
    python run.py audio URL         # تحميل صوت
    python run.py info URL          # معلومات
"""

import sys
from pathlib import Path

# إضافة مجلد src إلى مسار Python للوصول إلى الحزمة
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from novadl.cli.app import main

if __name__ == "__main__":
    main()
