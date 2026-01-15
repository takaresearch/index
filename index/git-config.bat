@echo off
REM Git初期設定スクリプト
REM このスクリプトは初回セットアップ時に実行する

cd /d %~dp0

echo ====================================
echo Git Initial Setup
echo ====================================
echo.

echo [1/3] ユーザー情報を設定中...
git config user.name "Taka"
git config user.email "takahisa523@gmail.com"
echo ✓ ユーザー名: Taka
echo ✓ メールアドレス: takahisa523@gmail.com

echo.
echo [2/3] リモートリポジトリを設定中...
git remote remove origin 2>nul
git remote add origin https://github.com/takaresearch/index.git
echo ✓ リモートリポジトリ: https://github.com/takaresearch/index.git

echo.
echo [3/3] ブランチを設定中...
git branch -M main
echo ✓ デフォルトブランチ: main

echo.
echo ====================================
echo 設定完了！
echo ====================================
echo.
echo 現在の設定:
git config user.name
git config user.email
git remote -v
echo.

pause
