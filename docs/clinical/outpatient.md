# 外来の型（レター中心）

このページは、外来レターを**再現可能な型**として固定し、上級医へのプレゼンテーション、紹介元への報告、患者説明の整合性を同時に担保することを目的としています。レターは常に、以下の順序で記載します。

1. **Diagnosis**  
2. **Plan**（次回外来のアクションを含む If–Then）  
3. **Main paragraph**（"It was a pleasure to see …" から開始）  
4. **Impression and recommendation**  

加えて、患者名は常に **`[PATIENT]`** とし、症例を特定できる要素（日時・施設・地域・職業など）はプレースホルダ（例：`[DATE]`, `[MONTH]`, `[OCCUPATION]`）で管理します。

## 0. 原則

- **診断とプランは常に同じアルゴリズム**（`clinical/algorithm.md`）で回します。
- **レターの冒頭は Diagnosis と Plan**であり、結論を先に提示します（情報の羅列を目的にしません）。
- Planは必ず「次回何をするか」を含み、可能な限り**次回で決着がつく設計**に寄せます。
- レター本文（Main paragraph）は「読者が前提知識なしに追える」よう、要点のみを因果順に配置します。

## 1. レターの型（共通）

以下は、外来レターを最短で作成するための共通骨格です。`New referral`と`Follow-up`のいずれでも、まずはこの枠で書き、必要に応じてState別の型（後述）へ寄せます。

---

### Diagnosis

**構造**: 診断名を簡潔に列挙します。

**よく使う単語・フレーズ**:
- chronic | acute | subacute | recurrent
- plantar fasciitis | Achilles tendinopathy | ankle instability | hallux valgus | tibialis posterior tendon dysfunction
- stage I / II / III
- bilateral | unilateral | left | right
- refractory to conservative management
- secondary to [CAUSE]
- injury occurred [DATE] | sustained [DATE]

**例**:
- [DIAGNOSIS 1]  
- [DIAGNOSIS 2]（必要に応じて）  

---

### Plan

**構造**: 検査、保存療法、次回予定、分岐（If-Then）を明示します。

**よく使う単語・フレーズ**:

*Investigation*:
- X-ray | MRI | CT | ultrasound | weightbearing CT
- to assess | to evaluate | to confirm | to rule out
- bone stock | cartilage integrity | ligament injury | alignment

*Conservative management*:
- physiotherapy | orthotics | heel cups | night splints | CAM boot
- NSAIDs | analgesia | injection (corticosteroid / PRP)
- activity modification | offloading | stretching program
- for [DURATION: 3 months / 6 weeks / until next review]

*Follow-up*:
- in [TIMEFRAME: 3 months / 6 weeks / after investigations complete]
- to review symptoms | to assess progress | to discuss next steps

*If-Then branching*:
- If symptoms persist → consider [injection / surgery / further imaging]
- If improvement → continue conservative | wean from support | return PRN
- If deterioration → urgent review | modify treatment

**例**:
- 検査：[INVESTIGATION]（目的：仮説の支持／否定）  
- 保存： [CONSERVATIVE]（期限：`[DURATION]`）  
- 次回： `[TIMEFRAME]` に再診し結果レビュー  
- If A（例：症状残存／所見陽性／画像で○○）→ Then B（追加検査／注射／手術検討）  
- If C（例：改善傾向）→ Then D（負荷調整／リハ継続／PRN）  

---

### Main paragraph

**構造**: 挨拶→主訴（機能障害として）→発症と経過→既治療→身体所見→検査

**よく使う単語・フレーズ**:

*Opening*:
- It was a pleasure to see [PATIENT]
- Thank you for referring [PATIENT]
- [PATIENT] returns today for review

*Chief complaint (functional)*:
- reports difficulty with | is unable to | experiences pain when
- walking distance limited to [DISTANCE]
- stairs are difficult | cannot stand for prolonged periods

*Onset*:
- began [TIMEFRAME] ago | following [INJURY / ACTIVITY]
- insidious onset | traumatic onset | gradual progression

*Course*:
- progressive | stable | intermittent | improving | worsening
- exacerbated by | relieved by

*Prior management*:
- has tried | has undergone | has completed
- physiotherapy | orthotics | injections | NSAIDs | immobilization
- with good / partial / minimal / no relief

*Examination*:
- On examination | Inspection reveals | Palpation demonstrates
- tenderness over | swelling is present | range of motion is limited
- neurovascularly intact | alignment is neutral / varus / valgus
- [TEST NAME] is positive / negative

*Investigations*:
- Radiographs demonstrate | MRI shows | CT reveals
- joint space narrowing | osteophytes | subchondral sclerosis
- tendon tear | cartilage defect | bone marrow edema

**例**:

