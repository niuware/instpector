from .definitions import TUser, TPageInfo

class Parser:

    @staticmethod
    def followers_page_info(data):
        return Parser._follow_page_info(data, "edge_followed_by")

    @staticmethod
    def following_page_info(data):
        return Parser._follow_page_info(data, "edge_follow")

    @staticmethod
    def followers(data):
        return Parser._follow_edge(data, "edge_followed_by")

    @staticmethod
    def following(data):
        return Parser._follow_edge(data, "edge_follow")

    @staticmethod
    def _follow_page_info(data, endpoint):
        end_cursor = ""
        has_next_page = False
        try:
            root = data["data"]["user"][endpoint]
            end_cursor = root["page_info"]["end_cursor"]
            has_next_page = root["page_info"]["has_next_page"]
        except KeyError:
            print(f"Error parsing follow_page_info for {endpoint}")
        return TPageInfo(
            end_cursor=end_cursor,
            has_next_page=has_next_page)

    @staticmethod
    def _follow_edge(data, endpoint):
        edges = []
        try:
            root = data["data"]["user"][endpoint]
            edges = root["edges"]
        except KeyError:
            print(f"Error parsing follow_edge for {endpoint}")
        for edge in edges:
            node = edge["node"]
            follower = TUser(
                id=node["id"],
                username=node["username"],
                full_name=node["full_name"],
                is_private=node["is_private"]
            )
            yield follower
