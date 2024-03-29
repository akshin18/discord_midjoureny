import os
from exiftool import ExifToolHelper


def set_metadata(data:list):
    for image_path, prompt in data:
        with ExifToolHelper() as et:
            et.set_tags(
                [image_path],
                tags={"XMP:Title": prompt},
                params=["-P", "-overwrite_original"]
            )


def get_metadata():
    for image_path in os.listdir("images"):
        with ExifToolHelper() as et:
            for d in et.get_metadata(f"images/{image_path}"):
                for k, v in d.items():
                    print(f"Dict: {k} = {v}")
        print("\n")


# a = [[f"images/{x}","SOme test "] for x in os.listdir("images")]
# # set_metadata(a)
# get_metadata()