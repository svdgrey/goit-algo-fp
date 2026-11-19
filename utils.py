# Допоміжні функції для збереження зображень.
from pathlib import Path


def save_figure(figure, filename: str, dpi: int = 160) -> Path:
    assets = Path(__file__).resolve().parent / "assets"
    assets.mkdir(exist_ok=True)

    output = assets / filename
    figure.savefig(output, dpi=dpi, bbox_inches="tight")
    print(f"Зображення збережено: {output.relative_to(assets.parent)}")
    return output
