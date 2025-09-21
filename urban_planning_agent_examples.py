#!/usr/bin/env python3
"""
Urban Planning Agent Usage Examples

This script demonstrates various ways to use the Urban Planning Agent
for geospatial analysis and urban planning tasks.
"""

import json
from urban_planning_agent import UrbanPlanningAgent


def example_basic_usage():
    """Basic usage example with urban indicators analysis."""
    print("=== Basic Urban Planning Agent Usage ===\n")

    # Initialize the agent
    agent = UrbanPlanningAgent()

    # Example urban indicators for a mid-sized city
    indicators = {
        "population": 750000,
        "population_density": 12000,  # per sq km
        "median_age": 35.2,
        "unemployment_rate": 5.1,
        "average_income": 65000,
        "housing_units": 280000,
        "vacancy_rate": 4.2,
        "green_space_percentage": 15.5,
        "public_transport_coverage": 68.0,
        "air_quality_index": 45
    }

    print("Analyzing urban indicators...")
    analysis = agent.analyze_urban_indicators(indicators)

    print("Analysis Results:")
    print("-" * 50)
    print(analysis["analysis"])
    print()


def example_planning_scenario():
    """Example of creating and analyzing a planning scenario."""
    print("=== Urban Planning Scenario Analysis ===\n")

    agent = UrbanPlanningAgent()

    # Define a sustainable development scenario
    scenario_params = {
        "growth_rate": 1.8,  # annual %
        "new_housing_units": 25000,
        "infrastructure_investment": 1500000000,  # $1.5B
        "green_space_target": 18.0,  # %
        "public_transport_expansion": True,
        "smart_city_initiatives": True,
        "renewable_energy_target": 40.0,  # %
        "time_horizon": 10  # years
    }

    print("Creating planning scenario...")
    scenario = agent.create_planning_scenario(
        "Sustainable Smart City 2035",
        scenario_params
    )

    print(f"Scenario: {scenario['name']}")
    print("-" * 50)
    print(scenario["analysis"])
    print()


def example_spatial_analysis():
    """Example of spatial analysis capabilities."""
    print("=== Spatial Analysis Example ===\n")

    agent = UrbanPlanningAgent()  # Initialize agent for spatial analysis

    # Note: This would require actual geospatial data files
    # For demonstration, we'll show the API usage

    print("Spatial Analysis Capabilities:")
    print("- Load geospatial data (Shapefiles, GeoJSON)")
    print("- Perform buffer analysis")
    print("- Calculate intersection areas")
    print("- Compute density statistics")
    print("- Find nearest neighbors")
    print("- Generate interactive maps")
    print()

    # Example of what the analysis results would look like
    sample_results = {
        "analysis_type": "density",
        "layer": "population_data",
        "timestamp": "2025-09-07T10:00:00",
        "density_stats": {
            "total_area": 1500000000,  # sq meters
            "feature_count": 50000,
            "average_density": 0.033
        }
    }

    print("Sample Analysis Results:")
    print(json.dumps(sample_results, indent=2))
    print()


def example_data_persistence():
    """Example of saving and loading data to/from Google Cloud Storage."""
    print("=== Data Persistence with Google Cloud Storage ===\n")

    agent = UrbanPlanningAgent()  # Initialize for GCS operations

    print("Data Persistence Features:")
    print("- Save geospatial data to GCS")
    print("- Load data from GCS")
    print("- Store analysis results")
    print("- Backup planning scenarios")
    print()

    # Example usage (would require actual data and GCS setup)
    print("Example code:")
    print("""
    # Save analysis results to GCS
    success = agent.save_to_gcs(
        analysis_results,
        bucket_name="urban-planning-data",
        blob_name="analysis_results/scenario_2035.json"
    )

    # Load geospatial data from GCS
    success = agent.load_geospatial_data(
        data_path="gs://urban-planning-data/city_boundaries.geojson",
        layer_name="city_boundaries",
        data_type="geojson"
    )
    """)
    print()


def example_visualization():
    """Example of data visualization capabilities."""
    print("=== Data Visualization Examples ===\n")

    agent = UrbanPlanningAgent()  # Initialize for visualization

    print("Visualization Capabilities:")
    print("- Interactive maps with Folium")
    print("- Population distribution plots")
    print("- Land use pie charts")
    print("- Density heatmaps")
    print("- Statistical visualizations")
    print()

    # Example of generating an interactive map
    print("Example: Generate Interactive Map")
    print("""
    # Create interactive map centered on city
    city_map = agent.generate_interactive_map(
        center_lat=40.7128,  # NYC coordinates
        center_lng=-74.0060,
        zoom_start=11
    )

    # Save map as HTML file
    city_map.save("city_planning_map.html")
    """)
    print()


