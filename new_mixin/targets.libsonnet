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
    local testNameLabel = config.testNameLabel,
    local nodeNameLabel = config.nodeNameLabel,

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