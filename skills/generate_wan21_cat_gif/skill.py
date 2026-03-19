from skills.generate_video_clip.skill import build as generic_build
from skills.generate_video_clip.skill import run as generic_run


def build(**kwargs):
    if "filename_prefix" not in kwargs:
        kwargs["filename_prefix"] = "video_clip_h264"
    return generic_build(**kwargs)


def run(**kwargs):
    result = generic_run(**kwargs)
    result["skill"] = "generate_wan21_cat_gif"
    result["alias_of"] = "generate_video_clip"
    return result