It was a pleasure to see **[PATIENT]** today for review of **[REGION/COMPLAINT]**.  
[PATIENT] reports **[CHIEF COMPLAINT AS FUNCTION]**, which began **[ONSET/INJURY BASIS]** and has followed **[TIME COURSE]**. Prior management has included **[TREATMENTS TRIED]**, with **[RESPONSE]**. On examination, **[KEY EXAM FINDINGS]**. Investigations **[IMAGING/TESTS REVIEWED OR REQUESTED]**.

---

### Impression and recommendation

**構造**: 診断のまとめ→鑑別診断→推奨事項→次回予定

**よく使う単語・フレーズ**:

*Summary*:
- In summary | Overall | In conclusion
- the presentation is consistent with | most likely represents
- diagnostic features include

*Differential*:
- The key differential diagnoses include
- Other considerations are
- We have ruled out | We need to exclude

*Recommendation*:
- I recommend | The plan is to | We will proceed with
- conservative management | surgical intervention | further investigation
- with close monitoring | as tolerated | until symptoms resolve

*Follow-up goal*:
- to reassess | to review progress | to finalize the plan
- to discuss surgical options | to ensure adequate healing

**例**:

In summary, [PATIENT]'s presentation is consistent with **[IMPRESSION]**. The key differential diagnoses include **[DIFFERENTIALS]**.  
I recommend **[RECOMMENDATION]**, and I will review [PATIENT] in **[FOLLOW-UP TIMEFRAME]** to **[GOAL OF REVIEW]**.

---

## 2. State別の型（最小差分）

先生の運用フロー（New referral → Conservative / Consider surgery → Follow-up）を、上記4枠の中で破綻なく回すため、Stateごとの“差分”のみを示す。

### 2-1. New referral（Diagnostic testing and follow up）

- **Diagnosis**: `Working diagnosis`（暫定）＋ `Differential`（上位）  
- **Plan**: 検査依頼（目的明記）＋「検査完了後に再診」＋待機期間中の保存療法（期限つき；= Temporarily）  
- **Impression and recommendation**: “暫定”であることを明示し、結果で分岐することを文章で固定する  

### 2-2. New referral（Conservative）

- **Diagnosis**: 確定診断＋重症度／ステージ  
- **Plan**: 保存療法を期限つきで提示し、成功／不成功の評価軸を If–Then に落とす  

### 2-3. New referral（Consider surgery）

- **Diagnosis**: 確定診断  
- **Plan**: IC（risk/benefit + recovery）を箇条書きで明示し、患者が“考える期間”と次アクション（連絡して日程調整）を固定する  

### 2-4. Follow-up（Post conservative）

- **Diagnosis**: 既診断＋経過（改善／不変／増悪のいずれか）  
- **Plan**:  
  - Success → PRN（フォロー終了条件を明示）  
  - Failure → Consider surgery（必要なら検査追加→IC）  

### 2-5. Follow-up（Post op）

- **Diagnosis**: 術式＋術後週数  
- **Plan**: 荷重・固定・リハ・画像フォロー・次回受診を、術後プロトコルとして固定する  

## 3. 次回アクション設計（AならB、CならD）

次回分岐は「都度考える」から「事前に定義する」へ移すことで、診療の一貫性と学習効率が上がる。典型的な分岐は以下である。

- **症状**: 改善／不変／増悪  
- **身体所見**: 誘発テスト陽性の持続／消失  
- **画像**: 追加撮像の要否（仮説検証のための追加）  
- **治療反応**: 固定・薬物・注射・リハへの反応  

## 4. 実装メモ（運用上の注意）

- 公開ノートでは、患者名は常に **`[PATIENT]`** とし、日時・施設・地域・職業などもプレースホルダで表現する。実症例の全文は公開外（`private/` 等）へ分離する。  
- “上級医に相談するための情報”と“患者説明に必要な情報”は重なるが同一ではない。前者は仮説と分岐設計、後者は期待値調整（治療期間と見通し）に重心がある。  

## 5. サンプルレター（完全匿名化）

以下は、先生が提示されたレター断片を、**患者名を`[PATIENT]`へ置換**し、日時・職業・施設などの症例同定性を**プレースホルダ化**した上で、**固定順序（Diagnosis → Plan → Main paragraph → Impression and recommendation）**に再構成したサンプルである。

### Sample 1（New referral：Diagnostic testing and follow up）

#### Diagnosis

- Chronic bilateral plantar fasciitis (L>R), refractory to standard conservative management  
- Differential diagnosis for medial heel pain includes Baxter’s nerve entrapment  
- Palpable dorsal left foot mass consistent with a ganglion cyst  

#### Plan

- Follow up in my clinic after investigations are complete (approx. **[~4 months]**).  
- Advised to continue physiotherapy, shockwave therapy, heel cups, and night splints for **[~4 months]** while awaiting investigations.  
- Investigations: **[INVESTIGATIONS]** (purpose: confirm plantar fascia pathology; assess for alternative causes of medial heel pain; characterise dorsal mass if required)  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for assessment of bilateral foot pain. [PATIENT] presents with a **[2–3 year]** history of bilateral foot pain, worse on the left. The pain is most severe with the first steps in the morning and after periods of rest. Symptoms have been refractory to conservative treatments, including physiotherapy exercises, hot and cold compresses, **[two]** steroid injections (providing only brief relief), shockwave therapy, and night splints.  
On examination, there is a palpable, soft, cystic-feeling mass on the dorsal aspect of the left foot, consistent with a ganglion cyst.

