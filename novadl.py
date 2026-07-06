#!/usr/bin/env python
"""NovaDL - أداة تحميل فيديوهات وصوت من الإنترنت.

الاستخدام:
    python novadl.py              # القائمة التفاعلية
    python novadl.py download URL  # تحميل مباشر
    python novadl.py audio URL     # تحميل صوت
    python novadl.py info URL      # معلومات
"""

from novadl.cli.app import main

if __name__ == "__main__":
    main()
