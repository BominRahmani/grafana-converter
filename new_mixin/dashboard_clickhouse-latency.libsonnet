local g = import './g.libsonnet';
local logslib = import 'logs-lib/logs/main.libsonnet';
{
  local root = self,
  new(this)::
    local prefix = this.config.dashboardNamePrefix;
    local links = this.grafana.links;
    local tags = this.config.dashboardTags;
    local uid = g.util.string.slugify(this.config.uid);
    local vars = this.grafana.variables;
    local annotations = this.grafana.annotations;
    local refresh = this.config.dashboardRefresh;
    local period = this.config.dashboardPeriod;
    local timezone = this.config.dashboardTimezone;
    local panels = this.grafana.panels;

    {
      'clickhouse-latency.json':
        g.dashboard.new(prefix + ' ClickHouse latency')
        + g.dashboard.withPanels(
          g.util.grid.wrapPanels([
            panels.diskReadLatencyPanel,
            panels.diskWriteLatencyPanel,
            panels.networkTransmitLatencyInboundPanel,
            panels.networkTransmitLatencyOutboundPanel,
            panels.zooKeeperWaitTimePanel,
          ])
        )
        + root.applyCommon(
          vars.singleInstance,
          uid,
          tags,
          links,
          annotations,
          timezone,
          refresh,
          period
        ),
    },
}