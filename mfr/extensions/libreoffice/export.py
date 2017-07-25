import os
import subprocess

from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.libreoffice import settings
import functools
print = functools.partial(print, flush=True)

class LibreOfficeExporter(extension.BaseExporter):

    def export(self):
        try:
            subprocess.check_call([
                'soffice',  # CHANGE TO CONFIG FILE OR SOMETHING
                '--headless',
                '--convert-to', self.format,
                '--nofirststartwizard',
                '--outdir', self.output_file_path.split('export/')[0] + 'export/',
                self.source_file_path

            ])
            for i in range(10):
                print('\n')
            print('LO ' + settings.LIBREOFFICE_BIN)

        except subprocess.CalledProcessError as err:
            name, extension = os.path.splitext(os.path.split(self.source_file_path)[-1])
            raise exceptions.SubprocessError(
                'Unable to export the file in the requested format, please try again later.',
                process='soffice',
                cmd=str(err.cmd),
                returncode=err.returncode,
                path=str(self.source_file_path),
                code=400,
                extension=extension or '',
                exporter_class='libreoffice',
            )
