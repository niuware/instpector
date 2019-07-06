import re

def get_ajax_id(content):
    match = re.findall(r"\"rollout_hash\":\"([\w]+)\"", content)
    if match:
        return match[0]
    return ""

def get_consumer_lib_path(content_lines):
    regex = re.compile(r"href=\"(.*ConsumerLibCommons.*\.js)\"")
    for line in content_lines:
        match = regex.findall(line)
        if match:
            return match[0]
    return ""

def get_app_id(content):
    match = re.findall(r"instagramWebDesktopFBAppId=\'(\d+)\'", content)
    if match:
        return match[0]
    return ""
