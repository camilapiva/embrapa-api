import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="CLI for project utility tasks")

BASE_DIR = Path(__file__).resolve().parent


@app.command()
def download_all():
    """Runs all scrapers (Embrapa)."""
    subprocess.run(["poetry", "run", "python", "scripts/download_production.py"])
    subprocess.run(["poetry", "run", "python", "scripts/download_processing.py"])
    subprocess.run(["poetry", "run", "python", "scripts/download_importation.py"])
    subprocess.run(["poetry", "run", "python", "scripts/download_exportation.py"])
    subprocess.run(["poetry", "run", "python", "scripts/download_commercialization.py"])


@app.command()
def test():
    """Run all tests with pytest."""
    subprocess.run(["poetry", "run", "pytest"])


@app.command()
def lint():
    """Runs Flake8 to check code style."""
    subprocess.run(["poetry", "run", "flake8", "app/", "tests/"])


@app.command()
def clean():
    """Removes .csv files from the data/ folder."""
    data_dir = BASE_DIR / "data"
    if data_dir.exists():
        for file in data_dir.glob("*.csv"):
            file.unlink()
        typer.echo("CSV files removed successfully.")
    else:
        typer.echo("Folder 'data/' not found.")


if __name__ == "__main__":
    app()
