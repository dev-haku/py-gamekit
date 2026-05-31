# py-gamekit

[English](../README.md) |

## 概要

py-gamekit は、2Dゲーム開発のための Python ベースのゲームフレームワークです。

## はじめに

### Python 3.13.9 のインストール


### クローン

```bash
git clone https://github.com/dev-haku/py-gamekit.git
cd py-gamekit
```

### 依存関係ライブラリのインストール

```bash
pip install -r requirements.txt
```

### ゲームのスタート

```bash
python run.py
```


## ビルド
実行ファイル (.exe) を生成には、PyInstallerが必須です。  
依存関係については [pyproject](../pyproject.toml) をチェック。

```bash
python build.py
```

ビルドされたファイルは自動的に `build/` ディレクトリに出力されます。

## ライセンス

ライセンスの詳細は、[LICENSE](../LICENSE) を参照してください。
