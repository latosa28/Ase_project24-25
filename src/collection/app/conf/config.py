from utils_helpers.config import load_config


def _check_rarities(rarities: dict):
    # Verifica che la somma delle percentuali sia 100
    total_percentage = sum(rarities.values())
    if total_percentage != 100.0:
        raise ValueError(
            f"Le percentuali sommano {total_percentage}. Devono essere esattamente 100."
        )


def setup_config(app):
    config_data = load_config(app)
    rarities = config_data.get("rarities")
    if rarities:
        _check_rarities(rarities)