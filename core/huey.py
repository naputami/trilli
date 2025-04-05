from huey import RedisHuey
from django.conf import settings

huey = RedisHuey(
    name=settings.HUEY['name'],
    host=settings.HUEY['connection']['host'],
    port=settings.HUEY['connection']['port'],
    db=settings.HUEY['connection']['db'],
    immediate=False
)