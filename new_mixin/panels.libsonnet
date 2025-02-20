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

      diskReadLatencyPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Disk read latency',
          targets=[t.ClickHouseProfileEvents_DiskReadElapsedMicroseconds],
          description='Time spent waiting for read syscall')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      diskWriteLatencyPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Disk write latency',
          targets=[t.ClickHouseProfileEvents_DiskWriteElapsedMicroseconds],
          description='Time spent waiting for write syscall')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      networkTransmitLatencyInboundPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network receive latency',
          targets=[t.ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds],
          description='Latency of inbound network traffic')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      networkTransmitLatencyOutboundPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network transmit latency',
          targets=[t.ClickHouseProfileEvents_NetworkSendElapsedMicroseconds],
          description='Latency of outbound network traffic')
        + g.panel.timeSeries.standardOptions.withUnit('µs')
        + g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity(0)
        + g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('false')
,

      zooKeeperWaitTimePanel:
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