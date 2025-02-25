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
    // Add default values if these labels don't exist in config
    local testNameLabel = if std.objectHas(config, 'testNameLabel') then config.testNameLabel else ['test'],
    local nodeNameLabel = if std.objectHas(config, 'nodeNameLabel') then config.nodeNameLabel else ['node'],

    ClickHouseProfileEvents_SelectQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_SelectQuery{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_InsertQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_InsertQuery{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_AsyncInsertQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_AsyncInsertQuery{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_FailedSelectQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_FailedSelectQuery{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_FailedInsertQuery:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_FailedInsertQuery{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_RejectedInserts:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_RejectedInserts{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseMetrics_MemoryTracking:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        '(ClickHouseMetrics_MemoryTracking{%(testNameSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseMetrics_TCPConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_TCPConnection{%(testNameSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseMetrics_HTTPConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_HTTPConnection{%(testNameSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseMetrics_MySQLConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_MySQLConnection{%(testNameSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseMetrics_PostgreSQLConnection:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'ClickHouseMetrics_PostgreSQLConnection{%(testNameSelector)s}' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_NetworkReceiveBytes:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_NetworkReceiveBytes{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_NetworkSendBytes:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'rate(ClickHouseProfileEvents_NetworkSendBytes{%(testNameSelector)s}[$__rate_interval]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_DiskReadElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_DiskReadElapsedMicroseconds{%(testNameSelector)s}[$__interval:]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_DiskWriteElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_DiskWriteElapsedMicroseconds{%(testNameSelector)s}[$__interval:]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds{%(testNameSelector)s}[$__interval:]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_NetworkSendElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_NetworkSendElapsedMicroseconds{%(testNameSelector)s}[$__interval:]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

    ClickHouseProfileEvents_ZooKeeperWaitMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_ZooKeeperWaitMicroseconds{%(testNameSelector)s}[$__interval:]' % vars
      )
      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(testNameLabel)),

  },
}