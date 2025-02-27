local clickhouselib = import './main.libsonnet';

local clickhouse =
  clickhouselib.new()
  + clickhouselib.withConfigMixin(
    {
      filteringSelector: 'job=~"integrations/clickhouse"',
      uid: 'clickhouse',
      enableLokiLogs: true,
    }
  );

// populate monitoring-mixin:
{
  grafanaDashboards+:: clickhouse.grafana.dashboards,
  prometheusAlerts+:: clickhouse.prometheus.alerts,
  prometheusRules+:: clickhouse.prometheus.recordingRules,
}
