import json
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

## How unfortunate is this, why do i torture myself???
## Laugh and the world laughs with you, weep and you weep alone.
## I dedicate this converter to my extrememe distaste in Grafana, all that is and all that will be.

class MixinConverter:
    
    def __init__(self):
        self.panel_definitions = {}
        self.variables = []
        self.links = []
        self.dashboards = []
        self.panel_types = {
            'timeseries': 'timeSeries',
            'stat': 'stat',
            'gauge': 'gauge', ## i dont understand why this shit doesn't work, TODO fix this later
            'table': 'table', ## hahahah this DEFINITELY does not work right now, TODO fix this later
            'row': 'row',
            'piechart': 'pieChart',
            'alertlist': 'alertList',
            'linear': 'timeSeries',
            'prometheus': 'timeSeries'
        }
        ## lol we do this so we can remember a metric that we will later use in the variables.libsonnet, 
        ## why?? because vitaly thats why
        self.example_metric = None 

    ## we create a dictionary of the panels to try to mimick whats going on behind the scenes in the old format.
    def extract_panel_definitions(self, content: str) -> Dict[str, Any]:
        panels = {}
        
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
                panel_def = {
                    'params': params,
                    'body': panel_body
                }
                # Remove the 'Panel' suffix if it's already in the name
                if panel_name.endswith('Panel'):
                    panels[panel_name] = panel_def
                else:
                    panels[panel_name + 'Panel'] = panel_def
            except Exception as e:
                print(f"Warning: Could not parse panel {panel_name}: {e}")
        
        return panels

    def convert_panel_to_new_format(self, panel_name: str, panel_def: Dict[str, Any]) -> str:
        raw_body = panel_def['body']
        
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
                f"  description='{description}'",
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
                    f"+ g.panel.timeSeries.fieldConfig.defaults.custom.withSpanNulls({span_nulls_match.group(1)})"
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
        
        # Keep track of total rows across all dashboards
        total_rows = 0
        
        # Process each dashboard
        for dashboard in self.dashboards:
            print(f"Debug: Processing dashboard: {dashboard}")
            if 'panels' in dashboard:
                # Group panels by their y-coordinate to form rows
                panels_by_y = {}
                for panel in dashboard['panels']:
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
                for y_pos in sorted_y:
                    total_rows += 1  # Increment total rows counter
                    row_panels = panels_by_y[y_pos]
                    content.append(f"    row_{total_rows}:")
                    content.append("      [")
                    content.append(f"        g.panel.row.new('Row {total_rows}'),")
                    
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

    def _create_link_name(self, name: str) -> str:
        """
        Standardized method to create link names from dashboard names/titles.
        Used by both dashboard and links generation.
        """
        # Remove .json extension if present
        name = name.replace('.json', '')
        # Replace both spaces and dashes with underscores
        words = name.replace(' ', '_').replace('-', '_').split('_')
        # Convert to camelCase
        return words[0].lower() + ''.join(word.title() for word in words[1:])

    def generate_dashboard_file(self, dashboards: List[Dict[str, Any]]) -> str:
        """
        Generates the new format dashboard.libsonnet file content combining all dashboards.
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

        # Add each dashboard
        for dashboard in dashboards:
            # Get the dashboard title
            title = dashboard['title']
            
            # Create full dashboard ID that preserves the mixin name
            # Convert to lowercase and replace spaces with underscores
            dashboard_id = title.lower().replace(' ', '_').replace('-', '_')
            
            # Create link name using standardized method
            base_link_name = self._create_link_name(title)
            
            content.append(f"      {dashboard_id}:")
            content.append(f"        g.dashboard.new(prefix + ' {title}')")
            content.append("        + g.dashboard.withPanels(")
            content.append("          g.util.grid.wrapPanels(")
            content.append("            [")

            # Add panels for this dashboard
            for panel in dashboard['panels']:
                grid_pos = panel.get('gridPos', {})
                # Use the panel name as is, without adding 'Panel' suffix
                content.append(f"              panels.{panel['name']} {{ gridPos+: {{ h: {grid_pos.get('h', 8)}, w: {grid_pos.get('w', 12)}, x: {grid_pos.get('x', 0)}, y: {grid_pos.get('y', 0)} }} }},")

            content.append("            ]")
            content.append("          )")
            content.append("        )")
            content.append("        + root.applyCommon(")
            content.append("          vars.singleInstance,")
            content.append(f"          uid + '_{dashboard_id}',")
            content.append("          tags,")
            content.append(f"          links {{ {base_link_name}+:: {{}} }},")
            content.append("          annotations,")
            content.append("          timezone,")
            content.append("          refresh,")
            content.append("          period")
            content.append("        ),")
            content.append("")

            # Store the full dashboard_id for use in links generation
            self.dashboard_names.append(f"{dashboard_id}.json")

        # Add the logs dashboard section
        content.append("    }")
        content.append("    +")
        content.append("    if this.config.enableLokiLogs then")
        content.append("      {")
        content.append("        logs:")
        content.append("          logslib.new(")
        content.append("            prefix + ' logs',")
        content.append("            datasourceName=this.grafana.variables.datasources.loki.name,")
        content.append("            datasourceRegex=this.grafana.variables.datasources.loki.regex,")
        content.append("            filterSelector=this.config.filteringSelector,")
        content.append("            labels=this.config.groupLabels + this.config.extraLogLabels,")
        content.append("            formatParser=null,")
        content.append("            showLogsVolume=this.config.showLogsVolume,")
        content.append("          )")
        content.append("          {")
        content.append("            dashboards+:")
        content.append("              {")
        content.append("                logs+:")
        content.append("                  // reference to self, already generated variables, to keep them, but apply other common data in applyCommon")
        content.append("                  root.applyCommon(super.logs.templating.list, uid=uid + '-logs', tags=tags, links=links { logs+:: {} }, annotations=annotations, timezone=timezone, refresh=refresh, period=period),")
        content.append("              },")
        content.append("            panels+:")
        content.append("              {")
        content.append("                // modify log panel")
        content.append("                logs+:")
        content.append("                  g.panel.logs.options.withEnableLogDetails(true)")
        content.append("                  + g.panel.logs.options.withShowTime(false)")
        content.append("                  + g.panel.logs.options.withWrapLogMessage(false),")
        content.append("              },")
        content.append("            variables+: {")
        content.append("              // add prometheus datasource for annotations processing")
        content.append("              toArray+: [")
        content.append("                this.grafana.variables.datasources.prometheus { hide: 2 },")
        content.append("              ],")
        content.append("            },")
        content.append("          }.dashboards.logs,")
        content.append("      }")
        content.append("    else {},")

        # Add the applyCommon function
        content.append("")
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

    def generate_g_file(self) -> str:
        """
        Generates the g.libsonnet file content that imports grafonnet.
        """
        return 'import \'github.com/grafana/grafonnet/gen/grafonnet-v11.0.0/main.libsonnet\''

    def extract_queries(self, content: str) -> Dict[str, Any]:
        """
        Extracts Prometheus queries from dashboard panels.
        Returns a dictionary of query definitions.
        """
        queries = {}
        
        # Find all expr definitions in panels
        expr_matches = re.finditer(
            r'expr:\s*[\'"]([^\'"]*)[\'"].*?legendFormat:\s*[\'"]([^\'"]*)[\'"]',
            content,
            re.DOTALL
        )
        
        for match in expr_matches:
            expr = match.group(1)
            legend = match.group(2)
            
            # Generate a query name based on the metric or pattern
            metric_match = re.search(r'([A-Za-z_]+){', expr)
            if metric_match:
                metric_name = metric_match.group(1)
                # Store the first metric name we find as an example
                if self.example_metric is None:
                    self.example_metric = metric_name
                
                query_name = f"{metric_name}"
                queries[query_name] = {
                    'expr': expr,
                    'legend': legend
                }
        
        return queries

    def generate_targets_file(self) -> str:
        """
        Generates the new format targets.libsonnet file content.
        """
        content = []
        # Add standard imports
        content.append("local g = import './g.libsonnet';")
        content.append("local prometheusQuery = g.query.prometheus;")
        content.append("local commonlib = import 'common-lib/common/main.libsonnet';")
        content.append("local utils = commonlib.utils {")
        content.append("  labelsToPanelLegend(labels): std.join(' - ', ['{{%s}}' % [label] for label in labels]),")
        content.append("};")
        content.append("")
        content.append("{")
        content.append("  new(this): {")
        content.append("    local vars = this.grafana.variables,")
        content.append("    local config = this.config,")
        
        # Add selector variables
        if hasattr(self, 'selector_patterns') and self.selector_patterns:
            main_selector = next((name for name in self.selector_patterns.keys() 
                                 if name.lower() != 'filterselector'), None)
            if main_selector:
                content.append(f"    // Main selector from old config: {main_selector}")
                content.append(f"    local selectorVar = vars.{main_selector},")
        else:
            content.append("    // Add default values if these labels don't exist in config")
            content.append("    local testNameLabel = if std.objectHas(config, 'testNameLabel') then config.testNameLabel else ['test'],")
            content.append("    local nodeNameLabel = if std.objectHas(config, 'nodeNameLabel') then config.nodeNameLabel else ['node'],")
        
        content.append("")
        
        # Add query definitions with improved selector handling
        for query_name, query_def in self.queries.items():
            expr = query_def['expr']
            legend = query_def.get('legend', '')
            
            # Determine which selector to use
            selector_var = None
            if hasattr(self, 'selector_patterns') and self.selector_patterns:
                # Try to find which selector pattern is used in this query
                used_selector = None
                for selector_name, selector_pattern in self.selector_patterns.items():
                    # Check if this selector pattern appears in the expression
                    if selector_pattern in expr:
                        used_selector = selector_name
                        break
                
                # If we found a matching selector, use it
                if used_selector:
                    # Replace the old selector pattern with the new variable reference
                    selector_var = f"%({used_selector})s"
                    expr = expr.replace('{' + selector_pattern + '}', '{' + selector_var + '}')
                else:
                    # Default to testNameSelector or nodeNameSelector based on content
                    if 'node_name' in expr:
                        selector_var = '%(nodeNameSelector)s'
                    else:
                        selector_var = '%(testNameSelector)s'
                
                # Apply the selector
                if '{' in expr and '}' in expr:
                    # Replace existing selector
                    expr = re.sub(r'{[^}]*}', '{' + selector_var + '}', expr)
                elif '{' in expr:
                    # Complete incomplete selector
                    expr = expr.replace('{', '{' + selector_var + '}')
            else:
                # Use the existing logic for determining selectors
                if 'node_name' in expr:
                    selector_var = '%(nodeNameSelector)s'
                    legend_label = 'nodeNameLabel'
                else:
                    selector_var = '%(testNameSelector)s'
                    legend_label = 'testNameLabel'
            
            # Ensure all queries have a selector
            if '{' not in expr:
                # If there's no selector at all, add one
                metric_match = re.search(r'^([A-Za-z0-9_]+)', expr)
                if metric_match:
                    metric_name = metric_match.group(1)
                    expr = expr.replace(metric_name, f"{metric_name}{{{selector_var}}}")
            elif '{' in expr and '}' not in expr:
                # If the selector is incomplete, complete it properly
                expr = expr.replace('{', '{' + selector_var + '}')
            elif '{' in expr and '}' in expr and '{}' in expr:
                # If there's an empty selector, add the appropriate one
                expr = expr.replace('{}', '{' + selector_var + '}')
            
            # Fix time intervals and other issues
            # Ensure the query has proper closing braces
            if expr.count('{') > expr.count('}'):
                expr += '}'  # Add closing brace if missing
            
            # Add time range for rate/increase functions if not present
            # IMPORTANT: Make sure the time interval is placed AFTER the closing curly brace, not inside the selector
            if any(func in expr for func in ['rate(', 'increase(', 'irate(']) and not any(interval in expr for interval in ['[$__interval]', '[$__rate_interval]']):
                # Find the position of the closing curly brace after the metric name
                metric_match = re.search(r'(rate|increase|irate)\(([A-Za-z0-9_]+){[^}]*}', expr)
                if metric_match:
                    # Insert the time interval after the closing curly brace
                    expr_parts = expr.split('}', 1)
                    if len(expr_parts) > 1:
                        expr = expr_parts[0] + '}[$__rate_interval]' + expr_parts[1]
                    else:
                        # If we can't split properly, add to the end before the last parenthesis
                        last_paren_index = expr.rfind(')')
                        if last_paren_index != -1:
                            expr = expr[:last_paren_index] + '[$__rate_interval]' + expr[last_paren_index:]
            
            # Ensure all opening parentheses have matching closing parentheses
            open_count = expr.count('(')
            close_count = expr.count(')')
            if open_count > close_count:
                expr += ')' * (open_count - close_count)
            
            content.append(f"    {query_name}:")
            content.append("      prometheusQuery.new(")
            content.append("        '${' + vars.datasources.prometheus.name + '}',")
            content.append(f"        '{expr}' % vars")
            content.append("      )")
            
            # Add legend format if present
            if legend:
                if hasattr(self, 'selector_patterns') and self.selector_patterns:
                    content.append("      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend(config.groupLabels + config.instanceLabels)),")
                else:
                    content.append(f"      + prometheusQuery.withLegendFormat('%s' % utils.labelsToPanelLegend({legend_label})),")
            else:
                content.append("      ,")
            content.append("")
        
        # Close the structure
        content.append("  },")
        content.append("}")
        
        return '\n'.join(content)

    def generate_variables_file(self) -> str:
        """
        Generates the new format variables.libsonnet file content.
        """
        content = []
        # Add standard imports
        content.append("local g = import './g.libsonnet';")
        content.append("local var = g.dashboard.variable;")
        content.append("local commonlib = import 'common-lib/common/main.libsonnet';")
        content.append("local utils = commonlib.utils;")
        content.append("")
        content.append("// Generates chained variables to use on all dashboards")
        content.append("{")
        content.append("  new(this, varMetric):")
        content.append("    {")
        content.append("      local filteringSelector = this.config.filteringSelector,")
        content.append("      local groupLabels = this.config.groupLabels,")
        content.append("      local instanceLabels = this.config.instanceLabels,")
        content.append("      local nodeNameLabel = if std.objectHas(this.config, 'nodeNameLabel') then this.config.nodeNameLabel else ['node'],")
        content.append("      local testNameLabel = if std.objectHas(this.config, 'testNameLabel') then this.config.testNameLabel else ['test'],")
        content.append("")
        content.append("      local root = self,")
        
        # Add variable generation function
        content.append("      local variablesFromLabels(groupLabels, instanceLabels, filteringSelector, multiInstance=true) =")
        content.append("        local chainVarProto(index, chainVar) =")
        content.append("          var.query.new(chainVar.label)")
        content.append("          + var.query.withDatasourceFromVariable(root.datasources.prometheus)")
        content.append("          + var.query.queryTypes.withLabelValues(")
        content.append("            chainVar.label,")
        content.append("            '%s{%s}' % [varMetric, chainVar.chainSelector],")
        content.append("          )")
        content.append("          + var.query.generalOptions.withLabel(utils.toSentenceCase(chainVar.label))")
        content.append("          + var.query.selectionOptions.withIncludeAll(")
        content.append("            value=true,")
        content.append("            customAllValue='.+'")
        content.append("          )")
        content.append("          + var.query.selectionOptions.withMulti(true)")
        content.append("          + var.query.refresh.onTime()")
        content.append("          + var.query.withSort(")
        content.append("            i=1,")
        content.append("            type='alphabetical',")
        content.append("            asc=true,")
        content.append("            caseInsensitive=false")
        content.append("          );")
        content.append("        std.mapWithIndex(chainVarProto, utils.chainLabels(groupLabels + instanceLabels, [filteringSelector])),")
        
        # Add datasource definition with both Prometheus and Loki
        content.append("      datasources: {")
        content.append("        prometheus:")
        content.append("          var.datasource.new('prometheus_datasource', 'prometheus')")
        content.append("          + var.datasource.generalOptions.withLabel('Prometheus data source')")
        content.append("          + var.datasource.withRegex(''),")
        content.append("        loki:")
        content.append("          var.datasource.new('loki_datasource', 'loki')")
        content.append("          + var.datasource.generalOptions.withLabel('Loki data source')")
        content.append("          + var.datasource.withRegex(''),")
        content.append("      },")
        content.append("")
        
        # Add variable sets
        content.append("      multiInstance:")
        content.append("        [root.datasources.prometheus]")
        content.append("        + variablesFromLabels(groupLabels, instanceLabels, filteringSelector),")
        content.append("")
        content.append("      singleInstance:")
        content.append("        [root.datasources.prometheus]")
        content.append("        + variablesFromLabels(groupLabels, instanceLabels, filteringSelector, multiInstance=false),")
        content.append("")
        content.append("      overviewVariables:")
        content.append("        [root.datasources.prometheus]")
        content.append("        + variablesFromLabels(groupLabels, instanceLabels + testNameLabel, filteringSelector, multiInstance=true),")
        content.append("")
        
        # Add selector definitions
        content.append("      queriesSelector:")
        content.append("        '%s' % [")
        content.append("          utils.labelsToPromQLSelector(groupLabels),")
        content.append("        ],")
        content.append("")
        content.append("      testNameSelector:")
        content.append("        '%s' % [")
        content.append("          utils.labelsToPromQLSelector(groupLabels + instanceLabels + testNameLabel),")
        content.append("        ],")
        content.append("")
        content.append("      nodeNameSelector:")
        content.append("        '%s' % [")
        content.append("          utils.labelsToPromQLSelector(groupLabels + instanceLabels + nodeNameLabel),")
        content.append("        ],")
        content.append("")
        
        # Add legacy selector compatibility
        if hasattr(self, 'selector_patterns') and self.selector_patterns:
            content.append("")
            content.append("      // Legacy selector compatibility")
            for selector_name, selector_pattern in self.selector_patterns.items():
                # Convert the old selector pattern to a new format reference
                if 'job' in selector_pattern and 'instance' in selector_pattern:
                    if 'cluster' in selector_pattern:
                        content.append(f"      {selector_name}:")
                        content.append("        utils.labelsToPromQLSelector(groupLabels + instanceLabels),")
                    else:
                        content.append(f"      {selector_name}:")
                        content.append("        utils.labelsToPromQLSelector(groupLabels + instanceLabels),")
                else:
                    # For custom selectors, keep the original pattern but reference it through variables
                    content.append(f"      {selector_name}: '{selector_pattern}',")
        
        content.append("    },")
        content.append("}")
        
        return '\n'.join(content)

    def generate_links_file(self) -> str:
        """
        Generates the new format links.libsonnet file content.
        """
        content = []
        # Add standard imports
        content.append("local g = import './g.libsonnet';")
        content.append("{")
        content.append("  local link = g.dashboard.link,")
        content.append("  new(this):")
        content.append("    {")
        
        # Track link names to avoid duplicates
        used_link_names = set()
        
        # Add regular dashboard links and "back to" links for each dashboard
        for dashboard_name in self.dashboard_names:
            # Use standardized method for link names
            link_name = self._create_link_name(dashboard_name)
            
            # Skip if we've already created this link
            if link_name in used_link_names:
                continue
            
            used_link_names.add(link_name)
            
            # First replace hyphens with underscores, then split by underscores
            clean_name = dashboard_name.replace('.json', '').replace('-', '_')
            display_name = ' '.join(word.title() for word in clean_name.split('_'))
            
            # Convert dashboard_name to a property name (remove .json, replace hyphens with underscores)
            dashboard_prop = dashboard_name.replace('.json', '').replace('-', '_')
            
            # Regular dashboard link - using property access notation
            content.append(f"      {link_name}:")
            content.append(f"        link.link.new('{display_name}', '/d/' + this.grafana.dashboards.{dashboard_prop}.uid)")
            content.append("        + link.link.options.withKeepTime(true),")
            content.append("")
            
            # Back to link - using property access notation
            content.append(f"      backTo{link_name[0].upper() + link_name[1:]}:")
            content.append(f"        link.link.new('Back to {display_name}', '/d/' + this.grafana.dashboards.{dashboard_prop}.uid)")
            content.append("        + link.link.options.withKeepTime(true),")
            content.append("")

        # Add the "All dashboards" dropdown link
        content.append("      otherDashboards:")
        content.append("        link.dashboards.new('All dashboards', this.config.dashboardTags)")
        content.append("        + link.dashboards.options.withIncludeVars(true)")
        content.append("        + link.dashboards.options.withKeepTime(true)")
        content.append("        + link.dashboards.options.withAsDropdown(true),")
        
        # Add the conditional logs link
        content.append("    }")
        content.append("    +")
        content.append("    if this.config.enableLokiLogs then")
        content.append("      {")
        content.append("        logs:")
        content.append("          link.link.new('Logs', '/d/' + this.grafana.dashboards.logs.uid)")
        content.append("          + link.link.options.withKeepTime(true),")
        content.append("      }")
        content.append("    else {},")
        content.append("}")
        
        return '\n'.join(content)

    def convert_config_file(self, content: str) -> str:
        """
        Converts old format config.libsonnet to new format.
        """
        # Extract selector patterns first
        self.selector_patterns = self.extract_selector_patterns(content)
        
        # Start with standard config structure
        new_config = [
            "{",
            "  // any modular library should include as inputs:",
            "  // 'dashboardNamePrefix' - Use as prefix for all Dashboards and (optional) rule groups",
            "  // 'filteringSelector' - Static selector to apply to ALL dashboard variables of type query, panel queries, alerts and recording rules.",
            "  // 'groupLabels' - one or more labels that can be used to identify 'group' of instances. In simple cases, can be 'job' or 'cluster'.",
            "  // 'instanceLabels' - one or more labels that can be used to identify single entity of instances. In simple cases, can be 'instance' or 'pod'.",
            "  // 'uid' - UID to prefix all dashboards original uids",
            "",
        ]

        # Extract values from old config using regex
        enable_multi_cluster = re.search(r'enableMultiCluster:\s*(true|false)', content)
        enable_multi_cluster = enable_multi_cluster.group(1) if enable_multi_cluster else 'false'

        filter_selector = re.search(r'filterSelector:\s*\'([^\']+)\'', content)
        filter_selector = filter_selector.group(1) if filter_selector else None

        # Extract uid from filter selector or dashboard tags
        dashboard_tags = re.search(r'dashboardTags:\s*\[(.*?)\]', content, re.DOTALL)
        if dashboard_tags:
            # Try to extract uid from dashboard tags
            tags = [tag.strip().strip("'").strip('"') for tag in dashboard_tags.group(1).split(',')]
            uid = next((tag.replace('-mixin', '') for tag in tags), 'unknown')
        elif filter_selector:
            # Try to extract from job selector
            job_match = re.search(r'job=~"([^"]+)"', filter_selector)
            if job_match:
                # Clean up the job pattern to create a uid
                uid = job_match.group(1).replace('.*/','').replace('.*','').replace('"','').split('/')[-1]
            else:
                uid = 'unknown'
        else:
            uid = 'unknown'

        dashboard_period = re.search(r'dashboardPeriod:\s*\'([^\']+)\'', content)
        dashboard_period = dashboard_period.group(1) if dashboard_period else 'now-30m'

        dashboard_timezone = re.search(r'dashboardTimezone:\s*\'([^\']+)\'', content)
        dashboard_timezone = dashboard_timezone.group(1) if dashboard_timezone else 'default'

        dashboard_refresh = re.search(r'dashboardRefresh:\s*\'([^\']+)\'', content)
        dashboard_refresh = dashboard_refresh.group(1) if dashboard_refresh else '1m'

        enable_loki_logs = re.search(r'enableLokiLogs:\s*(true|false)', content)
        enable_loki_logs = enable_loki_logs.group(1) if enable_loki_logs else 'true'

        # Find any selector pattern that uses multi-cluster logic
        selector_pattern = r'(\w+Selector):\s*if\s*self\.enableMultiCluster\s*then\s*\'([^\'"]*)[\'"]\s*else\s*\'([^\'"]*)[\'"]'
        selector_match = re.search(selector_pattern, content)
        
        if selector_match:
            multi_cluster_selector = selector_match.group(2)
            single_cluster_selector = selector_match.group(3)
            
            # Parse labels from selectors
            multi_cluster_labels = [label for label in re.findall(r'(\w+)=~"\$\w+"', multi_cluster_selector)]
            single_cluster_labels = [label for label in re.findall(r'(\w+)=~"\$\w+"', single_cluster_selector)]
        else:
            # Default to basic labels if no selector pattern found
            multi_cluster_labels = ['job', 'cluster']
            single_cluster_labels = ['job']

        # Extract log labels
        log_labels = re.search(r'logLabels:\s*if\s*self\.enableMultiCluster\s*then\s*\[(.*?)\]\s*else\s*\[(.*?)\]', content, re.DOTALL)
        if log_labels:
            multi_cluster_log_labels = log_labels.group(1).strip()
            single_cluster_log_labels = log_labels.group(2).strip()
        else:
            # Default log labels if not found
            multi_cluster_log_labels = "'job', 'instance', 'cluster', 'level'"
            single_cluster_log_labels = "'job', 'instance', 'level'"

        # Format the group labels as a proper array string
        multi_group_labels = "['" + "', '".join(multi_cluster_labels) + "']"
        single_group_labels = "['" + "', '".join(single_cluster_labels) + "']"

        # Add converted config
        new_config.extend([
            f"  enableMultiCluster: {enable_multi_cluster},",
            f"  filteringSelector: '{filter_selector}',",
            f"  groupLabels: if self.enableMultiCluster then {multi_group_labels} else {single_group_labels},",
            "  instanceLabels: ['instance'],",
            f"  dashboardTags: ['{uid}-mixin'],",
            f"  uid: '{uid}',",
            "  dashboardNamePrefix: '',",
            "",
            "  // additional params",
            f"  dashboardPeriod: '{dashboard_period}',",
            f"  dashboardTimezone: '{dashboard_timezone}',",
            f"  dashboardRefresh: '{dashboard_refresh}',",
            "",
            "  // logs lib related",
            f"  enableLokiLogs: {enable_loki_logs},",
            f"  logLabels: if self.enableMultiCluster then [{multi_cluster_log_labels}] else [{single_cluster_log_labels}],",
            "  extraLogLabels: [],  // Required by logs-lib",
            "  logsVolumeGroupBy: 'level',",
            "  showLogsVolume: true,",
            "}",
        ])

        return '\n'.join(new_config)

    def generate_makefile(self) -> str:
        """
        Generates a standard Makefile for the mixin.
        """
        return '''JSONNET_FMT := jsonnetfmt -n 2 --max-blank-lines 1 --string-style s --comment-style s

.PHONY: all
all: build dashboards_out prometheus_alerts.yaml

vendor: jsonnetfile.json
	jb install

.PHONY: build
build: vendor

.PHONY: fmt
fmt:
	find . -name 'vendor' -prune -o -name '*.libsonnet' -print -o -name '*.jsonnet' -print | \\
		xargs -n 1 -- $(JSONNET_FMT) -i

.PHONY: lint
lint: build
	find . -name 'vendor' -prune -o -name '*.libsonnet' -print -o -name '*.jsonnet' -print | \\
		while read f; do \\
			$(JSONNET_FMT) "$$f" | diff -u "$$f" -; \\
		done
	mixtool lint mixin.libsonnet

dashboards_out: mixin.libsonnet config.libsonnet dashboards.libsonnet
	@mkdir -p dashboards_out
	mixtool generate dashboards mixin.libsonnet -d dashboards_out

prometheus_alerts.yaml: mixin.libsonnet alerts.libsonnet
	mixtool generate alerts mixin.libsonnet -a prometheus_alerts.yaml

.PHONY: clean
clean:
	rm -rf dashboards_out prometheus_alerts.yaml
'''

    def copy_readme(self, input_dir: Path, output_dir: Path) -> None:
        """
        Copies README file from input directory to output directory if it exists.
        """
        readme_patterns = ['README.md', 'Readme.md', 'readme.md']
        for pattern in readme_patterns:
            readme_file = input_dir / pattern
            if readme_file.exists():
                output_readme = output_dir / pattern
                output_readme.write_text(readme_file.read_text())
                print(f"Copied {pattern} to output directory")
                break

    def generate_main_file(self) -> str:
        """
        Generates the main.libsonnet file that imports and packages all components.
        """
        # Use the stored example metric, or provide a fallback
        var_metric = self.example_metric or 'up'
        
        content = [
            "local alerts = import './alerts.libsonnet';",
            "local config = import './config.libsonnet';",
            "local dashboards = import './dashboards.libsonnet';",
            "local g = import './g.libsonnet';",
            "local links = import './links.libsonnet';",
            "local panels = import './panels.libsonnet';",
            "local targets = import './targets.libsonnet';",
            "local variables = import './variables.libsonnet';",
            "",
            "{",
            "  withConfigMixin(config): {",
            "    config+: config,",
            "  },",
            "",
            "  new(): {",
            "",
            "    local this = self,",
            "    config: config,",
            "",
            "    grafana: {",
            f"      variables: variables.new(this, varMetric='{var_metric}'),",
            "      targets: targets.new(this),",
            "      annotations: {},",
            "      links: links.new(this),",
            "      panels: panels.new(this),",
            "      dashboards: dashboards.new(this),",
            "    },",
            "",
            "    prometheus: {",
            "      alerts: alerts.new(this),",
            "      recordingRules: {},",
            "    },",
            "  },",
            "}",
        ]
        
        return '\n'.join(content)

    def run_make_build(self, output_dir: Path) -> None:
        """
        Runs 'make build' in the output directory.
        """
        import subprocess
        import os
        
        try:
            # Change to output directory
            original_dir = os.getcwd()
            os.chdir(output_dir)
            
            # Run make build
            print("Running 'make build'...")
            result = subprocess.run(['make', 'build'], 
                                 capture_output=True, 
                                 text=True)
            
            if result.returncode == 0:
                print("Successfully ran 'make build'")
            else:
                print("Error running 'make build':")
                print(result.stderr)
                
        except Exception as e:
            print(f"Error running make build: {e}")
        finally:
            # Change back to original directory
            os.chdir(original_dir)

    def generate_mixin_file(self, mixin_name: str = None) -> str:
        """
        Generates the mixin.libsonnet file that imports main.libsonnet and exports dashboards and rules.
        
        Args:
            mixin_name: Optional name of the mixin. If not provided, will try to determine from config or use 'mixin'.
        """
        # If mixin_name not provided, try to determine it from config or dashboard tags
        if not mixin_name:
            # Try to extract from dashboard titles
            if self.dashboards and len(self.dashboards) > 0:
                # Assume first word of first dashboard title is the mixin name
                first_dashboard = self.dashboards[0]
                if 'title' in first_dashboard and first_dashboard['title']:
                    mixin_name = first_dashboard['title'].split()[0].lower()
        
            # If still not found, use a default
            if not mixin_name:
                mixin_name = 'mixin'
        
        content = [
            f"local {mixin_name}lib = import './main.libsonnet';",
            "",
            f"local {mixin_name} =",
            f"  {mixin_name}lib.new()",
            f"  + {mixin_name}lib.withConfigMixin(",
            "    {",
            "      filteringSelector: 'job=~\"integrations/" + mixin_name + "\"',",
            f"      uid: '{mixin_name}',",
            "      enableLokiLogs: true,",
            "    }",
            "  );",
            "",
            "// populate monitoring-mixin:",
            "{",
            f"  grafanaDashboards+:: {mixin_name}.grafana.dashboards,",
            f"  prometheusAlerts+:: {mixin_name}.prometheus.alerts,",
            f"  prometheusRules+:: {mixin_name}.prometheus.recordingRules,",
            "}",
        ]
        
        return '\n'.join(content)

    def generate_alerts_file(self) -> str:
        """
        Generates a basic alerts.libsonnet file.
        """
        content = [
            "{",
            "  new(this): {",
            "    // Add your alerts here",
            "    // Example:",
            "    // exampleAlert:",
            "    //   {",
            "    //     alert: 'ExampleAlert',",
            "    //     expr: 'up == 0',",
            "    //     'for': '5m',",
            "    //     labels: {",
            "    //       severity: 'critical',",
            "    //     },",
            "    //     annotations: {",
            "    //       summary: 'Instance {{ $labels.instance }} down',",
            "    //       description: '{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes.',",
            "    //     },",
            "    //   },",
            "  },",
            "}",
        ]
        
        return '\n'.join(content)

    def convert_mixin(self, input_dir: Path, output_dir: Path) -> None:
        """
        Converts all dashboard and panel definitions from old format to new format.
        """
        # Initialize queries dictionary and dashboard names list
        self.queries = {}
        self.dashboard_names = []
        self.dashboards = []  # Store all dashboard definitions
        
        # Generate g.libsonnet file
        g_file = output_dir / 'g.libsonnet'
        g_file.write_text(self.generate_g_file())
        
        # Generate variables.libsonnet file
        variables_file = output_dir / 'variables.libsonnet'
        variables_file.write_text(self.generate_variables_file())

        # Generate Makefile
        makefile = output_dir / 'Makefile'
        makefile.write_text(self.generate_makefile())

        # Generate empty jsonnetfile.json
        jsonnetfile = output_dir / 'jsonnetfile.json'
        jsonnetfile.write_text(self.generate_jsonnetfile())

        # Copy README if it exists
        self.copy_readme(input_dir, output_dir)

        # Convert config.libsonnet if it exists
        config_file = input_dir / 'config.libsonnet'
        if config_file.exists():
            content = config_file.read_text()
            new_config = self.convert_config_file(content)
            new_config_file = output_dir / 'config.libsonnet'
            new_config_file.write_text(new_config)
        
        # Process dashboard files
        dashboards_dir = input_dir / 'dashboards'
        if dashboards_dir.exists():
            for dashboard_file in dashboards_dir.glob('*.libsonnet'):
                if dashboard_file.name != 'dashboards.libsonnet':
                    print(f"Processing {dashboard_file.name}...")
                    content = dashboard_file.read_text()
                    
                    # Extract panel definitions
                    self.panel_definitions.update(self.extract_panel_definitions(content))
                    
                    # Extract queries
                    self.queries.update(self.extract_queries(content))
                    
                    # Extract dashboard structure
                    dashboard = self.extract_dashboard_structure(content)
                    self.dashboards.append(dashboard)  # Store the dashboard
                    
                    # Store dashboard name for links generation
                    dashboard_name = f"{dashboard['title'].lower().replace(' ', '-')}.json"
                    self.dashboard_names.append(dashboard_name)

        # Generate single dashboards file with all dashboards
        dashboards_file = output_dir / 'dashboards.libsonnet'
        dashboards_file.write_text(self.generate_dashboard_file(self.dashboards))

        # Generate remaining files
        panels_file = output_dir / 'panels.libsonnet'
        panels_file.write_text(self.generate_panels_file())

        rows_file = output_dir / 'rows.libsonnet'
        rows_file.write_text(self.generate_rows_file())
        
        targets_file = output_dir / 'targets.libsonnet'
        targets_file.write_text(self.generate_targets_file())
        
        links_file = output_dir / 'links.libsonnet'
        links_file.write_text(self.generate_links_file())

        # Generate main.libsonnet
        main_file = output_dir / 'main.libsonnet'
        main_file.write_text(self.generate_main_file())
        
        # Generate mixin.libsonnet
        # Try to determine mixin name from dashboard titles
        mixin_name = None
        if self.dashboards and len(self.dashboards) > 0:
            first_dashboard = self.dashboards[0]
            if 'title' in first_dashboard and first_dashboard['title']:
                # Extract first word from title as mixin name
                mixin_name = first_dashboard['title'].split()[0].lower()
        
        mixin_file = output_dir / 'mixin.libsonnet'
        mixin_file.write_text(self.generate_mixin_file(mixin_name))
        
        # Generate alerts.libsonnet if it doesn't exist
        alerts_file = output_dir / 'alerts.libsonnet'
        if not alerts_file.exists():
            alerts_file.write_text(self.generate_alerts_file())

        # Run make build after all files are generated
        print("Running make build...")
        self.run_make_build(output_dir)

    def generate_jsonnetfile(self) -> str:
        """
        Generates jsonnetfile.json with required Grafana dependencies.
        """
        return '''{
  "version": 1,
  "dependencies": [
    {
      "source": {
        "git": {
          "remote": "https://github.com/grafana/jsonnet-libs.git",
          "subdir": "common-lib"
        }
      },
      "version": "master"
    },
    {
      "source": {
        "git": {
          "remote": "https://github.com/grafana/grafonnet.git",
          "subdir": "gen/grafonnet-v10.0.0"
        }
      },
      "version": "main"
    },
    {
      "source": {
        "git": {
          "remote": "https://github.com/grafana/jsonnet-libs.git",
          "subdir": "logs-lib"
        }
      },
      "version": "master"
    }
  ],
  "legacyImports": true
}'''

    def extract_selector_patterns(self, content: str) -> Dict[str, str]:
        """
        Extracts selector patterns from old config format.
        Returns a dictionary mapping selector names to their patterns.
        """
        selectors = {}
        
        # Find all selector definitions in the config
        selector_pattern = r'(\w+Selector):\s*(?:if\s*self\.enableMultiCluster\s*then\s*[\'"]([^\'"]*)[\'"](?:\s*else\s*[\'"]([^\'"]*)[\'"])|\s*[\'"]([^\'"]*)[\'"])'
        
        for match in re.finditer(selector_pattern, content, re.DOTALL):
            selector_name = match.group(1)
            
            # Handle conditional selectors (with enableMultiCluster)
            if match.group(2) is not None:
                # We'll use the non-multi-cluster version by default
                selector_value = match.group(3) if match.group(3) else match.group(2)
            else:
                # Simple selector
                selector_value = match.group(4)
            
            selectors[selector_name] = selector_value
        
        return selectors

def main():
    """
    Main function to run the converter.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 convert.py <input_directory>")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path('new_mixin')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    converter = MixinConverter()
    converter.convert_mixin(input_dir, output_dir)
    print("Conversion complete!")

if __name__ == '__main__':
    main()