#### Impression and recommendation

In summary, [PATIENT]’s presentation is consistent with chronic bilateral plantar fasciitis, more severe on the left, refractory to standard conservative management. The differential diagnosis for the medial heel pain includes Baxter’s nerve entrapment.  
I recommend completion of the requested investigations and continuation of the above conservative measures while awaiting results. I will review [PATIENT] after investigations are complete (approximately **[~4 months]**) to finalise management based on findings and clinical response.

---

### Sample 2（Follow-up：Post conservative / Failure → Consider surgery を含む）

#### Diagnosis

- Chronic right ankle instability and pain, secondary to inversion injuries in **[MONTH YEAR]** and **[MONTH YEAR]**  
- Secondary hindfoot varus and lateral ankle pain due to altered gait  
- Left ankle lateral ligament injury, approximately **[~9 months]** post injury (injury sustained on **[DATE]**)  
- Right 1st MTP joint arthritis with hallux rigidus and associated bony prominence  

#### Plan

- Conservative management with orthotics (including carbon shank) has been trialled  
- Continue symptomatic relief with paracetamol as needed  
- Continue home exercise program, focusing on proprioception and strengthening with ankle bands  
- Slow weaning from the boot in a controlled manner under physiotherapy guidance  
- Gradually return to higher-impact activities (running/jumping), starting on even, controlled surfaces  
- Cease smoking / nicotine use to improve tissue healing potential  
- Surgery (if symptoms significantly impact quality of life):
  - Consider 1st MTP joint fusion (non-weight bearing for **[~6 weeks]**, total recovery up to **[~1 year]**)  
  - If symptoms of pinching become frequent or limit activity, consider ankle arthroscopy to debride scar tissue  
- Review:
  - [PATIENT] will contact the office to schedule surgery if they decide to proceed  
  - If symptoms worsen or fail to improve by **[MONTH YEAR]**, return for review  
  - Review in **[X months]** to assess progress  

#### Main paragraph

It was a pleasure to see **[PATIENT]** for review regarding ankle and forefoot symptoms. [PATIENT] reports a history of inversion injuries affecting the ankles (including a significant inversion injury at work on **[DATE]** and a further inversion injury on **[DATE]**), with ongoing functional limitation. Prior management has included immobilisation in a boot and physiotherapy with mixed results.  
Currently, [PATIENT] describes episodic lateral ankle pain when overactive (e.g., running or jumping), with perceived instability and occasional rolling episodes. [PATIENT] also reports forefoot symptoms consistent with hallux rigidus, including hypersensitivity and activity limitation. There are **[no / some]** associated neuropathic symptoms, such as tingling or numbness over the dorsolateral foot, particularly at night, which may disturb sleep.  
On examination, gait is **[antalgic / normal]**. There is tenderness over the anterolateral ankle (including along the course of the superficial peroneal nerve) and lateral ligament complex. Stress testing demonstrates laxity with anterior drawer and talar tilt compared with the contralateral side. Range of motion is limited by pain.  
Investigations reviewed include **[X-rays / MRI]** demonstrating **[ligament injury / preserved cartilage space / no obvious fracture / incidental Haglund’s deformity]**.

#### Impression and recommendation

In summary, [PATIENT] remains symptomatic with chronic ankle instability with a mixed picture of soft tissue pain/nerve irritation and deconditioning-related perceived instability. While many patients improve with structured physiotherapy, [PATIENT] remains at higher risk of requiring surgery if instability and symptoms persist.  
I recommend a dedicated period of structured physiotherapy focused on proprioception and strength, with gradual functional re-introduction, and cessation of nicotine to optimise tissue healing. I will review [PATIENT] again in **[~3–4 months]** with weight-bearing X-rays (and/or other investigations as indicated) to assess progress and determine whether further intervention (including arthroscopy and/or ligament reconstruction) is warranted.

---

### Sample 3（New referral：Consider surgery / IC を前面化）

#### Diagnosis

- Right ankle lateral ligament and anteromedial ligament complex laxity  

#### Plan

- Plan: Right ankle arthroscopy and lateral and medial ligament stabilisation  
- IC (risk and benefit):
  - Benefits: improved stability, symptom reduction, functional improvement  
  - Risks: nerve injury (including superficial peroneal nerve proximity; temporary neuropraxia possible; permanent sensory change possible), infection, stiffness, recurrent instability, DVT/PE, anaesthetic risks  
  - Natural history: untreated instability increases risk of recurrent episodes and may increase risk of cartilage damage and long-term arthritis  
