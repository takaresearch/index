@echo off
REM GitHubへのデプロイスクリプト
REM 使用方法: deploy.bat "コミットメッセージ"

cd /d %~dp0

echo ====================================
echo GitHub Deploy Script
echo ====================================
echo.

REM コミットメッセージの確認
if "%~1"=="" (
    echo エラー: コミットメッセージを指定してください
    echo 使用例: deploy.bat "Update documentation"
    exit /b 1
)

REM Git設定確認
echo [1/6] Git設定を確認中...
git config user.name "Taka"
git config user.email "takahisa523@gmail.com"

REM 現在の状態を表示
echo.
echo [2/6] 現在の変更を確認中...
git status

REM 変更をステージング
echo.
echo [3/6] 変更をステージング中...
git add .

REM コミット
echo.
echo [4/6] コミット中...
git commit -m "%~1"
if errorlevel 1 (
    echo コミットするものがないか、エラーが発生しました
)

REM リモートの最新を取得
echo.
echo [5/6] リモートの最新を取得中...
git pull origin main --rebase
if errorlevel 1 (
    echo エラー: プルに失敗しました。コンフリクトを解決してください
    exit /b 1
)

REM プッシュ
echo.
echo [6/6] GitHubにプッシュ中...
git push origin main
if errorlevel 1 (
    echo エラー: プッシュに失敗しました
    exit /b 1
)

echo.
echo ====================================
echo デプロイ完了！
echo ====================================
echo.
echo GitHub Actions: https://github.com/takaresearch/index/actions
echo 公開サイト: https://takaresearch.github.io/index/
echo.
echo デプロイには2-3分かかります。
echo.

pause
