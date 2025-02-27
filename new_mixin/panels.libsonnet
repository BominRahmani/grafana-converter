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

      interserverConnectionsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Interserver connections',
          targets=[t.ClickHouseMetrics_InterserverConnection],
          description='Number of connections due to interserver communication'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
      ,

      replicaQueueSizePanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Replica queue size',
          targets=[t.ClickHouseAsyncMetrics_ReplicasMaxQueueSize],
          description='Number of replica tasks in queue'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
      ,

      replicaOperationsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Replica operations',
          targets=[t.ClickHouseProfileEvents_ReplicatedPartFetches, t.ClickHouseProfileEvents_ReplicatedPartMerges, t.ClickHouseProfileEvents_ReplicatedPartMutations, t.ClickHouseProfileEvents_ReplicatedPartChecks],
          description='Replica Operations over time to other nodes'
        )
        + g.panel.timeSeries.standardOptions.withUnit('ops')
      ,

      replicaReadOnlyPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Replica read only',
          targets=[t.ClickHouseMetrics_ReadonlyReplica],
          description='Shows replicas in read-only state over time'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
      ,

      zooKeeperWatchesPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Zookeeper watches',
          targets=[t.ClickHouseMetrics_ZooKeeperWatch],
          description='Current number of watches in ZooKeeper'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
      ,

      zooKeeperSessionsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Zookeeper sessions',
          targets=[t.ClickHouseMetrics_ZooKeeperSession],
          description='Current number of sessions to ZooKeeper'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
      ,

      zooKeeperRequestsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Zookeeper requests',
          targets=[t.ClickHouseMetrics_ZooKeeperRequest],
          description='Current number of active requests to ZooKeeper'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
      ,

      successfulQueriesPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Successful queries',
          targets=[t.ClickHouseProfileEvents_SelectQuery, t.ClickHouseProfileEvents_InsertQuery, t.ClickHouseProfileEvents_AsyncInsertQuery],
          description='Rate of successful queries per second'
        )
        + g.panel.timeSeries.standardOptions.withUnit('ops')
      ,

      failedQueriesPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Failed queries',
          targets=[t.ClickHouseProfileEvents_FailedSelectQuery, t.ClickHouseProfileEvents_FailedInsertQuery],
          description='Rate of failed queries per second'
        )
        + g.panel.timeSeries.standardOptions.withUnit('ops')
      ,

      rejectedInsertsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Rejected inserts',
          targets=[t.ClickHouseProfileEvents_RejectedInserts],
          description='Number of rejected inserts per second'
        )
        + g.panel.timeSeries.standardOptions.withUnit('ops')
      ,

      memoryUsagePanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Memory usage',
          targets=[t.ClickHouseMetrics_MemoryTracking],
          description='Memory usage over time'
        )
        + g.panel.timeSeries.standardOptions.withUnit('decbytes')
      ,

      memoryUsageGaugePanel:
        g.panel.gauge.new('Memory usage')
        + g.panel.gauge.queryOptions.withTargets([t.ClickHouseMetrics_MemoryUsageGauge])
        + g.panel.gauge.panelOptions.withDescription('Percentage of memory allocated by ClickHouse compared to OS total')
        + g.panel.gauge.standardOptions.withUnit('percent')
        + g.panel.gauge.standardOptions.withMin(0)
        + g.panel.gauge.standardOptions.withMax(100)
        + g.panel.gauge.standardOptions.thresholds.withMode('percentage')
        + g.panel.gauge.standardOptions.thresholds.withSteps([
          g.panel.gauge.standardOptions.threshold.step.withColor('green')
          + g.panel.gauge.standardOptions.threshold.step.withValue(null),
          g.panel.gauge.standardOptions.threshold.step.withColor('#EAB839')  // Yellow
          + g.panel.gauge.standardOptions.threshold.step.withValue(80),
          g.panel.gauge.standardOptions.threshold.step.withColor('red')
          + g.panel.gauge.standardOptions.threshold.step.withValue(90),
        ])
        + g.panel.gauge.options.withShowThresholdLabels(true)
        + g.panel.gauge.options.withShowThresholdMarkers(true)
        + g.panel.gauge.options.reduceOptions.withCalcs(['lastNotNull']),

      activeConnectionsPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Active connections',
          targets=[t.ClickHouseMetrics_TCPConnection, t.ClickHouseMetrics_HTTPConnection, t.ClickHouseMetrics_MySQLConnection, t.ClickHouseMetrics_PostgreSQLConnection],
          description='Current number of connections to ClickHouse'
        )
        + g.panel.timeSeries.standardOptions.withUnit('none')
      ,

      networkReceivedPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network received',
          targets=[t.ClickHouseProfileEvents_NetworkReceiveBytes],
          description='Received network throughput'
        )
        + g.panel.timeSeries.standardOptions.withUnit('Bps')
      ,

      networkTransmittedPanel:
        commonlib.panels.generic.timeSeries.base.new(
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
        commonlib.panels.generic.timeSeries.base.new(
          'Network receive latency',
          targets=[t.ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds],
          description='Latency of inbound network traffic'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs')
      ,

      networkTransmitLatencyOutboundPanel:
        commonlib.panels.generic.timeSeries.base.new(
          'Network transmit latency',
          targets=[t.ClickHouseProfileEvents_NetworkSendElapsedMicroseconds],
          description='Latency of outbound network traffic'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs')
      ,

      zooKeeperWaitTimePanel:
        commonlib.panels.generic.timeSeries.base.new(
          'ZooKeeper wait time',
          targets=[t.ClickHouseProfileEvents_ZooKeeperWaitMicroseconds],
          description='Time spent waiting for ZooKeeper request to process'
        )
        + g.panel.timeSeries.standardOptions.withUnit('µs'),

    },
}
