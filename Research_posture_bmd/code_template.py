"""
姿勢推定による骨密度予測研究 - 解析コードテンプレート

このファイルは、研究の解析パイプラインの概要を示すテンプレートです。
実際のデータ収集後に、具体的なパスやパラメータを設定して使用してください。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 機械学習ライブラリ
from sklearn.model_selection import cross_validate, GridSearchCV, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, classification_report

import xgboost as xgb
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import statsmodels.api as sm

# 姿勢推定ライブラリ
import cv2
import mediapipe as mp
# または OpenPose

# 設定
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# ディレクトリ構造
BASE_DIR = Path("Research_posture_bmd")
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"
FIGURES_DIR = BASE_DIR / "figures"

# ディレクトリ作成
for dir_path in [DATA_DIR, RAW_DIR, PROCESSED_DIR, RESULTS_DIR, FIGURES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("姿勢推定による骨密度予測研究 - 解析パイプライン")
print("=" * 80)


# ============================================================================
# 1. 姿勢推定とパラメータ抽出
# ============================================================================

class PoseEstimator:
    """姿勢推定とパラメータ抽出のクラス"""
    
    def __init__(self, method='mediapipe'):
        """
        Parameters
        ----------
        method : str
            'mediapipe' or 'openpose'
        """
        self.method = method
        if method == 'mediapipe':
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(
                static_image_mode=True,
                model_complexity=2,
                min_detection_confidence=0.5
            )
    
    def process_image(self, image_path):
        """
        画像から姿勢を推定し、キーポイントを取得
        
        Parameters
        ----------
        image_path : str or Path
            画像ファイルのパス
            
        Returns
        -------
        landmarks : dict
            検出されたキーポイントの座標
        """
        image = cv2.imread(str(image_path))
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = self.pose.process(image_rgb)
        
        if not results.pose_landmarks:
            print(f"警告: {image_path} でキーポイントが検出されませんでした")
            return None
        
        # ランドマークを辞書形式で保存
        landmarks = {}
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            landmarks[idx] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
        
        return landmarks
    
    def calculate_angle(self, p1, p2, p3):
        """
        3点から角度を計算
        
        Parameters
        ----------
        p1, p2, p3 : tuple
            (x, y)座標
            
        Returns
        -------
        angle : float
            角度(度)
        """
        v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        
        return np.degrees(angle)
    
    def extract_posture_parameters(self, landmarks, height_cm):
        """
        キーポイントから姿勢パラメータを抽出
        
        Parameters
        ----------
        landmarks : dict
            キーポイントの座標
        height_cm : float
            被験者の身長(cm)
            
        Returns
        -------
        parameters : dict
            姿勢パラメータ
        """
        # MediaPipeのランドマークインデックス
        # 0: nose, 11: left_shoulder, 12: right_shoulder
        # 23: left_hip, 24: right_hip, etc.
        
        parameters = {}
        
        try:
            # 1. 胸椎後弯角度(Thoracic Kyphosis Angle)
            # 肩峰、体幹中点、股関節を使って近似
            shoulder = (
                (landmarks[11]['x'] + landmarks[12]['x']) / 2,
                (landmarks[11]['y'] + landmarks[12]['y']) / 2
            )
            hip = (
                (landmarks[23]['x'] + landmarks[24]['x']) / 2,
                (landmarks[23]['y'] + landmarks[24]['y']) / 2
            )
            mid_trunk = (
                (shoulder[0] + hip[0]) / 2,
                (shoulder[1] + hip[1]) / 2 - 0.1  # 前方にシフト
            )
            
            kyphosis_angle = self.calculate_angle(shoulder, mid_trunk, hip)
            parameters['kyphosis_angle'] = kyphosis_angle
            
            # 2. 頭部前方位(Forward Head Posture)
            # 耳(近似: 鼻)から肩峰への水平距離
            ear = (landmarks[0]['x'], landmarks[0]['y'])
            fhp_distance = abs(ear[0] - shoulder[0])
            # 身長で正規化
            fhp_normalized = (fhp_distance / (landmarks[23]['y'] - landmarks[0]['y'])) * 100
            parameters['forward_head_posture'] = fhp_normalized
            
            # 3. 腰椎前弯角度(Lumbar Lordosis Angle)
            # 股関節、腰部中点、膝を使って近似
            knee = (
                (landmarks[25]['x'] + landmarks[26]['x']) / 2,
                (landmarks[25]['y'] + landmarks[26]['y']) / 2
            )
            lumbar_mid = (
                hip[0] + 0.05,  # 前方にシフト
                (hip[1] + shoulder[1]) / 2
            )
            
            lordosis_angle = self.calculate_angle(shoulder, lumbar_mid, hip)
            parameters['lordosis_angle'] = lordosis_angle
            
            # 4. 矢状面垂直軸(Sagittal Vertical Axis, SVA)
            # 頸部基部から股関節への水平距離
            neck_base = shoulder
            sva_distance = abs(neck_base[0] - hip[0])
            sva_normalized = (sva_distance / (landmarks[23]['y'] - landmarks[0]['y'])) * 100
            parameters['sva'] = sva_normalized
            
            # 5. 体幹傾斜角度(Trunk Inclination)
            trunk_vector = (shoulder[0] - hip[0], shoulder[1] - hip[1])
            trunk_angle = np.degrees(np.arctan2(trunk_vector[0], trunk_vector[1]))
            parameters['trunk_inclination'] = abs(trunk_angle)
            
            # 6. 頭頸部角度(Craniovertebral Angle)
            ear_to_shoulder = self.calculate_angle(
                ear,
                shoulder,
                (shoulder[0] + 0.1, shoulder[1])  # 水平線
            )
            parameters['craniovertebral_angle'] = ear_to_shoulder
            
        except Exception as e:
            print(f"エラー: 姿勢パラメータの抽出に失敗しました: {e}")
            return None
        
        return parameters


def process_all_images(image_dir, output_csv):
    """
    すべての画像を処理し、姿勢パラメータを抽出
    
    Parameters
    ----------
    image_dir : Path
        画像ディレクトリ
    output_csv : Path
        出力CSVファイルのパス
    """
    estimator = PoseEstimator(method='mediapipe')
    
    results = []
    
    for image_path in sorted(image_dir.glob("*.jpg")):
        # ファイル名から被験者IDと撮影回数を抽出
        # 例: subject_001_1.jpg -> ID=001, trial=1
        filename = image_path.stem
        parts = filename.split('_')
        subject_id = parts[1]
        trial = int(parts[2])
        
        print(f"処理中: {filename}")
        
        # 身長を取得(clinical_data.csvから)
        # ここでは仮に170cmとする
        height_cm = 170.0
        
        landmarks = estimator.process_image(image_path)
        if landmarks is None:
            continue
        
        parameters = estimator.extract_posture_parameters(landmarks, height_cm)
        if parameters is None:
            continue
        
        result = {
            'subject_id': subject_id,
            'trial': trial,
            **parameters
        }
        results.append(result)
    
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"姿勢パラメータを {output_csv} に保存しました")
    
    return df


# ============================================================================
# 2. データの読み込みと前処理
# ============================================================================

def load_and_preprocess_data():
    """
    データを読み込み、前処理を行う
    
    Returns
    -------
    df : pd.DataFrame
        前処理済みのデータフレーム
    """
    print("\n" + "=" * 80)
    print("2. データの読み込みと前処理")
    print("=" * 80)
    
    # 姿勢パラメータの読み込み
    pose_df = pd.read_csv(PROCESSED_DIR / "pose_parameters.csv")
    
    # 2枚の写真の平均を計算
    pose_avg = pose_df.groupby('subject_id').mean().reset_index()
    
    # 臨床データの読み込み(DXA結果、年齢、性別など)
    clinical_df = pd.read_csv(PROCESSED_DIR / "clinical_data.csv")
    
    # データの結合
    df = pd.merge(pose_avg, clinical_df, on='subject_id')
    
    print(f"データ読み込み完了: {len(df)}名")
    print(f"変数: {df.columns.tolist()}")
    
    # 欠損値の確認
    print("\n欠損値:")
    print(df.isnull().sum())
    
    # 欠損値の処理
    # 欠損率5%未満の変数は中央値で補完
    for col in df.columns:
        missing_rate = df[col].isnull().sum() / len(df)
        if 0 < missing_rate < 0.05:
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].median(), inplace=True)
                print(f"{col}: 中央値で補完しました")
    
    # 外れ値の検出
    print("\n外れ値の検出:")
    continuous_vars = ['age', 'bmi', 'lumbar_bmd', 'femoral_neck_bmd',
                       'kyphosis_angle', 'forward_head_posture']
    
    for var in continuous_vars:
        mean = df[var].mean()
        std = df[var].std()
        outliers = df[(df[var] < mean - 3*std) | (df[var] > mean + 3*std)]
        if len(outliers) > 0:
            print(f"{var}: {len(outliers)}個の外れ値を検出")
    
    return df


# ============================================================================
# 3. 記述統計
# ============================================================================

def descriptive_statistics(df):
    """
    記述統計を計算し、表とグラフを生成
    
    Parameters
    ----------
    df : pd.DataFrame
        データフレーム
    """
    print("\n" + "=" * 80)
    print("3. 記述統計")
    print("=" * 80)
    
    # 基本統計量
    print("\n被験者特性:")
    print(df[['age', 'bmi', 'lumbar_bmd', 'femoral_neck_bmd']].describe())
    
    print(f"\n性別分布:")
    print(df['sex'].value_counts())
    
    # 骨密度分類
    # T-scoreの計算(簡易版: 若年成人平均を仮定)
    # 実際にはDXA装置が提供するT-scoreを使用
    df['lumbar_tscore'] = (df['lumbar_bmd'] - 1.0) / 0.15  # 仮の値
    
    def classify_bmd(tscore):
        if tscore >= -1.0:
            return 'Normal'
        elif tscore > -2.5:
            return 'Osteopenia'
        else:
            return 'Osteoporosis'
    
    df['bmd_category'] = df['lumbar_tscore'].apply(classify_bmd)
    
    print(f"\n骨密度分類:")
    print(df['bmd_category'].value_counts())
    
    # 姿勢パラメータの記述統計
    pose_vars = ['kyphosis_angle', 'forward_head_posture', 'lordosis_angle',
                 'sva', 'trunk_inclination', 'craniovertebral_angle']
    
    print("\n姿勢パラメータ:")
    print(df[pose_vars].describe())
    
    # 可視化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, var in enumerate(pose_vars):
        df[var].hist(bins=20, ax=axes[i], edgecolor='black')
        axes[i].set_title(var)
        axes[i].set_xlabel('Value')
        axes[i].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "posture_parameters_distribution.png", dpi=300)
    print(f"\n図を保存しました: {FIGURES_DIR / 'posture_parameters_distribution.png'}")
    plt.close()
    
    return df


# ============================================================================
# 4. 相関分析
# ============================================================================

def correlation_analysis(df):
    """
    相関分析を実施
    
    Parameters
    ----------
    df : pd.DataFrame
        データフレーム
    """
    print("\n" + "=" * 80)
    print("4. 相関分析")
    print("=" * 80)
    
    # 変数選択
    pose_vars = ['kyphosis_angle', 'forward_head_posture', 'lordosis_angle',
                 'sva', 'trunk_inclination', 'craniovertebral_angle']
    bmd_vars = ['lumbar_bmd', 'femoral_neck_bmd']
    
    # Pearson相関係数
    print("\n腰椎BMDとの相関(Pearson):")
    for var in pose_vars:
        r, p = pearsonr(df[var], df['lumbar_bmd'])
        print(f"{var:30s}: r = {r:6.3f}, p = {p:.4f}")
    
    print("\n大腿骨頸部BMDとの相関(Pearson):")
    for var in pose_vars:
        r, p = pearsonr(df[var], df['femoral_neck_bmd'])
        print(f"{var:30s}: r = {r:6.3f}, p = {p:.4f}")
    
    # 相関行列とヒートマップ
    corr_vars = ['age', 'bmi'] + pose_vars + bmd_vars
    corr_matrix = df[corr_vars].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_matrix.png", dpi=300)
    print(f"\n相関行列を保存しました: {FIGURES_DIR / 'correlation_matrix.png'}")
    plt.close()
    
    return corr_matrix


# ============================================================================
# 5. 機械学習モデルの構築と評価
# ============================================================================

def build_and_evaluate_models(df):
    """
    機械学習モデルを構築し、評価する
    
    Parameters
    ----------
    df : pd.DataFrame
        データフレーム
        
    Returns
    -------
    results : dict
        各モデルの評価結果
    """
    print("\n" + "=" * 80)
    print("5. 機械学習モデルの構築と評価")
    print("=" * 80)
    
    # 特徴量とターゲット変数の定義
    pose_features = ['kyphosis_angle', 'forward_head_posture', 'lordosis_angle',
                     'sva', 'trunk_inclination', 'craniovertebral_angle']
    
    # ベースラインモデルの特徴量
    baseline_features = ['age', 'sex_encoded']
    
    # 拡張モデルの特徴量
    extended_features = baseline_features + pose_features
    
    # 性別をエンコード
    df['sex_encoded'] = df['sex'].map({'M': 0, 'F': 1})
    
    # ターゲット変数
    target = 'lumbar_bmd'
    
    # データ分割用の設定
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    
    # 評価指標の定義
    scoring = {
        'r2': 'r2',
        'neg_mae': 'neg_mean_absolute_error',
        'neg_rmse': 'neg_root_mean_squared_error'
    }
    
    # モデルの定義
    models = {
        'Baseline_LinearRegression': (LinearRegression(), baseline_features),
        'LinearRegression': (LinearRegression(), extended_features),
        'Ridge': (Ridge(random_state=RANDOM_STATE), extended_features),
        'Lasso': (Lasso(random_state=RANDOM_STATE), extended_features),
        'RandomForest': (RandomForestRegressor(random_state=RANDOM_STATE), extended_features),
        'XGBoost': (xgb.XGBRegressor(random_state=RANDOM_STATE), extended_features),
        'SVR': (SVR(), extended_features),
        'MLP': (MLPRegressor(random_state=RANDOM_STATE, max_iter=1000), extended_features)
    }
    
    results = {}
    
    for name, (model, features) in models.items():
        print(f"\n{name}を評価中...")
        
        X = df[features]
        y = df[target]
        
        # スケーリング(線形モデルとSVRに必要)
        if name in ['Ridge', 'Lasso', 'SVR', 'MLP']:
            scaler = StandardScaler()
            X = pd.DataFrame(scaler.fit_transform(X), columns=features)
        
        # 交差検証
        cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring,
                                     return_train_score=True)
        
        results[name] = {
            'r2_mean': cv_results['test_r2'].mean(),
            'r2_std': cv_results['test_r2'].std(),
            'mae_mean': -cv_results['test_neg_mae'].mean(),
            'mae_std': cv_results['test_neg_mae'].std(),
            'rmse_mean': -cv_results['test_neg_rmse'].mean(),
            'rmse_std': cv_results['test_neg_rmse'].std()
        }
        
        print(f"  R² = {results[name]['r2_mean']:.3f} ± {results[name]['r2_std']:.3f}")
        print(f"  MAE = {results[name]['mae_mean']:.3f} ± {results[name]['mae_std']:.3f}")
        print(f"  RMSE = {results[name]['rmse_mean']:.3f} ± {results[name]['rmse_std']:.3f}")
    
    # 結果の可視化
    plot_model_comparison(results)
    
    return results


def plot_model_comparison(results):
    """
    モデルの性能を比較するグラフを作成
    
    Parameters
    ----------
    results : dict
        各モデルの評価結果
    """
    models = list(results.keys())
    r2_means = [results[m]['r2_mean'] for m in models]
    r2_stds = [results[m]['r2_std'] for m in models]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    x_pos = np.arange(len(models))
    
    ax.bar(x_pos, r2_means, yerr=r2_stds, align='center', alpha=0.7,
           ecolor='black', capsize=10)
    ax.set_ylabel('R² Score')
    ax.set_xlabel('Model')
    ax.set_title('Model Performance Comparison (Lumbar BMD Prediction)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "model_comparison.png", dpi=300)
    print(f"\nモデル比較図を保存しました: {FIGURES_DIR / 'model_comparison.png'}")
    plt.close()


# ============================================================================
# 6. 多変量回帰分析
# ============================================================================

def multivariate_regression(df):
    """
    多変量回帰分析を実施
    
    Parameters
    ----------
    df : pd.DataFrame
        データフレーム
    """
    print("\n" + "=" * 80)
    print("6. 多変量回帰分析")
    print("=" * 80)
    
    # 特徴量
    features = ['age', 'sex_encoded', 'kyphosis_angle', 'forward_head_posture', 'bmi']
    
    X = df[features]
    y = df['lumbar_bmd']
    
    # 定数項の追加
    X = sm.add_constant(X)
    
    # OLSモデル
    model = sm.OLS(y, X).fit()
    
    print(model.summary())
    
    # 結果をファイルに保存
    with open(RESULTS_DIR / "multivariate_regression_summary.txt", 'w') as f:
        f.write(str(model.summary()))
    
    print(f"\n回帰分析結果を保存しました: {RESULTS_DIR / 'multivariate_regression_summary.txt'}")
    
    return model


# ============================================================================
# 7. 分類性能評価(骨粗鬆症 vs 非骨粗鬆症)
# ============================================================================

def classification_evaluation(df):
    """
    骨粗鬆症の分類性能を評価
    
    Parameters
    ----------
    df : pd.DataFrame
        データフレーム
    """
    print("\n" + "=" * 80)
    print("7. 分類性能評価")
    print("=" * 80)
    
    # 二値分類ターゲット(骨粗鬆症: T-score ≤ -2.5)
    df['osteoporosis'] = (df['lumbar_tscore'] <= -2.5).astype(int)
    
    print(f"骨粗鬆症の割合: {df['osteoporosis'].mean():.1%}")
    
    # 特徴量
    extended_features = ['age', 'sex_encoded', 'kyphosis_angle',
                        'forward_head_posture', 'lordosis_angle',
                        'sva', 'trunk_inclination', 'craniovertebral_angle']
    
    X = df[extended_features]
    y = df['osteoporosis']
    
    # スケーリング
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 回帰モデルで確率を予測(BMD予測 -> T-score -> 確率)
    # ここでは簡略化のため、ロジスティック回帰を使用
    from sklearn.linear_model import LogisticRegression
    
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    
    y_true_all = []
    y_pred_proba_all = []
    
    for train_idx, test_idx in cv.split(X_scaled):
        X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        clf = LogisticRegression(random_state=RANDOM_STATE)
        clf.fit(X_train, y_train)
        
        y_pred_proba = clf.predict_proba(X_test)[:, 1]
        
        y_true_all.extend(y_test)
        y_pred_proba_all.extend(y_pred_proba)
    
    # ROC曲線
    fpr, tpr, thresholds = roc_curve(y_true_all, y_pred_proba_all)
    auc = roc_auc_score(y_true_all, y_pred_proba_all)
    
    print(f"\nAUC: {auc:.3f}")
    
    # Youden指数で最適カットオフ値を決定
    youden_index = tpr - fpr
    optimal_idx = np.argmax(youden_index)
    optimal_threshold = thresholds[optimal_idx]
    
    print(f"最適カットオフ値: {optimal_threshold:.3f}")
    print(f"  感度: {tpr[optimal_idx]:.3f}")
    print(f"  特異度: {1 - fpr[optimal_idx]:.3f}")
    
    # ROC曲線のプロット
    plt.figure(figsize=(8, 8))
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {auc:.3f})', linewidth=2)
    plt.plot([0, 1], [0, 1], 'k--', label='Random classifier')
    plt.scatter(fpr[optimal_idx], tpr[optimal_idx], marker='o', color='red',
                s=100, label=f'Optimal threshold = {optimal_threshold:.3f}')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve - Osteoporosis Classification')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "roc_curve.png", dpi=300)
    print(f"\nROC曲線を保存しました: {FIGURES_DIR / 'roc_curve.png'}")
    plt.close()
    
    # 混同行列
    y_pred = (np.array(y_pred_proba_all) >= optimal_threshold).astype(int)
    cm = confusion_matrix(y_true_all, y_pred)
    
    print("\n混同行列:")
    print(cm)
    
    # 分類レポート
    print("\n分類レポート:")
    print(classification_report(y_true_all, y_pred,
                                target_names=['Non-osteoporosis', 'Osteoporosis']))
    
    return auc, optimal_threshold


# ============================================================================
# 8. メイン実行関数
# ============================================================================

def main():
    """
    解析パイプラインのメイン関数
    """
    print("\n" + "=" * 80)
    print("解析パイプライン開始")
    print("=" * 80)
    
    # ステップ1: 画像処理と姿勢推定(データ収集後に実行)
    # image_dir = RAW_DIR / "images"
    # if image_dir.exists():
    #     pose_df = process_all_images(image_dir, PROCESSED_DIR / "pose_parameters.csv")
    
    # ステップ2: データの読み込みと前処理
    # df = load_and_preprocess_data()
    
    # ステップ3: 記述統計
    # df = descriptive_statistics(df)
    
    # ステップ4: 相関分析
    # corr_matrix = correlation_analysis(df)
    
    # ステップ5: 機械学習モデルの構築と評価
    # results = build_and_evaluate_models(df)
    
    # ステップ6: 多変量回帰分析
    # model = multivariate_regression(df)
    
    # ステップ7: 分類性能評価
    # auc, threshold = classification_evaluation(df)
    
    print("\n" + "=" * 80)
    print("解析パイプライン完了")
    print("=" * 80)
    
    # 注: 実際のデータ収集後に、各ステップのコメントを外して実行してください


if __name__ == "__main__":
    # サンプルデータでのテスト(実際のデータがない場合)
    print("注意: このコードはテンプレートです。")
    print("実際のデータ収集後に、適切なパスとパラメータを設定して実行してください。")
    
    # main()  # 実際のデータがある場合にコメントを外す
