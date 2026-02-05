from services.engines.jsearch import JSearchEngine

def get_engine(country: str):
    country = country.lower()

    if country in ("uk", "gb"):
        return JSearchEngine()  # later: AdzunaEngine
    return JSearchEngine()