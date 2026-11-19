# PyGamekit

[English](../README.md)

## 概要

PyGamekit は、2Dゲーム開発のための Python ベースのゲームフレームワークです。

## はじめに

### Python のインストール

PyGamekit には Python 3.13.9 が必要です。

### リポジトリのクローン

```bash
git clone https://github.com/dev-haku/py-gamekit.git
cd py-gamekit
```

### 仮想環境の構築

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

### 依存関係のインストール

```bash
python -m pip install -r requirements.txt
```

## ゲームの実行

```bash
python ./run.py
```

## ビルド

PyInstaller を使用して、単体で実行可能なファイルをビルドできます。

ビルドされたファイルは `build/` ディレクトリに出力されます。

```bash
python ./build.py
```

## ライセンス

ライセンスの詳細については、[LICENSE](../LICENSE) を参照してください。