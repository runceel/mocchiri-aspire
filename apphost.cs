#:sdk Aspire.AppHost.Sdk@13.6.0
#:package Aspire.Hosting.PostgreSQL@13.6.0
#:package Aspire.Hosting.Redis@13.6.0
#:package Aspire.Hosting.Python@13.6.0
#:package Aspire.Hosting.JavaScript@13.6.0

// apphost.mts と同じ構成を C# で書いたもの。
// 起動するときは aspire run --apphost apphost.cs を実行する。

var builder = DistributedApplication.CreateBuilder(args);

var postgres = builder.AddPostgres("postgres");
var db = postgres.AddDatabase("bookfest");
var cache = builder.AddRedis("cache");

var api = builder.AddUvicornApp("api", "./api", "main:app")
    .WithUv()
    .WithEnvironment("DATABASE_URL", db.Resource.UriExpression)
    .WithEnvironment("REDIS_URL", cache.Resource.UriExpression)
    .WithHttpHealthCheck("/health")
    .WaitFor(db)
    .WaitFor(cache);

builder.AddViteApp("frontend", "./frontend")
    .WithReference(api)
    .WaitFor(api)
    .WithEnvironment("BROWSER", "none")
    .WithExternalHttpEndpoints();

builder.Build().Run();
