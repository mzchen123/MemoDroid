# Experiment Results

The APK files for all 60 memory pool apps and 30 test apps used in our experiments can be downloaded from: [Google Drive](https://drive.google.com/drive/folders/1NsunAviTb9xCClY5hBjbxu-3792_C8f-?usp=sharing)

## RQ1: Effectiveness Evaluation
Our evaluation on 30 real-world Android apps across 15 categories demonstrates that MemoDroid significantly enhances GUI testing performance across all five baseline approaches:

| Baseline          | Activity Coverage Improvement | Code Coverage Improvement | Bug Detection Improvement |
|-------------------|-------------------------------|---------------------------|---------------------------|
| GPTDroid          | ↑79%                          | ↑81%                      | ↑194%                     |
| DroidAgent        | ↑96%                          | ↑89%                      | ↑198%                     |
| AUITestAgent      | ↑86%                          | ↑86%                      | ↑57%                      |
| VisionDroid       | ↑88%                          | ↑87%                      | ↑71%                      |
| Guardian          | ↑93%                          | ↑97%                      | ↑72%                      |

Key findings:
- Episodic memory enables effective action replication
- Reflective memory helps identify crash-prone behaviors
- Strategic memory provides high-level exploration guidance

## RQ2: Ablation Study
Removing any memory layer causes significant performance degradation:

| Memory Layer Removed | Avg. Coverage Drop | Avg. Bug Detection Drop |
|----------------------|--------------------|-------------------------|
| Episodic Memory      | 23-26%             | 14-24%                  |
| Reflective Memory    | 29-38%             | 19-39%                  |
| Strategic Memory     | 15-22%             | 11-19%                  |

Reflective memory shows the strongest individual contribution to performance.

## RQ3: Memory Evolving Effect
Testing performance improves progressively as memory pool expands:

- Initial 5 apps provide sufficient diversity for generalization
- Performance gains continue through 60-app memory pool
- VisionDroid+MemoDroid achieves 0.71 activity coverage (+73% from baseline)

## RQ4: Practical Usefulness
In large-scale evaluation on 200 popular apps:
- Detected **49 previously unknown bugs** in 47 apps
- **35 bugs fixed** and **14 confirmed** by developers
- 7 bugs were only detectable with MemoDroid augmentation

| ID | App name        | Category | Down  | Version | Status    | GP | GP+MemoDroid | DA | DA+MemoDroid | ATA | ATA+MemoDroid | VD | VD+MemoDroid | GU | GU+MemoDroid |
| -- | --------------- | -------- | ----- | ------- | --------- | -- | ------------ | -- | ------------ | --- | ------------- | -- | ------------ | -- | ------------ |
| 1  | Traveloka       | Travel   | 50M+  | 5.20.0  | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 2  | Yelp            | Food     | 50M+  | 25.11   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 3  | BeautyCam       | Photo    | 50M+  | 12.5.35 | Fixed     |    | \*           |    |              |     | \*            |    | \*           |    | \*           |
| 4  | Wattpad         | Book     | 50M+  | 11.2.0  | Fixed     | \* | \*           | \* | \*           | \*  | \*            | \* | \*           | \* | \*           |
| 5  | Strava          | Health   | 50M+  | 4.2.5   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 6  | Klook           | Travel   | 10M+  | 7.20.2  | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 7  | HelloTalk       | Edu      | 10M+  | 6.0.6   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 8  | Xbrowser        | Commun   | 10M+  | 5.2.0   | Fixed     |    |              |    |              |     |               |    | \*           |    | \*           |
| 9  | MMWbO           | Health   | 10M+  | 25.2.0  | Fixed     | \* | \*           | \* | \*           |     | \*            |    | \*           | \* | \*           |
| 10 | SportsTrack     | Health   | 10M+  | 5.0.1   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 11 | Deliveroo       | Food     | 10M+  | 3.215   | Fixed     |    | \*           |    |              |     | \*            |    | \*           |    | \*           |
| 12 | KiKUU           | Shop     | 10M+  | 30.1.6  | Fixed     |    | \*           | \* | \*           |     | \*            |    | \*           |    | \*           |
| 13 | Wink            | Video    | 10M+  | 2.7.5   | Fixed     | \* | \*           |    | \*           |     | \*            | \* | \*           | \* | \*           |
| 14 | StepsApp        | Health   | 10M+  | 6.0.12  | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 15 | eSound          | Music    | 10M+  | 6.11    | Fixed     |    |              |    | \*           |     | \*            |    | \*           |    | \*           |
| 16 | HabitNow        | Product  | 5M+   | 2.2.3d  | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 17 | Sectograph      | Product  | 5M+   | 2.3.1   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 18 | Comera          | Commun   | 5M+   | 5.0.23  | Fixed     |    |              |    |              |     | \*            |    | \*           | \* | \*           |
| 19 | NetSpeed        | Tool     | 5M+   | 1.10.0  | Fixed     |    | \*           |    | \*           |     |               |    | \*           | \* | \*           |
| 20 | Speaky          | Edu      | 5M+   | 3.3.5   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 21 | FSBrowser       | Social   | 5M+   | 8.4.38  | Fixed     | \* | \*           |    | \*           | \*  | \*            |    | \*           |    | \*           |
| 22 | Sketchbook      | Art      | 5M+   | 6.10.0  | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 23 | FlipaClip       | Art      | 5M+   | 4.2.5   | Fixed     |    |              |    |              |     | \*            |    | \*           |    | \*           |
| 24 | ClickUp         | Product  | 1M+   | 5.4.6   | Fixed     |    | \*           |    | \*           |     | \*            | \* | \*           |    | \*           |
| 25 | Tawasal         | Commun   | 1M+   | 5.4.0   | Fixed     |    | \*           | \* | \*           |     | \*            | \* | \*           | \* | \*           |
| 26 | VERO            | Social   | 1M+   | 2.3.3   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 27 | Hilokal         | Edu      | 1M+   | 12.15.3 | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 28 | 9Weather        | Weather  | 1M+   | 1.134   | Fixed     |    | \*           |    | \*           |     | \*            | \* | \*           | \* | \*           |
| 29 | BEA             | Finance  | 1M+   | 10.0.1  | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 30 | Joytify         | Music    | 1M+   | 1.2.9   | Fixed     |    | \*           |    | \*           |     |               |    | \*           |    | \*           |
| 31 | Weezer          | Music    | 1M+   | 2.4.4   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 32 | Vyke            | Commun   | 1M+   | 1.20.3  | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 33 | DailyExpenses   | Finance  | 1M+   | 249     | Fixed     |    |              |    |              |     | \*            |    | \*           |    | \*           |
| 34 | Supershift      | Product  | 1M+   | 25.15   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 35 | Timeleft        | Travel   | 500K+ | 3.3.0   | Fixed     |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 36 | Sofascore       | Sport    | 50M+  | 13.3    | Confirmed |    |              |    |              |     |               |    | \*           |    | \*           |
| 37 | WePlay          | Enter    | 10M+  | 5.2.10  | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 38 | FotMob          | Sport    | 10M+  | 9.2     | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 39 | Bluecoins       | Finance  | 1M+   | 12.9.5  | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 40 | Logos Bible     | Book     | 1M+   | 42.0.2  | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 41 | Moviebase       | Enter    | 1M+   | 5.3.15  | Confirmed |    | \*           |    |              |     | \*            |    | \*           |    | \*           |
| 42 | Domino's        | Food     | 1M+   | 2.0.39  | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 43 | Weezer          | Music    | 1M+   | 2.4.4   | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 44 | Eatigo          | Food     | 1M+   | 8.10.0  | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 45 | SideChef        | Food     | 1M+   | 5.31.1  | Confirmed |    |              |    |              |     | \*            |    | \*           |    | \*           |
| 46 | BluShopSMecoins | Shop     | 1M+   | 5.3.0   | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 47 | Moviebase       | Enter    | 1M+   | 5.3.15  | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 48 | Domino's        | Food     | 1M+   | 2.0.39  | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |
| 49 | Money Pro       | Finance  | 500K+ | 2.11.15 | Confirmed |    | \*           |    | \*           |     | \*            |    | \*           |    | \*           |

Example developer feedback:  
*"This bug affects core functionality and was hindering users' ability..."* - Wallet App maintainer

## Cross-Version & Cross-Platform Testing
- **Version Evolution**: Maintains effectiveness across 5 versions of Wallet app (v2.0-v5.0)
- **Platform Transfer**: Android memory improves web testing (7 vs 3 bugs detected in SeeAct)


