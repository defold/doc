---
title: プロジェクトのセットアップ
brief: このマニュアルでは、Defold でプロジェクトを作成する方法と開く方法を説明します。
---

# プロジェクトのセットアップ {#project-setup}

Defold エディターから新しいプロジェクトを簡単に作成できます。コンピューター上にある既存のプロジェクトを開くこともできます。

## 新しいローカルプロジェクトの作成 {#creating-a-new-project}

<kbd>New Project</kbd> オプションをクリックし、作成するプロジェクトの種類を選択します。プロジェクトファイルを保存するハードドライブ上の場所を指定します。<kbd>Create New Project</kbd> をクリックすると、選択した場所にプロジェクトが作成されます。テンプレート（Template）から新しいプロジェクトを作成できます:

![プロジェクトを開く](images/workflow/open_project.png)

手順を段階的に説明するチュートリアル（Tutorial）から作成することもできます:

![チュートリアルからプロジェクトを作成](images/workflow/create_from_tutorial.png)

また、完成済みのサンプルゲーム（Sample）から作成することもできます:

![サンプルからプロジェクトを作成](images/workflow/create_from_sample.png)

### プロジェクトを GitHub に追加する {#adding-the-project-to-github}

ローカルプロジェクトはどのバージョン管理システムとも連携していないため、ファイルはハードドライブ上にしか存在せず、変更を元に戻すための履歴もありません。エディターの *Assets* ペインで削除したファイルは、対応している場合はシステムのごみ箱（Trash または Recycle Bin）に移動しますが、この操作を利用できない場合や操作が失敗した場合は、完全に削除されることがあります。ごみ箱は任意の編集からファイルを保護するものではなく、バージョン履歴も提供しないため、Git などのバージョン管理システムを使ってファイルの変更を追跡することをお勧めします。これにより、ほかの人とプロジェクトを共同で開発することも非常に容易になります。ローカルプロジェクトは、わずか数ステップで GitHub にアップロードできます:

1. [GitHub](https://github.com/) でアカウントを作成するか、アカウントにログインします。
2. [New Repository](https://help.github.com/en/articles/creating-a-new-repository) オプションを使ってリポジトリを作成します。
3. [Upload Files](https://help.github.com/en/articles/adding-a-file-to-a-repository) オプションを使って、すべてのプロジェクトファイルをアップロードします。

これでプロジェクトがバージョン管理の対象になります。[プロジェクトをクローン](https://help.github.com/en/articles/cloning-a-repository)してローカルのハードドライブに保存し、以後はこの新しい場所で作業することをお勧めします。

## 既存のプロジェクトを開く {#open-an-existing-project}

<kbd>Open From Disk</kbd> オプションをクリックすると、コンピューター上にあるプロジェクトを開けます。

![プロジェクトをインポート](images/workflow/open_from_disk.png)

## 最近使ったプロジェクトを開く {#open-a-recent-project}

一度開いたプロジェクトは、最近使ったプロジェクトの一覧に表示されます。この一覧には最近作業したプロジェクトが表示され、一覧内のプロジェクトをダブルクリックすると、どのプロジェクトでもすぐに開けます。