- Postoperative recovery:
  - **[~6 weeks]** weight-bearing in a CAM boot, then commence physiotherapy  
  - Expected recovery **[~3–6 months]** (variable)  

#### Main paragraph

It was a pleasure to see **[PATIENT]** for review of persistent ankle symptoms. [PATIENT] reports ankle pain and instability, including morning pain and functional limitation, and wishes to proceed with operative management after consideration of timing and goals.  
On examination, foot and ankle alignment is **[normal]** with full range of motion of the ankle and subtalar joint. There is severe lateral ligament laxity and anteromedial laxity, with the ability to partially sublux the talus anteriorly on the tibial mortise.  
Investigations: ankle MRI reviewed, demonstrating a severely attenuated and lax ATFL and CFL. The deltoid ligament is intact but lax. Cartilage is intact.

#### Impression and recommendation

In summary, [PATIENT] has clinically and radiologically significant ligamentous laxity consistent with mechanical instability. I believe [PATIENT] would benefit from ankle arthroscopy and lateral and medial ligament stabilisation. I have discussed the procedure and the specific risks, including nerve injury and recurrent instability, as well as the expected recovery pathway.  
We will proceed with organising surgery and postoperative rehabilitation as outlined.

---

### Sample 4（Post op：Acute / TAR 3 weeks）



---

### Sample 5（Post op：Sub acute / TAR 8 weeks）

#### Diagnosis

- **[~8 weeks]** post left total ankle replacement and gastrocnemius/Achilles lengthening, performed [DATE]
- Neuropathic pain symptoms, likely related to the tibial nerve (working diagnosis)  

#### Plan

- Weight-bearing: commence WBAT in boot; remove boot for sleep and exercises  
- Boot weaning: stop boot altogether in **[~4 weeks]** if progressing  
- Imaging: weight-bearing X-ray of the left ankle today; repeat X-rays in **[~6 weeks]**  
- Follow-up: review in **[~6 weeks]** to reassess symptoms, neurogenic pain, and radiographic progression  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for review of a left ankle replacement, **[~8 weeks]** post-operatively. [PATIENT] reports the ankle feels “pretty good” overall, with minimal mechanical ankle pain, but describes neuropathic pain characterised by shooting pain into the great toe and dysaesthetic sensations (including coldness and nocturnal symptoms).  
On examination, the left foot shows mild colour difference compared to the contralateral side, with a small residual scab at the anterior wound. Range of motion is good (**[~10° dorsiflexion / ~40° plantarflexion]**), hindfoot alignment is neutral, swelling is controlled, and there is no focal tenderness around the ankle.  
Investigations: weight-bearing X-rays demonstrate satisfactory alignment and evidence of bone ingrowth onto components.

#### Impression and recommendation

In summary, [PATIENT] shows satisfactory mechanical recovery at **[~8 weeks]** post total ankle replacement. The primary issue is neuropathic pain symptoms, likely tibial nerve related. I recommend progressing to WBAT in a boot with planned weaning, ongoing exercises, and radiographic follow-up. I will review [PATIENT] in **[~6 weeks]** with repeat X-rays to reassess both symptoms and implant integration.

---

### Sample 6（Post op：Long term / TAR 8 years）

#### Diagnosis

- **[~8 years]** post right total ankle replacement, performed [DATE], stable  
- Residual hindfoot varus  
- Right lateral forefoot discomfort likely footwear-related / varus moment exacerbation  

#### Plan
#### Diagnosis

- **[~3 weeks]** post right total ankle replacement, performed [DATE]  

#### Plan

- Wound care: remove anterior wound sutures today; continue local wound care  
- Rehabilitation: commence/continue active range of motion exercises  
- Weight-bearing: remain non-weight-bearing until **[~6 weeks]**  
- Imaging: review at **[~6 weeks]** with X-ray; consider progression to WBAT in boot depending on radiographic and clinical status  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for a post-operative review, **[~3 weeks]** following a right total ankle replacement. The anterior wound sutures were removed today and the wound is satisfactory. [PATIENT] is performing active range of motion exercises. There are no red flags reported.

#### Impression and recommendation

In summary, [PATIENT] is progressing appropriately in the acute post-operative phase. I recommend continuing non-weight-bearing and range of motion exercises as outlined. I will review [PATIENT] at the **[~6-week]** mark with X-rays to determine readiness for progression to weight-bearing in a boot.
- Continue conservative management (footwear modification, orthoses as required)  
- Imaging: repeat X-ray in **[~12 months]**  
- Review: earlier review if pain worsens, swelling develops, or functional decline occurs  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for review of the right ankle, **[~8 years]** following a total ankle replacement. [PATIENT] reports right lateral forefoot discomfort aggravated by walking, which appears temporally related to new shoes that push the foot into varus; the insoles have been modified.  
On examination, [PATIENT] has good ankle range of motion (**[~20° dorsiflexion / ~35° plantarflexion]**), no ankle tenderness or swelling, and mild hindfoot varus.  
Imaging: X-rays show a fixed-bearing ankle prosthesis in situ without subsidence. A mild halo around the tibial component is unchanged compared with prior imaging and is asymptomatic.

