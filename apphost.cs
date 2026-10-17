#:sdk Aspire.AppHost.Sdk@13.6.0
#:package Aspire.Hosting.PostgreSQL@13.6.0
#:package Aspire.Hosting.Redis@13.6.0
#:package Aspire.Hosting.Python@13.6.0
#:package Aspire.Hosting.JavaScript@13.6.0

// apphost.mts と同じ構成を C# で書いたもの。
// 起動するときは aspire run --apphost apphost.cs を実行する。

var builder = DistributedApplication.CreateBuilder(args);

var postgres = builder.AddPostgres("postgres")
    .WithRepl();
var db = postgres.AddDatabase("bookfest");
var cache = builder.AddRedis("cache")
    .WithRepl();

var api = builder.AddUvicornApp("api", "./api", "main:app")
    .WithUv()
    .WithEnvironment("DATABASE_URL", db.Resource.UriExpression)
    .WithEnvironment("REDIS_URL", cache.Resource.UriExpression)
    .WithHttpHealthCheck("/health")
    .WaitFor(db)
    .WaitFor(cache);

if (builder.ExecutionContext.IsRunMode)
{
    api.WithEnvironment("ENABLE_SEED_API", "true")
        .WithHttpCommand("/admin/seed", "テストデータを投入", commandOptions: new()
        {
            Description = "本と在庫のテストデータを入れ直します",
            ConfirmationMessage = "今のデータは消えます。テストデータを投入しますか？",
        });
}

builder.AddViteApp("frontend", "./frontend")
    .WithReference(api)
    .WaitFor(api)
    .WithEnvironment("BROWSER", "none")
    .WithExternalHttpEndpoints();

builder.Build().Run();
