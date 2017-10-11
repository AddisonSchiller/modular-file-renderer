import re
import csv

from mfr.extensions.tabular import utilities
from mfr.extensions.tabular.exceptions import EmptyTableError, TabularRendererError


def csv_stdlib(fp):
    data = fp.seek(2048)
    fp.seek(0)
    # set the dialect instead of sniffing for it.
    # sniffing can cause things like spaces or characters to be the delimiter
    dialect = csv.excel
    try:
        _set_dialect_quote_attrs(dialect, data)
    except:
        # if this errors it is not an exception
        pass

    reader = csv.DictReader(fp, dialect=dialect)
    return parse_stdlib(reader)

def tsv_stdlib(fp):
    data = fp.seek(2048)
    fp.seek(0)
    # set the dialect instead of sniffing for it.
    # sniffing can cause things like spaces or characters to be the delimiter
    dialect = csv.excel_tab
    try:
        _set_dialect_quote_attrs(dialect, data)
    except:
        # if this errors it is not an exception
        pass

    reader = csv.DictReader(fp, dialect=dialect)
    return parse_stdlib(reader)

def parse_stdlib(reader):
    """Read and convert a csv like file to JSON format using the python standard library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    columns = []
    # update the reader field names to avoid duplicate column names when performing row extraction
    for idx, fieldname in enumerate(reader.fieldnames or []):
        column_count = sum(1 for column in columns if fieldname == column['name'])
        if column_count:
            unique_fieldname = '{}-{}'.format(fieldname, column_count + 1)
            reader.fieldnames[idx] = unique_fieldname
        else:
            unique_fieldname = fieldname
        columns.append({
            'id': unique_fieldname,
            'field': unique_fieldname,
            'name': fieldname,
            'sortable': True,
        })

    try:
        rows = [row for row in reader]
    except csv.Error as e:
        if any("field larger than field limit" in errorMsg for errorMsg in e.args):
            raise TabularRendererError(
                'This file contains a field too large to render. '
                'Please download and view it locally.',
                code=400,
                extension='csv',
            ) from e
        else:
            raise TabularRendererError('csv.Error: {}'.format(e), extension='csv') from e

    if not columns and not rows:
        raise EmptyTableError('Table empty or corrupt.', extension='csv')

    return {'Sheet 1': (columns, rows)}


def sav_stdlib(fp):
    """Read and convert a .sav file to .csv with pspp, then convert that to JSON format using
    the python standard library

    :param fp: File pointer object to a .sav file
    :return: tuple of table headers and data
    """
    csv_file = utilities.sav_to_csv(fp)
    with open(csv_file.name, 'r') as file:
        csv_file.close()
        return csv_stdlib(file)


def _set_dialect_quote_attrs(dialect, data):
    """Set quote-related dialect attributes based on up to 2kb of csv data.

    The regular expressions search for things that look like the beginning of
    a list, wrapped in a quotation mark that is not dialect.quotechar, with
    list items wrapped in dialect.quotechar and seperated by commas.

    Example matches include:
        "['1', '2', '3'         for quotechar == '
        '{"a", "b", "c"         for quotechar == "
    """
    if dialect.quotechar == '"':
        if re.search('\'[[({]".+",', data):
            dialect.quotechar = "'"
        if re.search("'''[[({]\".+\",", data):
            dialect.doublequote = True
    elif dialect.quotechar == "'":
        if re.search("\"[[({]'.+',", data):
            dialect.quotechar = '"'
        if re.search('"""[[({]\'.+\',', data):
            dialect.doublequote = True