def example_comprehensive_workflow():
    """Complete workflow example combining multiple features."""
    print("=== Comprehensive Urban Planning Workflow ===\n")

    agent = UrbanPlanningAgent()  # Initialize for complete workflow

    print("Complete Workflow:")
    print("1. Load geospatial data layers")
    print("2. Analyze current urban indicators")
    print("3. Create planning scenarios")
    print("4. Perform spatial analysis")
    print("5. Generate visualizations")
    print("6. Create comprehensive reports")
    print("7. Save results to cloud storage")
    print()

    # Example workflow code
    print("Example Workflow Code:")
    print("""
    # 1. Load data
    agent.load_geospatial_data("city_blocks.shp", "blocks")
    agent.load_geospatial_data("parks.geojson", "parks")

    # 2. Analyze indicators
    analysis = agent.analyze_urban_indicators(current_indicators)

    # 3. Create scenario
    scenario = agent.create_planning_scenario("Green City 2040", params)

    # 4. Spatial analysis
    density_analysis = agent.spatial_analysis("density", "blocks")
    buffer_analysis = agent.spatial_analysis("buffer", "parks",
                                           distance=500)

    # 5. Generate map
    planning_map = agent.generate_interactive_map()

    # 6. Create report
    report = agent.generate_planning_report("Green City 2040")

    # 7. Save everything
    agent.save_to_gcs(scenario, "urban-data",
                     "scenarios/green_city.json")
    agent.save_to_gcs(report, "urban-data",
                     "reports/green_city_report.txt")
    """)
    print()


def example_real_time_traffic_analysis():
    """Example of real-time traffic analysis capabilities."""
    print("=== Real-Time Traffic Analysis Example ===\n")

    agent = UrbanPlanningAgent()

    # Define area bounds for traffic analysis (e.g., downtown area)
    area_bounds = {
        "north": 40.7589,  # Northern latitude
        "south": 40.7505,  # Southern latitude
        "east": -73.9851,  # Eastern longitude
        "west": -74.0071   # Western longitude
    }

    print("Analyzing real-time traffic patterns...")
    print(f"Analysis area: {area_bounds}")
    print()

    # Perform real-time traffic analysis
    traffic_analysis = agent.analyze_real_time_traffic(
        area_bounds=area_bounds,
        time_window=60  # 60 minutes
    )

    print("Traffic Analysis Results:")
    print("-" * 50)

    if "error" in traffic_analysis:
        print(f"Note: {traffic_analysis['error']}")
        print("This is expected if ML libraries are not installed.")
        print()
    else:
        print(f"Analysis Timestamp: {traffic_analysis['timestamp']}")
        print(f"Time Window: {traffic_analysis['time_window_minutes']} "
              "minutes")
        print()

        if "current_congestion" in traffic_analysis:
            print("Current Congestion Analysis:")
            congestion = traffic_analysis["current_congestion"]
            print("- Congestion hotspots identified: "
                  f"{len(congestion.get('hotspots', []))}")
            print("- Peak congestion hours: "
                  f"{congestion.get('peak_hours', 'N/A')}")
            print()

        if "predictions" in traffic_analysis:
            print("Traffic Predictions:")
            predictions = traffic_analysis["predictions"]
            print("- Prediction confidence: "
                  f"{predictions.get('confidence_intervals', 'N/A')}")
            print()

        if "recommendations" in traffic_analysis:
            print("Traffic Management Recommendations:")
            for i, rec in enumerate(traffic_analysis["recommendations"], 1):
                print(f"{i}. {rec}")
            print()

    # Example of what the results would look like with full implementation
    print("Expected Results Structure:")
    sample_traffic_results = {
        "analysis_type": "real_time_traffic",
        "timestamp": "2025-09-08T14:30:00",
        "time_window_minutes": 60,
        "current_congestion": {
            "hotspots": ["Downtown Intersection", "Highway Exit"],
            "peak_hours": ["8-9 AM", "5-6 PM"],
            "severity_levels": {"low": 0.2, "medium": 0.5, "high": 0.8}
        },
        "predictions": {
            "predicted_congestion": [0.3, 0.7, 0.9, 0.6],
            "peak_prediction_times": ["4:30 PM", "5:15 PM"]
        },
        "recommendations": [
            "Implement dynamic traffic signal timing",
            "Consider congestion pricing during peak hours",
            "Improve public transportation coverage"
        ]
    }
    print(json.dumps(sample_traffic_results, indent=2))
    print()


