# クラス図

このドキュメントは、フレームワークの主要なクラスとその関係を Mermaid クラス図で説明します。ゲーム開発におけるアーキテクチャの理解に役立ててください。

## ゲームオブジェクトの継承関係

以下の図は、ゲームオブジェクトの継承階層を示しています。BaseGameobject を基に、ワールドオブジェクトと UI オブジェクトが分かれています。

```mermaid
classDiagram

BaseGameobject <|-- BaseWorldobject
BaseGameobject <|-- BaseUiobject

BaseWorldobject <|-- Camera
BaseWorldobject <|-- Actor
BaseWorldobject <|-- Ground
BaseWorldobject <|-- Overground
BaseWorldobject <|-- DropItem
BaseWorldobject <|-- Projectile
BaseWorldobject <|-- Effect

BaseUiobject <|-- Inventory
BaseUiobject <|-- Hotbar
```

## エンジンの詳細

Engine クラスはゲームのメインループを管理します。以下の図は Engine の主要な属性とメソッドを示しています。

```mermaid
classDiagram

class Engine {
    +object screen
    +Scene current_scene
    +bool running

    +__init__()
    +start()
    +loop()
    +update()
    +draw()
}
```

## ベースクラスの詳細

BaseScene, BaseGameObject, BaseComponent はフレームワークの基盤となるクラスです。これらのクラスはゲームの構造を定義します。

```mermaid
classDiagram

class BaseScene {
    +bool active
    +bool is_started
    +list~GameObject~ world
    +list~GameObject~ canvas

    +__init__()
    +start()
    +update()
    +draw()
}

class BaseGameObject {
    +bool active
    +bool is_started
    +list~Component~ components

    +__init__()
    +start()
    +update()
    +draw()

    +add_component()
    +find_component()
    +remove_component()
}

class BaseComponent {
    +bool active
    +bool is_started

    +__init__()
    +start()
    +update()
    +draw()
}
```