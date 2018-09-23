#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

# По умолчанию используется версия Django 1.11,
# если вы хотите использовать другие версии, поменяйте эту переменную.
# Если оставить строку пустой, будет использоваться версия, установленная на сервере.

django_version = '1.11'

# Добавьте нужные вам пути поиска.
# Если вы получаете ошибку 500 Internal Server Error,
# скорее всего проблема именно в путях поиска.

sys.path.insert(0, '/home/hosting_russianchoco/projects/russian-souvenir-staging/choco')
sys.path.insert(0, '/home/hosting_russianchoco/projects/russian-souvenir-staging')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# ------ Ниже этой линии изменения скорее всего не нужны --------
if not hasattr(sys, 'real_prefix'):
    python_lib = "python%d.%d" % (sys.version_info[0], sys.version_info[1])
    if django_version:
        sys.path.insert(0, "/opt/django-%s/lib/%s/site-packages/" % (django_version, python_lib))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()