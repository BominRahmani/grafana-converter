local g = import './g.libsonnet';

// Use g.util.grid.wrapPanels() to import into custom dashboard
{
  new(panels): {
    row_1:
      [
        g.panel.row.new('Row 1'),
        panels.successfulQueriesPanel { gridPos+: { h: 8, w: 24, x: 0, y: 0 } },
      ],

    row_2:
      [
        g.panel.row.new('Row 2'),
        panels.failedQueriesPanel { gridPos+: { h: 8, w: 12, x: 0, y: 8 } },
        panels.rejectedInsertsPanel { gridPos+: { h: 8, w: 12, x: 12, y: 8 } },
      ],

    row_3:
      [
        g.panel.row.new('Row 3'),
        panels.memoryUsagePanel { gridPos+: { h: 8, w: 12, x: 0, y: 16 } },
        panels.memoryUsageGaugePanel { gridPos+: { h: 8, w: 12, x: 12, y: 16 } },
      ],

    row_4:
      [
        g.panel.row.new('Row 4'),
        panels.activeConnectionsPanel { gridPos+: { h: 8, w: 24, x: 0, y: 24 } },
      ],

    row_5:
      [
        g.panel.row.new('Row 5'),
        panels.networkReceivedPanel { gridPos+: { h: 8, w: 12, x: 0, y: 32 } },
        panels.networkTransmittedPanel { gridPos+: { h: 8, w: 12, x: 12, y: 32 } },
      ],

    row_6:
      [
        g.panel.row.new('Row 6'),
        panels.diskReadLatencyPanel { gridPos+: { h: 8, w: 12, x: 0, y: 0 } },
        panels.diskWriteLatencyPanel { gridPos+: { h: 8, w: 12, x: 12, y: 0 } },
      ],

    row_7:
      [
        g.panel.row.new('Row 7'),
        panels.networkTransmitLatencyInboundPanel { gridPos+: { h: 8, w: 12, x: 0, y: 8 } },
        panels.networkTransmitLatencyOutboundPanel { gridPos+: { h: 8, w: 12, x: 12, y: 8 } },
      ],

    row_8:
      [
        g.panel.row.new('Row 8'),
        panels.zooKeeperWaitTimePanel { gridPos+: { h: 8, w: 24, x: 0, y: 16 } },
      ],

  },
}
