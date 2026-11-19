# PyGamekit

![Status](https://img.shields.io/badge/status-in%20development-orange?style=for-the-badge&labelColor=gray)

[日本語ドキュメント](./docs/README.ja.md)

## About

This is a Python-based game framework for creating 2D games.

## Getting Started

### Install Python

PyGamekit requires Python 3.13.9.

### Clone the Repository

```bash
git clone https://github.com/dev-haku/py-gamekit.git
cd py-gamekit
```

### Create a Virtual Environment

**Windows**

```bash
py -3.13 -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Game

```bash
python ./run.py
```

## Building

To build a standalone executable, PyInstaller is required.

The build output will be generated in the `build/` directory.

```bash
python ./build.py
```

## License

See the [LICENSE](./LICENSE) file for details.