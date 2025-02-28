{
  // any modular library should include as inputs:
  // 'dashboardNamePrefix' - Use as prefix for all Dashboards and (optional) rule groups
  // 'filteringSelector' - Static selector to apply to ALL dashboard variables of type query, panel queries, alerts and recording rules.
  // 'groupLabels' - one or more labels that can be used to identify 'group' of instances. In simple cases, can be 'job' or 'cluster'.
  // 'instanceLabels' - one or more labels that can be used to identify single entity of instances. In simple cases, can be 'instance' or 'pod'.
  // 'uid' - UID to prefix all dashboards original uids

  enableMultiCluster: false,
  filteringSelector: 'job=~".*/clickhouse.*"',
  groupLabels: if self.enableMultiCluster then ['job', 'cluster'] else ['job'],
  instanceLabels: ['instance'],
  dashboardTags: ['clickhouse-mixin'],
  uid: 'clickhouse',
  dashboardNamePrefix: '',

  // additional params
  dashboardPeriod: 'now-30m',
  dashboardTimezone: 'default',
  dashboardRefresh: '1m',

  // alert thresholds
  alertsReplicasMaxQueueSize: '99',

  // logs lib related
  enableLokiLogs: true,
  logLabels: if self.enableMultiCluster then ['job', 'instance', 'cluster', 'level'] else ['job', 'instance', 'level'],
  extraLogLabels: [],  // Required by logs-lib
  logsVolumeGroupBy: 'level',
  showLogsVolume: true,
}
