local g = import './g.libsonnet';
local commonlib = import 'common-lib/common/main.libsonnet';
local utils = commonlib.utils;

{
  new(this)::
    {
      local t = this.grafana.targets,
      local stat = g.panel.stat,
      local fieldOverride = g.panel.table.fieldOverride,
      local alertList = g.panel.alertList,
      local pieChart = g.panel.pieChart,
      local barGauge = g.panel.barGauge,

      successfulQueriesPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Successful queries',
          targets=[t.ClickHouseProfileEvents_SelectQuery, t.ClickHouseProfileEvents_InsertQuery, t.ClickHouseProfileEvents_AsyncInsertQuery],
          description='Rate of successful queries per second')
        + g.panel.timeSeries.standardOptions.withUnit('/ sec')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      failedQueriesPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Failed queries',
          targets=[t.ClickHouseProfileEvents_FailedSelectQuery, t.ClickHouseProfileEvents_FailedInsertQuery],
          description='Rate of failed queries per second')
        + g.panel.timeSeries.standardOptions.withUnit('/ sec')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      rejectedInsertsPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Rejected inserts',
          targets=[t.ClickHouseProfileEvents_RejectedInserts],
          description='Number of rejected inserts per second')
        + g.panel.timeSeries.standardOptions.withUnit('/ sec')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      memoryUsagePanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Memory usage',
          targets=[t.ClickHouseMetrics_MemoryTracking],
          description='Memory usage over time')
        + g.panel.timeSeries.standardOptions.withUnit('decbytes')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      memoryUsageGaugePanelPanel:
        // Unsupported panel type: barGauge
,

      activeConnectionsPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Active connections',
          targets=[t.ClickHouseMetrics_TCPConnection, t.ClickHouseMetrics_HTTPConnection, t.ClickHouseMetrics_MySQLConnection, t.ClickHouseMetrics_PostgreSQLConnection],
          description='Current number of connections to ClickHouse')
        + g.panel.timeSeries.standardOptions.withUnit('none')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      networkReceivedPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network received',
          targets=[t.ClickHouseProfileEvents_NetworkReceiveBytes],
          description='Received network throughput')
        + g.panel.timeSeries.standardOptions.withUnit('Bps')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      networkTransmittedPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network transmitted',
          targets=[t.ClickHouseProfileEvents_NetworkSendBytes],
          description='Transmitted network throughput')
        + g.panel.timeSeries.standardOptions.withUnit('Bps')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      diskReadLatencyPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Disk read latency',
          targets=[t.ClickHouseProfileEvents_DiskReadElapsedMicroseconds],
          description='Time spent waiting for read syscall')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      diskWriteLatencyPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Disk write latency',
          targets=[t.ClickHouseProfileEvents_DiskWriteElapsedMicroseconds],
          description='Time spent waiting for write syscall')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      networkTransmitLatencyInboundPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network receive latency',
          targets=[t.ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds],
          description='Latency of inbound network traffic')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      networkTransmitLatencyOutboundPanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network transmit latency',
          targets=[t.ClickHouseProfileEvents_NetworkSendElapsedMicroseconds],
          description='Latency of outbound network traffic')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      zooKeeperWaitTimePanelPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'ZooKeeper wait time',
          targets=[t.ClickHouseProfileEvents_ZooKeeperWaitMicroseconds],
          description='Time spent waiting for ZooKeeper request to process')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

    },
}