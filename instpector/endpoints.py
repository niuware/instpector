from .endpoint_factory import EndpointFactory
from .apis import instagram


factory = EndpointFactory() #pylint: disable=invalid-name
factory.register_endpoint('followers', instagram.Followers)
factory.register_endpoint('following', instagram.Following)
factory.register_endpoint('profile', instagram.Profile)
factory.register_endpoint('timeline', instagram.Timeline)
factory.register_endpoint('story_reel', instagram.StoryReel)
factory.register_endpoint('story', instagram.Story)
factory.register_endpoint('comments', instagram.Comments)
