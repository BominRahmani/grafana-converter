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

      successfulQueriesPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Successful queries',
          targets=[t.ClickHouseProfileEvents_SelectQuery, t.ClickHouseProfileEvents_InsertQuery, t.ClickHouseProfileEvents_AsyncInsertQuery],
          description='Rate of successful queries per second'
        )
        + g.panel.timeSeries.standardOptions.withUnit('ops')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls(false)
      ,

      failedQueriesPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Failed queries',
          targets=[t.ClickHouseProfileEvents_FailedSelectQuery, t.ClickHouseProfileEvents_FailedInsertQuery],
          description='Rate of failed queries per second'
        )
        + g.panel.timeSeries.standardOptions.withUnit('ops')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls(false)
      ,

      rejectedInsertsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Rejected inserts',
          targets=[t.ClickHouseProfileEvents_RejectedInserts],
          description='Number of rejected inserts per second'
        )
        + g.panel.timeSeries.standardOptions.withUnit('ops')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls(false)
      ,

      memoryUsagePanel:
        commonlib.panels.disk.timeSeries.usage.new(
          'Memory usage',
          targets=[t.ClickHouseMetrics_MemoryTracking],
          description='Memory usage over time'
        )
      ,

      memoryUsageGaugePanel:
        barGauge.new(title='Memory usage')
        + barGauge.queryOptions.withTargets([t.ClickHouseMetrics_MemoryTracking])
        + barGauge.panelOptions.withDescription('Percentage of memory allocated by ClickHouse compared to OS total')
        + barGauge.options.withOrientation('auto')
      ,

      activeConnectionsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Active connections',
          targets=[t.ClickHouseMetrics_TCPConnection, t.ClickHouseMetrics_HTTPConnection, t.ClickHouseMetrics_MySQLConnection, t.ClickHouseMetrics_PostgreSQLConnection],
          description='Current number of connections to ClickHouse'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls(false)
      ,

      networkReceivedPanel:
        commonlib.panels.network.timeSeries.traffic.new(
          'Network received',
          targets=[t.ClickHouseProfileEvents_NetworkReceiveBytes],
          description='Received network throughput'
        )
          + g.panel.timeSeries.standardOptions.withUnit('Bps')
      ,

      networkTransmittedPanel:
        commonlib.panels.network.timeSeries.traffic.new(
          'Network transmitted',
          targets=[t.ClickHouseProfileEvents_NetworkSendBytes],
          description='Transmitted network throughput'
        )
        + g.panel.timeSeries.standardOptions.withUnit('Bps')
      ,

      diskReadLatencyPanel:
        commonlib.panels.disk.timeSeries.ioWaitTime.new(
          'Disk read latency',
          targets=[t.ClickHouseProfileEvents_DiskReadElapsedMicroseconds],
          description='Time spent waiting for read syscall'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs')
      ,

      diskWriteLatencyPanel:
        commonlib.panels.disk.timeSeries.ioWaitTime.new(
          'Disk write latency',
          targets=[t.ClickHouseProfileEvents_DiskWriteElapsedMicroseconds],
          description='Time spent waiting for write syscall'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs')
      ,

      networkTransmitLatencyInboundPanel:
        commonlib.panels.disk.timeSeries.ioWaitTime.new(
          'Network receive latency',
          targets=[t.ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds],
          description='Latency of inbound network traffic'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs')
      ,

      networkTransmitLatencyOutboundPanel:
        commonlib.panels.disk.timeSeries.ioWaitTime.new(
          'Network transmit latency',
          targets=[t.ClickHouseProfileEvents_NetworkSendElapsedMicroseconds],
          description='Latency of outbound network traffic'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs')
      ,

      zooKeeperWaitTimePanel:
        commonlib.panels.disk.timeSeries.ioWaitTime.new(
          'ZooKeeper wait time',
          targets=[t.ClickHouseProfileEvents_ZooKeeperWaitMicroseconds],
          description='Time spent waiting for ZooKeeper request to process'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs')
      ,
    },
}
