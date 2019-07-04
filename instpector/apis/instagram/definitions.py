from collections import namedtuple

TUser = namedtuple("TUser", "id username full_name is_private")

TPageInfo = namedtuple("TPageInfo", "end_cursor has_next_page")
