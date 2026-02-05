from services.engines.jsearch import JSearchEngine
from services.engines.adzuna import AdzunaEngine

def get_engine(country: str):
    country = country.lower()

    if country in ("uk", "gb"):
        return AdzunaEngine()

    return JSearchEngine()