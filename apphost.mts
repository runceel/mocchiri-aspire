// Aspire TypeScript AppHost
// For more information, see: https://aspire.dev

import { createBuilder } from './.aspire/modules/aspire.mjs';

const builder = await createBuilder();

// compose.yaml の postgres / redis の代わり。
// AppHost を止めるたびに破棄する（persistent にせず、データボリュームも付けない）。
// ユーザー名・パスワード・ポートは Aspire の既定（パスワードは自動生成）。
// withRepl で、ダッシュボードのターミナルから psql / redis-cli を開けるようにする（aspire run のときだけ）。
const postgres = await builder.addPostgres('postgres')
    .withRepl();
const db = await postgres.addDatabase('bookfest');
const cache = await builder.addRedis('cache')
    .withRepl();

// scripts/dev.sh の `uv run uvicorn main:app --port 8000` の代わり。ポートは Aspire が決める。
// 接続情報は api/.env に書かず、アプリが読む環境変数名のまま AppHost から渡す。
const api = await builder.addUvicornApp('api', './api', 'main:app')
    .withUv()
    .withEnvironment('DATABASE_URL', await db.uriExpression())
    .withEnvironment('REDIS_URL', await cache.uriExpression())
    .withHttpHealthCheck({ path: '/health' })
    .waitFor(db)
    .waitFor(cache);

// aspire run で動かしているときだけ、テストデータを入れ直す /admin/seed を有効にして、
// ダッシュボードのコマンドから呼べるようにする（デプロイ先では有効にしない）。
if (await builder.executionContext().isRunMode()) {
    await api.withEnvironment('ENABLE_SEED_API', 'true')
        .withHttpCommand('/admin/seed', 'テストデータを投入', {
            description: '本と在庫のテストデータを入れ直します',
            confirmationMessage: '今のデータは消えます。テストデータを投入しますか？',
        });
}

// scripts/dev.sh の `npm run dev` の代わり。
// withReference(api) で API の URL が API_HTTP として渡り、vite.config.ts の proxy 先になる。
await builder.addViteApp('frontend', './frontend')
    .withReference(api)
    .waitFor(api)
    .withEnvironment('BROWSER', 'none')
    .withExternalHttpEndpoints();

await builder.build().run();