import os


def open_file(filename, mode="r"):
    if filename.startswith("gs://"):
        import gcsfs
        fs = gcsfs.GCSFileSystem(token='google_default')
        return fs.open(filename, mode)
    else:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        return open(filename, mode)
