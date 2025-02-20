local g = import './g.libsonnet';
{
  local link = g.dashboard.link,
  new(this):
    {
      clickhouseOverview:
        link.link.new('Clickhouse Overview', '/d/' + this.grafana.dashboards['clickhouse-overview.json'].uid)
        + link.link.options.withKeepTime(true),

      backToClickhouseOverview:
        link.link.new('Back to Clickhouse Overview', '/d/' + this.grafana.dashboards['clickhouse-overview.json'].uid)
        + link.link.options.withKeepTime(true),

      clickhouseLatency:
        link.link.new('Clickhouse Latency', '/d/' + this.grafana.dashboards['clickhouse-latency.json'].uid)
        + link.link.options.withKeepTime(true),

      backToClickhouseLatency:
        link.link.new('Back to Clickhouse Latency', '/d/' + this.grafana.dashboards['clickhouse-latency.json'].uid)
        + link.link.options.withKeepTime(true),

      otherDashboards:
        link.dashboards.new('All dashboards', this.config.dashboardTags)
        + link.dashboards.options.withIncludeVars(true)
        + link.dashboards.options.withKeepTime(true)
        + link.dashboards.options.withAsDropdown(true),
    }
    +
    if this.config.enableLokiLogs then
      {
        logs:
          link.link.new(std.join(' ', [this.config.dashboardNamePrefix, 'Logs']), '/d/' + this.grafana.dashboards.logs.uid)
          + link.link.options.withKeepTime(true),
      }
    else {},
}