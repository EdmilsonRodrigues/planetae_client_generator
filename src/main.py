import typer
from models.clent_generator import ClientGenerator

VERSION = "1.0.0"
app = typer.Typer()


@app.command()
def run(source_path: str, dest: str = ".", client: str = "Angular"):
    client = client.capitalize()
    typer.echo(f"Generating client for {client}")
    generator = ClientGenerator(
        src_path=source_path, output_path=dest, client=client
    )
    generator.generate_client()
    typer.echo("Client generated successfully")


if __name__ == "__main__":
    app()