def example_predictive_urban_growth():
    """Example of predictive urban growth modeling."""
    print("=== Predictive Urban Growth Modeling Example ===\n")

    agent = UrbanPlanningAgent()

    # Historical data for growth prediction
    historical_data = {
        "population_trends": [
            {"year": 2020, "population": 750000},
            {"year": 2021, "population": 765000},
            {"year": 2022, "population": 780000},
            {"year": 2023, "population": 795000},
            {"year": 2024, "population": 810000}
        ],
        "economic_indicators": [
            {"year": 2020, "gdp_growth": 2.1, "employment_rate": 94.5},
            {"year": 2021, "gdp_growth": 2.8, "employment_rate": 95.1},
            {"year": 2022, "gdp_growth": 1.9, "employment_rate": 94.8},
            {"year": 2023, "gdp_growth": 2.5, "employment_rate": 95.3},
            {"year": 2024, "gdp_growth": 2.2, "employment_rate": 95.0}
        ],
        "landuse_changes": [
            {"year": 2020, "urban_area_km2": 150.5, "residential": 45.2},
            {"year": 2021, "urban_area_km2": 152.1, "residential": 46.1},
            {"year": 2022, "urban_area_km2": 153.8, "residential": 47.0},
            {"year": 2023, "urban_area_km2": 155.2, "residential": 47.8},
            {"year": 2024, "urban_area_km2": 156.9, "residential": 48.5}
        ]
    }

    print("Predicting urban growth for next 10 years...")
    print("Historical data points analyzed: "
          f"{len(historical_data['population_trends'])}")
    print()

    # Perform predictive urban growth modeling
    growth_predictions = agent.predict_urban_growth(
        historical_data=historical_data,
        prediction_years=10
    )

    print("Urban Growth Prediction Results:")
    print("-" * 50)

    if "error" in growth_predictions:
        print(f"Note: {growth_predictions['error']}")
        print("This is expected if ML libraries are not installed.")
        print()
    else:
        print(f"Analysis Timestamp: {growth_predictions['timestamp']}")
        print("Prediction Horizon: "
              f"{growth_predictions['prediction_horizon_years']} years")
        print()

        if "population_predictions" in growth_predictions:
            print("Population Growth Predictions:")
            pop_pred = growth_predictions["population_predictions"]
            print(".1f")
            print("- Predicted population in 2034: "
                  f"{pop_pred['predicted_population'][-1]['population']:,}")
            print()

        if "infrastructure_needs" in growth_predictions:
            print("Infrastructure Requirements:")
            infra = growth_predictions["infrastructure_needs"]
            print("- Additional housing units needed: "
                  f"{infra['housing_units_needed']:,}")
            print("- New schools required: "
                  f"{infra['school_capacity_required']}")
            print("- Healthcare facilities needed: "
                  f"{infra['healthcare_facilities']}")
            print("- New roads required: "
                  f"{infra['transportation_infrastructure']['new_roads_km']} "
                  "km")
            print()

        if "growth_scenarios" in growth_predictions:
            print("Alternative Growth Scenarios:")
            for scenario in growth_predictions["growth_scenarios"]:
                print(f"- {scenario['name']}: {scenario['description']}")
                print(f"  Population growth: {scenario['population_growth']}")
                print("  Environmental impact: "
                      f"{scenario['environmental_impact']}")
            print()

        if "policy_recommendations" in growth_predictions:
            print("Policy Recommendations:")
            for i, rec in enumerate(
                growth_predictions["policy_recommendations"], 1
            ):
                print(f"{i}. {rec}")
            print()

    # Example of what the results would look like with full implementation
    print("Expected Results Structure:")
    sample_growth_results = {
        "analysis_type": "urban_growth_prediction",
        "prediction_horizon_years": 10,
        "population_predictions": {
            "annual_growth_rate": 0.025,
            "predicted_population": [
                {"year": 2026, "population": 830250},
                {"year": 2027, "population": 851013},
                {"year": 2034, "population": 1023456}
            ]
        },
        "infrastructure_needs": {
            "housing_units_needed": 15000,
            "school_capacity_required": 5000,
            "healthcare_facilities": 5,
            "transportation_infrastructure": {
                "new_roads_km": 25,
                "public_transport_expansion": "moderate"
            }
        },
        "growth_scenarios": [
            {
                "name": "Business-as-Usual",
                "population_growth": "2.5% annual",
                "environmental_impact": "moderate"
            },
            {
                "name": "Sustainable Growth",
                "population_growth": "2.0% annual",
                "environmental_impact": "low"
            }
        ]
    }
    print(json.dumps(sample_growth_results, indent=2))
    print()


def main():
    """Run all examples."""
    print("Urban Planning Agent - Usage Examples")
    print("=" * 50)
    print()

    try:
        example_basic_usage()
        example_planning_scenario()
        example_spatial_analysis()
        example_real_time_traffic_analysis()
        example_predictive_urban_growth()
        example_data_persistence()
        example_visualization()
        example_comprehensive_workflow()

        print("All examples completed successfully!")
        print("\nTo use the Urban Planning Agent:")
        print("1. Install dependencies:")
        print("   pip install -r requirements_urban_planning.txt")
        print("2. Set up Google Cloud credentials")
        print("   (SERVICE_ACCOUNT_KEY and PROJECT_ID)")
        print("3. Import and initialize:")
        print("   from urban_planning_agent import UrbanPlanningAgent")
        print("4. Create agent instance:")
        print("   agent = UrbanPlanningAgent()")

    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure all dependencies are installed")
        print("and credentials are configured.")


if __name__ == "__main__":
    main()