#### Impression and recommendation

In summary, [PATIENT]’s ankle replacement remains stable long term. The forefoot discomfort is most consistent with footwear-related exacerbation of a pre-existing hindfoot varus. I recommend continued conservative management and annual radiographic surveillance.

---

### Sample 7（New referral：TKR plan surgery）

#### Diagnosis

- Left knee medial compartment osteoarthritis (bone-on-bone)  
- Background: prior right total ankle replacement and left flatfoot reconstruction (historical)  

#### Plan

- Plan: left total knee replacement  
- Preoperative work-up: **[pre-op imaging / templating / medical clearance]**  
- IC (risk and benefit):
  - Benefits: pain relief and improved mobility  
  - Risks: infection, vascular injury, numbness, stiffness, pain, incomplete pain relief  
  - Expectations: recovery milestones (e.g., **[~6 weeks]**, **[~3 months]**, **[~6 months]**, **[~12 months]**)  
- Next steps: provide consent form; organise **[imaging]**; schedule surgery after **[DATE]**; arrange rehabilitation plan **[LOCATION/HOSPITAL]**  

#### Main paragraph

It was a pleasure to see **[PATIENT]** for review. [PATIENT] has a background history of a right total ankle replacement and left flatfoot reconstruction and now presents with worsening left knee pain affecting gait and function.  
On examination, gait is antalgic. Knee range of motion is **[~0–100°]** with mild varus alignment.  
Investigations: X-rays demonstrate bone-on-bone medial compartment osteoarthritis of the left knee.

#### Impression and recommendation

In summary, [PATIENT] has symptomatic end-stage medial compartment osteoarthritis of the left knee. I recommend a left total knee replacement and have discussed the procedure, risks, and expected recovery. We will proceed with preoperative planning and scheduling as outlined.

---

### Sample 8（Post op：Sub acute / TKR 2 weeks）

#### Diagnosis

- **[~2 weeks]** post left total knee replacement, performed [DATE]  

#### Plan

- Continue rehabilitation program; analgesia optimisation as needed  
- Imaging: knee X-ray at next review **[~4 weeks]**  
- Follow-up: review in **[~4 weeks]**  
- Safety net: urgent review if fever, increasing redness/drainage, calf pain/swelling, escalating pain, or functional decline  

#### Main paragraph

It was a pleasure to see **[PATIENT]** for review following a recent left total knee replacement, **[~2 weeks]** post-operatively. [PATIENT] reports ongoing pain and is currently in rehabilitation, with concern that pain feels worse than the contralateral side did at a similar stage.  
On examination, the wound is healing well with good alignment. Range of motion is improving with almost full extension and **[~100°]** flexion. There are no clinical signs of infection or other red flags. Postoperative X-rays obtained soon after surgery were satisfactory.

#### Impression and recommendation

In summary, [PATIENT] is progressing appropriately at **[~2 weeks]** post TKR without evidence of infection. I recommend continuing rehabilitation and will review [PATIENT] in **[~4 weeks]** with a knee X-ray to assess ongoing progress.

---

### Sample 9（Post op：Sub acute / TKR 6 weeks）

#### Diagnosis

- **[~6 weeks]** post left total knee replacement, performed [DATE]  
- History of postoperative cellulitis, resolved (historical)  

#### Plan

- Continue range of motion and strengthening program  
- Return to driving: permitted from **[~6 weeks]** post-op if safe and functional  
- Follow-up: review in **[~2–3 months]**  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for review. [PATIENT] underwent a left total knee replacement **[~6 weeks]** ago. [PATIENT] has been walking well and is able to walk long distances, noting mild stiffness after prolonged sitting that improves with movement.  
On examination, gait is normal. The knee extends fully with good quadriceps tone. There is no effusion and the surgical incision is well healed.  
Investigations: postoperative X-rays demonstrate satisfactory bone–prosthesis interface with good integration.

#### Impression and recommendation

In summary, [PATIENT] has satisfactory clinical and radiographic progress at **[~6 weeks]** post TKR. I recommend ongoing range of motion work and will review [PATIENT] again in a few months.

---

### Sample 10（New referral：THR plan surgery）

#### Diagnosis

- Right hip osteoarthritis (symptomatic, function-limiting)  
- Past surgical history: left total hip replacement **[YEAR]** (stable)  
- Possible obstructive sleep apnoea / CPAP pending (medical background)  

#### Plan

- Plan: right total hip replacement  
- Further imaging: preoperative templating to assess component sizing and leg length/offset  
- IC (risk and benefit):
  - Benefits: pain relief, improved function  
  - Risks: nerve injury, leg length discrepancy, dislocation, fracture, subsidence/revision, thromboembolism (DVT/PE), infection, medical complications  
