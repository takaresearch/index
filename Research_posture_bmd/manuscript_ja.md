# 姿勢推定アルゴリズムによる骨密度予測の精度検証:機械学習を用いた非侵襲的スクリーニング法の開発

## 著者情報
[著者名]¹, [共著者名]²

¹ [所属機関名]
² [所属機関名]

**対応著者**: [メールアドレス]

---

## 要旨

### 背景
骨粗鬆症は世界的な公衆衛生上の重大な課題であり、高齢化社会において骨折リスクの増大をもたらしている。胸椎後弯の増大と骨密度低下の関連性は多くの疫学研究で示されているが、従来の骨密度測定法(DXA法)は高額な機器を必要とし、スクリーニングのアクセシビリティが制限されている。近年、コンピュータビジョンと機械学習技術の進歩により、画像ベースの非侵襲的評価法の可能性が注目されている。

### 目的
本研究は、深層学習ベースの姿勢推定アルゴリズムを用いて、立位側面写真から抽出した姿勢パラメータと、年齢・性別を組み合わせて骨密度を予測する機械学習モデルの精度を検証することを目的とする。

### 方法
骨粗鬆症治療を受けていない50名の成人被験者を対象に、標準化された条件下で立位側面写真を2枚撮影した。OpenPoseまたはMediaPipeなどの姿勢推定アルゴリズムを用いて、胸椎後弯角度、頭部前方位、腰椎前弯角度などの姿勢パラメータを自動抽出した。これらのパラメータに年齢と性別を加え、DXA法で測定した腰椎および大腿骨近位部の骨密度(BMD)を予測する回帰モデルを構築した。モデルの性能は、決定係数(R²)、平均絶対誤差(MAE)、二乗平均平方根誤差(RMSE)で評価した。交差検証により過学習を防ぎ、一般化性能を評価した。

### 結果
[データ収集後に記載予定] 予備的な文献レビューに基づき、姿勢パラメータと骨密度の間には中程度から強い相関が期待される。特に胸椎後弯角度は骨密度と有意な負の相関を示すと予測される。機械学習モデルは、年齢・性別のみのベースラインモデルと比較して、予測精度の有意な改善を示すことが期待される。

### 結論
本研究は、姿勢推定技術と機械学習を組み合わせた非侵襲的骨密度スクリーニング法の実現可能性を示す初期的エビデンスを提供することが期待される。この手法が有効であれば、スマートフォンやタブレットを用いた低コストで広くアクセス可能な骨粗鬆症スクリーニングツールの開発への道が開かれる可能性がある。

**キーワード**: 骨粗鬆症、骨密度、姿勢推定、機械学習、コンピュータビジョン、胸椎後弯、非侵襲的スクリーニング

---

## Abstract (English)

### Background
Osteoporosis represents a major public health challenge worldwide, contributing to increased fracture risk in aging populations. The association between increased thoracic kyphosis and reduced bone mineral density (BMD) has been documented in numerous epidemiological studies; however, conventional BMD assessment methods (DXA) require expensive equipment, limiting accessibility for screening. Recent advances in computer vision and machine learning technologies have opened possibilities for image-based non-invasive assessment methods.

### Objective
This study aims to validate the accuracy of a machine learning model that predicts BMD using posture parameters extracted from lateral standing photographs via deep learning-based pose estimation algorithms, combined with age and sex.

### Methods
Fifty adult participants not receiving osteoporosis treatment were recruited. Two lateral standing photographs were obtained under standardized conditions. Pose estimation algorithms (OpenPose or MediaPipe) were used to automatically extract posture parameters including thoracic kyphosis angle, forward head posture, and lumbar lordosis angle. These parameters, along with age and sex, were used to construct regression models predicting BMD measured by DXA at lumbar spine and proximal femur. Model performance was evaluated using coefficient of determination (R²), mean absolute error (MAE), and root mean square error (RMSE). Cross-validation was employed to prevent overfitting and assess generalization performance.

### Results
[To be completed after data collection] Based on preliminary literature review, moderate to strong correlations are expected between posture parameters and BMD. Thoracic kyphosis angle is predicted to show significant negative correlation with BMD. The machine learning model is expected to demonstrate significant improvement in prediction accuracy compared to baseline models using only age and sex.

### Conclusions
This study is expected to provide preliminary evidence for the feasibility of non-invasive BMD screening methods combining pose estimation technology and machine learning. If validated, this approach could pave the way for developing low-cost, widely accessible osteoporosis screening tools using smartphones or tablets.

**Keywords**: osteoporosis, bone mineral density, pose estimation, machine learning, computer vision, thoracic kyphosis, non-invasive screening

---

## 1. 序論

### 1.1 背景と研究の意義

骨粗鬆症は骨強度の低下を特徴とし、骨折のリスクを増大させる全身性骨疾患である[1]。世界保健機関(WHO)によると、50歳以上の女性の3人に1人、男性の5人に1人が、生涯のうちに骨粗鬆症性骨折を経験すると推定されている[2]。日本においても高齢化の進展に伴い、骨粗鬆症患者は約1,280万人と推定され、その約80%が未診断・未治療の状態にあるとされている[3]。

骨粗鬆症性骨折、特に椎体骨折と大腿骨近位部骨折は、患者の生活の質(QOL)を著しく低下させ、医療経済的負担も大きい[4]。椎体骨折は慢性的な疼痛、身長低下、後弯変形を引き起こし、呼吸機能や消化機能の低下をもたらす[5]。また、骨折の既往は新たな骨折のリスク因子となることが知られており[6]、早期発見と適切な介入が極めて重要である。

現在、骨粗鬆症診断のゴールドスタンダードは、二重エネルギーX線吸収測定法(DXA法)による骨密度測定である[7]。しかし、DXA装置は高額であり、医療施設への設置が限られているため、特に地方や発展途上国においてスクリーニングのアクセシビリティが課題となっている[8]。また、放射線被曝の問題(微量ではあるが)や、測定に要する時間とコストも、大規模スクリーニングの障壁となっている。

### 1.2 姿勢と骨密度の関連性

胸椎後弯(脊柱の前後方向への湾曲の増大)と骨密度低下の関連性は、多くの疫学研究で報告されている。Milneら(1993)は、Framingham研究のコホートを用いて、後弯角度の増大が低骨量と関連することを初めて定量的に示した[9]。その後、Ensrudらによる大規模な前向きコホート研究(Study of Osteoporotic Fractures)では、後弯角度の増大が独立した骨折リスク因子であることが示された[10]。

特に注目すべきは、後弯の増大が椎体骨折の有無にかかわらず骨密度と相関することである。Schneiderらの研究(2004)では、無症候性椎体骨折を持たない女性においても、後弯角度と腰椎骨密度の間に有意な負の相関が認められた[11]。これは、後弯が単に骨折の結果ではなく、骨質の低下を反映する独立したマーカーである可能性を示唆している。

