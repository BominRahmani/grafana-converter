import json
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

class MixinConverter:
    """Converts old format Grafana mixin dashboards and panels to new format."""
    
    def __init__(self):
        self.panel_definitions = {}
        self.variables = []
        self.links = []
        self.panel_types = {
            'timeseries': 'timeSeries',
            'stat': 'stat',
            'gauge': 'barGauge',
            'table': 'table',
            'row': 'row',
            'piechart': 'pieChart',
            'alertlist': 'alertList',
            'linear': 'timeSeries',
            'prometheus': 'timeSeries'
        }

    def extract_panel_definitions(self, content: str) -> Dict[str, Any]:
        """
        Extracts panel definitions from the dashboard file content.
        Handles function-style panel definitions.
        """
        panels = {}
        
        # Find all local panel function definitions
        panel_matches = re.finditer(
            r'local\s+(\w+)\s*\(([^)]*)\)\s*=\s*({[^;]*});',
            content,
            re.DOTALL
        )
        
        for match in panel_matches:
            panel_name = match.group(1)
            params = match.group(2).strip()
            panel_body = match.group(3)
            
            try:
                # Store the raw panel definition
                panel_def = {
                    'params': params,
                    'body': panel_body  # Store the raw body, don't parse as JSON yet
                }
                panels[panel_name + 'Panel'] = panel_def
            except Exception as e:
                print(f"Warning: Could not parse panel {panel_name}: {e}")
        
        return panels

    def convert_panel_to_new_format(self, panel_name: str, panel_def: Dict[str, Any]) -> str:
        """
        Converts a panel definition to the new format.
        Returns a string with the converted panel definition.
        """
        raw_body = panel_def['body']
        
        # Extract title and description using regex
        title_match = re.search(r'title:\s*[\'"]([^\'"]*)[\'"]', raw_body)
        title = title_match.group(1) if title_match else ''
        
        desc_match = re.search(r'description:\s*[\'"]([^\'"]*)[\'"]', raw_body)
        description = desc_match.group(1) if desc_match else ''
        
        # Extract type
        type_match = re.search(r'type:\s*[\'"]([^\'"]*)[\'"]', raw_body)
        panel_type = type_match.group(1).lower() if type_match else 'timeseries'
        
        # Map the panel type using the panel_types dictionary
        panel_type = self.panel_types.get(panel_type, panel_type)
        
        # Extract targets
        targets = []
        target_matches = re.finditer(r'expr:\s*[\'"]([^\'"]*)[\'"]', raw_body)
        for match in target_matches:
            expr = match.group(1)
            metric_match = re.search(r'([A-Za-z_]+){', expr)
            if metric_match:
                metric_name = metric_match.group(1)
                targets.append(f"t.{metric_name}")

        # Start with the base panel definition
        if panel_type == 'timeSeries':  # Note: using the mapped type here
            panel_lines = [
                "commonlib.panels.generic.timeSeries.base.new(",
                f"  '{title}',",
                "  targets=[" + ", ".join(targets) + "]," if targets else "  targets=[],",
                f"  description='{description}'"
                ")"
            ]

            # Add field config options if present
            if 'unit:' in raw_body:
                unit_match = re.search(r'unit:\s*[\'"]([^\'"]*)[\'"]', raw_body)
                if unit_match:
                    panel_lines.append(f"+ g.panel.timeSeries.standardOptions.withUnit('{unit_match.group(1)}')")

            # Add fillOpacity if present
            fill_opacity_match = re.search(r'fillOpacity:\s*(\d+)', raw_body)
            if fill_opacity_match:
                panel_lines.append(
                    f"+ g.panel.timeSeries.fieldConfig.defaults.custom.withFillOpacity({fill_opacity_match.group(1)})"
                )

            # Add spanNulls if present
            span_nulls_match = re.search(r'spanNulls:\s*(true|false)', raw_body)
            if span_nulls_match:
                panel_lines.append(
                    f"+ g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls('{span_nulls_match.group(1)}')"
                )

            return '\n'.join(panel_lines)
        
        elif panel_type == 'gauge':
            panel_lines = [
                f"barGauge.new(title='{title}')",
                "+ barGauge.queryOptions.withTargets([" + 
                ", ".join(targets) + 
                "])" if targets else "+ barGauge.queryOptions.withTargets([])"
            ]
            
            if description:
                panel_lines.append(f"+ barGauge.panelOptions.withDescription('{description}')")

            # Add orientation if present
            orientation_match = re.search(r'orientation:\s*[\'"]([^\'"]*)[\'"]', raw_body)
            if orientation_match:
                panel_lines.append(f"+ barGauge.options.withOrientation('{orientation_match.group(1)}')")

            return '\n'.join(panel_lines)
        
        else:
            return f"// Unsupported panel type: {panel_type}"

    def generate_panels_file(self) -> str:
        """
        Generates the new format panels.libsonnet file content.
        """
        content = []
        # Add standard imports and header
        content.append("local g = import './g.libsonnet';")
        content.append("local commonlib = import 'common-lib/common/main.libsonnet';")
        content.append("local utils = commonlib.utils;")
        content.append("")
        content.append("{")
        content.append("  new(this)::")
        content.append("    {")
        
        # Add local variable definitions
        content.append("      local t = this.grafana.targets,")
        content.append("      local stat = g.panel.stat,")
        content.append("      local fieldOverride = g.panel.table.fieldOverride,")
        content.append("      local alertList = g.panel.alertList,")
        content.append("      local pieChart = g.panel.pieChart,")
        content.append("      local barGauge = g.panel.barGauge,")
        content.append("")
        
        # Add panel definitions
        for panel_name, panel_def in self.panel_definitions.items():
            # Convert the panel to new format
            panel_code = self.convert_panel_to_new_format(panel_name, panel_def)
            
            # Add the panel definition with proper indentation
            content.append(f"      {panel_name}:")
            for line in panel_code.split('\n'):
                content.append(f"        {line}")
            content.append(",")
            content.append("")
        
        # Close the structure
        content.append("    },")
        content.append("}")
        
        return '\n'.join(content)

    def generate_rows_file(self) -> str:
        """
        Generates the new format rows.libsonnet file content based on parsed dashboard layouts.
        """
        content = []
        # Add standard imports and header
        content.append("local g = import './g.libsonnet';")
        content.append("")
        content.append("// Use g.util.grid.wrapPanels() to import into custom dashboard")
        content.append("{")
        content.append("  new(panels): {")

        print("\nDebug: Starting generate_rows_file")
        print(f"Debug: Dashboard panels: {self.dashboard['panels']}")

        # Group panels by their y-coordinate to form rows
        panels_by_y = {}
        for panel in self.dashboard['panels']:
            print(f"\nDebug: Processing panel: {panel}")
            y_pos = panel['gridPos']['y']
            x_pos = panel['gridPos']['x']
            
            if y_pos not in panels_by_y:
                panels_by_y[y_pos] = []
            panels_by_y[y_pos].append((x_pos, panel))

        print(f"\nDebug: Panels by y: {panels_by_y}")

        # Sort rows by y-coordinate
        sorted_y = sorted(panels_by_y.keys())
        print(f"Debug: Sorted y coordinates: {sorted_y}")

        # Generate each row
        for i, y_pos in enumerate(sorted_y):
            row_panels = panels_by_y[y_pos]
            content.append(f"    row_{i + 1}:")
            content.append("      [")
            content.append(f"        g.panel.row.new('Row {i + 1}'),")
            
            # Sort panels within row by x-coordinate
            row_panels.sort(key=lambda p: p[0])  # Sort by x_pos
            
            # Add panels to row
            for _, panel in row_panels:
                grid_pos = panel['gridPos']
                grid_pos_str = f"{{ h: {grid_pos['h']}, w: {grid_pos['w']}, x: {grid_pos['x']}, y: {grid_pos['y']} }}"
                content.append(f"        panels.{panel['name']} {{ gridPos+: {grid_pos_str} }},")
            
            content.append("      ],")
            content.append("")

        # Close the structure
        content.append("  },")
        content.append("}")
        
        return '\n'.join(content)

    def extract_dashboard_structure(self, content: str) -> Dict[str, Any]:
        """
        Extracts the overall dashboard structure including panels layout.
        """
        dashboard = {
            'title': '',
            'panels': []
        }
        
        # Extract dashboard title
        title_match = re.search(r'dashboard\.new\(\s*\'([^\']+)\'', content)
        if title_match:
            dashboard['title'] = title_match.group(1)
            
        # Extract panel layout
        layout_match = re.search(r'\.addPanels\(\s*std\.flattenArrays\(\[(.*?)\]\)\s*\)', content, re.DOTALL)
        if layout_match:
            layout_content = layout_match.group(1)
            print("\nLayout content found:")
            print(layout_content)  # Debug print full layout content
            
            panels = []
            # Simpler pattern to match panel definitions
            panel_pattern = r'(\w+Panel).*?gridPos:\s*({[^}]+})'
            
            for match in re.finditer(panel_pattern, layout_content, re.DOTALL):
                panel_name = match.group(1)
                grid_pos_str = match.group(2).strip()
                
                # Convert gridPos string to dictionary
                grid_pos = {}
                x_match = re.search(r'x:\s*(\d+)', grid_pos_str)
                y_match = re.search(r'y:\s*(\d+)', grid_pos_str)
                w_match = re.search(r'w:\s*(\d+)', grid_pos_str)
                h_match = re.search(r'h:\s*(\d+)', grid_pos_str)
                
                if x_match: grid_pos['x'] = int(x_match.group(1))
                if y_match: grid_pos['y'] = int(y_match.group(1))
                if w_match: grid_pos['w'] = int(w_match.group(1))
                if h_match: grid_pos['h'] = int(h_match.group(1))
                
                print(f"\nMatched panel: {panel_name}")
                print(f"With gridPos: {grid_pos}")
                
                panel = {
                    'name': panel_name,
                    'gridPos': grid_pos
                }
                panels.append(panel)
            
            if not panels:
                print("\nNo panels matched! Check the regex pattern.")
            
            dashboard['panels'] = panels
            
        else:
            print("\nNo layout content found! Check the layout match pattern.")
            
        return dashboard

    def generate_dashboard_file(self, dashboard: Dict[str, Any]) -> str:
        """
        Generates the new format dashboard.libsonnet file content.
        """
        content = []
        content.append("local g = import './g.libsonnet';")
        content.append("local logslib = import 'logs-lib/logs/main.libsonnet';")
        content.append("{")
        content.append("  local root = self,")
        content.append("  new(this)::")
        content.append("    local prefix = this.config.dashboardNamePrefix;")
        content.append("    local links = this.grafana.links;")
        content.append("    local tags = this.config.dashboardTags;")
        content.append("    local uid = g.util.string.slugify(this.config.uid);")
        content.append("    local vars = this.grafana.variables;")
        content.append("    local annotations = this.grafana.annotations;")
        content.append("    local refresh = this.config.dashboardRefresh;")
        content.append("    local period = this.config.dashboardPeriod;")
        content.append("    local timezone = this.config.dashboardTimezone;")
        content.append("    local panels = this.grafana.panels;")
        content.append("")
        content.append("    {")
        content.append(f"      '{dashboard['title'].lower().replace(' ', '-')}.json':")
        content.append(f"        g.dashboard.new(prefix + ' {dashboard['title']}')")
        content.append("        + g.dashboard.withPanels(")
        content.append("          g.util.grid.wrapPanels(")
        content.append("            std.flattenArrays([")

        # Add all rows from the rows file
        num_rows = len(set(panel['gridPos'].get('y', 0) for panel in dashboard['panels']))
        for i in range(1, num_rows + 1):
            content.append(f"              this.grafana.rows.row_{i},")

        content.append("            ])")
        content.append("          )")
        content.append("        )")
        content.append("        + root.applyCommon(")
        content.append("          vars.singleInstance,")
        content.append("          uid,")
        content.append("          tags,")
        content.append("          links,")
        content.append("          annotations,")
        content.append("          timezone,")
        content.append("          refresh,")
        content.append("          period")
        content.append("        ),")
        content.append("    },")
        content.append("")
        # Add the applyCommon function
        content.append("  applyCommon(vars, uid, tags, links, annotations, timezone, refresh, period):")
        content.append("    g.dashboard.withTags(tags)")
        content.append("    + g.dashboard.withUid(uid)")
        content.append("    + g.dashboard.withLinks(std.objectValues(links))")
        content.append("    + g.dashboard.withTimezone(timezone)")
        content.append("    + g.dashboard.withRefresh(refresh)")
        content.append("    + g.dashboard.time.withFrom(period)")
        content.append("    + g.dashboard.withVariables(vars)")
        content.append("    + g.dashboard.withAnnotations(std.objectValues(annotations)),")
        content.append("}")
        
        return '\n'.join(content)

    def _clean_jsonnet(self, jsonnet: str) -> str:
        """
        Cleans Jsonnet code to make it valid JSON.
        """
        # Remove comments
        jsonnet = re.sub(r'//.*$', '', jsonnet, flags=re.MULTILINE)
        jsonnet = re.sub(r'/\*.*?\*/', '', jsonnet, flags=re.DOTALL)
        
        # Handle string concatenation and template strings
        jsonnet = re.sub(r"'\s*\+\s*'", '', jsonnet)
        
        # Handle variable interpolation
        jsonnet = re.sub(r'\$\{[^}]+\}', 'placeholder', jsonnet)
        jsonnet = re.sub(r'%\([^)]+\)s', 'placeholder', jsonnet)
        
        # Handle function calls and references
        jsonnet = re.sub(r'matcher', '"placeholder"', jsonnet)
        jsonnet = re.sub(r'promDatasource', '{"uid": "prometheus"}', jsonnet)
        
        # Handle expressions with +
        jsonnet = re.sub(r'\+[^{}\[\]]*$', '', jsonnet, flags=re.MULTILINE)
        
        # Fix object keys that don't have quotes
        jsonnet = re.sub(r'(\w+)(?=\s*:(?!\s*[{:]))', r'"\1"', jsonnet)
        
        # Remove trailing commas
        jsonnet = re.sub(r',(\s*[}\]])', r'\1', jsonnet)
        
        # Replace single quotes with double quotes
        jsonnet = re.sub(r"'([^']*)'", r'"\1"', jsonnet)
        
        return jsonnet

    def convert_mixin(self, input_dir: Path, output_dir: Path) -> None:
        """
        Converts all dashboard and panel definitions from old format to new format.
        """
        all_panels = {}
        
        for dashboard_file in input_dir.glob('*.libsonnet'):
            if dashboard_file.name != 'dashboards.libsonnet':
                print(f"Processing {dashboard_file.name}...")
                content = dashboard_file.read_text()
                
                # Extract panel definitions
                panel_matches = re.finditer(
                    r'local\s+(\w+)\s*\(([^)]*)\)\s*=\s*({[^;]*});',
                    content,
                    re.DOTALL
                )
                
                for match in panel_matches:
                    panel_name = match.group(1)
                    params = match.group(2)
                    panel_body = match.group(3)
                    
                    try:
                        panel_def = {
                            'params': params,
                            'body': panel_body
                        }
                        all_panels[panel_name] = panel_def
                        print(f"Found panel: {panel_name}")
                    except Exception as e:
                        print(f"Warning: Could not parse panel {panel_name}: {e}")
                
                # Store the panels in the converter instance
                self.panel_definitions.update(all_panels)
                
                # Extract dashboard structure and store it
                self.dashboard = self.extract_dashboard_structure(content)
                
                # Generate dashboard file
                dashboard_output = output_dir / f"dashboard_{dashboard_file.stem}.libsonnet"
                dashboard_output.write_text(self.generate_dashboard_file(self.dashboard))
        
        # Generate panels file
        print(f"Found {len(self.panel_definitions)} panels")
        panels_file = output_dir / 'panels.libsonnet'
        panels_file.write_text(self.generate_panels_file())

        # Generate rows file
        rows_file = output_dir / 'rows.libsonnet'
        rows_file.write_text(self.generate_rows_file())

def main():
    """
    Main function to run the converter.
    """
    input_dir = Path('dashboards')
    output_dir = Path('new_mixin')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    converter = MixinConverter()
    converter.convert_mixin(input_dir, output_dir)
    print("Conversion complete!")

if __name__ == '__main__':
    main()