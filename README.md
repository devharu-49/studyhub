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
## 🏆 開発概要
このアプリはハッカソンでチーム開発した作品です。  
私は主に **インフラ構築・環境設計（AWS, Docker, nginx, uWSGI, MySQL）** を担当しました。

## 👥 チーム構成
- フロントエンド：2名（HTML, Tailwind CSS, JavaScript）
- バックエンド：1名（Django, API開発）
- インフラ：私（AWS, Docker, nginx,）

## 🧩 担当範囲
- Docker を利用した開発／本番環境の構築
- AWS上へのデプロイ（EC2, RDS, ALB, S3）
- nginx + uWSGI のリバースプロキシ設定
- セキュリティグループ／VPC設計
## 🏗 インフラ構成図

![Infrastructure Diagram](docs/infrastructure.png)

- 開発環境：Docker Compose（nginx + Django + MySQL）
- 本番環境：AWS EC2 / RDS(MySQL)  / nginx / Gunicorn
- セキュリティ：Security Group設計、CloudWatch監視
- 今後の拡張：ALB + Auto Scaling、GitHub ActionsによるCI/CD化


## ディレクトリ構成

```
.
├── map
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── static
│ ├── css
│ ├── images
│ └── js
├── studyhub
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── templates
│ ├── base.html
│ ├── login.html
│ ├── main.html
│ ├── search.html
│ ├── search_detail.html
│ ├── search_result.html
│ ├── signup.html
│ ├── todo.html
│ ├── tododetail.html
│ └── todoform.html
├── timer
│ ├── admin.py
│ ├── apps.py
│ ├── context_processors.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── todo
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── user
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── Dockerfile
├── README.md
├── docker-compose.yml
├── manage.py
├── package-lock.json
├── package.json
├── requirements.txt
├── tailwind.config.js
└── wait-for-it.sh
```

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