- Medical workup: **[cardiology / general medical clearance]**; request relevant correspondence as indicated  
- Postoperative pathway: early mobilisation; typically full weight-bearing; physiotherapy plan **[home program / fund]**  

#### Main paragraph

It was a pleasure to meet **[PATIENT]** today. [PATIENT] previously underwent a left total hip replacement in **[YEAR]**, which has remained successful and asymptomatic. [PATIENT] now presents with right hip pain predominantly in the groin, aggravated by turning and activity, with functional limitation sufficient to consider surgery.  
On examination, [PATIENT] demonstrates a limp with walking. Hip examination is consistent with established osteoarthritis, with irritability and restricted movement.  
Investigations: X-rays confirm right hip osteoarthritis; further imaging is required for templating.

#### Impression and recommendation

In summary, [PATIENT] has symptomatic right hip osteoarthritis with significant impact on mobility and quality of life. I recommend proceeding with right total hip replacement after completion of preoperative templating and medical clearance, and I have discussed surgical risks, benefits, and recovery expectations.

---

### Sample 11（Post op：Acute / THR 2 weeks）

#### Diagnosis

- **[~2 weeks]** post right total hip replacement, performed [DATE]  

#### Plan

- Wound check: wound healed; continue standard wound care  
- DVT assessment: **[doppler]** negative (if performed)  
- Imaging: review at **[~6 weeks]** with X-ray  
- Follow-up: **[~6 weeks]** post-op review  

#### Main paragraph

It was a pleasure to see **[PATIENT]** for a post-operative wound check, **[~2 weeks]** following a right total hip replacement. [PATIENT] is doing well and is being discharged home from rehabilitation today. The wound has healed well. A Doppler study was negative for DVT.

#### Impression and recommendation

In summary, [PATIENT] is recovering well in the acute post-operative period following right THR. I recommend continuing the standard postoperative pathway and will review [PATIENT] at **[~6 weeks]** with an X-ray.

---

### Sample 12（Complex clinic：Knee multi-factorial / imaging-based planning）

#### Diagnosis

- Bilateral knee osteochondral lesions / osteoarthritis (side-specific as per imaging)  
- Varus malalignment (left) and valgus alignment (right)  
- Avascular necrosis of femoral condyles (bilateral)  
- Significant medical comorbidity (e.g., immunosuppression, transplant, anticoagulation) **[as applicable]**  

#### Plan

- Imaging:
  - Weight-bearing CT scan **[region]** (bilateral)  
  - Standing EOS scan  
  - Supine fine-cut CT for 3D modelling  
  - Updated MRI scans (bilateral knees)  
- 3D modelling review with **[TEAM/SURGEON]**  
- Discuss staged surgical options as indicated (e.g., high tibial osteotomy left; distal femoral osteotomy right)  
- Follow-up: review imaging results and finalise management plan in complex clinic  
- Risk management: surgical caution given medical background; balance disease progression and infection/thrombotic risk  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today in the complex clinic for assessment of progressive knee pain and functional limitation. [PATIENT] has a significant medical background including **[immunosuppression / transplant / anticoagulation]**. Symptoms are activity-related, with the left knee typically the clinical priority.  
On examination, gait is antalgic. The left knee shows reduced range of motion (**[~5–115°]**) with patellofemoral crepitus and medial pseudolaxity consistent with medial compartment disease. The right knee demonstrates valgus alignment with functional limitation.  
Investigations reviewed include prior MRI/CT findings consistent with osteochondral disease and compartment-specific osteoarthritis, and updated imaging is requested for comprehensive alignment and 3D planning.

#### Impression and recommendation

In summary, [PATIENT] has multi-factorial bilateral knee pathology with malalignment and progressive arthritic change. I recommend a structured imaging workup and 3D modelling review to determine the most appropriate staged intervention, balancing potential benefit with elevated perioperative risk.

---

### Sample 13（Functional support letter：NDIS / mobility assistance）

#### Diagnosis

- Leg length discrepancy  
- Right hip excision arthroplasty (Girdlestone appearance) secondary to prior infected THR and femoral osteomyelitis (historical)  
- Left leg radicular pain, likely secondary to lumbar spondylosis (working diagnosis)  

#### Plan

- Referral: **[NEUROSURGEON/PAIN SPECIALIST]** for assessment of back pain and radiculopathy  
- Imaging: plain X-ray and CT scan of the lumbar spine  
- Report: to GP and copied to [PATIENT], supporting funding for:
  - Home modifications  
  - Mobility assistance devices  
  - Occupational therapy input  
- Safety net: review if neurological deficit progresses, pain escalates, or functional capacity declines  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today to assist with an application for functional support and home modifications. [PATIENT] ambulated with **[two crutches]** and reports significant mobility limitation and pain. [PATIENT] has a complex surgical history including a right total hip replacement complicated by infection requiring multiple surgeries, followed by right hip excision arthroplasty and subsequent femoral osteomyelitis, now resolved. [PATIENT] has not required further hip surgery since **[YEAR]**.  
On examination, [PATIENT] demonstrates a positive Trendelenburg gait, significant right leg shortening, and instability. Hip examination is consistent with an excision arthroplasty state. The left hip and knee demonstrate preserved range of motion without focal pain. Straight leg raise is **[positive/negative]** for radicular symptoms.  
Investigations: plain X-rays demonstrate a Girdlestone appearance of the right hip and lumbar spondylosis.

