import os
from tqdm import tqdm
from six.moves.urllib.request import urlretrieve


def reporthook(t):
    """https://github.com/tqdm/tqdm"""
    last_b = [0]

    def inner(b=1, bsize=1, tsize=None):
        """
        b: int, optional
            Number of blocks just transferred [default: 1].
        bsize: int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize: int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return inner

def maybe_download(url, filename, prefix, num_bytes=None):
    """Takes an URL, a filename, and the expected bytes, download
    the contents and returns the filename.
    num_bytes=None disables the file size check."""
    local_filename = None
    output_path = os.path.join(prefix, filename)
    if not os.path.exists(output_path):
        try:
            print("Downloading file {} to {}...".format(url + filename, output_path))
            with tqdm(unit='B', unit_scale=True, miniters=1, desc=filename) as t:
                local_filename, _ = urlretrieve(url + filename, output_path, reporthook=reporthook(t))
        except AttributeError as e:
            print("An error occurred when downloading the file! Please get the dataset using a browser.")
            raise e
    # We have a downloaded file
    # Check the stats and make sure they are ok
    file_stats = os.stat(os.path.join(prefix, filename))
    if num_bytes is None or file_stats.st_size == num_bytes:
        print("File {} successfully downloaded to {}.".format(filename, output_path))
    else:
        raise Exception("Unexpected dataset size. Please get the dataset using a browser.")

    return local_filename

def download_bert_chinese():
    import zipfile
    data_dir = '/tmp/'
    base_url = ' https://github.com/SunYanCN/bert-text/raw/master/'
    local_filepath = maybe_download(base_url, filename='bert_tfhub.zip', prefix=data_dir)
    print("Unzipping {}...".format(local_filepath))
    glove_zip_ref = zipfile.ZipFile(local_filepath, 'r')
    glove_zip_ref.extractall(data_dir)
    glove_zip_ref.close()