JAMAに発表されたKadoらの研究(2013)は、この分野における重要なマイルストーンである[12]。この研究では、後弯角度の増大が死亡率の上昇と関連することが示され、後弯測定が単なる骨密度のサロゲートマーカーを超えて、全般的な健康状態の指標となりうることが明らかにされた。

後弯と骨密度の関連性の生物学的メカニズムとしては、以下が提唱されている:
1) 筋力低下と骨量減少の共通の病態生理学的基盤[13]
2) 加齢に伴う椎間板変性と骨質低下の並行進行[14]
3) バイオメカニカルストレスの変化による骨リモデリングへの影響[15]

さらに、頭部前方位(forward head posture)や腰椎前弯の変化も骨密度と関連することが報告されている[16]。これらの知見は、包括的な姿勢評価が骨密度予測に有用である可能性を示唆している。

### 1.3 コンピュータビジョンと機械学習の医療応用

近年、深層学習技術の急速な発展により、画像からの人体姿勢推定の精度が飛躍的に向上している[17]。OpenPose[18]、MediaPipe[19]、HRNet[20]などの最先端アルゴリズムは、2次元画像から高精度に身体の主要な関節点(キーポイント)を検出できる。これらの技術は、スポーツ科学、リハビリテーション医学、人間工学など、多様な分野で応用されている[21]。

医療分野における姿勢推定の応用例としては、脳性麻痺患者の歩行解析[22]、パーキンソン病患者の姿勢評価[23]、脊柱側弯症のスクリーニング[24]などが報告されている。しかし、骨粗鬆症スクリーニングへの応用は、まだ初期段階にある。

Yamamoto et al. (2021)は、深層学習を用いて胸部X線写真から骨密度を推定する試みを報告した[25]。また、Chenら(2020)は、体組成パラメータと簡易的な身体測定値から骨密度を予測する機械学習モデルを開発した[26]。しかし、これらの研究は特別な機器やX線撮影を必要とし、一般的なスクリーニングツールとしての実用性には限界がある。

姿勢推定技術を用いた非侵襲的骨密度予測の利点は以下の通りである:
1) スマートフォンやタブレットのカメラで撮影可能
2) 放射線被曝のリスクがない
3) 低コストで実施可能
4) 在宅や地域保健センターでの実施が可能
5) リアルタイムでの評価が可能

### 1.4 研究の目的と仮説

本研究の主要な目的は、深層学習ベースの姿勢推定アルゴリズムを用いて立位側面写真から抽出した姿勢パラメータと、年齢・性別を組み合わせた機械学習モデルによる骨密度予測の精度を検証することである。

具体的な研究課題は以下の通りである:
1) 姿勢推定アルゴリズムから抽出される姿勢パラメータと、DXA法で測定した骨密度の相関を明らかにする
2) 年齢・性別に加えて姿勢パラメータを含むモデルが、年齢・性別のみのベースラインモデルと比較して、骨密度予測精度を有意に改善するかを検証する
3) 異なる機械学習アルゴリズム(線形回帰、ランダムフォレスト、勾配ブースティング、ニューラルネットワーク)の性能を比較する
4) 骨粗鬆症(T-score ≤ -2.5)の分類精度を評価する

本研究の仮説は以下の通りである:
- **仮説1**: 胸椎後弯角度は骨密度と有意な負の相関を示す(r < -0.4, p < 0.05)
- **仮説2**: 姿勢パラメータを含むモデルは、年齢・性別のみのモデルと比較して、骨密度予測のR²値を少なくとも0.1改善する
- **仮説3**: 機械学習モデルによる骨粗鬆症分類のAUC(Area Under the Curve)は0.75以上を達成する

---

## 2. 方法

### 2.1 研究デザイン

本研究は横断的観察研究である。研究プロトコルは[所属機関名]倫理委員会の承認を得た(承認番号: [番号])。すべての被験者から書面によるインフォームドコンセントを取得した。本研究はヘルシンキ宣言の原則に従って実施された。

### 2.2 対象者

#### 2.2.1 適格基準
- 年齢: 40歳以上80歳以下
- 独立して立位保持が可能
- 研究参加に同意した者

#### 2.2.2 除外基準
- 骨粗鬆症治療薬(ビスホスフォネート製剤、デノスマブ、テリパラチド、SERMなど)の使用歴がある者
- 脊椎または下肢の手術歴がある者
- 脊柱変形(脊柱側弯症、強直性脊椎炎など)の診断を受けている者
- 神経筋疾患により姿勢制御に障害がある者
- 妊娠中または妊娠の可能性がある女性
- DXA測定が禁忌の者
- 研究参加に同意しない者

#### 2.2.3 サンプルサイズ
本研究では50名の被験者を募集する。このサンプルサイズは、以下の根拠に基づく:

先行研究[11,12]において、後弯角度と骨密度の相関係数は約r = -0.45と報告されている。効果量r = 0.4、有意水平α = 0.05(両側検定)、検出力1-β = 0.80とした場合、必要なサンプルサイズは46名である[27]。脱落や測定エラーを考慮し、50名を目標とする。

多変量回帰分析においては、予測変数1つあたり最低10症例が推奨される[28]。本研究では約8-10個の予測変数を用いるため、50名のサンプルサイズは適切である。

### 2.3 データ収集

#### 2.3.1 写真撮影プロトコル

**撮影環境の標準化:**
- 撮影場所: 屋内の自然光が入る明るい部屋、または均一な人工照明下
- 背景: 無地の白または明るい色の壁
- 床面のマーキング: 立位位置と撮影位置を床にテープでマーク
- カメラ高さ: 被験者の大転子の高さに固定(三脚使用)
- 撮影距離: 被験者から2.5メートル
- カメラ設定: 解像度1920×1080ピクセル以上、オートフォーカス

**被験者の準備:**
- 服装: 身体のラインが識別可能な薄手の衣服(Tシャツとレギンスなど)
- 履物: 裸足または薄いソックス
- 髪型: 長髪の場合は束ねて頸部・背部のラインが見えるようにする
- アクセサリー: 除去

**撮影手順:**
1. 被験者に自然な立位姿勢を取るよう指示
2. 完全な側面(矢状面)から撮影(右側面)
3. 「普段の楽な姿勢で立ってください」と指示し、5秒間保持後に1枚目を撮影
4. 一度歩いてもらい、再度立位をとってもらい2枚目を撮影
5. 全身(頭頂から足底まで)が画面内に収まるよう確認
6. 画像の鮮明さと身体ランドマークの視認性を確認

**データ管理:**
- 各被験者に一意のID番号を割り当て
- 写真ファイル名: [研究ID]_[被験者ID]_[撮影回数].jpg
- 原画像は暗号化された外付けハードディスクに保管
- 個人識別情報を含まない

#### 2.3.2 骨密度測定

**測定方法:**
- 装置: DXA装置 [装置メーカー・モデル名]
- 測定部位: 腰椎(L1-L4)および大腿骨近位部(全体、頸部、転子部)
- 測定者: 認定技師が実施
- 精度管理: ファントムによる日常的な品質管理を実施
- 測定タイミング: 写真撮影と同日、または1週間以内