#### Impression and recommendation

In summary, [PATIENT] has major ongoing functional impairment and pain related to the sequelae of multiple right hip operations and chronic leg length discrepancy, compounded by probable lumbar radiculopathy. Further reconstructive hip surgery is not practically available given complexity and high risk.  
I recommend specialist assessment of spinal symptoms and lumbar imaging as outlined. I will provide a report to the GP (copied to [PATIENT]) documenting the functional limitations and supporting funding for home modifications, mobility assistance, and occupational therapy.

---

### Sample 14（New referral：Insertional Achilles tendinopathy / decision against surgery for now）

#### Diagnosis

- Insertional Achilles tendinopathy with calcaneal spur / insertional swelling  
- Rheumatologic background on immunomodulatory therapy **[as applicable]**  

#### Plan

- Continue non-operative management (footwear modification, activity modification, physiotherapy as appropriate)  
- Review in **[~6 months]**  
- If symptoms significantly deteriorate, revisit operative options; coordinate perioperative medication management **[DMARD/antiplatelet]** with treating teams  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for assessment of right heel pain. [PATIENT] has a background history of multiple orthopaedic procedures and inflammatory arthritis managed with **[medications]**, currently well controlled. Over the last **[~12 months]**, the right Achilles insertion has become increasingly symptomatic, though not yet severely restrictive, and [PATIENT] has partially improved with footwear modification.  
On examination, there is swelling and tenderness at the Achilles insertion.  
Investigations: X-rays demonstrate a calcaneal spur with associated soft tissue swelling.

#### Impression and recommendation

In summary, [PATIENT]’s presentation is consistent with insertional Achilles tendinopathy. Given the current symptom severity and elevated perioperative considerations, I recommend continued non-operative management and review in **[~6 months]**, with earlier review if symptoms worsen.

---

### Sample 15（New referral：Achilles rupture / plan surgery）

#### Diagnosis

- Left Achilles tendon rupture, sustained [DATE] (delayed diagnosis)
- Left talar bone bruising (likely impingement related to injury mechanism)  
- Relevant comorbidity increasing infection risk **[as applicable]**  

#### Plan

- Plan: left Achilles tendon percutaneous repair on **[DATE]**  
- Physiotherapy referral: pre-op training for non-weight-bearing strategies and post-op rehabilitation  
- Postoperative pathway: **[~6 weeks]** non-weight-bearing in a CAM boot  
- IC (risk and benefit): infection, DVT/PE, nerve injury, wound complications, re-rupture, need for further surgery  
- Work planning: arrange **[~6 weeks]** off work post-operatively  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for assessment of left ankle pain following an injury **[~3 months]** ago involving hyperdorsiflexion. [PATIENT] reports posterior ankle pain radiating into the calf, worse with walking and improved with rest, with incomplete improvement despite use of a CAM boot.  
On examination, there is a positive Thompson test and a palpable defect in the Achilles tendon.  
Investigations: MRI demonstrates a complete rupture of the Achilles tendon and increased signal in the talar neck consistent with bone bruising.

#### Impression and recommendation

In summary, [PATIENT] has a complete Achilles tendon rupture with delayed diagnosis and associated talar bone bruising. I recommend percutaneous repair as outlined, with appropriate thromboprophylaxis and rehabilitation planning. We will proceed with surgery scheduling and physiotherapy coordination.

---

### Sample 16（New referral：Hallux valgus + crossover/hammer toe / plan surgery）

#### Diagnosis

- Right hallux valgus  
- Right second hammer toe with MTP dislocation / crossover deformity  
- Midfoot arthritis **[if present]**  

#### Plan

- Plan: percutaneous correction of hallux valgus + correction of second toe position  
- Alternatives: non-operative care; in selected cases, second toe amputation discussed **[context-dependent]**  
- IC (risk and benefit): infection, DVT/PE, nerve injury/neuroma, non-union, fracture, incomplete correction, need for hardware removal, anaesthetic risks  
- Recovery: post-op shoe or boot; adherence to post-op instructions for optimal healing  
- Next steps: provide consent forms; schedule surgery at **[HOSPITAL/CLINIC]** depending on availability and patient preference  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for an initial consult regarding bunion symptoms and difficulty with footwear. [PATIENT] reports progressive pain and functional limitation, including nocturnal neuropathic-type discomfort and difficulty finding comfortable shoes.  
On examination, there is severe hallux valgus with a palpable medial bony prominence at the 1st MTP joint. The second toe is dislocated with fixed deformity and tight surrounding soft tissues. Distal neurovascular status is grossly intact.  
Investigations: X-rays demonstrate hallux valgus deformity with second MTP dislocation and midfoot arthritic changes.

