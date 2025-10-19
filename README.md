# 📚 StudyHub
**学習場所検索 × 学習管理アプリ**

学習場所の検索と、TODOリストやタイマーなどの学習管理機能を一つにまとめることで、  
**「どこで勉強するか」** から **「実際に勉強を始める」** までをシームレスにつなぎ、  
勉強を始めるまでの手間を減らすことを目的としたWebアプリです。

---

## 🏆 開発概要
本アプリは **ハッカソン形式のチーム開発** で制作しました。  
私は主に **インフラ構築・環境設計（AWS / Docker / nginx / uWSGI / MySQL）** を担当しました。  
開発環境と本番環境の整合性を重視し、Docker Compose による統一環境構築を行いました。

---

## 👥 チーム構成
| 役割 | 人数 | 主な担当技術 |
|------|------|---------------|
| フロントエンド | 2名 | HTML / Tailwind CSS / JavaScript |
| バックエンド | 1名 | Django / API設計 / データベース連携 |
| インフラ | 1名（井上智晴） | AWS / Docker / nginx / uWSGI / RDS |

---

## 🧩 担当範囲（井上智晴）
- Docker による開発・本番環境構築  
- AWS上でのデプロイ設計（EC2 / RDS / ALB）  
- nginx + uWSGI のリバースプロキシ設定  
- Security Group / VPC 設計  
- チームメンバーが容易に環境構築できるようドキュメント整備

---

## 🏗️ インフラ構成図
![Infrastructure](https://raw.githubusercontent.com/devharu-49/studyhub/main/docs/infrastructure.jpg)

- **開発環境**：Docker Compose（nginx + Django + MySQL）  
- **本番環境**：AWS EC2 / RDS(MySQL) / nginx / uWSGI  
- **監視**：CloudWatchによる稼働監視  
- **今後の拡張予定**：ALB + Auto Scaling、GitHub ActionsによるCI/CD自動化

---

## ⚙️ 使用技術
| Category | Technology Stack |
|-----------|------------------|
| Frontend | JavaScript / HTML / Tailwind CSS |
| Backend | Python / Django / uWSGI |
| Infrastructure | AWS / Docker / nginx |
| Database | MySQL |
| Design | Figma / Canva |
| Tools | Prettier / Git / GitHub / Docker Compose |

---

## 🗂 ディレクトリ構成
studyhub/
├── manage.py
├── templates/
├── static/
├── user/
├── todo/
├── timer/
├── map/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── docs/
    └── infrastructure.jpg


---

## 🔄 ブランチ運用ルール
- **main**：本番環境ブランチ（直接push禁止）  
- **develop**：開発中の最新状態を保持  
- **feature/***：機能単位ブランチ（例：feature/todo-list）

すべての変更はプルリクエスト経由でレビュー後にマージ。

---

## 💬 振り返り
> ローカル環境では動作しても、AWS上では動かないケースが多く発生しました。  
> Dockerネットワークやセキュリティ設定など、インフラの奥深さを実感。  
> 今後はCI/CD導入や運用フェーズも強化していきたいと考えています。

---

## 👤 作者
**井上 智晴（Haru Inoue）**  
- 🔗 [GitHub: devharu-49](https://github.com/devharu-49)

---

## 🏆 Hackathon 2025 冬の陣 Dチーム
**テーマ:** 「学びを支える仕組みを創る」  
**制作期間:** 2025年1月〜2月  
**開発人数:** 4名（フロント2名 / バック1名 / インフラ1名）  

---