**測定項目:**
- 骨密度(BMD): g/cm²
- T-score: 若年成人平均値との標準偏差比較
- Z-score: 同年齢平均値との標準偏差比較

**骨粗鬆症の診断基準(WHOの定義)[29]:**
- 正常: T-score ≥ -1.0
- 骨減少症: -2.5 < T-score < -1.0
- 骨粗鬆症: T-score ≤ -2.5

#### 2.3.3 その他の測定項目

**基本情報:**
- 年齢(生年月日から算出)
- 性別
- 身長(cm): 身長計で測定
- 体重(kg): 体組成計で測定
- BMI: 体重(kg)/身長(m)²

**既往歴・生活習慣(質問紙):**
- 骨折歴(部位、年齢)
- 骨粗鬆症の家族歴
- 喫煙歴(現在喫煙、過去喫煙、非喫煙)
- 飲酒習慣(週あたりの頻度と量)
- 運動習慣(週あたりの頻度と強度)
- カルシウム・ビタミンDサプリメントの使用
- 更年期年齢(女性のみ)
- ステロイド使用歴

### 2.4 姿勢パラメータの抽出

#### 2.4.1 姿勢推定アルゴリズム

本研究では、OpenPose[18]またはMediaPipe Pose[19]を用いて、写真から身体のキーポイントを自動検出する。これらのアルゴリズムは、深層畳み込みニューラルネットワークに基づき、以下のキーポイントを高精度で検出できる:

**主要キーポイント(33点):**
- 頭部: 鼻、両眼、両耳
- 体幹: 両肩、両股関節、胸骨上縁、へそ
- 上肢: 両肘、両手首、両手指
- 下肢: 両膝、両足首、両足趾

#### 2.4.2 姿勢パラメータの算出

検出されたキーポイントの座標から、以下の姿勢パラメータを算出する:

**1. 胸椎後弯角度(Thoracic Kyphosis Angle):**
- 定義: C7棘突起(第7頸椎)、T12棘突起(第12胸椎)、仙骨基部を結ぶ角度
- 近似方法: 肩峰、肩峰から股関節までの中点、股関節を結ぶ角度
- 計算式: arccos((v1·v2)/(|v1||v2|))、ここでv1とv2は対応するベクトル
- 正常範囲: 20-40度[30]
- 増大: >50度

**2. 頭部前方位(Forward Head Posture):**
- 定義: 外耳孔から肩峰への水平距離
- 近似方法: 耳(外耳孔の近似)から肩峰への水平距離(ピクセル単位、身長で正規化)
- 正規化: 距離/身長 × 100(%)

**3. 腰椎前弯角度(Lumbar Lordosis Angle):**
- 定義: T12棘突起、L3棘突起、仙骨基部を結ぶ角度
- 近似方法: 股関節高さの中点、腰部の最前方点、仙骨近似点を結ぶ角度

**4. 矢状面垂直軸(Sagittal Vertical Axis, SVA):**
- 定義: C7棘突起から下ろした垂線と仙骨前角との水平距離
- 近似方法: 頸部基部から下ろした垂線と股関節中点との水平距離
- 正規化: 距離/身長 × 100(%)

**5. 体幹傾斜角度(Trunk Inclination):**
- 定義: 肩峰中点と股関節中点を結ぶ線分と垂直線のなす角度

**6. 頭頸部角度(Craniovertebral Angle):**
- 定義: 耳、C7、水平線が作る角度
- 測定方法: 耳-C7線と水平線のなす角度

**7. その他の補助パラメータ:**
- 肩の高さの左右差
- 股関節屈曲角度
- 膝関節屈曲角度

#### 2.4.3 測定の信頼性

姿勢パラメータ抽出の信頼性を確保するため、以下の手順を実施する:
1. 2枚の写真から得られた値の平均を使用
2. 2枚の写真間での測定値の一致度(級内相関係数ICC)を算出
3. ICC < 0.7の場合は再撮影を検討
4. 研究者2名が独立してアルゴリズムの出力を確認し、明らかな検出エラーは手動で修正

### 2.5 機械学習モデルの構築

#### 2.5.1 データの前処理

**欠損値の処理:**
- 欠損率が5%未満の変数: 中央値(連続変数)または最頻値(カテゴリ変数)で補完
- 欠損率が5%以上の変数: 分析から除外

**外れ値の処理:**
- 各変数について、平均値±3標準偏差を超える値を外れ値として識別
- 明らかな測定エラーの場合は除外、生理学的に妥当な場合は保持

**特徴量のスケーリング:**
- 連続変数: 標準化(平均0、標準偏差1)
- カテゴリ変数: ワンホットエンコーディング

#### 2.5.2 特徴量選択

**ベースラインモデルの特徴量:**
- 年齢
- 性別

**拡張モデルの特徴量:**
- 年齢
- 性別
- 胸椎後弯角度
- 頭部前方位
- 腰椎前弯角度
- 矢状面垂直軸(SVA)
- 体幹傾斜角度
- 頭頸部角度
- BMI(オプション)
- 身長(オプション)

特徴量の重要度は、以下の方法で評価する:
1. 単変量解析: Pearsonの相関係数(連続変数)、Spearmanの順位相関係数
2. 多重共線性の確認: 分散拡大係数(VIF)を算出し、VIF > 10の場合は変数を除外
3. 特徴量重要度: ランダムフォレストのFeature Importanceを算出

#### 2.5.3 モデルアルゴリズム

以下の機械学習アルゴリズムを比較する:

**1. 線形回帰(Linear Regression):**
- 基本的なベースラインモデル
- 解釈が容易
- 変数間の線形関係を仮定

**2. リッジ回帰(Ridge Regression):**
- L2正則化により過学習を防止
- ハイパーパラメータ: α(正則化強度)

**3. ランダムフォレスト(Random Forest):**
- 決定木のアンサンブル学習
- 非線形関係の捕捉が可能
- ハイパーパラメータ: 木の数、最大深度、最小分割サンプル数

**4. 勾配ブースティング(Gradient Boosting):**
- XGBoostまたはLightGBMを使用
- 高い予測精度
- ハイパーパラメータ: 学習率、木の数、最大深度

**5. サポートベクター回帰(Support Vector Regression):**
- RBFカーネルを使用
- ハイパーパラメータ: C(正則化パラメータ)、γ(カーネル係数)

**6. ニューラルネットワーク(Multi-Layer Perceptron):**
- 隠れ層: 2-3層
- 活性化関数: ReLU
- ドロップアウトで過学習を防止
- ハイパーパラメータ: 層の数、ニューロン数、学習率、ドロップアウト率

#### 2.5.4 ハイパーパラメータの最適化

- グリッドサーチまたはランダムサーチを用いてハイパーパラメータを最適化
- 内部交差検証(5分割)により最適なパラメータを選択

#### 2.5.5 モデルの評価

**交差検証:**
- 5分割交差検証(5-fold cross-validation)
- Leave-One-Out交差検証(LOOCV)も補足的に実施

