import os
import pytest
from tempfile import NamedTemporaryFile

from mfr.core.exceptions import RendererError
from mfr.core.provider import ProviderMetadata

from mfr.extensions.codepygments import settings, CodePygmentsRenderer
from mfr.extensions.codepygments.exceptions import FileTooLargeError


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.xml', 'text/plain', '1234', 'http://wb.osf.io/file/good.xml?token=1234')


@pytest.fixture
def test_file_path():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.xml')

@pytest.fixture
def max_size_file_path():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'files')
    with NamedTemporaryFile(mode='w+b', suffix='.txt', dir=dir_path,
                            delete=False) as temp_file:
        temp_file_path = temp_file.name
        file_size = settings.MAX_SIZE
        temp_file.seek(file_size -1)
        temp_file.write(b'0')
    return temp_file_path

@pytest.fixture
def over_size_file_path():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'files')
    with NamedTemporaryFile(mode='w+b', suffix='.txt', dir=dir_path,
                            delete=False) as temp_file:
        temp_file_path = temp_file.name
        file_size = settings.MAX_SIZE
        temp_file.seek(file_size)
        temp_file.write(b'0')
    return temp_file_path

@pytest.fixture
def invalid_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.xml')


@pytest.fixture
def url():
    return 'http://osf.io/file/good.xml'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def extension():
    return '.mp3'


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return CodePygmentsRenderer(metadata, test_file_path, url, assets_url, export_url)


class TestCodePygmentsRenderer:

    def test_render_codepygments(self, renderer):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body

    def test_render_codepygments_invalid(self, metadata, invalid_file_path, url, assets_url, export_url):
        renderer = CodePygmentsRenderer(metadata, invalid_file_path, url, assets_url, export_url)
        with pytest.raises(RendererError):
            renderer.render()

    def test_render_codepygments_max_size(self, metadata, max_size_file_path, url, assets_url, export_url):
        try:
            renderer = CodePygmentsRenderer(metadata, max_size_file_path, url, assets_url, export_url)
            body = renderer.render()
            assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body
        finally:
            os.remove(max_size_file_path)

    def test_render_codepygments_over_size(self, metadata, over_size_file_path, url, assets_url, export_url):
        with pytest.raises(FileTooLargeError):
            try:
                renderer = CodePygmentsRenderer(metadata, over_size_file_path,
                                                url, assets_url, export_url)
                renderer.render()
            finally:
                os.remove(over_size_file_path)

    def test_render_codepygments_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_codepygments_cache_result(self, renderer):
        assert renderer.cache_result is True

    # 'é' and 'ö' are encoded differently in utf-8, utf-16, and cp1252/iso-8559-1.  Each file
    # contains the string "Héllö" in the listed encoding and should be matchable if correctly
    # decoded.  The complex* files also contain some higher codepoints (Thai) just to ensure
    # that chardet handles that.
    @pytest.mark.parametrize("filename", [
        ('complex.utf16.txt'),
        ('complex.utf8.txt'),
        ('simple.cp1252.txt'),
        ('simple.utf16.txt'),
        ('simple.utf8.txt'),
    ])
    def test_render_encodings(self, metadata, invalid_file_path, url, assets_url, export_url, filename):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'encodings', filename)
        renderer = CodePygmentsRenderer(metadata, file_path, url, assets_url, export_url)
        body = renderer.render()
        assert 'Héllö' in body

    # this file (iso-8859-looks-like-utf16.txt) is both valid iso-8859-1 AND UTF-16. Heuristic
    # detection (like chardet.detect()) should correctly recognize it as iso-8859-1.  If it is
    # decoded as UTF-16, it will be mostly garbled Chinese characters.
    def test_render_iso_not_utf16(self, metadata, url, assets_url, export_url):
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'files', 'encodings',
            'iso-8859-looks-like-utf16.txt',
        )
        renderer = CodePygmentsRenderer(metadata, file_path, url, assets_url, export_url)
        body = renderer.render()
        assert 'CREATIVE COMMONS' in body
