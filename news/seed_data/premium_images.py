"""Curated image URLs per editorial category (reliable high-res sources)."""

PICSUM = 'https://picsum.photos/seed/{seed}/1200/800'

CATEGORY_SEEDS = {
    'breaking_news': ['breaking-1', 'breaking-2', 'breaking-3', 'breaking-4'],
    'world': ['world-1', 'world-2', 'world-3', 'world-4'],
    'politics': ['politics-1', 'politics-2', 'politics-3', 'politics-4'],
    'business': ['business-1', 'business-2', 'business-3', 'business-4'],
    'economy': ['economy-1', 'economy-2', 'economy-3', 'economy-4'],
    'technology': ['technology-1', 'technology-2', 'technology-3', 'technology-4'],
    'science': ['science-1', 'science-2', 'science-3', 'science-4'],
    'health': ['health-1', 'health-2', 'health-3', 'health-4'],
    'sports': ['sports-1', 'sports-2', 'sports-3', 'sports-4'],
    'entertainment': ['entertainment-1', 'entertainment-2', 'entertainment-3', 'entertainment-4'],
    'culture': ['culture-1', 'culture-2', 'culture-3', 'culture-4'],
    'lifestyle': ['lifestyle-1', 'lifestyle-2', 'lifestyle-3', 'lifestyle-4'],
    'opinion': ['opinion-1', 'opinion-2', 'opinion-3', 'opinion-4'],
    'education': ['education-1', 'education-2', 'education-3', 'education-4'],
    'environment': ['environment-1', 'environment-2', 'environment-3', 'environment-4'],
    'crime': ['crime-1', 'crime-2', 'crime-3', 'crime-4'],
    'travel': ['travel-1', 'travel-2', 'travel-3', 'travel-4'],
    'food': ['food-1', 'food-2', 'food-3', 'food-4'],
    'real_estate': ['realestate-1', 'realestate-2', 'realestate-3', 'realestate-4'],
    'weather': ['weather-1', 'weather-2', 'weather-3', 'weather-4'],
    'video': ['video-1', 'video-2', 'video-3', 'video-4'],
}


def image_url(category: str, index: int) -> str:
    pool = CATEGORY_SEEDS.get(category, CATEGORY_SEEDS['world'])
    seed = pool[index % len(pool)]
    return PICSUM.format(seed=seed)
