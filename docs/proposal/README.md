# py-gamekit
[English](../README.md)

## 概要
py-gamekit は、2Dゲーム開発のための Python ベースのゲームフレームワークです。

## デフォルトのゲームをプレイ

### セットアップ

- Python 3.13 をインストール

- クローン
   ```bash
   git clone https://github.com/dev-haku/py-gamekit.git
   ```

- ディレクトリへの移動
   ```bash
   cd py-gamekit
   ```

- 依存関係ライブラリのインストール
   ```bash
   pip install -r requirements.txt
   ```
   

### ゲームを起動
```bash   
python build.py
```


### 自分のゲームをビルド(.exe化)
```bash
python build.py
```
ビルド (.exeファイルの生成) には、**PyInstallerライブラリ**が必須です。  
依存関係については [pyproject](../pyproject.toml) をチェック。

## ドキュメント
| ドキュメント | 内容 |
|:---|:---:|
|[チュートリアル](./tutorial.md)|まずは、ゲームをつくってみよう！|

## ライセンス

ライセンスの詳細は、[LICENSE](../LICENSE) を参照してください。