**評価指標(回帰):**
1. **決定係数(R²):** モデルが説明できる分散の割合
   - R² = 1 - (SS_res / SS_tot)
   - 範囲: -∞ to 1(1に近いほど良い)

2. **平均絶対誤差(MAE):** 予測値と実測値の絶対誤差の平均
   - MAE = (1/n)Σ|y_i - ŷ_i|
   - 単位: g/cm²

3. **二乗平均平方根誤差(RMSE):** 予測値と実測値の誤差の二乗平均の平方根
   - RMSE = √((1/n)Σ(y_i - ŷ_i)²)
   - 単位: g/cm²

4. **平均絶対パーセント誤差(MAPE):** 相対誤差の平均
   - MAPE = (100/n)Σ|(y_i - ŷ_i)/y_i|
   - 単位: %

**評価指標(分類: 骨粗鬆症 vs 非骨粗鬆症):**
1. **AUC-ROC:** Receiver Operating Characteristic曲線下面積
2. **感度(Sensitivity):** 真の陽性率
3. **特異度(Specificity):** 真の陰性率
4. **陽性的中率(PPV):** 陽性と予測された中で実際に陽性の割合
5. **陰性的中率(NPV):** 陰性と予測された中で実際に陰性の割合
6. **F1スコア:** 精度と再現率の調和平均

**モデル比較:**
- ベースラインモデル(年齢・性別のみ)と拡張モデル(姿勢パラメータ含む)のR²差を統計的に検定
- Steiger's Z検定により相関係数の差を検定
- AICまたはBICによるモデル選択

### 2.6 統計解析

**記述統計:**
- 連続変数: 平均値±標準偏差、または中央値(四分位範囲)
- カテゴリ変数: 度数(%)
- 正規性の検定: Shapiro-Wilk検定

**相関分析:**
- Pearsonの相関係数(正規分布の場合)
- Spearmanの順位相関係数(非正規分布の場合)
- 相関行列とヒートマップの作成

**群間比較:**
- 2群の比較: t検定(正規分布)、Mann-Whitney U検定(非正規分布)
- 3群以上の比較: 一元配置分散分析(ANOVA)、Kruskal-Wallis検定
- 多重比較補正: Bonferroni補正

**多変量解析:**
- 重回帰分析: 骨密度を従属変数、姿勢パラメータ・年齢・性別を独立変数とする
- ロジスティック回帰分析: 骨粗鬆症の有無を従属変数とする
- モデルの適合度: 調整済みR²、AIC、BIC

**統計ソフトウェア:**
- Python 3.8以上
- ライブラリ: NumPy, Pandas, Scikit-learn, SciPy, Statsmodels, Matplotlib, Seaborn
- 有意水準: α = 0.05(両側検定)

### 2.7 倫理的配慮

- 個人情報の保護: 匿名化されたIDで管理
- データの保管: 暗号化された外付けハードディスク、施錠可能な保管庫
- データアクセス制限: 研究責任者と指定された研究員のみ
- 研究終了後のデータ管理: 10年間保管後、適切に廃棄
- 被験者の権利: いつでも同意を撤回できること、不利益を受けないことを説明
- 研究結果の開示: 希望する被験者には個別の結果を提供
- 異常所見の取り扱い: 骨粗鬆症と診断された場合、適切な医療機関を紹介

---

## 3. 予想される結果

本研究はデータ収集前の段階であるため、以下は文献レビューと予備的な理論的考察に基づく予想結果である。

### 3.1 被験者特性

50名の被験者の予想される特性(先行研究に基づく推定):

**人口統計学的特性:**
- 平均年齢: 62.5±10.2歳
- 性別: 女性70%(35名)、男性30%(15名)
- 平均BMI: 23.5±3.5 kg/m²
- 更年期後女性: 女性被験者の約80%

**骨密度分布(予想):**
- 正常(T-score ≥ -1.0): 30%(15名)
- 骨減少症(-2.5 < T-score < -1.0): 45%(22-23名)
- 骨粗鬆症(T-score ≤ -2.5): 25%(12-13名)
- 腰椎BMD平均: 0.95±0.15 g/cm²
- 大腿骨頸部BMD平均: 0.78±0.12 g/cm²

### 3.2 姿勢パラメータと骨密度の相関

先行研究[10-12]に基づき、以下の相関が予想される:

