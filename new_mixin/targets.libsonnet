local g = import './g.libsonnet';
local prometheusQuery = g.query.prometheus;
local commonlib = import 'common-lib/common/main.libsonnet';
local utils = commonlib.utils {
  labelsToPanelLegend(labels): std.join(' - ', ['{{%s}}' % [label] for label in labels]),
};

{
  new(this): {
    local vars = this.grafana.variables,
    local config = this.config,

    ClickHouseMetrics_InterserverConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_InterserverConnection{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - interserver connections' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseAsyncMetrics_ReplicasMaxQueueSize:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseAsyncMetrics_ReplicasMaxQueueSize{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - max queue size' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_ReplicatedPartFetches:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_ReplicatedPartFetches{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - part fetches' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_ReplicatedPartMerges:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_ReplicatedPartMerges{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - part merges' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_ReplicatedPartMutations:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_ReplicatedPartMutations{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - part mutations' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_ReplicatedPartChecks:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_ReplicatedPartChecks{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - part checks' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_ReadonlyReplica:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_ReadonlyReplica{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - read only' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_ZooKeeperWatch:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_ZooKeeperWatch{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - ZooKeeper watch' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_ZooKeeperSession:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_ZooKeeperSession{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - ZooKeeper session' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_ZooKeeperRequest:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_ZooKeeperRequest{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - ZooKeeper request' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_SelectQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_SelectQuery{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - select' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_InsertQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_InsertQuery{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - insert' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_AsyncInsertQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_AsyncInsertQuery{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - async insert' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_FailedSelectQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_FailedSelectQuery{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - failed select' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_FailedInsertQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_FailedInsertQuery{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - failed insert' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_RejectedInserts:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_RejectedInserts{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - rejected inserts' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_MemoryTracking:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        '(ClickHouseMetrics_MemoryTracking{%(queriesSelector)s})' % vars
      )
      + prometheusQuery.withLegendFormat('%s - memory tracking' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_TCPConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_TCPConnection{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - TCP' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_MemoryUsage:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        '(ClickHouseMetrics_MemoryTracking{%(queriesSelector)s} / ClickHouseAsyncMetrics_OSMemoryTotal{%(queriesSelector)s}) * 100' % vars
      )
      + prometheusQuery.withLegendFormat('%s - memory usage' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_HTTPConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_HTTPConnection{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - HTTP' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_MySQLConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_MySQLConnection{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - MySQL' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseMetrics_PostgreSQLConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_PostgreSQLConnection{%(queriesSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s - PostgreSQL' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_NetworkReceiveBytes:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_NetworkReceiveBytes{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - receive' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_NetworkSendBytes:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_NetworkSendBytes{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - send' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_DiskReadElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_DiskReadElapsedMicroseconds{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - read' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_DiskWriteElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_DiskWriteElapsedMicroseconds{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - write' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - receive' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_NetworkSendElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_NetworkSendElapsedMicroseconds{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - send' % utils.labelsToPanelLegend(config.instanceLabels)),

    ClickHouseProfileEvents_ZooKeeperWaitMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_ZooKeeperWaitMicroseconds{%(queriesSelector)s}[$__rate_interval])' % vars
      )
      + prometheusQuery.withLegendFormat('%s - ZooKeeper wait' % utils.labelsToPanelLegend(config.instanceLabels)),

  },
}
