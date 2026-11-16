## Hello World

ここでは Defold ですばやく何かを作ってみます。手順に沿って操作した後、マニュアルの続きを読んでください。

1. `Templates` から空のプロジェクトを選択し、`Title` に名前を入力して保存先を選び、`Create New Project` をクリックして作成します。プロジェクトが Defold エディターで開きます。
![Hello World の手順1](../manuals/images/unity/helloworld_1.png)
2. 左側の `Assets` ペインで `main` フォルダーを開き、`main.collection` をダブルクリックして開きます。
3. 右側の `Outline` ペインで `Collection` を右クリックし、`Add Game Object` を選択します。
![Hello World の手順2](../manuals/images/unity/helloworld_2.png)
4. 作成した `go` ゲームオブジェクト（game object）を右クリックし、`Add Component`、続いて `Label` を選択します。
![Hello World の手順3](../manuals/images/unity/helloworld_3.png)
5. その下の左側にある `Properties` ペインで、`Text` プロパティに何か入力します。
6. 中央のメインのシーンビューで、ラベルをドラッグして `(480,320,0)` 付近まで移動し、ドロップします。または、`Properties` の `Position` で位置を変更します。
![Hello World の手順4](../manuals/images/unity/helloworld_4.png)
7. ラベルの位置を変更したら、`File` -> `Save All` をクリックするか、ショートカット <kbd>Ctrl</kbd>+<kbd>S</kbd>（Mac では <kbd>Cmd</kbd>+<kbd>S</kbd>）でプロジェクトを保存します。
8. `Project` -> `Build` をクリックするか、ショートカット <kbd>Ctrl</kbd>+<kbd>B</kbd>（Mac では <kbd>Cmd</kbd>+<kbd>B</kbd>）でプロジェクトをビルドします。
![Hello World の手順5](../manuals/images/unity/helloworld_5.png)

これで Defold で最初のプロジェクトをビルドできました。ウィンドウに入力したテキストが表示されるはずです。ゲームオブジェクトとコンポーネントの概念には、すでになじみがあるでしょう。コレクション（collection）、Outline、Properties、そしてラベルを少し右上に移動する必要があった理由については、以下で説明します。
