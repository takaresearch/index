# GitHubへのデプロイスクリプト（PowerShell版）
# 使用方法: .\deploy.ps1 -Message "コミットメッセージ"

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

# スクリプトのディレクトリに移動
Set-Location $PSScriptRoot

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "GitHub Deploy Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Git設定
Write-Host "[1/6] Git設定を確認中..." -ForegroundColor Yellow
git config user.name "Taka"
git config user.email "takahisa523@gmail.com"

# 現在の状態を表示
Write-Host ""
Write-Host "[2/6] 現在の変更を確認中..." -ForegroundColor Yellow
git status

# 変更をステージング
Write-Host ""
Write-Host "[3/6] 変更をステージング中..." -ForegroundColor Yellow
git add .

# コミット
Write-Host ""
Write-Host "[4/6] コミット中..." -ForegroundColor Yellow
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
    Write-Host "コミットするものがないか、エラーが発生しました" -ForegroundColor Gray
}

# リモートの最新を取得
Write-Host ""
Write-Host "[5/6] リモートの最新を取得中..." -ForegroundColor Yellow
git pull origin main --rebase
if ($LASTEXITCODE -ne 0) {
    Write-Host "エラー: プルに失敗しました。コンフリクトを解決してください" -ForegroundColor Red
    exit 1
}

# プッシュ
Write-Host ""
Write-Host "[6/6] GitHubにプッシュ中..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "エラー: プッシュに失敗しました" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "デプロイ完了！" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "GitHub Actions: https://github.com/takaresearch/index/actions" -ForegroundColor Cyan
Write-Host "公開サイト: https://takaresearch.github.io/index/" -ForegroundColor Cyan
Write-Host ""
Write-Host "デプロイには2-3分かかります。" -ForegroundColor Gray
Write-Host ""
