local g = import './g.libsonnet';
local prometheusQuery = g.query.prometheus;

{
  new(this): {
    local vars = this.grafana.variables,

    ClickHouseProfileEvents_DiskReadElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_DiskReadElapsedMicroseconds{'
      )
      + prometheusQuery.withLegendFormat('{{ instance }} - disk read elapsed'),

    ClickHouseProfileEvents_DiskWriteElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_DiskWriteElapsedMicroseconds{'
      )
      + prometheusQuery.withLegendFormat('{{ instance }} - disk write elapsed'),

    ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_NetworkReceiveElapsedMicroseconds{'
      )
      + prometheusQuery.withLegendFormat('{{ instance }} - network receive elapsed'),

    ClickHouseProfileEvents_NetworkSendElapsedMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_NetworkSendElapsedMicroseconds{'
      )
      + prometheusQuery.withLegendFormat('{{ instance }} - network send elapsed'),

    ClickHouseProfileEvents_ZooKeeperWaitMicroseconds:
      prometheusQuery.new(
        '${' + vars.datasources.prometheus.name + '}',
        'increase(ClickHouseProfileEvents_ZooKeeperWaitMicroseconds{'
      )
      + prometheusQuery.withLegendFormat('{{ instance }} - ZooKeeper wait'),

  },
}