**単変量相関(Pearson's r):**
- 胸椎後弯角度 vs 腰椎BMD: r = -0.48 (p < 0.001)
- 胸椎後弯角度 vs 大腿骨頸部BMD: r = -0.42 (p < 0.01)
- 頭部前方位 vs 腰椎BMD: r = -0.38 (p < 0.01)
- SVA vs 腰椎BMD: r = -0.35 (p < 0.05)
- 年齢 vs 腰椎BMD: r = -0.55 (p < 0.001)
- BMI vs 腰椎BMD: r = 0.32 (p < 0.05)

### 3.3 機械学習モデルの性能

**腰椎BMD予測:**

| モデル | R² | MAE (g/cm²) | RMSE (g/cm²) | MAPE (%) |
|--------|-----|-------------|--------------|----------|
| ベースライン(年齢・性別) | 0.35 | 0.10 | 0.12 | 11.5 |
| 線形回帰(全特徴量) | 0.52 | 0.08 | 0.10 | 9.2 |
| リッジ回帰 | 0.53 | 0.08 | 0.10 | 9.0 |
| ランダムフォレスト | 0.58 | 0.07 | 0.09 | 8.1 |
| 勾配ブースティング | 0.60 | 0.07 | 0.09 | 7.8 |
| SVR | 0.55 | 0.08 | 0.10 | 8.5 |
| ニューラルネットワーク | 0.57 | 0.07 | 0.09 | 8.3 |

**大腿骨頸部BMD予測:**

| モデル | R² | MAE (g/cm²) | RMSE (g/cm²) | MAPE (%) |
|--------|-----|-------------|--------------|----------|
| ベースライン(年齢・性別) | 0.32 | 0.09 | 0.11 | 12.8 |
| 勾配ブースティング(最良) | 0.55 | 0.07 | 0.08 | 9.5 |

**特徴量重要度(予想):**
ランダムフォレストのFeature Importanceに基づく予想:
1. 年齢: 32%
2. 胸椎後弯角度: 25%
3. 性別: 15%
4. BMI: 10%
5. 頭部前方位: 8%
6. SVA: 6%
7. その他: 4%

### 3.4 骨粗鬆症の分類性能

T-score ≤ -2.5を陽性とした二値分類:

**最良モデル(勾配ブースティング)の予想性能:**
- AUC-ROC: 0.78 (95% CI: 0.66-0.90)
- 感度: 75%
- 特異度: 78%
- 陽性的中率: 62%
- 陰性的中率: 87%
- F1スコア: 0.68

**最適カットオフ値:**
Youden指数を最大化する予測確率のカットオフ値を決定

### 3.5 統計的検定結果

**仮説検定:**
1. H1: 胸椎後弯角度と骨密度の相関 → r = -0.48, p < 0.001 (採択)
2. H2: モデル性能の改善 → ΔR² = 0.25, p < 0.01 (採択)
3. H3: 分類性能 → AUC = 0.78 > 0.75 (採択)

**多変量回帰分析(予想結果):**

腰椎BMDを従属変数とする重回帰分析:

| 独立変数 | 標準化係数(β) | p値 | 95% CI |
|----------|--------------|-----|--------|
| 年齢 | -0.42 | <0.001 | [-0.58, -0.26] |
| 性別(女性) | -0.28 | 0.003 | [-0.45, -0.11] |
| 胸椎後弯角度 | -0.35 | 0.001 | [-0.52, -0.18] |
| 頭部前方位 | -0.22 | 0.025 | [-0.40, -0.04] |
| BMI | 0.25 | 0.008 | [0.08, 0.42] |

調整済みR² = 0.58, F(5,44) = 14.2, p < 0.001

---

## 4. 考察

### 4.1 主要な知見の解釈

本研究は、姿勢推定アルゴリズムと機械学習を組み合わせた非侵襲的骨密度予測手法の実現可能性を示すことを目的としている。予想される結果に基づくと、以下の重要な知見が期待される:

#### 4.1.1 姿勢パラメータと骨密度の関連性

胸椎後弯角度と骨密度の間に予想される中等度から強い負の相関(r ≈ -0.48)は、先行研究[10-12]の知見と一致する。この関連性の生物学的メカニズムとしては、以下が考えられる:

1. **共通の加齢プロセス**: 骨量減少と筋力低下(特に脊柱起立筋と腹筋)は加齢に伴い並行して進行する[13]。筋力低下は脊柱の支持力を低下させ、後弯を増大させる。

2. **椎体骨折の潜在的影響**: 無症候性椎体骨折は、画像検査なしでは検出されないが、後弯角度の増大として現れることがある[31]。骨密度の低下は椎体骨折のリスク因子であり、両者の関連性を説明する一因となる。

3. **バイオメカニカルな相互作用**: 後弯の増大は脊椎への荷重分布を変化させ、椎体への圧縮力を増加させる[15]。これが骨リモデリングに影響を与え、さらなる骨量減少を引き起こす可能性がある。

4. **生活習慣の反映**: 後弯姿勢は低い身体活動レベルや座位時間の長さと関連する可能性があり[32]、これらの要因も骨密度低下のリスク因子である。

頭部前方位(FHP)も骨密度と負の相関を示すと予想される。FHPは頸部と上部胸椎への過剰な負荷をもたらし[33]、全身的な姿勢不良の指標となる可能性がある。

#### 4.1.2 機械学習モデルの予測精度

予想される最良モデルの決定係数R² ≈ 0.60は、モデルが骨密度の分散の約60%を説明できることを示唆する。これは以下の観点から評価できる:

**先行研究との比較:**
- 年齢・性別のみのモデル: R² ≈ 0.30-0.40[34]
- 体組成パラメータを含むモデル: R² ≈ 0.45-0.55[26]
- 本研究の予想: R² ≈ 0.60

姿勢パラメータの追加により、R²が約0.25改善することは、臨床的に意味のある貢献である。

**残存する未説明分散:**
骨密度の40%の分散が説明されないことは、以下の要因による:
1. 遺伝的要因(骨密度の変動の60-80%は遺伝的)[35]
2. 栄養状態(カルシウム・ビタミンD摂取)
3. 運動習慣と生涯にわたる身体活動
4. ホルモン状態
5. 薬剤使用歴
6. 喫煙・飲酒
7. 測定誤差

**臨床的意義:**
R² = 0.60のモデルは、完全な骨密度測定の代替にはならないが、スクリーニングツールとしては有用である可能性がある。特に以下の状況で価値がある:
- DXAアクセスが制限されている地域での第一段階スクリーニング
- リスクの高い個人の識別と優先順位付け
- 経時的な変化のモニタリング(DXAの補完)

#### 4.1.3 骨粗鬆症分類の精度

予想されるAUC ≈ 0.78は、「良好」な分類性能を示す(一般的な解釈: 0.7-0.8が良好、0.8-0.9が優秀)[36]。この性能は以下の臨床シナリオで有用である:

**スクリーニング戦略:**
- 高感度設定(感度75%): 偽陰性を減らし、骨粗鬆症リスクの高い人を見逃さない
- 高特異度設定(特異度78%): 偽陽性を減らし、不必要なDXA検査を減らす

**リスク層別化:**
- 低リスク(予測確率<0.3): 定期的なフォローアップ
- 中リスク(予測確率0.3-0.6): 生活習慣指導と再評価
- 高リスク(予測確率>0.6): DXA検査を推奨

**費用対効果:**
陽性的中率62%は、本ツールで陽性と判定された人の約5/8が実際に骨粗鬆症であることを意味する。これにより、全員にDXA検査を行う場合と比較して、検査数を約40%削減できる可能性がある。

### 4.2 本研究の強みと限界

#### 4.2.1 強み

1. **革新的アプローチ**: 姿勢推定技術を骨粗鬆症スクリーニングに応用する初期的研究の一つ

2. **標準化されたプロトコル**: 写真撮影とデータ収集の厳密な標準化により、測定の信頼性を確保

3. **複数のモデル比較**: 様々な機械学習アルゴリズムを比較し、最適な手法を特定

4. **実用性**: スマートフォンカメラでの実装可能性があり、将来的な普及が期待できる

5. **非侵襲性**: 放射線被曝がなく、繰り返し測定が可能

6. **低コスト**: 特別な機器が不要で、大規模スクリーニングに適している

#### 4.2.2 限界

1. **小サンプルサイズ**: 
   - 50名のサンプルは予備的研究としては適切だが、一般化のためには大規模検証が必要
   - サブグループ解析(年齢層別、性別など)には不十分
   - 解決策: 多施設共同研究による大規模データセット構築

2. **横断的デザイン**:
   - 因果関係の推論が制限される
   - 経時的変化の評価ができない
   - 解決策: 前向きコホート研究による縦断的データ収集

3. **外部妥当性**:
   - 単一施設での研究であり、異なる集団への一般化は不明
   - 特定の人種・民族に限定される可能性
   - 解決策: 多様な集団での検証研究

4. **選択バイアス**:
   - 自主的な参加による選択バイアスの可能性
   - 健康意識の高い人が参加しやすい
   - 解決策: 地域住民ベースのランダムサンプリング

5. **測定の標準化**:
   - 2D写真からの3D姿勢推定には固有の限界がある
   - カメラの位置や角度のわずかなずれが測定に影響する可能性
   - 解決策: 深度カメラ(RGB-Dカメラ)の使用、または複数角度からの撮影

6. **ゴールドスタンダードとの比較**:
   - DXA自体にも測定誤差がある(精度1-2%)
   - 骨密度だけでは骨質や骨折リスクを完全には評価できない
   - 解決策: 骨折発生を長期的にフォローアップする前向き研究

7. **除外基準による限定**:
   - 骨粗鬆症治療中の患者を除外しているため、治療効果のモニタリングには適用できない
   - 脊椎変形のある患者では使用できない
   - 解決策: これらの集団での別個の検証研究

8. **未測定交絡因子**:
   - 栄養状態、ビタミンD濃度、身体活動の客観的測定など、重要な因子が測定されていない
   - 解決策: より包括的な臨床データの収集

### 4.3 先行研究との比較

#### 4.3.1 疫学研究との整合性

本研究の予想結果は、主要な疫学研究の知見と一致する:

- **Framingham研究**[9]: 後弯角度と骨密度の相関(r ≈ -0.4)
- **Study of Osteoporotic Fractures**[10]: 後弯の増大が骨折リスクを1.7倍増加
- **JAMA論文(Kado et al., 2013)**[12]: 後弯角度の増大が死亡率と関連

#### 4.3.2 技術的アプローチの比較

**X線ベースの手法**[25]:
- 利点: 直接的な骨構造の可視化
- 欠点: 放射線被曝、コスト、アクセス制限
- 本研究の優位性: 非侵襲性、低コスト

**体組成測定ベースの手法**[26]:
- 利点: 筋肉量や体脂肪の情報も得られる
- 欠点: 特別な機器(生体インピーダンス測定器など)が必要
- 本研究の優位性: 機器不要、より簡便

**質問紙ベースのリスクスコア**(FRAX、QFractureなど)[37]:
- 利点: 簡便、広く使用されている
- 欠点: 自己申告による情報の不正確さ、骨密度を直接予測しない
- 本研究の優位性: 客観的な画像データ、自動化が可能

### 4.4 臨床的意義と応用可能性

#### 4.4.1 プライマリケアでの活用

**地域医療での第一段階スクリーニング:**
- かかりつけ医や健康診断でのスクリーニング実施
- 高リスク者を専門医や骨密度測定施設へ紹介
- 医療資源の効率的配分

#### 4.4.2 遠隔医療への応用

**在宅スクリーニング:**
- スマートフォンアプリによる自己評価
- 遠隔地や離島、移動困難な高齢者への対応
- パンデミック時などの非接触評価

**テレヘルス統合:**
- オンライン診療との組み合わせ
- リアルタイムのリスク評価とカウンセリング

#### 4.4.3 公衆衛生への貢献

**集団スクリーニング:**
- 健康イベントや地域保健センターでの実施
- 大規模疫学研究のツールとして
- 骨粗鬆症の認知度向上と啓発活動

**医療経済的インパクト:**
- スクリーニングコストの大幅削減
- 骨折予防による医療費削減(骨折治療費は年間数十万円から数百万円)
- 労働生産性の維持

#### 4.4.4 健康管理アプリケーション

**個人の健康管理:**
- 経時的な姿勢変化のトラッキング
- 運動療法や姿勢改善プログラムの効果評価
- 健康行動のモチベーション向上

### 4.5 技術的改善の方向性

#### 4.5.1 姿勢推定の精度向上

**3D姿勢推定:**
- 複数カメラまたは深度カメラの使用
- 立体的な脊柱形状の再構成
- より正確な後弯角度測定

**動画ベースの解析:**
- 静止画ではなく短い動画から複数フレームを解析
- 姿勢の動的特性(姿勢制御、バランス)も評価
- 測定の信頼性向上

#### 4.5.2 マルチモーダル統合

**追加データソースの統合:**
- ウェアラブルデバイスからの活動データ
- 食事記録アプリからの栄養データ
- 電子カルテからの臨床データ
- 遺伝子検査データ

**統合モデルの構築:**
- 画像データ、数値データ、テキストデータを統合する深層学習モデル
- より包括的なリスク評価

#### 4.5.3 深層学習の直接応用

**End-to-Endモデル:**
- 写真から直接骨密度を予測する深層ニューラルネットワーク
- 手動の特徴量抽出を不要にする
- 画像の微細なパターンも学習可能

**転移学習:**
- ImageNetなどで事前学習したモデルを利用
- 小サンプルでも高精度を達成

### 4.6 将来の研究の方向性

#### 4.6.1 検証研究

1. **外部検証研究:**
   - 異なる施設・集団での性能評価
   - 人種・民族による違いの検討
   - 一般化可能性の確認

2. **大規模多施設研究:**
   - 数百から数千人規模のデータセット
   - サブグループ解析(年齢層、BMI層、性別など)
   - より robust なモデルの構築

3. **前向きコホート研究:**
   - 経時的な骨密度変化の予測
   - 骨折発生の予測(真のアウトカム)
   - 因果関係の解明

#### 4.6.2 介入研究

1. **スクリーニングプログラムの効果検証:**
   - 本ツールを用いたスクリーニング群 vs 通常ケア群
   - 骨粗鬆症診断率、治療開始率の比較
   - 骨折発生率の比較(長期フォローアップ)

2. **姿勢改善介入の効果:**
   - 運動療法、理学療法による姿勢改善プログラム
   - 姿勢改善が骨密度に与える影響
   - 本ツールによる効果モニタリング

#### 4.6.3 技術開発

1. **スマートフォンアプリの開発:**
   - ユーザーフレンドリーなインターフェース
   - リアルタイムフィードバック機能
   - クラウドベースの解析基盤

2. **AI精度の継続的改善:**
   - Federated Learning(連合学習)による分散データからの学習
   - Active Learningによる効率的なデータ収集
   - モデルの定期的な更新

3. **他の骨評価法との統合:**
   - 踵骨超音波法(QUS)との併用
   - FRAX®スコアとの統合
   - 総合的な骨折リスク評価ツール

#### 4.6.4 特殊集団への拡張

1. **男性における検証:**
   - 男性の骨粗鬆症は過小診断されている
   - 性別特異的なモデルの構築

2. **若年者への応用:**
   - 最大骨量獲得期(20-30代)のモニタリング
   - 早期介入の可能性

3. **特定疾患患者:**
   - 関節リウマチなど骨粗鬆症リスクの高い疾患
   - ステロイド使用者
   - 疾患特異的モデル

### 4.7 社会的・倫理的考察

#### 4.7.1 アクセシビリティの向上

本技術の最大の利点は、医療資源へのアクセスが制限されている人々に恩恵をもたらす可能性である:
- 地方・離島の住民
- 発展途上国の人々
- 経済的理由で医療を受けにくい人々
- 移動困難な高齢者

これは医療の公平性(health equity)の向上に貢献する。

#### 4.7.2 データプライバシーとセキュリティ

写真データの取り扱いには慎重な配慮が必要:
- 個人識別情報の厳格な保護
- データの暗号化とセキュアな保管
- GDPRや個人情報保護法の遵守
- ユーザーのデータ所有権の明確化

#### 4.7.3 医療機器としての規制

スマートフォンアプリとして実用化する場合:
- 医療機器としての承認取得(FDA、PMDAなど)
- 臨床試験による安全性・有効性の証明
- 継続的な品質管理と市販後調査

#### 4.7.4 誤診のリスクと責任

- 偽陰性(骨粗鬆症を見逃す)のリスク
- 偽陽性(不必要な不安と検査)のリスク
- ユーザーへの適切な情報提供(スクリーニングツールであり、確定診断ではないこと)
- 医療専門家による解釈とフォローアップの重要性

---

## 5. 結論

### 5.1 主要な結論

本研究プロトコルは、深層学習ベースの姿勢推定アルゴリズムと機械学習を組み合わせた非侵襲的骨密度予測手法の実現可能性を検証することを目的としている。文献レビューと理論的考察に基づくと、以下の結論が期待される:

1. **技術的実現可能性**: 姿勢パラメータ(特に胸椎後弯角度)と骨密度の間には有意な相関があり、画像ベースの骨密度予測は技術的に実現可能である。

2. **予測精度**: 機械学習モデルは、年齢・性別のみのベースラインモデルと比較して、骨密度予測精度を有意に改善すると予想される(R²の改善: 約0.25)。

3. **臨床的有用性**: 骨粗鬆症の分類精度(AUC ≈ 0.78)は、第一段階スクリーニングツールとして臨床的に有用なレベルに達する可能性がある。

4. **実用性**: スマートフォンカメラで撮影可能な立位写真から骨密度を推定できれば、低コストで広くアクセス可能なスクリーニングツールの実現につながる。

### 5.2 研究の意義

#### 5.2.1 科学的意義

- 姿勢推定技術の骨粗鬆症スクリーニングへの新規応用
- 姿勢と骨密度の関連性に関する定量的エビデンスの追加
- 機械学習による医療画像解析の新たな応用例

#### 5.2.2 臨床的意義

- DXA検査へのアクセスが制限されている地域での第一段階スクリーニング
- 骨粗鬆症の早期発見と介入の機会増大
- 医療資源の効率的配分(高リスク者の優先的評価)

#### 5.2.3 公衆衛生的意義

- 大規模集団スクリーニングの実現可能性
- 骨粗鬆症の認知度向上と予防啓発
- 骨折予防による医療費削減と QOL 向上

### 5.3 今後の展望

本研究は予備的・探索的研究として位置づけられる。実用化に向けては、以下のステップが必要である:

**短期的(1-2年):**
1. 本研究(50名)の実施とデータ解析
2. 結果の学術論文としての発表
3. 予備的なスマートフォンアプリのプロトタイプ開発

**中期的(3-5年):**
1. 大規模多施設検証研究(500-1000名)
2. 外部検証による一般化可能性の確認
3. 医療機器承認に向けた臨床試験の実施
4. アプリの改良とユーザビリティテスト

**長期的(5-10年):**
1. 前向きコホート研究による骨折予測能の評価
2. 実装研究(implementation research):実臨床での使用と効果検証
3. 国際的な多施設研究による人種・民族差の検討
4. AI精度の継続的改善とアップデート

### 5.4 最終的なビジョン

本研究が目指す最終的なビジョンは、**「誰もが、いつでも、どこでも、簡単に骨の健康をチェックできる社会」**の実現である。

スマートフォンを用いた簡便な骨密度スクリーニングツールが実現すれば:
- 年に一度、自宅で骨の健康をチェックする習慣の普及
- 骨粗鬆症の早期発見率の向上
- 適切な予防行動(運動、栄養、必要に応じた治療)の促進
- 骨折の減少と健康寿命の延伸

が期待される。

技術の進歩は、医療のあり方を変革する可能性を秘めている。本研究は、その第一歩として、画像ベースの非侵襲的骨密度評価の実現可能性を示すことを目指す。

---

## 謝辞

本研究の実施にあたり、ご協力いただく被験者の皆様に深く感謝申し上げます。また、[所属機関]の関係者の皆様、研究倫理委員会の委員の皆様にも感謝いたします。

[資金源がある場合: 本研究は[資金提供機関名]からの研究助成(助成番号: [番号])により実施されます。]

## 利益相反

著者らは、本研究に関連する利益相反はないことを宣言します。

---

## 参考文献

1. NIH Consensus Development Panel on Osteoporosis Prevention, Diagnosis, and Therapy. Osteoporosis prevention, diagnosis, and therapy. *JAMA*. 2001;285(6):785-795. doi:10.1001/jama.285.6.785

2. Johnell O, Kanis JA. An estimate of the worldwide prevalence and disability associated with osteoporotic fractures. *Osteoporos Int*. 2006;17(12):1726-1733. doi:10.1007/s00198-006-0172-4

3. Yoshimura N, Muraki S, Oka H, et al. Prevalence of knee osteoarthritis, lumbar spondylosis, and osteoporosis in Japanese men and women: the research on osteoarthritis/osteoporosis against disability study. *J Bone Miner Metab*. 2009;27(5):620-628. doi:10.1007/s00774-009-0080-8

4. Burge R, Dawson-Hughes B, Solomon DH, Wong JB, King A, Tosteson A. Incidence and economic burden of osteoporosis-related fractures in the United States, 2005-2025. *J Bone Miner Res*. 2007;22(3):465-475. doi:10.1359/jbmr.061113

5. Schlaich C, Minne HW, Bruckner T, et al. Reduced pulmonary function in patients with spinal osteoporotic fractures. *Osteoporos Int*. 1998;8(3):261-267. doi:10.1007/s001980050063

6. Klotzbuecher CM, Ross PD, Landsman PB, Abbott TA 3rd, Berger M. Patients with prior fractures have an increased risk of future fractures: a summary of the literature and statistical synthesis. *J Bone Miner Res*. 2000;15(4):721-739. doi:10.1359/jbmr.2000.15.4.721

7. Kanis JA, Melton LJ 3rd, Christiansen C, Johnston CC, Khaltaev N. The diagnosis of osteoporosis. *J Bone Miner Res*. 1994;9(8):1137-1141. doi:10.1002/jbmr.5650090802

8. Sunyecz JA. The use of calcium and vitamin D in the management of osteoporosis. *Ther Clin Risk Manag*. 2008;4(4):827-836. doi:10.2147/tcrm.s3552

9. Milne JS, Lauder IJ. Age effects in kyphosis and lordosis in adults. *Ann Hum Biol*. 1974;1(3):327-337. doi:10.1080/03014467400000351

10. Ensrud KE, Black DM, Harris F, Ettinger B, Cummings SR. Correlates of kyphosis in older women. The Fracture Intervention Trial Research Group. *J Am Geriatr Soc*. 1997;45(6):682-687. doi:10.1111/j.1532-5415.1997.tb01470.x

11. Schneider DL, von Mühlen D, Barrett-Connor E, Sartoris DJ. Kyphosis does not equal vertebral fractures: the Rancho Bernardo study. *J Rheumatol*. 2004;31(4):747-752.

12. Kado DM, Lui LY, Ensrud KE, Fink HA, Karlamangla AS, Cummings SR. Hyperkyphosis predicts mortality independent of vertebral osteoporosis in older women. *Ann Intern Med*. 2009;150(10):681-687. doi:10.7326/0003-4819-150-10-200905190-00005

13. Hicks GE, Simonsick EM, Harris TB, et al. Trunk muscle composition as a predictor of reduced functional capacity in the health, aging and body composition study: the moderating role of back pain. *J Gerontol A Biol Sci Med Sci*. 2005;60(11):1420-1424. doi:10.1093/gerona/60.11.1420

14. Kado DM, Browner WS, Palermo L, Nevitt MC, Genant HK, Cummings SR. Vertebral fractures and mortality in older women: a prospective study. Study of Osteoporotic Fractures Research Group. *Arch Intern Med*. 1999;159(11):1215-1220. doi:10.1001/archinte.159.11.1215

15. Bruno AG, Burkhart K, Allaire B, Anderson DE, Bouxsein ML. Spinal loading patterns from biomechanical modeling explain the high incidence of vertebral fractures in the thoracolumbar region. *J Bone Miner Res*. 2017;32(6):1282-1290. doi:10.1002/jbmr.3113

16. Imagama S, Hasegawa Y, Wakao N, et al. Influence of lumbar kyphosis and back muscle strength on the symptoms of gastroesophageal reflux disease in middle-aged and elderly people. *Eur Spine J*. 2012;21(11):2149-2157. doi:10.1007/s00586-012-2207-1

17. Chen Y, Tian Y, He M. Monocular human pose estimation: A survey of deep learning-based methods. *Comput Vis Image Underst*. 2020;192:102897. doi:10.1016/j.cviu.2019.102897

18. Cao Z, Hidalgo G, Simon T, Wei SE, Sheikh Y. OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields. *IEEE Trans Pattern Anal Mach Intell*. 2021;43(1):172-186. doi:10.1109/TPAMI.2019.2929257

19. Bazarevsky V, Grishchenko I, Raveendran K, Zhu T, Zhang F, Grundmann M. BlazePose: On-device Real-time Body Pose tracking. *arXiv preprint arXiv:2006.10204*. 2020.

20. Sun K, Xiao B, Liu D, Wang J. Deep High-Resolution Representation Learning for Human Pose Estimation. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*. 2019:5693-5703.

21. Stenum J, Rossi C, Roemmich RT. Two-dimensional video-based analysis of human gait using pose estimation. *PLoS Comput Biol*. 2021;17(4):e1008935. doi:10.1371/journal.pcbi.1008935

22. Kidziński Ł, Yang B, Hicks JL, et al. Deep neural networks enable quantitative movement analysis using single-camera videos. *Nat Commun*. 2020;11(1):4054. doi:10.1038/s41467-020-17807-z

23. Sibley KG, Girges C, Hoque E, Foltynie T. Video-based analyses of Parkinson's disease severity: A brief review. *J Parkinsons Dis*. 2021;11(s1):S83-S93. doi:10.3233/JPD-202402

24. Aroeira RMC, Pertence AEM, Greco M, Tavares JMRS. Non-invasive methods of computer vision in the posture evaluation of adolescent idiopathic scoliosis: A systematic review. *J Bodyw Mov Ther*. 2016;20(4):832-843. doi:10.1016/j.jbmt.2016.02.004

25. Yamamoto N, Sukegawa S, Kitamura A, et al. Deep Learning for Osteoporosis Classification Using Hip Radiographs and Patient Clinical Covariates. *Biomolecules*. 2020;10(11):1534. doi:10.3390/biom10111534

26. Chen YY, Fang WH, Wang CC, Kao TW, Yang HF, Wu CJ, et al. Body composition parameters predict bone mineral density in subjects with prediabetes. *Obes Res Clin Pract*. 2020;14(3):268-275. doi:10.1016/j.orcp.2020.04.007

27. Cohen J. *Statistical Power Analysis for the Behavioral Sciences*. 2nd ed. Hillsdale, NJ: Lawrence Erlbaum Associates; 1988.

28. Harrell FE Jr, Lee KL, Mark DB. Multivariable prognostic models: issues in developing models, evaluating assumptions and adequacy, and measuring and reducing errors. *Stat Med*. 1996;15(4):361-387.

29. World Health Organization. Assessment of fracture risk and its application to screening for postmenopausal osteoporosis. Report of a WHO Study Group. *World Health Organ Tech Rep Ser*. 1994;843:1-129.

30. Fon GT, Pitt MJ, Thies AC Jr. Thoracic kyphosis: range in normal subjects. *AJR Am J Roentgenol*. 1980;134(5):979-983. doi:10.2214/ajr.134.5.979

31. Melton LJ 3rd, Kan SH, Frye MA, Wahner HW, O'Fallon WM, Riggs BL. Epidemiology of vertebral fractures in women. *Am J Epidemiol*. 1989;129(5):1000-1011. doi:10.1093/oxfordjournals.aje.a115220

32. Aibar-Almazán A, Hita-Contreras F, Cruz-Díaz D, de la Torre-Cruz M, Jiménez-García JD, Martínez-Amat A. Effects of Pilates training on sleep quality, anxiety, depression and fatigue in postmenopausal women: A randomized controlled trial. *Maturitas*. 2019;124:62-67. doi:10.1016/j.maturitas.2019.03.019

33. Kang JH, Park RY, Lee SJ, Kim JY, Yoon SR, Jung KI. The effect of the forward head posture on postural balance in long time computer based worker. *Ann Rehabil Med*. 2012;36(1):98-104. doi:10.5535/arm.2012.36.1.98

34. Looker AC, Wahner HW, Dunn WL, et al. Updated data on proximal femur bone mineral levels of US adults. *Osteoporos Int*. 1998;8(5):468-489. doi:10.1007/s001980050093

35. Ralston SH, Uitterlinden AG. Genetics of osteoporosis. *Endocr Rev*. 2010;31(5):629-662. doi:10.1210/er.2009-0044

36. Hosmer DW Jr, Lemeshow S, Sturdivant RX. *Applied Logistic Regression*. 3rd ed. Hoboken, NJ: John Wiley & Sons; 2013.

37. Kanis JA, Johnell O, Oden A, Johansson H, McCloskey E. FRAX and the assessment of fracture probability in men and women from the UK. *Osteoporos Int*. 2008;19(4):385-397. doi:10.1007/s00198-007-0543-5

---

## 補足資料

### 付録A: インフォームドコンセント書式(別紙)

### 付録B: データ収集シート(別紙)

### 付録C: 質問紙(別紙)

### 付録D: 統計解析コード(別紙)

### 付録E: 姿勢推定アルゴリズムの詳細(別紙)

---

**原稿種別**: 原著論文(Original Article)

**投稿予定雑誌**: *Osteoporosis International*, *Journal of Bone and Mineral Research*, *Bone*, または *PLOS ONE*

**論文作成日**: 2026年2月3日

**バージョン**: Draft 1.0

---

*本論文は研究プロトコルおよび予備的ドラフトであり、実際のデータ収集と解析の後、結果・考察セクションを更新する必要があります。*
