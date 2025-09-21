# Urban Planning Agent

An AI-powered geospatial agent for urban planning and analysis, combining Large Language Model capabilities with geospatial data processing and visualization tools.

## Features

### 🤖 AI-Powered Analysis
- **Urban Indicators Analysis**: Analyze population, economic, and environmental indicators using advanced AI
- **Planning Scenario Generation**: Create and evaluate urban development scenarios
- **Intelligent Recommendations**: Get AI-generated insights and recommendations for urban planning decisions

### 🗺️ Geospatial Capabilities
- **Data Loading**: Support for Shapefiles, GeoJSON, and other geospatial formats
- **Spatial Analysis**: Buffer analysis, intersection calculations, density analysis
- **Interactive Maps**: Generate interactive maps with Folium for data visualization
- **Cloud Storage Integration**: Seamless integration with Google Cloud Storage

### 📊 Data Visualization
- **Statistical Plots**: Population distribution, land use analysis
- **Heatmaps**: Density and activity visualization
- **Interactive Dashboards**: Web-based planning dashboards

### ☁️ Cloud Integration
- **Google Cloud Storage**: Store and retrieve geospatial data
- **Vertex AI**: Leverage Google's AI models for analysis
- **Scalable Processing**: Handle large datasets with cloud infrastructure

## Installation

### Prerequisites
- Python 3.8+
- Google Cloud Project with Vertex AI enabled
- Service account key with appropriate permissions

### Install Dependencies
```bash
pip install -r requirements_urban_planning.txt
```

### Environment Setup
1. Set up your Google Cloud credentials:
```bash
export SERVICE_ACCOUNT_KEY='<base64-encoded-service-account-json>'
export PROJECT_ID='<your-gcp-project-id>'
```

Or create a `.env` file:
```
SERVICE_ACCOUNT_KEY=<base64-encoded-service-account-json>
PROJECT_ID=<your-gcp-project-id>
```

## Quick Start

### Basic Usage
```python
from urban_planning_agent import UrbanPlanningAgent

# Initialize the agent
agent = UrbanPlanningAgent()

# Analyze urban indicators
indicators = {
    "population": 750000,
    "population_density": 12000,
    "median_age": 35.2,
    "unemployment_rate": 5.1,
    "green_space_percentage": 15.5
}

analysis = agent.analyze_urban_indicators(indicators)
print(analysis["analysis"])
```

### Create Planning Scenarios
```python
# Define a sustainable development scenario
scenario_params = {
    "growth_rate": 1.8,
    "new_housing_units": 25000,
    "green_space_target": 18.0,
    "public_transport_expansion": True,
    "smart_city_initiatives": True
}

scenario = agent.create_planning_scenario(
    "Sustainable Smart City 2035",
    scenario_params
)
print(scenario["analysis"])
```

### Load and Analyze Geospatial Data
```python
# Load geospatial data
agent.load_geospatial_data(
    "city_blocks.shp",
    "city_blocks",
    data_type="shapefile"
)

# Perform spatial analysis
density_analysis = agent.spatial_analysis("density", "city_blocks")
print(density_analysis)
```

### Generate Interactive Maps
```python
# Create interactive map
city_map = agent.generate_interactive_map(
    center_lat=40.7128,  # NYC coordinates
    center_lng=-74.0060,
    zoom_start=11
)

# Save map
city_map.save("urban_planning_map.html")
```

### Cloud Storage Operations
```python
# Save analysis results to Google Cloud Storage
agent.save_to_gcs(
    analysis_results,
    bucket_name="urban-planning-data",
    blob_name="analysis/scenario_2035.json"
)

# Load data from GCS
agent.load_geospatial_data(
    "gs://urban-planning-data/city_data.geojson",
    "city_boundaries",
    data_type="geojson"
)
```

## Advanced Usage

