# AGENTS.md

このリポジトリは Aspire で動かしています。AppHost は `apphost.mts` です。

## 起動

- `aspire run` で、フロントエンド、API、PostgreSQL、Redis をまとめて起動します。
- 起動しているかどうかは `aspire ps` で確認できます。

## 実行時の不具合を調べるとき

実行時の不具合は、Aspire が集めているテレメトリーで調べてください。

- `aspire otel traces <リソース名>`: トレース
- `aspire otel spans <リソース名>`: スパン
- `aspire otel logs <リソース名>`: 構造化ログ
- `aspire logs <リソース名>`: コンソールログ