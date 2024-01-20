import os
from exiftool import ExifToolHelper


def set_metadata(data:list):
    for image_path, prompt in data:
        with ExifToolHelper() as et:
            et.set_tags(
                [image_path],
                tags={"Title": prompt},
                params=["-P", "-overwrite_original"]
            )

