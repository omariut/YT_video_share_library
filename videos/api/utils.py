from urllib.parse import urlparse, parse_qs


def get_video_code(url):
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    code = query["v"][0]
    return code

