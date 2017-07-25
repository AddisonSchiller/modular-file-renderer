import os

from mfr import settings


config = settings.child('LIBREOFFICE_EXTENSION_CONFIG')

LIBREOFFICE_BIN = config.get('LIBREOFFICE_BIN', '/usr/bin/soffice')


DEFAULT_RENDER = {'renderer': '.pdf', 'format': 'pdf'}

RENDER_MAP = config.get('RENDER_MAP', {
    # 'csv': {'renderer': '.xlsx', 'format': 'xlsx'},
    # 'ppt': {'renderer': '.pdf', 'format': 'pdf'},
    # 'pptx': {'renderer': '.pdf', 'format': 'pdf'},
})
