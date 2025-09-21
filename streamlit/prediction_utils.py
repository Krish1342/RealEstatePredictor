"""
Model prediction utilities and enhanced visualization components
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class ModelPredictor:
    """
    Enhanced model prediction interface
    """
    
    def __init__(self, models_dir="../ensemble_learning/saved_models"):
        self.models_dir = models_dir
        self.models = {}
        self.scaler = None
        self.feature_names = None
        self.model_results = None
        self.load_models()
    
    def load_models(self):
        """Load all available models and metadata"""
        try:
            # Load model results
            results_path = os.path.join(self.models_dir, "ensemble_learning_results.csv")
            if os.path.exists(results_path):
                self.model_results = pd.read_csv(results_path)
            
            # Load scaler
            scaler_path = os.path.join(self.models_dir, "feature_scaler.pkl")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
            
            # Load models
            model_files = [f for f in os.listdir(self.models_dir) if f.endswith('.pkl') and 'model' in f]
            for model_file in model_files:
                try:
                    model_path = os.path.join(self.models_dir, model_file)
                    model = joblib.load(model_path)
                    
                    # Extract clean model name
                    model_name = model_file.replace('.pkl', '').replace('_', ' ').replace('model ', '').title()
                    if 'best' in model_file.lower():
                        model_name = "Best " + model_name
                    
                    self.models[model_name] = {
                        'model': model,
                        'file': model_file,
                        'performance': self.get_model_performance(model_name)
                    }
                    
                except Exception as e:
                    st.warning(f"Could not load model {model_file}: {str(e)}")
            
            return len(self.models) > 0
            
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            return False
    
    def get_model_performance(self, model_name):
        """Get performance metrics for a specific model"""
        if self.model_results is None:
            return None
        
        # Try to match model name
        for _, row in self.model_results.iterrows():
            if any(word in row['Model'].lower() for word in model_name.lower().split()):
                return {
                    'r2': row['R²'],
                    'rmse': row['RMSE'],
                    'mae': row['MAE'],
                    'mape': row['MAPE (%)'] if 'MAPE (%)' in row else None
                }
        return None
    
    def create_prediction_form(self):
        """Create comprehensive prediction input form"""
        st.subheader("🏠 Property Information")
        
        # Model selection
        if not self.models:
            st.error("No models available for prediction")
            return None
        
        model_names = list(self.models.keys())
        selected_model = st.selectbox("🤖 Select Prediction Model:", model_names)
        
        # Display model performance
        if selected_model in self.models and self.models[selected_model]['performance']:
            perf = self.models[selected_model]['performance']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model R² Score", f"{perf['r2']:.4f}")
            with col2:
                st.metric("RMSE", f"₹{perf['rmse']:,.0f}")
            with col3:
                if perf['mape']:
                    st.metric("MAPE", f"{perf['mape']:.2f}%")
        
        # Property input form
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🏠 Basic Property Details**")
                
                bhk = st.number_input("🛏️ BHK (Bedrooms)", min_value=1, max_value=10, value=2, step=1)
                size_sqft = st.number_input("📐 Size (Sq Ft)", min_value=300, max_value=20000, value=1000, step=50)
                bathrooms = st.number_input("🚿 Bathrooms", min_value=1, max_value=10, value=2, step=1)
                
                total_floors = st.number_input("🏢 Total Floors in Building", min_value=1, max_value=100, value=5, step=1)
                floor_no = st.number_input("🔢 Floor Number", min_value=1, max_value=100, value=3, step=1)
                
                property_age = st.number_input("📅 Property Age (years)", min_value=0, max_value=100, value=5, step=1)
            
            with col2:
                st.markdown("**🌍 Location & Environment**")
                
                location_popularity = st.slider("📍 Location Popularity Score", 0.0, 1.0, 0.5, 0.1)
                environmental_score = st.slider("🌱 Environmental Quality Score", 0.0, 1.0, 0.7, 0.1)
                
                aqi = st.number_input("🌫️ Air Quality Index (AQI)", min_value=0, max_value=500, value=100, step=5)
                day_noise = st.number_input("🔊 Day Noise Level (dB)", min_value=30.0, max_value=100.0, value=55.0, step=1.0)
                night_noise = st.number_input("🌙 Night Noise Level (dB)", min_value=20.0, max_value=80.0, value=45.0, step=1.0)
                
                # Additional features
                st.markdown("**🏘️ Property Features**")
                furnished = st.selectbox("🪑 Furnished Status", ["Unfurnished", "Semi-Furnished", "Furnished"])
                parking = st.selectbox("🚗 Parking", ["No", "Yes", "Covered"])
                balcony = st.number_input("🌤️ Number of Balconies", min_value=0, max_value=10, value=1, step=1)
            
            submitted = st.form_submit_button("🔮 Predict Price", type="primary")
            
            if submitted:
                return self.make_prediction(
                    selected_model, bhk, size_sqft, bathrooms, total_floors, floor_no,
                    property_age, location_popularity, environmental_score, aqi,
                    day_noise, night_noise, furnished, parking, balcony
                )
        
        return None
    
    def make_prediction(self, model_name, bhk, size_sqft, bathrooms, total_floors, 
                       floor_no, property_age, location_popularity, environmental_score,
                       aqi, day_noise, night_noise, furnished, parking, balcony):
        """Make price prediction with comprehensive input handling"""
        
        try:
            # Create input dataframe with comprehensive features
            input_data = {
                'BHK': bhk,
                'Size_in_SqFt': size_sqft,
                'Baths': bathrooms,
                'Total_Floors': total_floors,
                'Floor_No': floor_no,
                'Age_of_Property': property_age,
                'location_popularity': location_popularity,
                'environmental_score': environmental_score,
                'AQI': aqi,
                'Day': day_noise,
                'Night': night_noise,
                
                # Derived features
                'Price_per_SQFT': 0,  # Will be calculated after prediction
                'area_per_bedroom': size_sqft / bhk,
                'bath_bedroom_ratio': bathrooms / bhk,
                'Floor_Ratio': floor_no / total_floors,
                'BHK_Size_in_SqFt_interaction': bhk * size_sqft,
                'Baths_BHK_interaction': bathrooms * bhk,
                
                # Log features
                'Size_in_SqFt_log': np.log1p(size_sqft),
                'location_popularity_log': np.log1p(location_popularity),
                
                # Environmental features
                'AQI_normalized': 1 - (aqi / 500),  # Normalize AQI
                'DayExcess': max(0, day_noise - 55),  # Day noise excess
                'NightExcess': max(0, night_noise - 45),  # Night noise excess
                
                # Encoded categorical features (simplified)
                'furnished_binary': 1 if furnished != "Unfurnished" else 0,
                'parking_binary': 1 if parking != "No" else 0,
                'Balcony_encoded': balcony,
                
                # Additional common features with default values
                'Total_Area': size_sqft,
                'PM2.5': aqi / 4,  # Approximate PM2.5 from AQI
                'PM10': aqi / 3,   # Approximate PM10 from AQI
                'NO2': aqi / 5,    # Approximate NO2 from AQI
                'SO2': aqi / 6,    # Approximate SO2 from AQI
                'CO': aqi / 8,     # Approximate CO from AQI
                'O3': aqi / 7,     # Approximate O3 from AQI
                'Year_Built': 2024 - property_age,
                'Month_x': 6,      # Default month
                'Month_y': 6,      # Default month
                'Year_x': 2024,    # Default year
                'Year_y': 2024,    # Default year
            }
            
            # Load feature engineered dataset to get all required features
            feature_data_path = "../feature_engineering/feature_engineered_expert.csv"
            if os.path.exists(feature_data_path):
                feature_df = pd.read_csv(feature_data_path)
                
                # Get all feature columns (excluding target and price features that shouldn't be in prediction)
                target_cols = ['target_price', 'Price_numeric', 'Price_in_Lakhs', 'Price_encoded', 'Price', 'price']
                all_features = [col for col in feature_df.columns if col not in target_cols]
                
                # Create prediction dataframe with all required features
                prediction_df = pd.DataFrame([input_data])
                
                # Add missing features with median values from training data
                for feature in all_features:
                    if feature not in prediction_df.columns:
                        if feature in feature_df.columns:
                            if feature_df[feature].dtype in ['int64', 'float64']:
                                default_value = feature_df[feature].median()
                                if pd.isna(default_value):
                                    default_value = 0
                            else:
                                default_value = 0
                        else:
                            default_value = 0
                        prediction_df[feature] = default_value
                
                # Only include features that exist in the training data
                available_features = [col for col in all_features if col in feature_df.columns]
                prediction_df = prediction_df[available_features]
                
                # Fill any remaining NaN values
                prediction_df = prediction_df.fillna(0)
                
                # Make prediction
                model = self.models[model_name]['model']
                prediction = model.predict(prediction_df)
                predicted_price = prediction[0]
                
                # Display results
                self.display_prediction_results(
                    predicted_price, model_name, bhk, size_sqft, 
                    location_popularity, environmental_score
                )
                
                return predicted_price
            
            else:
                st.error("Feature dataset not found. Cannot make prediction.")
                return None
                
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            st.error("Please ensure all inputs are valid and try again.")
            return None
    
    def display_prediction_results(self, predicted_price, model_name, bhk, size_sqft, 
                                 location_popularity, environmental_score):
        """Display prediction results with comprehensive analysis"""
        
        # Main prediction display
        st.markdown(
            f'<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); '
            f'padding: 2rem; border-radius: 15px; color: white; text-align: center; '
            f'font-size: 2rem; font-weight: bold; margin: 2rem 0;">'
            f'💰 Predicted Price: ₹{predicted_price:,.0f}</div>',
            unsafe_allow_html=True
        )
        
        # Detailed metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            price_per_sqft = predicted_price / size_sqft
            st.metric("Price per Sq Ft", f"₹{price_per_sqft:,.0f}")
        
        with col2:
            price_in_lakhs = predicted_price / 100000
            st.metric("Price in Lakhs", f"₹{price_in_lakhs:.2f}L")
        
        with col3:
            price_per_bhk = predicted_price / bhk
            st.metric("Price per BHK", f"₹{price_per_bhk:,.0f}")
        
        with col4:
            if self.models[model_name]['performance']:
                r2 = self.models[model_name]['performance']['r2']
                st.metric("Model Accuracy", f"{r2:.4f}")
        
        # Confidence interval
        if self.models[model_name]['performance']:
            rmse = self.models[model_name]['performance']['rmse']
            lower_bound = max(0, predicted_price - rmse)
            upper_bound = predicted_price + rmse
            
            st.info(f"📊 **Confidence Range:** ₹{lower_bound:,.0f} - ₹{upper_bound:,.0f}")
        
        # Market analysis
        st.subheader("📈 Market Analysis")
        
        # Property category based on price
        if predicted_price < 2500000:
            category = "Budget"
            category_color = "green"
        elif predicted_price < 5000000:
            category = "Mid-Range"
            category_color = "orange"
        elif predicted_price < 10000000:
            category = "Premium"
            category_color = "blue"
        else:
            category = "Luxury"
            category_color = "purple"
        
        st.markdown(f"**Property Category:** :{category_color}[{category}]")
        
        # Price comparison visualization
        self.create_price_comparison_chart(predicted_price, size_sqft, bhk)
        
        # Feature impact analysis
        self.analyze_feature_impact(
            predicted_price, location_popularity, environmental_score, size_sqft, bhk
        )
    
    def create_price_comparison_chart(self, predicted_price, size_sqft, bhk):
        """Create price comparison chart"""
        
        # Create comparison data
        comparison_data = {
            'Category': ['Budget', 'Mid-Range', 'Premium', 'Luxury', 'Your Property'],
            'Price Range (₹)': [2500000, 5000000, 10000000, 20000000, predicted_price],
            'Color': ['green', 'orange', 'blue', 'purple', 'red']
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        
        fig = px.bar(
            df_comparison,
            x='Category',
            y='Price Range (₹)',
            color='Category',
            title="Price Comparison Across Market Segments",
            color_discrete_map={
                'Budget': 'green',
                'Mid-Range': 'orange', 
                'Premium': 'blue',
                'Luxury': 'purple',
                'Your Property': 'red'
            }
        )
        
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def analyze_feature_impact(self, predicted_price, location_popularity, 
                             environmental_score, size_sqft, bhk):
        """Analyze the impact of different features on price"""
        
        st.subheader("🔍 Feature Impact Analysis")
        
        # Feature contributions (simplified analysis)
        feature_impacts = {
            'Size': (size_sqft / 1000) * 0.3,  # Size impact
            'Location': location_popularity * 0.25,  # Location impact
            'Environment': environmental_score * 0.2,  # Environmental impact
            'BHK': (bhk / 3) * 0.15,  # BHK impact
            'Other Factors': 0.1  # Other factors
        }
        
        # Normalize to 100%
        total_impact = sum(feature_impacts.values())
        normalized_impacts = {k: (v/total_impact)*100 for k, v in feature_impacts.items()}
        
        # Create pie chart
        fig = px.pie(
            values=list(normalized_impacts.values()),
            names=list(normalized_impacts.keys()),
            title="Estimated Feature Contribution to Price"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature recommendations
        st.subheader("💡 Recommendations")
        
        recommendations = []
        
        if location_popularity < 0.5:
            recommendations.append("🏘️ **Location:** Consider properties in more popular areas for better appreciation")
        
        if environmental_score < 0.6:
            recommendations.append("🌱 **Environment:** Look for areas with better air quality and lower noise levels")
        
        if size_sqft / bhk < 800:
            recommendations.append("📐 **Space:** Consider larger properties for better space per bedroom")
        
        if not recommendations:
            recommendations.append("✅ **Great Choice:** This property has excellent characteristics!")
        
        for rec in recommendations:
            st.markdown(rec)

class VisualizationEngine:
    """
    Advanced visualization components
    """
    
    def __init__(self):
        self.color_schemes = {
            'default': px.colors.qualitative.Set3,
            'performance': px.colors.sequential.Viridis,
            'importance': px.colors.sequential.Plasma
        }
    
    def create_model_performance_dashboard(self, model_results):
        """Create comprehensive model performance dashboard"""
        
        if model_results is None:
            st.error("No model results available")
            return
        
        # Performance overview
        st.subheader("📊 Model Performance Overview")
        
        # Top models summary
        top_5 = model_results.head(5)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('R² Score Rankings', 'RMSE Comparison', 
                          'Model Performance Scatter', 'Training Time vs Accuracy'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # R² Score bar chart
        fig.add_trace(
            go.Bar(x=top_5['Model'], y=top_5['R²'], name='R² Score',
                  marker_color=px.colors.sequential.Viridis),
            row=1, col=1
        )
        
        # RMSE comparison
        fig.add_trace(
            go.Bar(x=top_5['Model'], y=top_5['RMSE'], name='RMSE',
                  marker_color=px.colors.sequential.Reds),
            row=1, col=2
        )
        
        # Performance scatter
        fig.add_trace(
            go.Scatter(x=model_results['RMSE'], y=model_results['R²'], 
                      mode='markers+text', text=model_results['Model'],
                      name='Models', marker=dict(size=10)),
            row=2, col=1
        )
        
        # Training time vs accuracy
        if 'Training_Time (s)' in model_results.columns:
            fig.add_trace(
                go.Scatter(x=model_results['Training_Time (s)'], y=model_results['R²'],
                          mode='markers+text', text=model_results['Model'],
                          name='Time vs Accuracy', marker=dict(size=10)),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    def create_feature_importance_visualization(self, feature_importance):
        """Create comprehensive feature importance visualization"""
        
        if feature_importance is None:
            st.error("No feature importance data available")
            return
        
        st.subheader("🔍 Feature Importance Analysis")
        
        # Top features
        top_20 = feature_importance.head(20)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Horizontal bar chart
            fig = px.bar(
                top_20,
                x='avg_importance',
                y='feature',
                orientation='h',
                title="Top 20 Most Important Features",
                color='avg_importance',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Treemap visualization
            fig = px.treemap(
                top_20,
                path=['feature'],
                values='avg_importance',
                title="Feature Importance Treemap"
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        # Cumulative importance
        sorted_importance = feature_importance.sort_values('avg_importance', ascending=False)
        sorted_importance['cumulative_percentage'] = (
            sorted_importance['avg_importance'].cumsum() / 
            sorted_importance['avg_importance'].sum() * 100
        )
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(1, min(51, len(sorted_importance) + 1))),
            y=sorted_importance.head(50)['cumulative_percentage'],
            mode='lines+markers',
            name='Cumulative Importance',
            line=dict(color='red', width=3)
        ))
        
        fig.add_hline(y=80, line_dash="dash", line_color="green", 
                     annotation_text="80% Threshold")
        fig.add_hline(y=95, line_dash="dash", line_color="orange", 
                     annotation_text="95% Threshold")
        
        fig.update_layout(
            title="Cumulative Feature Importance",
            xaxis_title="Number of Features",
            yaxis_title="Cumulative Importance (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_data_exploration_dashboard(self, df, target_col=None):
        """Create comprehensive data exploration dashboard"""
        
        if df is None or df.empty:
            st.error("No data available for exploration")
            return
        
        st.subheader("📊 Data Exploration Dashboard")
        
        # Basic statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Features", f"{len(df.columns):,}")
        with col3:
            st.metric("Missing Values", f"{df.isnull().sum().sum():,}")
        with col4:
            memory_mb = df.memory_usage(deep=True).sum() / 1024**2
            st.metric("Memory Usage", f"{memory_mb:.1f} MB")
        
        # Distribution analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if target_col and target_col in numeric_cols:
            # Target variable analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # Target distribution
                fig = px.histogram(df, x=target_col, bins=50, 
                                 title=f"Distribution of {target_col}")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Target boxplot
                fig = px.box(df, y=target_col, title=f"Box Plot of {target_col}")
                st.plotly_chart(fig, use_container_width=True)
            
            # Correlation with target
            correlations = df[numeric_cols].corr()[target_col].abs().sort_values(ascending=False)
            top_corr = correlations.head(15)
            
            fig = px.bar(
                x=top_corr.values,
                y=top_corr.index,
                orientation='h',
                title=f"Top Features Correlated with {target_col}",
                labels={'x': 'Absolute Correlation', 'y': 'Features'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature distributions
        if len(numeric_cols) > 0:
            selected_features = st.multiselect(
                "Select features to visualize:",
                numeric_cols[:20],  # Limit to first 20 for performance
                default=numeric_cols[:4]
            )
            
            if selected_features:
                n_cols = min(2, len(selected_features))
                n_rows = (len(selected_features) + 1) // 2
                
                fig = make_subplots(
                    rows=n_rows, cols=n_cols,
                    subplot_titles=selected_features
                )
                
                for i, feature in enumerate(selected_features):
                    row = (i // n_cols) + 1
                    col = (i % n_cols) + 1
                    
                    fig.add_trace(
                        go.Histogram(x=df[feature], name=feature, showlegend=False),
                        row=row, col=col
                    )
                
                fig.update_layout(height=300 * n_rows)
                st.plotly_chart(fig, use_container_width=True)

def create_comprehensive_dashboard():
    """Create the complete dashboard with all visualization components"""
    
    # Initialize components
    predictor = ModelPredictor()
    visualizer = VisualizationEngine()
    
    st.title("🏠 Real Estate Predictor - Complete Dashboard")
    
    # Sidebar for navigation
    st.sidebar.title("🧭 Dashboard Navigation")
    section = st.sidebar.radio(
        "Select Section:",
        ["🏠 Home", "🔮 Price Prediction", "📊 Model Analysis", 
         "📈 Data Exploration", "🎯 Feature Analysis"]
    )
    
    if section == "🏠 Home":
        st.markdown("## Welcome to Real Estate Price Predictor")
        st.markdown("""
        This comprehensive dashboard provides:
        - **Price Prediction**: AI-powered property price estimation
        - **Model Analysis**: Performance comparison of multiple ML models
        - **Data Exploration**: Interactive data visualization and analysis
        - **Feature Analysis**: Understanding what drives property prices
        """)
        
        # Quick stats
        if predictor.model_results is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Available Models", len(predictor.models))
            with col2:
                best_r2 = predictor.model_results['R²'].max()
                st.metric("Best Model Accuracy", f"{best_r2:.4f}")
            with col3:
                avg_rmse = predictor.model_results['RMSE'].mean()
                st.metric("Avg RMSE", f"₹{avg_rmse:,.0f}")
    
    elif section == "🔮 Price Prediction":
        st.markdown("## 🔮 AI-Powered Price Prediction")
        predictor.create_prediction_form()
    
    elif section == "📊 Model Analysis":
        st.markdown("## 📊 Model Performance Analysis")
        if predictor.model_results is not None:
            visualizer.create_model_performance_dashboard(predictor.model_results)
        else:
            st.error("Model results not available")
    
    elif section == "📈 Data Exploration":
        st.markdown("## 📈 Data Exploration")
        # Load and explore data
        data_path = "../feature_engineering/feature_engineered_expert.csv"
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            target_col = 'target_price' if 'target_price' in df.columns else 'Price_numeric'
            visualizer.create_data_exploration_dashboard(df, target_col)
        else:
            st.error("Data not available for exploration")
    
    elif section == "🎯 Feature Analysis":
        st.markdown("## 🎯 Feature Importance Analysis")
        importance_path = "../ensemble_learning/saved_models/feature_importance.csv"
        if os.path.exists(importance_path):
            feature_importance = pd.read_csv(importance_path)
            visualizer.create_feature_importance_visualization(feature_importance)
        else:
            st.error("Feature importance data not available")

if __name__ == "__main__":
    create_comprehensive_dashboard()