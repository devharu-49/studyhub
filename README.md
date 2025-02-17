# StudyHub

## 学習場所検索 ＋ 学習管理アプリ

学習場所の検索と、TODOリストやタイマーなどの学習管理機能を一つにまとめることで、  
**「どこで勉強するか」** から **「実際に勉強を始める」** までをシームレスにつなぎ、勉強の開始までの手間を減らすアプリ。

## 使用技術

| Category       | Technology Stack                      |
| -------------- | ------------------------------------- |
| Frontend       | JavaScript, HTML, Tailwind CSS        |
| Backend        | Python, Django, uWSGI                 |
| Infrastructure | Amazon Web Services, Docker, nginx    |
| Database       | MySQL                                 |
| Design         | Figma, Canva                          |
| etc.           | Prettier, Git, GitHub, Docker Compose |

<br />

## ブランチ運用について

### 1.ブランチの説明

**main**  
本番環境にデプロイするためのブランチです。  
直接コミットやプッシュは行わず、必ずプルリクエストを通してマージします。

**develop**  
開発中の最新の状態を保持するためのブランチです。  
機能が完成したら、feature/\*ブランチからこのブランチにマージします。

**feature/\***  
新機能や修正を実装するためのブランチです。  
機能ごとに個別にブランチを作成し、作業が完了したらdevelopにマージします。  
例: feature/todo-list, feature/authentication

### 2.プルリクエスト（PR）のルール

新しい機能を実装した場合は、必ず feature/\* ブランチから develop ブランチに向けてプルリクエストを作成します。  
プルリクエストには詳細な説明を記載し、どのような変更が行われたかを説明します。  
プルリクエストは必ず他のチームメンバーによるレビューを受け、問題がない場合にマージします。
