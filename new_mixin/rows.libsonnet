local g = import './g.libsonnet';

// Use g.util.grid.wrapPanels() to import into custom dashboard
{
  new(panels): {
    row_1:
      [
        g.panel.row.new('Row 1'),
        panels.diskReadLatencyPanel { gridPos+: { h: 8, w: 12, x: 0, y: 0 } },
        panels.diskWriteLatencyPanel { gridPos+: { h: 8, w: 12, x: 12, y: 0 } },
      ],

    row_2:
      [
        g.panel.row.new('Row 2'),
        panels.networkTransmitLatencyInboundPanel { gridPos+: { h: 8, w: 12, x: 0, y: 8 } },
        panels.networkTransmitLatencyOutboundPanel { gridPos+: { h: 8, w: 12, x: 12, y: 8 } },
      ],

    row_3:
      [
        g.panel.row.new('Row 3'),
        panels.zooKeeperWaitTimePanel { gridPos+: { h: 8, w: 24, x: 0, y: 16 } },
      ],

  },
}