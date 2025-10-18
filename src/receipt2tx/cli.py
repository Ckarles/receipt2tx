#!/usr/bin/env python3

import typing as t

import click
import typer

from .image_fetch import backends


# List of supported URI protocols
SUPPORTED_URI_PROTOCOLS = [
    f"{uri_protocol}://"
    for uri_protocol in backends.SUPPORTED_URI_PROTOCOL_TO_BACKEND.keys()
]

app = typer.Typer()


class URICustomClassParser(click.ParamType):
    """Custom click parser for a URI string that can be parsed to a Backend object.

    c.f. typer documentation https://typer.tiangolo.com/tutorial/parameter-types/custom-types/?h=custom#click-custom-type
    This class is needed in order to have descriptive error messages, as described in the click documentation:
    > For simple cases, passing a Python function that fails with a ValueError is also supported, though discouraged.
    c.f. click documentation https://click.palletsprojects.com/en/stable/parameter-types/#how-to-implement-custom-types
    """

    name = "Backend"

    def convert(self, value, param, ctx):
        try:
            return backends.select_backend_from_uri_raw(value)
        except ValueError as e:
            self.fail(str(e), param, ctx)


@app.command()
def list_new_receipts(
    receipts_uris: t.Annotated[
        list[backends.Backend],
        typer.Option(
            "--receipts_uri",
            "-u",
            metavar="URI",
            click_type=URICustomClassParser(),
            help=f"Receipts backend URI. Use this option multiple times to add multiple URIs. Supported URI protocols: {SUPPORTED_URI_PROTOCOLS}",
        ),
    ],
) -> None:
    """List new receipts to be processed, given a list of receipts URIs."""
    print(receipts_uris)


if __name__ == "__main__":
    app()
