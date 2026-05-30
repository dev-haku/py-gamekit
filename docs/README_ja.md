# py-gamekit

[English](../README.md) |

## 概要

py-gamekit は、2Dゲーム開発のための Python ベースのゲームフレームワークです。

## はじめに

### クローン

```bash
git clone https://github.com/dev-haku/py-gamekit.git
cd py-gamekit
```

### 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### あなたのゲームをスタートするには

```bash
python run.py
```


## あなたのゲームのビルド方法
実行ファイル (.exe) を生成するには、PyInstallerが必須です。  
依存関係については [pyproject](../pyproject.toml) をチェック。

```bash
python build.py
```

ビルドされたファイルは自動的に `build/` ディレクトリに出力されます。

## ライセンス

ライセンスの詳細は、[LICENSE](../LICENSE) を参照してください。