### Comprehensive Planning Workflow
```python
# 1. Load multiple data layers
agent.load_geospatial_data("buildings.shp", "buildings")
agent.load_geospatial_data("roads.geojson", "roads")
agent.load_geospatial_data("parks.geojson", "parks")

# 2. Analyze current conditions
current_analysis = agent.analyze_urban_indicators(current_indicators)

# 3. Create multiple scenarios
scenarios = []
for scenario_name, params in scenario_definitions.items():
    scenario = agent.create_planning_scenario(scenario_name, params)
    scenarios.append(scenario)

# 4. Perform spatial analysis
building_density = agent.spatial_analysis("density", "buildings")
park_accessibility = agent.spatial_analysis("buffer", "parks", distance=1000)

# 5. Generate comprehensive report
final_report = agent.generate_planning_report("Optimal Development Scenario")

# 6. Create visualization
planning_map = agent.generate_interactive_map()
planning_map.save("comprehensive_planning_map.html")

# 7. Save everything to cloud
agent.save_to_gcs(final_report, "reports", "final_planning_report.txt")
```

### Custom Analysis Functions
```python
# Define custom urban planning metrics
def calculate_walkability_score(agent, residential_layer, commercial_layer):
    """Calculate walkability score based on proximity to amenities."""
    # Implementation here
    pass

def assess_environmental_impact(agent, development_scenario):
    """Assess environmental impact of development scenarios."""
    # Implementation here
    pass
```

## API Reference

### UrbanPlanningAgent Class

#### Methods

- `__init__(project_id=None, location="us-central1")`: Initialize the agent
- `load_geospatial_data(data_path, layer_name, data_type="shapefile")`: Load geospatial data
- `analyze_urban_indicators(indicators)`: Analyze urban planning indicators
- `create_planning_scenario(scenario_name, parameters)`: Create planning scenario
- `spatial_analysis(analysis_type, layer_name, **kwargs)`: Perform spatial analysis
- `generate_interactive_map(center_lat=40.7128, center_lng=-74.0060, zoom_start=10)`: Generate interactive map
- `generate_planning_report(scenario_name)`: Generate comprehensive planning report
- `save_to_gcs(data, bucket_name, blob_name)`: Save data to Google Cloud Storage
- `visualize_urban_data(data_type, **kwargs)`: Create data visualizations

#### Spatial Analysis Types
- `"buffer"`: Create buffer zones around features
- `"intersection"`: Find intersections between layers
- `"density"`: Calculate density statistics
- `"nearest_neighbor"`: Find nearest neighbors analysis

## Examples

See `urban_planning_agent_examples.py` for comprehensive usage examples including:
- Basic urban indicators analysis
- Planning scenario creation
- Spatial analysis demonstrations
- Data visualization examples
- Complete workflow integration

Run the examples:
```bash
python urban_planning_agent_examples.py
```

## Data Formats Supported

### Geospatial Data
- **Shapefiles** (.shp, .dbf, .shx, .prj)
- **GeoJSON** (.geojson)
- **Geospatial databases** (PostGIS, SpatiaLite)
- **CSV with coordinates** (lat/lng columns)

### Urban Indicators
- Population statistics
- Economic indicators
- Environmental metrics
- Infrastructure data
- Transportation statistics
- Housing market data

## Cloud Architecture

### Google Cloud Services Used
- **Vertex AI**: For LLM-powered analysis and recommendations
- **Cloud Storage**: For data persistence and sharing
- **BigQuery**: For large-scale urban data analysis (optional)
- **Cloud Functions**: For automated processing (optional)

### Security Considerations
- Service account keys are encrypted and stored securely
- Data access is controlled through IAM permissions
- All data transmission is encrypted
- Audit logs are maintained for compliance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all lint checks pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Check the examples in `urban_planning_agent_examples.py`
- Review the API documentation above
- Open an issue on GitHub for bugs or feature requests

## Roadmap

### Planned Features
- [ ] Web-based dashboard interface
- [ ] Real-time urban monitoring
- [ ] Integration with IoT sensors
- [ ] Multi-city comparative analysis
- [ ] Automated report generation
- [ ] Mobile application companion
- [ ] Integration with urban planning software (ArcGIS, QGIS)

### Research Areas
- [ ] Predictive modeling for urban growth
- [ ] Climate change impact assessment
- [ ] Social equity analysis
- [ ] Economic impact modeling
- [ ] Transportation optimization</content>
<parameter name="filePath">/Users/koushikannamalai/Downloads/Github/AI/AI/README_urban_planning_agent.md
