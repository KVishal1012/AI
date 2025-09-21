"""
Urban Planning Agent for Geospatial Applications

This agent combines Large Language Model capabilities with geospatial analysis
tools to assist in urban planning decisions and analysis.
"""

import os
import json
from datetime import datetime
from typing import Dict, Optional, Any, List 
try:
    import geopandas as gpd
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False

try:
    import folium
    from folium.plugins import HeatMap
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    HAS_VERTEXAI = True
except ImportError:
    HAS_VERTEXAI = False

try:
    import scipy
    from scipy.spatial import cKDTree
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    import sklearn
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import tensorflow as tf
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False

try:
    import torch
    HAS_PYTORCH = True
except ImportError:
    HAS_PYTORCH = False

try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

try:
    import statsmodels.api as sm
    from statsmodels.tsa.arima.model import ARIMA
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False

from google.cloud import storage
from utils import authenticate


class UrbanPlanningAgent:
    """
    An AI agent specialized in urban planning and geospatial analysis.

    This agent can:
    - Analyze geospatial data for urban planning
    - Generate planning recommendations using LLM
    - Visualize urban data on interactive maps
    - Store and retrieve planning data from cloud storage
    - Perform spatial analysis and modeling
    """

    def __init__(self, project_id: Optional[str] = None,
                 location: str = "us-central1"):
        """
        Initialize the Urban Planning Agent.

        Args:
            project_id: Google Cloud Project ID (optional, will use from env)
            location: Google Cloud region for Vertex AI
        """
        self.credentials, self.project_id = authenticate()
        if project_id:
            self.project_id = project_id

        if HAS_VERTEXAI:
            vertexai.init(
                project=self.project_id,
                location=location,
                credentials=self.credentials
            )

        # Initialize Generative Model for planning analysis
        if HAS_VERTEXAI:
            try:
                # Try different model names in order of preference
                model_names = [
                    "gemini-1.5-pro",
                    "gemini-1.5-flash",
                    "gemini-pro",
                    "text-bison-001"
                ]

                self.model = None
                for model_name in model_names:
                    try:
                        self.model = GenerativeModel(model_name)
                        print(f"Successfully initialized model: {model_name}")
                        break
                    except Exception as e:
                        print(f"Model {model_name} not available: {e}")
                        continue

                if self.model is None:
                    print("Warning: No Vertex AI models available.")
                    print("LLM features will be disabled.")
                    print("To enable LLM features, ensure Vertex AI")
                    print("API is enabled and models are available.")

            except Exception as e:
                print(f"Error initializing Vertex AI model: {e}")
                self.model = None
        else:
            self.model = None

        # Initialize Cloud Storage client
        self.storage_client = storage.Client(
            credentials=self.credentials,
            project=self.project_id
        )

        # Data storage
        self.geospatial_data = {}
        self.urban_indicators = {}
        self.planning_scenarios = []

        print(f"Urban Planning Agent initialized for project: "
              f"{self.project_id}")

    def load_geospatial_data(self, data_path: str, layer_name: str,
                             data_type: str = "shapefile") -> bool:
        """
        Load geospatial data from various sources.

        Args:
            data_path: Path to geospatial data (local or GCS)
            layer_name: Name to assign to this data layer
            data_type: Type of geospatial data (shapefile, geojson, etc.)

        Returns:
            Success status
        """
        try:
            if data_path.startswith("gs://"):
                # Load from Google Cloud Storage
                gdf = self._load_from_gcs(data_path, data_type)
            else:
                # Load from local file
                if data_type == "shapefile":
                    gdf = gpd.read_file(data_path)
                elif data_type == "geojson":
                    gdf = gpd.read_file(data_path, driver="GeoJSON")
                else:
                    raise ValueError(f"Unsupported data type: {data_type}")

            self.geospatial_data[layer_name] = gdf
            print(f"Loaded {len(gdf)} features for layer: {layer_name}")
            return True

        except Exception as e:
            print(f"Error loading geospatial data: {e}")
            return False

    def _load_from_gcs(self, gcs_path: str,
                       data_type: str) -> Optional[Any]:
        """Load geospatial data from Google Cloud Storage."""
        bucket_name = gcs_path.split("/")[2]
        blob_path = "/".join(gcs_path.split("/")[3:])

        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        # Download to temporary file
        temp_file = f"/tmp/temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if data_type == "geojson":
            temp_file += ".geojson"
        else:
            temp_file += ".zip"  # Assuming shapefile in zip

        blob.download_to_filename(temp_file)

        try:
            if data_type == "geojson":
                gdf = gpd.read_file(temp_file, driver="GeoJSON")
            else:
                gdf = gpd.read_file(f"zip://{temp_file}")

            # Clean up temp file
            os.remove(temp_file)
            return gdf

        except Exception as e:
            os.remove(temp_file)
            raise e

    def analyze_urban_indicators(self, indicators: Dict[str, Any],
                                 ) -> Dict[str, Any]:
        """
        Analyze urban planning indicators using LLM.

        Args:
            indicators: Dictionary of urban indicators
                (population, density, etc.)

        Returns:
            Analysis results and recommendations
        """
        self.urban_indicators.update(indicators)

        # Check if model is available
        if self.model is None:
            return {
                "indicators": indicators,
                "analysis": "LLM analysis not available.",
                "timestamp": datetime.now().isoformat(),
                "note": "Enable Vertex AI API and ensure models are available."
            }

        # Create analysis prompt
        prompt = f"""
        Analyze the following urban planning indicators and provide insights:

        Urban Indicators:
        {json.dumps(indicators, indent=2)}

        Please provide:
        1. Current urban development assessment
        2. Key challenges and opportunities
        3. Recommended planning strategies
        4. Potential impact on quality of life
        5. Sustainability considerations

        Format your response as a structured analysis.
        """

        try:
            response = self.model.generate_content(prompt)
            analysis = response.text
        except Exception as e:
            analysis = f"Error generating analysis: {e}"

        return {
            "indicators": indicators,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

    def create_planning_scenario(self, scenario_name: str,
                                 parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a planning scenario for urban development.

        Args:
            scenario_name: Name of the planning scenario
            parameters: Scenario parameters (growth rate, zoning changes, etc.)

        Returns:
            Scenario definition
        """
        scenario = {
            "name": scenario_name,
            "parameters": parameters,
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }

        self.planning_scenarios.append(scenario)

        # Generate scenario analysis
        if self.model is None:
            scenario["analysis"] = (
                "LLM analysis not available for scenario planning."
            )
        else:
            prompt = (
                "Create a detailed urban planning scenario based on these "
                "parameters:\n\n"
                f"Scenario: {scenario_name}\n"
                f"Parameters: {json.dumps(parameters, indent=2)}\n\n"
                "Please provide:\n"
                "1. Scenario description and objectives\n"
                "2. Expected outcomes and impacts\n"
                "3. Implementation timeline\n"
                "4. Risk assessment\n"
                "5. Monitoring and evaluation plan"
            )

            try:
                response = self.model.generate_content(prompt)
                scenario["analysis"] = response.text
            except Exception as e:
                scenario["analysis"] = (
                    f"Error generating scenario analysis: {e}"
                )

        return scenario

    def generate_interactive_map(self, center_lat: float = 40.7128,
                                 center_lng: float = -74.0060,
                                 zoom_start: int = 10) -> Optional[Any]:
        """
        Generate an interactive map for urban planning visualization.

        Args:
            center_lat: Center latitude (default: NYC)
            center_lng: Center longitude
            zoom_start: Initial zoom level

        Returns:
            Folium map object
        """
        # Create base map
        if HAS_FOLIUM:
            m = folium.Map(
                location=[center_lat, center_lng],
                zoom_start=zoom_start
            )
        else:
            print("Warning: Folium not available. Map generation disabled.")
            return None

        # Add geospatial layers
        for layer_name, gdf in self.geospatial_data.items():
            if not gdf.empty:
                # Convert to GeoJSON for Folium
                geojson_data = gdf.to_json()

                # Add layer to map
                folium.GeoJson(
                    geojson_data,
                    name=layer_name,
                    tooltip=folium.GeoJsonTooltip(fields=list(gdf.columns))
                ).add_to(m)

        # Add layer control
        folium.LayerControl().add_to(m)

        return m

    def spatial_analysis(self, analysis_type: str, layer_name: str,
                         **kwargs) -> Dict[str, Any]:
        """
        Perform spatial analysis on geospatial data.

        Args:
            analysis_type: Type of analysis (buffer, intersection,
                density, etc.)
            layer_name: Name of the data layer to analyze
            **kwargs: Additional parameters for analysis

        Returns:
            Analysis results
        """
        if layer_name not in self.geospatial_data:
            raise ValueError(f"Layer '{layer_name}' not found")

        gdf = self.geospatial_data[layer_name]

        results = {
            "analysis_type": analysis_type,
            "layer": layer_name,
            "timestamp": datetime.now().isoformat()
        }

        if analysis_type == "buffer":
            distance = kwargs.get("distance", 1000)  # meters
            results["buffered_data"] = gdf.buffer(distance)

        elif analysis_type == "intersection":
            other_layer = kwargs.get("other_layer")
            if other_layer in self.geospatial_data:
                results["intersection"] = gpd.overlay(
                    gdf, self.geospatial_data[other_layer], how="intersection"
                )

        elif analysis_type == "density":
            # Calculate density statistics
            area = gdf.geometry.area.sum()
            count = len(gdf)
            results["density_stats"] = {
                "total_area": area,
                "feature_count": count,
                "average_density": count / area if area > 0 else 0
            }

        elif analysis_type == "nearest_neighbor":
            # Find nearest neighbors
            if not HAS_SCIPY:
                results["error"] = "scipy not available for analysis"
            else:
                try:
                    centroids = gdf.geometry.centroid
                    coords = [(p.x, p.y) for p in centroids]
                    tree = cKDTree(coords)

                    distances, indices = tree.query(coords, k=2)
                    results["nearest_distances"] = distances[:, 1].tolist()
                except Exception as e:
                    results["error"] = f"Error in analysis: {e}"

        return results

    def analyze_real_time_traffic(self, area_bounds: Dict[str, float],
                                  time_window: int = 60) -> Dict[str, Any]:
        """
        Analyze real-time traffic patterns and congestion.

        Args:
            area_bounds: Dictionary with lat/lng bounds
                {'north': lat, 'south': lat, 'east': lng, 'west': lng}
            time_window: Time window in minutes for analysis

        Returns:
            Traffic analysis results
        """
        results = {
            "analysis_type": "real_time_traffic",
            "timestamp": datetime.now().isoformat(),
            "time_window_minutes": time_window,
            "area_bounds": area_bounds
        }

        # Simulate traffic data fetching (replace with actual API calls)
        if not HAS_SKLEARN:
            results["error"] = (
                "scikit-learn not available for traffic analysis"
            )
            return results

        try:
            # Mock traffic data - replace with actual API integration
            traffic_data = self._fetch_traffic_data(area_bounds, time_window)

            # Analyze congestion patterns
            congestion_analysis = self._analyze_congestion_patterns(
                traffic_data
            )

            # Predict future congestion
            predictions = self._predict_traffic_congestion(
                traffic_data, time_window
            )

            results.update({
                "current_congestion": congestion_analysis,
                "predictions": predictions,
                "traffic_flow_analysis": self._analyze_traffic_flow(
                    traffic_data
                ),
                "recommendations": self._generate_traffic_recommendations(
                    congestion_analysis
                )
            })

        except Exception as e:
            results["error"] = f"Error in traffic analysis: {e}"

        return results

    def _fetch_traffic_data(self, area_bounds: Dict[str, float],
                            time_window: int) -> Dict[str, Any]:
        """Fetch real-time traffic data from APIs."""
        # Placeholder for actual API integration
        # Could integrate with Google Maps API, TomTom API, etc.
        return {
            "traffic_incidents": [],
            "flow_data": [],
            "speed_data": [],
            "congestion_levels": []
        }

    def _analyze_congestion_patterns(self,
                                     traffic_data: Dict[str, Any]
                                     ) -> Dict[str, Any]:
        """Analyze traffic congestion patterns using ML."""
        if not HAS_SKLEARN:
            return {"error": "ML libraries not available"}

        # Use clustering to identify congestion hotspots
        # This is a simplified example - replace with actual implementation
        return {
            "hotspots": [],
            "peak_hours": [],
            "congestion_trends": [],
            "severity_levels": {"low": 0.2, "medium": 0.5, "high": 0.8}
        }

    def _predict_traffic_congestion(self, traffic_data: Dict[str, Any],
                                    time_window: int) -> Dict[str, Any]:
        """Predict future traffic congestion using time series analysis."""
        if not HAS_STATSMODELS and not HAS_PROPHET:
            return {"error": "Time series libraries not available"}

        # Use ARIMA or Prophet for prediction
        # This is a simplified example
        return {
            "predicted_congestion": [],
            "confidence_intervals": [],
            "peak_prediction_times": []
        }

    def _analyze_traffic_flow(self,
                              traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze traffic flow patterns and bottlenecks."""
        return {
            "flow_efficiency": 0.75,
            "bottlenecks": [],
            "alternative_routes": [],
            "traffic_distribution": {}
        }

    def _generate_traffic_recommendations(self,
                                          congestion_analysis: Dict[str, Any]
                                          ) -> List[str]:
        """Generate traffic management recommendations."""
        recommendations = [
            "Implement dynamic traffic signal timing",
            "Consider congestion pricing during peak hours",
            "Improve public transportation coverage",
            "Add bike lanes to reduce car dependency"
        ]
        return recommendations

    def predict_urban_growth(self, historical_data: Dict[str, Any],
                             prediction_years: int = 10) -> Dict[str, Any]:
        """
        Predict urban growth patterns using machine learning.

        Args:
            historical_data: Historical urban indicators and geospatial data
            prediction_years: Number of years to predict

        Returns:
            Urban growth predictions
        """
        results = {
            "analysis_type": "urban_growth_prediction",
            "timestamp": datetime.now().isoformat(),
            "prediction_horizon_years": prediction_years,
            "methodology": "machine_learning"
        }

        if not HAS_SKLEARN:
            results["error"] = (
                "scikit-learn not available for growth prediction"
            )
            return results

        try:
            # Prepare training data
            training_data = self._prepare_growth_training_data(historical_data)

            # Train growth prediction models
            population_model = self._train_population_growth_model(
                training_data
            )
            landuse_model = self._train_landuse_change_model(training_data)

            # Generate predictions
            predictions = self._generate_growth_predictions(
                population_model, landuse_model, prediction_years
            )

            # Analyze infrastructure needs
            infrastructure_needs = self._analyze_infrastructure_requirements(
                predictions
            )

            results.update({
                "population_predictions": predictions.get("population", {}),
                "landuse_predictions": predictions.get("landuse", {}),
                "infrastructure_needs": infrastructure_needs,
                "growth_scenarios": self._generate_growth_scenarios(
                    predictions
                ),
                "policy_recommendations": (
                    self._generate_growth_policy_recommendations(predictions)
                )
            })

        except Exception as e:
            results["error"] = f"Error in urban growth prediction: {e}"

        return results

    def _prepare_growth_training_data(self,
                                      historical_data: Dict[str, Any]
                                      ) -> Dict[str, Any]:
        """Prepare historical data for ML training."""
        # Process historical urban indicators
        # This is a simplified example
        return {
            "population_trends": [],
            "landuse_changes": [],
            "economic_indicators": [],
            "infrastructure_data": []
        }

    def _train_population_growth_model(self,
                                       training_data: Dict[str, Any]) -> Any:
        """Train ML model for population growth prediction."""
        if not HAS_SKLEARN:
            return None

        # Use Random Forest or other ML models for prediction
        # This is a simplified example
        return {"model_type": "random_forest", "trained": True}

    def _train_landuse_change_model(self,
                                    training_data: Dict[str, Any]) -> Any:
        """Train ML model for land use change prediction."""
        if not HAS_SKLEARN:
            return None

        # Use classification models for land use prediction
        return {"model_type": "classification", "trained": True}

    def _generate_growth_predictions(self, population_model: Any,
                                     landuse_model: Any,
                                     prediction_years: int) -> Dict[str, Any]:
        """Generate urban growth predictions."""
        predictions = {
            "population": {
                "annual_growth_rate": 0.025,
                "predicted_population": [],
                "confidence_intervals": []
            },
            "landuse": {
                "urban_expansion_rate": 0.015,
                "new_development_areas": [],
                "landuse_changes": []
            }
        }

        # Generate year-by-year predictions
        for year in range(1, prediction_years + 1):
            pop_prediction = 750000 * (1.025 ** year)  # Example calculation
            predictions["population"]["predicted_population"].append({
                "year": 2025 + year,
                "population": int(pop_prediction)
            })

        return predictions

    def _analyze_infrastructure_requirements(self,
                                             predictions: Dict[str, Any]
                                             ) -> Dict[str, Any]:
        """Analyze infrastructure needs based on growth predictions."""
        return {
            "housing_units_needed": 15000,
            "school_capacity_required": 5000,
            "healthcare_facilities": 5,
            "transportation_infrastructure": {
                "new_roads_km": 25,
                "public_transport_expansion": "moderate",
                "parking_spaces": 8000
            },
            "utility_capacity": {
                "water_treatment": "upgrade_required",
                "power_generation": "expansion_needed",
                "waste_management": "new_facility"
            }
        }

    def _generate_growth_scenarios(self,
                                   predictions: Dict[str, Any]
                                   ) -> List[Dict[str, Any]]:
        """Generate different urban growth scenarios."""
        scenarios = [
            {
                "name": "Business-as-Usual",
                "description": "Continued current growth patterns",
                "population_growth": "2.5% annual",
                "land_use_intensity": "high",
                "environmental_impact": "moderate"
            },
            {
                "name": "Sustainable Growth",
                "description": (
                    "Balanced development with environmental considerations"
                ),
                "population_growth": "2.0% annual",
                "land_use_intensity": "medium",
                "environmental_impact": "low"
            },
            {
                "name": "Compact City",
                "description": (
                    "High-density development with mixed-use zoning"
                ),
                "population_growth": "1.8% annual",
                "land_use_intensity": "very_high",
                "environmental_impact": "low"
            }
        ]
        return scenarios

    def _generate_growth_policy_recommendations(self,
                                                predictions: Dict[str, Any]
                                                ) -> List[str]:
        """Generate policy recommendations for urban growth management."""
        recommendations = [
            "Implement smart growth policies to manage urban expansion",
            "Invest in public transportation to reduce car dependency",
            "Develop mixed-use zoning to create walkable neighborhoods",
            "Preserve green spaces and agricultural land on urban fringes",
            "Implement water conservation measures for growing population",
            "Plan for renewable energy infrastructure expansion"
        ]
        return recommendations

    def save_to_gcs(self, data: Any, bucket_name: str, blob_name: str) -> bool:
        """
        Save data to Google Cloud Storage.

        Args:
            data: Data to save (GeoDataFrame, dict, etc.)
            bucket_name: GCS bucket name
            blob_name: Blob name/path

        Returns:
            Success status
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            if isinstance(data, gpd.GeoDataFrame):
                # Save as GeoJSON
                geojson_str = data.to_json()
                blob.upload_from_string(
                    geojson_str,
                    content_type="application/json"
                )
            elif isinstance(data, dict):
                # Save as JSON
                json_str = json.dumps(data, indent=2)
                blob.upload_from_string(
                    json_str,
                    content_type="application/json"
                )
            else:
                # Save as string
                blob.upload_from_string(str(data), content_type="text/plain")

            print(f"Data saved to gs://{bucket_name}/{blob_name}")
            return True

        except Exception as e:
            print(f"Error saving to GCS: {e}")
            return False

    def generate_planning_report(self, scenario_name: str) -> str:
        """
        Generate a comprehensive planning report.

        Args:
            scenario_name: Name of the planning scenario

        Returns:
            Formatted report
        """
        # Find the scenario
        scenario = None
        for s in self.planning_scenarios:
            if s["name"] == scenario_name:
                scenario = s
                break

        if not scenario:
            return f"Scenario '{scenario_name}' not found"

        # Generate comprehensive report
        prompt = f"""
        Generate a comprehensive urban planning report based on the
        following scenario:

        Scenario Details:
        {json.dumps(scenario, indent=2)}

        Urban Indicators:
        {json.dumps(self.urban_indicators, indent=2)}

        Available Data Layers:
        {list(self.geospatial_data.keys())}

        Please create a detailed report including:
        1. Executive Summary
        2. Current Situation Analysis
        3. Proposed Development Scenario
        4. Environmental Impact Assessment
        5. Infrastructure Requirements
        6. Economic Analysis
        7. Community Impact
        8. Implementation Plan
        9. Risk Assessment
        10. Recommendations

        Format as a professional planning document.
        """

        response = self.model.generate_content(prompt)
        return response.text

    def visualize_urban_data(self, data_type: str, **kwargs) -> plt.Figure:
        """
        Create visualizations for urban planning data.

        Args:
            data_type: Type of visualization (population, density, etc.)
            **kwargs: Additional parameters

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        if data_type == "population_distribution":
            # Create population distribution plot
            if "population_data" in kwargs:
                pop_data = kwargs["population_data"]
                sns.histplot(data=pop_data, ax=ax)
                ax.set_title("Population Distribution")
                ax.set_xlabel("Population")
                ax.set_ylabel("Frequency")

        elif data_type == "land_use_pie":
            # Create land use pie chart
            if "land_use_data" in kwargs:
                land_use = kwargs["land_use_data"]
                ax.pie(land_use.values(),
                       labels=land_use.keys(),
                       autopct='%1.1f%%')
                ax.set_title("Land Use Distribution")

        elif data_type == "density_heatmap":
            # Create density heatmap
            if "coordinates" in kwargs and "values" in kwargs:
                coords = kwargs["coordinates"]
                values = kwargs["values"]
                heatmap_data = [
                    [coord[0], coord[1], val]
                    for coord, val in zip(coords, values)
                ]
                m = folium.Map(
                    location=[coords[0][0], coords[0][1]],
                    zoom_start=10
                )
                HeatMap(heatmap_data).add_to(m)
                return m  # Return folium map instead of matplotlib

        return fig


def main():
    """Example usage of the Urban Planning Agent."""
    # Initialize agent
    agent = UrbanPlanningAgent()

    # Example urban indicators
    indicators = {
        "population": 850000,
        "population_density": 15000,  # per sq km
        "median_age": 34.5,
        "unemployment_rate": 4.2,
        "average_income": 75000,
        "housing_units": 350000,
        "vacancy_rate": 3.1,
        "green_space_percentage": 12.5
    }

    # Analyze indicators
    analysis = agent.analyze_urban_indicators(indicators)
    print("Urban Analysis Results:")
    print(analysis["analysis"])

    # Create a planning scenario
    scenario_params = {
        "growth_rate": 2.5,  # annual %
        "new_housing_units": 50000,
        "infrastructure_investment": 2000000000,  # $2B
        "green_space_target": 15.0,  # %
        "public_transport_expansion": True,
        "smart_city_initiatives": True
    }

    scenario = agent.create_planning_scenario(
        "Sustainable Urban Growth 2030",
        scenario_params
    )
    print(f"\nPlanning Scenario: {scenario['name']}")
    print(scenario["analysis"])

    # Generate planning report
    report = agent.generate_planning_report("Sustainable Urban Growth 2030")
    print("\n" + "="*50)
    print("URBAN PLANNING REPORT")
    print("="*50)
    print(report)


if __name__ == "__main__":
    main()
