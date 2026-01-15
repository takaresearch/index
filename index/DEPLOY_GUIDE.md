# GitHubへのデプロイガイド

このドキュメントは、ローカルでの変更をGitHubにアップロードし、GitHub Pagesを更新する手順を記載している。

## 前提条件

- Gitがインストールされていること
- GitHubアカウントを持っていること
- リモートリポジトリ: `https://github.com/takaresearch/index.git`

## 初回セットアップ（一度だけ実行）

### 1. Git設定

```bash
cd c:\GITHUB_takaresearch\index
git config user.name "Taka"
git config user.email "takahisa523@gmail.com"
```

### 2. リモートリポジトリの追加（初回のみ）

```bash
git remote add origin https://github.com/takaresearch/index.git
git branch -M main
```

### 3. 既存のリモート設定確認

```bash
git remote -v
```

出力例：
```
origin  https://github.com/takaresearch/index.git (fetch)
origin  https://github.com/takaresearch/index.git (push)
```

## 日常的なワークフロー

### 変更をGitHubにアップロード

#### 1. 現在の状態を確認

```bash
cd c:\GITHUB_takaresearch\index
git status
```

#### 2. 変更をステージング

```bash
# すべての変更を追加
git add .

# または特定のファイルのみ
git add docs/clinical/outpatient.md
```

#### 3. コミット

```bash
git commit -m "変更内容の簡潔な説明"
```

コミットメッセージの例：
- `git commit -m "Add new clinical documentation for hallux valgus"`
- `git commit -m "Update research achievements"`
- `git commit -m "Fix typos in patient communication guide"`

#### 4. リモートの最新状態を取得（推奨）

```bash
git pull origin main
```

#### 5. GitHubにプッシュ

```bash
git push origin main
```

### プッシュ後の自動デプロイ

`main`ブランチへのプッシュ後、GitHub Actionsが自動的に以下を実行する：

1. MkDocsでサイトをビルド
2. GitHub Pagesにデプロイ

**進捗確認：**
- Actions: https://github.com/takaresearch/index/actions
- 公開サイト: https://takaresearch.github.io/index/

デプロイには通常2-3分かかる。

## コンフリクト解決

リモートとローカルで同じファイルが異なる変更をされている場合、コンフリクトが発生する。

### コンフリクト発生時の対応

```bash
# コンフリクトが発生
git pull origin main

# コンフリクトファイルを確認
git status
```

コンフリクトが発生したファイルを開き、以下のマーカーを探す：

```
<<<<<<< HEAD
（ローカルの変更）
=======
（リモートの変更）
>>>>>>> commit-hash
```

### 解決手順

1. ファイルを編集して、保持したい内容のみ残す
2. マーカー（`<<<<<<<`、`=======`、`>>>>>>>`）を削除
3. ファイルを保存
4. 解決したファイルをステージング

```bash
git add コンフリクトファイル名
git commit -m "Resolve merge conflict"
git push origin main
```

## トラブルシューティング

### リモートリポジトリが設定されていない

```bash
git remote add origin https://github.com/takaresearch/index.git
```

### プッシュが拒否される（リモートが先に進んでいる）

```bash
git pull origin main --rebase
git push origin main
```

### 誤ってコミットした場合（プッシュ前）

```bash
# 直前のコミットを取り消し（変更は保持）
git reset --soft HEAD~1

# 変更も含めて取り消し
git reset --hard HEAD~1
```

### ユーザー名/メールアドレスを変更したい

```bash
git config user.name "新しい名前"
git config user.email "新しいメールアドレス"
```

## ローカルプレビュー

GitHubにプッシュする前に、ローカルでプレビュー可能：

```bash
cd c:\GITHUB_takaresearch\index

# 仮想環境がない場合は作成
python -m venv .venv

# 仮想環境を有効化（Windows）
.venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt

# プレビューサーバーを起動
mkdocs serve
```

ブラウザで `http://127.0.0.1:8000/` を開く。

## 便利なGitコマンド

```bash
# コミット履歴を表示
git log --oneline

# 変更差分を表示
git diff

# 特定ファイルの変更履歴
git log -p docs/clinical/outpatient.md

# ブランチ一覧
git branch -a

# 最新のリモート情報を取得（ダウンロードはしない）
git fetch origin
```

## 注意事項

1. **privateフォルダは追跡されない**: `.gitignore`により、`private/`内のファイルはGitHubにアップロードされない
2. **機密情報の確認**: コミット前に機密情報が含まれていないか確認する
3. **定期的なプッシュ**: 作業終了時には必ずプッシュして、リモートと同期する
4. **コミットメッセージ**: 後で見返した時に分かるよう、具体的な変更内容を記載する

## GitHub Pages設定（確認用）

GitHub Pages設定が正しく行われているか確認：

1. リポジトリの **Settings** → **Pages** を開く
2. **Build and deployment** が **GitHub Actions** になっていることを確認
3. **Branch** は自動設定されるため変更不要

## ワークフロー確認

GitHub Actionsのワークフローファイル: `.github/workflows/deploy-pages.yml`

このファイルにより、`main`ブランチへのプッシュで自動デプロイが実行される。

---

**最終更新日**: 2026年1月15日
