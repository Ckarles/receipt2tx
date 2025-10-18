#!/usr/bin/env python3

import typer

app = typer.Typer()


@app.command()
def list_new_receipts(
    receipts_url: list[str],
) -> None:
    print(receipts_url)


if __name__ == "__main__":
    app()
