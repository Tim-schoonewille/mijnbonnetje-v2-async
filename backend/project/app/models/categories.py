from enum import Enum


class Categories(str, Enum):
    GROCERIES = "groceries"
    RESTAURANT = "restaurant"
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    MEDIA = "media"
    EVENTS = "events"
    HARDWARE = "hardware"
    SUPPLIES = "supplies"
    OTHER = "OTHER"
