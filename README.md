# receipt2tx
>
> A receipt to transaction converter.

## Features

- Convert images from most common mobile phones pictures formats
- Support multiple storage backends (local, S3, gcs..)

## Installation

```sh
pip install receipt2tx
```

## Usage

Extract receipts from a local directory `./receipts`

```sh
uv run receipt2tx -d file://receipts
```

## Contributing

We're using `uv` for our development workflow.

### Run unit tests

```sh
uv run pytest
```
