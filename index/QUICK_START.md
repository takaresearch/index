# クイックスタートガイド

このガイドでは、最も簡単な方法でGitHubへのデプロイを行う手順を説明する。

## 📋 準備されているファイル

- `DEPLOY_GUIDE.md` - 詳細なデプロイガイド
- `git-config.bat` - Git初期設定スクリプト
- `deploy.bat` - デプロイスクリプト（バッチファイル）
- `deploy.ps1` - デプロイスクリプト（PowerShell版）

## 🚀 初回セットアップ

### 方法1: スクリプトを使用（推奨）

1. `git-config.bat` をダブルクリック
2. 設定が完了したら、任意のキーを押して終了

### 方法2: 手動設定

```bash
cd c:\GITHUB_takaresearch\index
git config user.name "Taka"
git config user.email "takahisa523@gmail.com"
git remote add origin https://github.com/takaresearch/index.git
git branch -M main
```

## 📤 日常的なデプロイ

### 方法1: バッチファイルを使用（最も簡単）

1. `deploy.bat` をダブルクリック、または
2. コマンドプロンプトで実行：

```cmd
deploy.bat "変更内容の説明"
```

例：
```cmd
deploy.bat "Update clinical documentation"
deploy.bat "Add new pathology section"
deploy.bat "Fix typos"
```

### 方法2: PowerShellスクリプトを使用

```powershell
.\deploy.ps1 -Message "変更内容の説明"
```

例：
```powershell
.\deploy.ps1 -Message "Update clinical documentation"
```

### 方法3: 手動で実行

```bash
cd c:\GITHUB_takaresearch\index
git add .
git commit -m "変更内容の説明"
git pull origin main --rebase
git push origin main
```

## ✅ デプロイ確認

デプロイ後、以下のURLで進捗と結果を確認：

- **GitHub Actions**: https://github.com/takaresearch/index/actions
- **公開サイト**: https://takaresearch.github.io/index/

通常2-3分でデプロイが完了する。

## 🔍 ローカルプレビュー

GitHubにプッシュする前に、ローカルで確認する場合：

```bash
cd c:\GITHUB_takaresearch\index

# 仮想環境がない場合は作成（初回のみ）
python -m venv .venv

# 仮想環境を有効化
.venv\Scripts\activate

# 依存パッケージをインストール（初回のみ）
pip install -r requirements.txt

# プレビューサーバーを起動
mkdocs serve
```

ブラウザで `http://127.0.0.1:8000/` を開く。

## ⚠️ トラブルシューティング

### エラー: "not a git repository"

→ `git-config.bat` を実行してGitを初期化する

### エラー: "Updates were rejected"

→ リモートに新しい変更がある。以下を実行：

```bash
git pull origin main --rebase
git push origin main
```

### コンフリクトが発生

→ `DEPLOY_GUIDE.md` の「コンフリクト解決」セクションを参照

### スクリプトが実行できない（PowerShell）

→ 実行ポリシーを変更：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📚 詳細情報

より詳しい情報は `DEPLOY_GUIDE.md` を参照してください。

---

**作成日**: 2026年1月15日
