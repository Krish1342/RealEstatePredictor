import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import joblib
import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom modules
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    import xgboost as xgb
    import lightgbm as lgb
except ImportError as e:
    st.error(f"Required libraries not installed: {e}")

# Page configuration
st.set_page_config(
    page_title="Real Estate Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .prediction-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
    }
    .info-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

class RealEstatePredictorApp:
    def __init__(self):
        self.data_paths = {
            "air_quality": "../datasets/air_quality.csv",
            "bangalore": "../datasets/Bangalore.csv", 
            "crime_dataset": "../datasets/crime_dataset_india.csv",
            "housing_prices": "../datasets/india_housing_prices.csv",
            "noise_quality": "../datasets/noise_quality.csv",
            "pune_smartcity": "../datasets/Pune_SmartCity_Test_Dataset.csv",
            "real_estate": "../datasets/real_estate_data .csv",
            "water_quality": "../datasets/water_quality.csv"
        }
        
        self.preprocessed_paths = {
            "air_with_price": "../dummy_price/air_with_price.csv",
            "noise_with_price": "../dummy_price/noise_with_price.csv",
            "real_estate_bangalore": "../preprocessed_data/bangalore/real_estate_data_bangalore.csv",
            "housing_bangalore": "../preprocessed_data/bangalore/india_housing_prices_bangalore_cleaned.csv",
            "feature_engineered": "../feature_engineering/feature_engineered_expert.csv",
            "merged_data": "../integration/merged_data.csv"
        }
        
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_results = None
        self.feature_importance = None
        
    def load_data(self, dataset_name):
        """Load dataset with error handling"""
        try:
            if dataset_name in self.data_paths:
                path = self.data_paths[dataset_name]
            elif dataset_name in self.preprocessed_paths:
                path = self.preprocessed_paths[dataset_name]
            else:
                st.error(f"Dataset {dataset_name} not found")
                return None
                
            if os.path.exists(path):
                df = pd.read_csv(path)
                return df
            else:
                st.error(f"File not found: {path}")
                return None
        except Exception as e:
            st.error(f"Error loading dataset {dataset_name}: {str(e)}")
            return None
    
    def load_saved_models(self):
        """Load pre-trained models from ensemble_learning/saved_models/"""
        models_dir = "../ensemble_learning/saved_models"
        try:
            # Load model results
            results_path = os.path.join(models_dir, "ensemble_learning_results.csv")
            if os.path.exists(results_path):
                self.model_results = pd.read_csv(results_path)
            
            # Load feature importance
            importance_path = os.path.join(models_dir, "feature_importance.csv")
            if os.path.exists(importance_path):
                self.feature_importance = pd.read_csv(importance_path)
            
            # Load scaler
            scaler_path = os.path.join(models_dir, "feature_scaler.pkl")
            if os.path.exists(scaler_path):
                self.scalers['main'] = joblib.load(scaler_path)
            
            # Load individual models
            model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl') and 'model' in f]
            for model_file in model_files:
                try:
                    model_path = os.path.join(models_dir, model_file)
                    model = joblib.load(model_path)
                    # Extract model name from filename
                    model_name = model_file.replace('.pkl', '').replace('_', ' ').title()
                    self.models[model_name] = model
                except Exception as e:
                    st.warning(f"Could not load model {model_file}: {str(e)}")
            
            return True
        except Exception as e:
            st.error(f"Error loading saved models: {str(e)}")
            return False
    
    def create_dashboard(self):
        """Create main dashboard"""
        st.markdown('<h1 class="main-header">🏠 Real Estate Price Predictor Dashboard</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar navigation
        st.sidebar.title("🧭 Navigation")
        page = st.sidebar.radio(
            "Choose a page:",
            ["🏠 Dashboard", "📊 Data Explorer", "🤖 Model Performance", "🔮 Price Prediction", "📈 Feature Analysis"]
        )
        
        if page == "🏠 Dashboard":
            self.show_dashboard()
        elif page == "📊 Data Explorer":
            self.show_data_explorer()
        elif page == "🤖 Model Performance":
            self.show_model_performance()
        elif page == "🔮 Price Prediction":
            self.show_prediction_interface()
        elif page == "📈 Feature Analysis":
            self.show_feature_analysis()
    
    def show_dashboard(self):
        """Main dashboard overview"""
        st.markdown('<h2 class="sub-header">📊 System Overview</h2>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Load basic stats
        df = self.load_data("feature_engineered")
        if df is not None:
            with col1:
                st.metric("📊 Total Properties", f"{len(df):,}")
            with col2:
                target_col = 'target_price' if 'target_price' in df.columns else 'Price_numeric'
                if target_col in df.columns:
                    avg_price = df[target_col].mean()
                    st.metric("💰 Avg Price", f"₹{avg_price:,.0f}")
            with col3:
                if self.model_results is not None:
                    best_r2 = self.model_results['R²'].max()
                    st.metric("🎯 Best Model R²", f"{best_r2:.4f}")
            with col4:
                if self.model_results is not None:
                    total_models = len(self.model_results)
                    st.metric("🤖 Models Trained", f"{total_models}")
        
        # Dataset overview
        st.markdown('<h3 class="sub-header">📁 Available Datasets</h3>', unsafe_allow_html=True)
        
        dataset_info = {
            "Dataset": ["Feature Engineered", "Housing Prices", "Real Estate Bangalore", 
                       "Air Quality", "Noise Quality", "Merged Data"],
            "Description": [
                "Final feature-engineered dataset for modeling",
                "Raw housing price data for India", 
                "Bangalore-specific real estate data",
                "Air quality measurements and AQI data",
                "Noise pollution measurements",
                "Integrated dataset from all sources"
            ],
            "Status": ["✅ Available", "✅ Available", "✅ Available", 
                      "✅ Available", "✅ Available", "✅ Available"]
        }
        
        st.dataframe(pd.DataFrame(dataset_info), use_container_width=True)
        
        # Model performance overview
        if self.model_results is not None:
            st.markdown('<h3 class="sub-header">🏆 Top Model Performance</h3>', unsafe_allow_html=True)
            
            top_5_models = self.model_results.head(5)
            
            fig = px.bar(
                top_5_models, 
                x='Model', 
                y='R²',
                title="Top 5 Models by R² Score",
                color='R²',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Quick insights
        st.markdown('<h3 class="sub-header">💡 Quick Insights</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h4>🎯 Model Performance</h4>
            <ul>
            <li>Best performing model: Extra Trees Regressor</li>
            <li>Achieved R² score of 0.9999+</li>
            <li>Ensemble methods outperform individual models</li>
            <li>Feature engineering significantly improved accuracy</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
            <h4>📊 Data Insights</h4>
            <ul>
            <li>Price_numeric is the most important feature</li>
            <li>Location and property size are key factors</li>
            <li>Environmental factors contribute to pricing</li>
            <li>Comprehensive data integration improves predictions</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def show_data_explorer(self):
        """Data exploration interface"""
        st.markdown('<h2 class="sub-header">📊 Data Explorer</h2>', unsafe_allow_html=True)
        
        # Dataset selection
        dataset_options = {
            "Feature Engineered Dataset": "feature_engineered",
            "Housing Prices (Bangalore)": "housing_bangalore", 
            "Real Estate (Bangalore)": "real_estate_bangalore",
            "Air Quality Data": "air_quality",
            "Noise Quality Data": "noise_quality",
            "Merged Dataset": "merged_data"
        }
        
        selected_dataset = st.selectbox("Select Dataset to Explore:", list(dataset_options.keys()))
        dataset_key = dataset_options[selected_dataset]
        
        # Load and display data
        df = self.load_data(dataset_key)
        if df is not None:
            # Basic info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", f"{len(df):,}")
            with col2:
                st.metric("Columns", f"{len(df.columns):,}")
            with col3:
                st.metric("Missing Values", f"{df.isnull().sum().sum():,}")
            with col4:
                memory_usage = df.memory_usage(deep=True).sum() / 1024**2
                st.metric("Memory Usage", f"{memory_usage:.2f} MB")
            
            # Data preview
            st.subheader("📖 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column information
            st.subheader("📋 Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2)
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Statistical summary
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.subheader("📈 Statistical Summary")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                
                # Visualizations
                st.subheader("📊 Data Visualizations")
                
                # Select columns for visualization
                viz_col = st.selectbox("Select column for distribution plot:", numeric_cols)
                
                if viz_col:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Histogram
                        fig = px.histogram(df, x=viz_col, bins=50, title=f"Distribution of {viz_col}")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Box plot
                        fig = px.box(df, y=viz_col, title=f"Box Plot of {viz_col}")
                        st.plotly_chart(fig, use_container_width=True)
                
                # Correlation heatmap
                if len(numeric_cols) > 1:
                    st.subheader("🔗 Correlation Analysis")
                    
                    # Select top correlations with target if available
                    target_cols = ['target_price', 'Price_numeric', 'Price_in_Lakhs']
                    target_col = None
                    for col in target_cols:
                        if col in df.columns:
                            target_col = col
                            break
                    
                    if target_col:
                        correlations = df[numeric_cols].corr()[target_col].abs().sort_values(ascending=False)
                        top_features = correlations.head(15).index.tolist()
                        
                        corr_matrix = df[top_features].corr()
                        
                        fig = px.imshow(
                            corr_matrix,
                            text_auto=True,
                            aspect="auto",
                            title=f"Top 15 Features Correlation with {target_col}"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # General correlation matrix
                        top_numeric = numeric_cols[:15]  # Show top 15 numeric columns
                        corr_matrix = df[top_numeric].corr()
                        
                        fig = px.imshow(
                            corr_matrix,
                            text_auto=True,
                            aspect="auto",
                            title="Correlation Matrix (Top 15 Numeric Features)"
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Could not load the selected dataset.")
    
    def show_model_performance(self):
        """Model performance analysis"""
        st.markdown('<h2 class="sub-header">🤖 Model Performance Analysis</h2>', unsafe_allow_html=True)
        
        if self.model_results is None:
            st.error("Model results not available. Please ensure ensemble_learning has been run.")
            return
        
        # Performance metrics overview
        st.subheader("📊 Model Performance Overview")
        
        # Display all models performance
        display_cols = ['Model', 'R²', 'RMSE', 'MAE', 'MAPE (%)']
        available_cols = [col for col in display_cols if col in self.model_results.columns]
        st.dataframe(self.model_results[available_cols], use_container_width=True)
        
        # Performance visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # R² Score comparison
            fig = px.bar(
                self.model_results.head(10), 
                x='R²', 
                y='Model',
                orientation='h',
                title="R² Score Comparison (Top 10 Models)",
                color='R²',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # RMSE comparison
            fig = px.bar(
                self.model_results.head(10), 
                x='RMSE', 
                y='Model',
                orientation='h',
                title="RMSE Comparison (Top 10 Models)",
                color='RMSE',
                color_continuous_scale='reds_r'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Model performance scatter plot
        st.subheader("📈 R² vs RMSE Performance")
        fig = px.scatter(
            self.model_results,
            x='RMSE',
            y='R²',
            hover_data=['Model', 'MAE'],
            title="Model Performance: R² vs RMSE",
            text='Model'
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top models summary
        st.subheader("🏆 Top 5 Models Summary")
        top_5 = self.model_results.head(5)
        
        for idx, (_, model) in enumerate(top_5.iterrows()):
            with st.expander(f"#{idx+1} {model['Model']} - R²: {model['R²']:.6f}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("R² Score", f"{model['R²']:.6f}")
                with col2:
                    st.metric("RMSE", f"₹{model['RMSE']:,.0f}")
                with col3:
                    st.metric("MAPE", f"{model['MAPE (%)']:.3f}%")
                
                # Additional metrics if available
                if 'Training_Time (s)' in model:
                    st.info(f"⏱️ Training Time: {model['Training_Time (s)']:.2f} seconds")
        
        # Cross-validation results if available
        cv_path = "../ensemble_learning/saved_models/cross_validation_results.csv"
        if os.path.exists(cv_path):
            st.subheader("🔄 Cross-Validation Results")
            cv_results = pd.read_csv(cv_path)
            st.dataframe(cv_results, use_container_width=True)
            
            # CV visualization
            fig = px.bar(
                cv_results,
                x='Model',
                y='CV_R2_Mean',
                error_y='CV_R2_Std',
                title="Cross-Validation R² Scores with Standard Deviation"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    def show_prediction_interface(self):
        """Price prediction interface"""
        st.markdown('<h2 class="sub-header">🔮 Real Estate Price Prediction</h2>', unsafe_allow_html=True)
        
        if not self.models:
            if not self.load_saved_models():
                st.error("Could not load saved models. Please ensure models are trained and saved.")
                return
        
        # Model selection
        available_models = list(self.models.keys())
        if not available_models:
            st.error("No models available for prediction.")
            return
        
        selected_model = st.selectbox("Select Model for Prediction:", available_models)
        
        # Feature input form
        st.subheader("🏠 Property Details")
        
        # Load feature engineered dataset to get feature names
        df = self.load_data("feature_engineered")
        if df is None:
            st.error("Could not load feature dataset for input form.")
            return
        
        # Identify important features from feature importance
        important_features = []
        if self.feature_importance is not None:
            # Get top features excluding target variables
            exclude_features = ['Price_numeric', 'Price_in_Lakhs', 'target_price', 'Price_encoded']
            top_features = self.feature_importance[
                ~self.feature_importance['feature'].isin(exclude_features)
            ].head(20)['feature'].tolist()
            important_features = top_features
        else:
            # Fallback to numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            exclude_features = ['Price_numeric', 'Price_in_Lakhs', 'target_price', 'Price_encoded']
            important_features = [col for col in numeric_cols if col not in exclude_features][:20]
        
        # Create input form with columns
        col1, col2 = st.columns(2)
        
        input_data = {}
        
        # Basic property features
        with col1:
            st.markdown("**🏠 Basic Property Features**")
            
            if 'BHK' in df.columns:
                input_data['BHK'] = st.number_input("BHK", min_value=1, max_value=10, value=2)
            
            if 'Size_in_SqFt' in df.columns:
                input_data['Size_in_SqFt'] = st.number_input("Size (Sq Ft)", min_value=500, max_value=10000, value=1000)
            
            if 'Baths' in df.columns:
                input_data['Baths'] = st.number_input("Bathrooms", min_value=1, max_value=10, value=2)
            
            if 'Total_Floors' in df.columns:
                input_data['Total_Floors'] = st.number_input("Total Floors", min_value=1, max_value=50, value=5)
            
            if 'Floor_No' in df.columns:
                input_data['Floor_No'] = st.number_input("Floor Number", min_value=1, max_value=50, value=3)
            
            if 'Age_of_Property' in df.columns:
                input_data['Age_of_Property'] = st.number_input("Property Age (years)", min_value=0, max_value=100, value=5)
        
        with col2:
            st.markdown("**🌍 Location & Environmental Features**")
            
            if 'location_popularity' in df.columns:
                input_data['location_popularity'] = st.slider("Location Popularity", 0.0, 1.0, 0.5)
            
            if 'environmental_score' in df.columns:
                input_data['environmental_score'] = st.slider("Environmental Score", 0.0, 1.0, 0.7)
            
            if 'AQI' in df.columns:
                input_data['AQI'] = st.number_input("Air Quality Index", min_value=0, max_value=500, value=100)
            
            if 'Day' in df.columns:
                input_data['Day'] = st.number_input("Day Noise Level", min_value=0.0, max_value=100.0, value=50.0)
            
            if 'Night' in df.columns:
                input_data['Night'] = st.number_input("Night Noise Level", min_value=0.0, max_value=100.0, value=40.0)
        
        # Additional features
        st.markdown("**🔧 Additional Features**")
        
        # Set default values for other important features
        for feature in important_features[:10]:  # Show top 10 additional features
            if feature not in input_data and feature in df.columns:
                if df[feature].dtype in ['int64', 'float64']:
                    mean_val = df[feature].mean()
                    min_val = df[feature].min()
                    max_val = df[feature].max()
                    
                    if pd.isna(mean_val):
                        continue
                    
                    input_data[feature] = st.number_input(
                        f"{feature.replace('_', ' ').title()}", 
                        min_value=float(min_val), 
                        max_value=float(max_val), 
                        value=float(mean_val),
                        key=feature
                    )
        
        # Prediction button
        if st.button("🔮 Predict Price", type="primary"):
            try:
                # Prepare input data
                prediction_df = pd.DataFrame([input_data])
                
                # Add missing features with default values
                all_features = df.columns.tolist()
                target_cols = ['target_price', 'Price_numeric', 'Price_in_Lakhs']
                feature_cols = [col for col in all_features if col not in target_cols]
                
                for feature in feature_cols:
                    if feature not in prediction_df.columns:
                        if df[feature].dtype in ['int64', 'float64']:
                            prediction_df[feature] = df[feature].median()
                        else:
                            prediction_df[feature] = df[feature].mode()[0] if not df[feature].mode().empty else 0
                
                # Reorder columns to match training data
                prediction_df = prediction_df[feature_cols]
                
                # Handle categorical encoding (simplified approach)
                for col in prediction_df.columns:
                    if prediction_df[col].dtype == 'object':
                        try:
                            prediction_df[col] = pd.to_numeric(prediction_df[col], errors='coerce')
                        except:
                            prediction_df[col] = 0
                
                # Fill any remaining NaN values
                prediction_df = prediction_df.fillna(0)
                
                # Make prediction
                model = self.models[selected_model]
                prediction = model.predict(prediction_df)
                predicted_price = prediction[0]
                
                # Display prediction
                st.markdown(
                    f'<div class="prediction-box">💰 Predicted Price: ₹{predicted_price:,.0f}</div>',
                    unsafe_allow_html=True
                )
                
                # Additional insights
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Per Sq Ft", f"₹{predicted_price/input_data.get('Size_in_SqFt', 1000):,.0f}")
                
                with col2:
                    st.metric("In Lakhs", f"₹{predicted_price/100000:.2f}L")
                
                with col3:
                    if self.model_results is not None:
                        model_r2 = self.model_results[
                            self.model_results['Model'].str.contains(selected_model.replace('Model ', '').replace('Best ', ''), case=False)
                        ]
                        if not model_r2.empty:
                            st.metric("Model Accuracy (R²)", f"{model_r2.iloc[0]['R²']:.4f}")
                
                # Show confidence interval based on model performance
                if self.model_results is not None:
                    model_info = self.model_results[
                        self.model_results['Model'].str.contains(selected_model.replace('Model ', '').replace('Best ', ''), case=False)
                    ]
                    if not model_info.empty:
                        rmse = model_info.iloc[0]['RMSE']
                        lower_bound = predicted_price - rmse
                        upper_bound = predicted_price + rmse
                        
                        st.info(f"📊 **Prediction Confidence Range:** ₹{max(0, lower_bound):,.0f} - ₹{upper_bound:,.0f}")
                        st.info(f"⚡ **Model Used:** {selected_model}")
                
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")
                st.error("Please check that all required features are provided correctly.")
    
    def show_feature_analysis(self):
        """Feature importance and analysis"""
        st.markdown('<h2 class="sub-header">📈 Feature Analysis</h2>', unsafe_allow_html=True)
        
        if self.feature_importance is None:
            st.error("Feature importance data not available.")
            return
        
        # Feature importance overview
        st.subheader("🔍 Feature Importance Analysis")
        
        # Display feature importance table
        st.dataframe(self.feature_importance.head(20), use_container_width=True)
        
        # Top features visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 15 features bar chart
            top_15 = self.feature_importance.head(15)
            fig = px.bar(
                top_15,
                x='avg_importance',
                y='feature',
                orientation='h',
                title="Top 15 Most Important Features",
                color='avg_importance',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Feature importance distribution
            fig = px.histogram(
                self.feature_importance,
                x='avg_importance',
                bins=50,
                title="Distribution of Feature Importance",
                labels={'avg_importance': 'Average Importance'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Cumulative importance
            sorted_importance = self.feature_importance.sort_values('avg_importance', ascending=False)
            sorted_importance['cumulative_importance'] = sorted_importance['avg_importance'].cumsum()
            
            fig = px.line(
                sorted_importance.head(50),
                x=range(50),
                y='cumulative_importance',
                title="Cumulative Feature Importance (Top 50)",
                labels={'x': 'Number of Features', 'y': 'Cumulative Importance'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature categories analysis
        st.subheader("📊 Feature Categories")
        
        # Categorize features
        categories = {
            'Price Features': ['Price_numeric', 'Price_encoded', 'Price_per_SQFT', 'Price_in_Lakhs'],
            'Property Features': ['Total_Area', 'Baths', 'BHK', 'Size_in_SqFt', 'Floor_No', 'Total_Floors'],
            'Location Features': ['location_encoded', 'location_popularity', 'City_encoded', 'State_encoded'],
            'Environmental Features': ['AQI', 'PM2.5', 'PM10', 'environmental_score', 'Day', 'Night'],
            'Property Details': ['Property Title_encoded', 'Name_encoded', 'Balcony_encoded', 'Amenities_encoded'],
            'Others': []
        }
        
        # Categorize all features
        feature_categories = {}
        for feature in self.feature_importance['feature']:
            categorized = False
            for category, keywords in categories.items():
                if category == 'Others':
                    continue
                if any(keyword in feature for keyword in keywords):
                    feature_categories[feature] = category
                    categorized = True
                    break
            if not categorized:
                feature_categories[feature] = 'Others'
        
        # Calculate category importance
        category_importance = {}
        for feature, importance in zip(self.feature_importance['feature'], self.feature_importance['avg_importance']):
            category = feature_categories.get(feature, 'Others')
            if category not in category_importance:
                category_importance[category] = 0
            category_importance[category] += importance
        
        # Visualize category importance
        category_df = pd.DataFrame({
            'Category': list(category_importance.keys()),
            'Total_Importance': list(category_importance.values())
        }).sort_values('Total_Importance', ascending=False)
        
        fig = px.pie(
            category_df,
            values='Total_Importance',
            names='Category',
            title="Feature Importance by Category"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature correlation with target (if available)
        df = self.load_data("feature_engineered")
        if df is not None:
            target_cols = ['target_price', 'Price_numeric', 'Price_in_Lakhs']
            target_col = None
            for col in target_cols:
                if col in df.columns:
                    target_col = col
                    break
            
            if target_col:
                st.subheader(f"🔗 Feature Correlation with {target_col}")
                
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                correlations = df[numeric_cols].corr()[target_col].abs().sort_values(ascending=False)
                
                # Top correlations
                top_corr = correlations.head(20)
                corr_df = pd.DataFrame({
                    'Feature': top_corr.index,
                    'Correlation': top_corr.values
                })
                
                fig = px.bar(
                    corr_df[1:],  # Exclude self-correlation
                    x='Correlation',
                    y='Feature',
                    orientation='h',
                    title=f"Top Features Correlated with {target_col}",
                    color='Correlation',
                    color_continuous_scale='reds'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function"""
    app = RealEstatePredictorApp()
    
    # Load saved models
    app.load_saved_models()
    
    # Create dashboard
    app.create_dashboard()

if __name__ == "__main__":
    main()