import os
import tarfile

import shutil

from catalyst.data.bundles.core import download_without_progress
from catalyst.utils.paths import data_root, ensure_directory


def get_data_source_folder(data_source_name, environ=None):
    """
    The root path of an data_source folder.

    Parameters
    ----------
    data_source_name: str
    environ:

    Returns
    -------
    str

    """
    if not environ:
        environ = os.environ

    root = data_root(environ)
    data_source_folder = os.path.join(root, 'marketplace', data_source_name)
    ensure_directory(data_source_folder)

    return data_source_folder


def get_bundle_folder(data_source_name, data_frequency, environ=None):
    data_source_folder = get_data_source_folder(data_source_name, environ)

    bundle_folder = os.path.join(data_source_folder, data_frequency)

    ensure_directory(bundle_folder)

    return bundle_folder


def get_temp_bundles_folder(data_source_name, environ=None):
    """
    The temp folder for bundle downloads by algo name.

    Parameters
    ----------
    data_source_name: str
    environ:

    Returns
    -------
    str

    """
    data_source_folder = get_data_source_folder(data_source_name, environ)

    temp_bundles = os.path.join(data_source_folder, 'temp_bundles')
    ensure_directory(temp_bundles)

    return temp_bundles


def get_data_source(data_source_name, period, force_download=False):
    """
    Download and extract a bcolz bundle.

    Parameters
    ----------
    exchange_name: str
    symbol: str
    data_frequency: str
    period: str

    Returns
    -------
    str

    """
    root = get_temp_bundles_folder(data_source_name)
    name = '{data_source}_{period}'.format(
        data_source=data_source_name,
        period=period,
    )
    path = os.path.join(root, name)

    if os.path.isdir(path):
        if force_download:
            shutil.rmtree(path)

        else:
            return path

    ensure_directory(path)

    url = 'http://127.0.0.1:8080/{data_source}/{name}.tar.gz'.format(
        data_source=data_source_name,
        name=name,
    )
    bytes = download_without_progress(url)
    with tarfile.open('r', fileobj=bytes) as tar:
        tar.extractall(path)

    return path