#### Impression and recommendation

In summary, [PATIENT] has a complex forefoot deformity consistent with hallux valgus and second toe dislocation, correlating with symptoms and shoe-wear difficulty. I recommend operative correction as outlined and have discussed realistic goals, risks, and recovery. [PATIENT] will consider scheduling options and advise the clinic of their decision.

---

### Sample 17（Post op：Acute / forefoot deformity correction 2 weeks）

#### Diagnosis

- **[~2 weeks]** post bilateral hallux valgus and crossover/second toe correction, performed [DATE]  

#### Plan

- Wound care: sutures removed today; continue swelling control  
- Weight-bearing: WBAT with post-op shoe/boot as directed; progress to normal footwear in **[~4 weeks]** if appropriate  
- Imaging: repeat X-ray at **[~4 weeks]**  
- Follow-up: review in **[~4 weeks]**  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for review **[~2 weeks]** after bilateral hallux valgus and crossover second toe correction. [PATIENT] reports minimal pain and no neurological complications. Wounds have healed nicely and sutures were removed. Swelling is well controlled and overall foot and toe positioning is satisfactory.

#### Impression and recommendation

In summary, [PATIENT] is progressing well in the early postoperative phase. I recommend continuing swelling control and protected weight-bearing as outlined, with repeat X-rays and review in **[~4 weeks]** to guide progression to normal footwear.

---

### Sample 18（New referral：Forefoot-driven varus + gouty tophus / imaging-based planning）

#### Diagnosis

- Gouty tophus around the 1st MTP joint region (working diagnosis based on exam/imaging)  
- Forefoot-driven varus deformity with plantarflexion of first/second rays contributing to varus moment on weight-bearing  
- Bilateral fourth curly toes secondary to FDL tightness  

#### Plan

- Imaging: updated weight-bearing X-rays, weight-bearing CT, and MRI as indicated  
- Medical: continue gout management **[medication]** with coordination **[GP/Rheumatology]**  
- Consider procedures depending on imaging and symptoms:
  - FDL release to fourth toe  
  - Extension osteotomy of first/second rays to address forefoot pronation/plantarflexion component  
- Follow-up: review once imaging is complete to finalise operative vs non-operative strategy and provide a quote if required  

#### Main paragraph

It was a pleasure to see **[PATIENT]** today for review of forefoot symptoms and deformity. [PATIENT] reports a history of intermittent gout and progressive functional difficulty.  
On examination, there is a large soft tissue swelling under the first metatarsal region consistent with gouty tophus, along with a forefoot-driven varus deformity and bilateral fourth curly toes. There is relative plantarflexion of the first and second rays contributing to a varus moment on weight-bearing.  
Investigations: prior plain X-rays showed erosive changes consistent with gout; updated imaging is requested to delineate current anatomy and guide management.

#### Impression and recommendation

In summary, [PATIENT] has a combined medical (gouty tophus) and mechanical (forefoot-driven varus) problem contributing to symptoms. I recommend updated imaging and a structured review to determine the most appropriate staged intervention, including possible tendon release and osteotomy if indicated.

---

### Sample 19（Follow-up：Post op / sinus tarsi impingement concern）

#### Diagnosis

- **[~6 weeks]** post-operative right lateral process of talus osteotomy  
- Persistent peroneal spasm (pain-related)  
- Concern for recurrent sinus tarsi impingement (working diagnosis)  
- Background: possible tarsal coalition **[if applicable]**  

#### Plan

- Imaging: request weight-bearing CT scan of right foot and ankle to assess for recurrent sinus tarsi impingement and delineate anatomy  
- Symptom management: supportive footwear; avoid high-impact activities  
- Infection control (if scar inflammation): prescribe oral antibiotics **[if indicated]**  
- Follow-up: review in **[~2 weeks]** to discuss CT results and formulate further management  
- Contingency: consider arthroscopic debridement if recurrent impingement confirmed and symptoms persist; reserve subtalar fusion as salvage procedure  

#### Main paragraph

It was a pleasure to see **[PATIENT]** for review **[~6 weeks]** following a right lateral process of talus osteotomy. [PATIENT] reports the ankle is sore after work.  
On examination, gait is normal. There is mild ongoing inflammation along the lateral ankle scar. Ankle range of motion is symmetrical. There is spasm of the peroneal tendons.  
Investigations: a weight-bearing CT scan has been requested to assess for recurrent sinus tarsi impingement.

#### Impression and recommendation

In summary, [PATIENT]’s persistent peroneal spasm is most likely pain-mediated, with concern for recurrent sinus tarsi impingement. I recommend weight-bearing CT assessment and close follow-up. Further intervention will be guided by CT findings and clinical course, with arthroscopic debridement considered if indicated and subtalar fusion reserved as salvage.


