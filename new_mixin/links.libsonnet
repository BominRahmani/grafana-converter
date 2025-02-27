local g = import './g.libsonnet';
{
  local link = g.dashboard.link,
  new(this):
    {
      clickhouseReplica:
        link.link.new('Clickhouse Replica', '/d/' + this.grafana.dashboards.clickhouse_replica.uid)
        + link.link.options.withKeepTime(true),

      clickhouseOverview:
        link.link.new('Clickhouse Overview', '/d/' + this.grafana.dashboards.clickhouse_overview.uid)
        + link.link.options.withKeepTime(true),

      clickhouseLatency:
        link.link.new('Clickhouse Latency', '/d/' + this.grafana.dashboards.clickhouse_latency.uid)
        + link.link.options.withKeepTime(true),
    }
    +
    if this.config.enableLokiLogs then
      {
        logs:
          link.link.new('Logs', '/d/' + this.grafana.dashboards.logs.uid)
          + link.link.options.withKeepTime(true),
      }
    else {},
}
