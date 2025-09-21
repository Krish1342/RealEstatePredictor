"""
Data preprocessing and feature engineering utilities for Real Estate Predictor
Based on the existing preprocessing notebooks and feature engineering pipeline
"""

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler, RobustScaler, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    """
    Data preprocessing utilities based on existing preprocessing notebooks
    """
    
    def __init__(self):
        self.label_encoders = {}
        self.scalers = {}
        
    def load_raw_datasets(self):
        """Load all raw datasets"""
        datasets = {}
        
        # Dataset paths
        data_paths = {
            "air_quality": "../datasets/air_quality.csv",
            "bangalore": "../datasets/Bangalore.csv", 
            "crime_dataset": "../datasets/crime_dataset_india.csv",
            "housing_prices": "../datasets/india_housing_prices.csv",
            "noise_quality": "../datasets/noise_quality.csv",
            "pune_smartcity": "../datasets/Pune_SmartCity_Test_Dataset.csv",
            "real_estate": "../datasets/real_estate_data .csv",
            "water_quality": "../datasets/water_quality.csv"
        }
        
        for name, path in data_paths.items():
            if os.path.exists(path):
                try:
                    datasets[name] = pd.read_csv(path)
                    print(f"✅ Loaded {name}: {datasets[name].shape}")
                except Exception as e:
                    print(f"❌ Error loading {name}: {e}")
            else:
                print(f"⚠️ File not found: {path}")
        
        return datasets
    
    def preprocess_air_quality(self, df):
        """Preprocess air quality data"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Handle missing values
        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            processed_df[col] = processed_df[col].fillna(processed_df[col].median())
        
        # Handle categorical columns
        categorical_cols = processed_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            processed_df[col] = processed_df[col].fillna(processed_df[col].mode()[0] if not processed_df[col].mode().empty else 'Unknown')
        
        # Create AQI categories
        if 'AQI' in processed_df.columns:
            processed_df['AQI_Category'] = pd.cut(
                processed_df['AQI'], 
                bins=[0, 50, 100, 150, 200, 300, float('inf')],
                labels=['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe'],
                include_lowest=True
            )
        
        # Log transform for pollutants
        pollutant_cols = ['PM2.5', 'PM10', 'NO', 'NO2', 'SO2', 'CO', 'O3', 'NH3']
        for col in pollutant_cols:
            if col in processed_df.columns:
                processed_df[f'{col}_log'] = np.log1p(processed_df[col])
        
        return processed_df
    
    def preprocess_noise_quality(self, df):
        """Preprocess noise quality data"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Handle missing values
        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            processed_df[col] = processed_df[col].fillna(processed_df[col].median())
        
        # Create noise level categories
        if 'Day' in processed_df.columns:
            processed_df['Day_Category'] = pd.cut(
                processed_df['Day'],
                bins=[0, 55, 65, 75, float('inf')],
                labels=['Quiet', 'Moderate', 'Loud', 'Very Loud'],
                include_lowest=True
            )
        
        if 'Night' in processed_df.columns:
            processed_df['Night_Category'] = pd.cut(
                processed_df['Night'],
                bins=[0, 45, 55, 65, float('inf')],
                labels=['Quiet', 'Moderate', 'Loud', 'Very Loud'],
                include_lowest=True
            )
        
        # Calculate excess noise
        if 'Day' in processed_df.columns and 'DayLimit' in processed_df.columns:
            processed_df['DayExcess'] = np.maximum(0, processed_df['Day'] - processed_df['DayLimit'])
        
        if 'Night' in processed_df.columns and 'NightLimit' in processed_df.columns:
            processed_df['NightExcess'] = np.maximum(0, processed_df['Night'] - processed_df['NightLimit'])
        
        return processed_df
    
    def preprocess_real_estate(self, df):
        """Preprocess real estate data"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Clean price columns
        price_columns = ['Price', 'Price_in_Lakhs', 'price']
        for col in price_columns:
            if col in processed_df.columns:
                # Remove non-numeric characters and convert
                if processed_df[col].dtype == 'object':
                    processed_df[col] = processed_df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
                    processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
        
        # Clean area/size columns
        area_columns = ['Area', 'Size', 'Size_in_SqFt', 'area', 'Total_Area']
        for col in area_columns:
            if col in processed_df.columns:
                if processed_df[col].dtype == 'object':
                    processed_df[col] = processed_df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
                    processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
        
        # Clean BHK column
        if 'BHK' in processed_df.columns:
            processed_df['BHK'] = processed_df['BHK'].astype(str).str.extract(r'(\d+)').astype(float)
        
        # Create price per sqft
        price_col = None
        area_col = None
        
        for col in price_columns:
            if col in processed_df.columns and processed_df[col].notna().sum() > 0:
                price_col = col
                break
        
        for col in area_columns:
            if col in processed_df.columns and processed_df[col].notna().sum() > 0:
                area_col = col
                break
        
        if price_col and area_col:
            processed_df['Price_per_SqFt'] = processed_df[price_col] / processed_df[area_col]
        
        # Handle missing values
        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            processed_df[col] = processed_df[col].fillna(processed_df[col].median())
        
        categorical_cols = processed_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            processed_df[col] = processed_df[col].fillna(processed_df[col].mode()[0] if not processed_df[col].mode().empty else 'Unknown')
        
        return processed_df
    
    def preprocess_housing_prices(self, df):
        """Preprocess housing prices data"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Standardize column names
        column_mapping = {
            'Area': 'Total_Area',
            'Size': 'Size_in_SqFt',
            'Price': 'Price_numeric',
            'Locality': 'location'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in processed_df.columns:
                processed_df = processed_df.rename(columns={old_col: new_col})
        
        # Clean price data
        if 'Price_numeric' in processed_df.columns:
            processed_df['Price_numeric'] = pd.to_numeric(processed_df['Price_numeric'], errors='coerce')
        
        # Create property age from year built
        if 'Year_Built' in processed_df.columns:
            current_year = pd.Timestamp.now().year
            processed_df['Age_of_Property'] = current_year - processed_df['Year_Built']
        
        # Handle missing values
        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            processed_df[col] = processed_df[col].fillna(processed_df[col].median())
        
        categorical_cols = processed_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            processed_df[col] = processed_df[col].fillna(processed_df[col].mode()[0] if not processed_df[col].mode().empty else 'Unknown')
        
        return processed_df

class FeatureEngineer:
    """
    Feature engineering utilities based on existing feature engineering notebook
    """
    
    def __init__(self):
        self.encoders = {}
        
    def create_basic_features(self, df):
        """Create basic engineered features"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Price per square foot
        if 'Price_numeric' in processed_df.columns and 'Size_in_SqFt' in processed_df.columns:
            processed_df['Price_per_SQFT'] = processed_df['Price_numeric'] / processed_df['Size_in_SqFt']
        
        # Area per bedroom
        if 'Size_in_SqFt' in processed_df.columns and 'BHK' in processed_df.columns:
            processed_df['area_per_bedroom'] = processed_df['Size_in_SqFt'] / processed_df['BHK']
        
        # Bath to bedroom ratio
        if 'Baths' in processed_df.columns and 'BHK' in processed_df.columns:
            processed_df['bath_bedroom_ratio'] = processed_df['Baths'] / processed_df['BHK']
        
        # Floor ratio
        if 'Floor_No' in processed_df.columns and 'Total_Floors' in processed_df.columns:
            processed_df['Floor_Ratio'] = processed_df['Floor_No'] / processed_df['Total_Floors']
        
        # Create size categories
        if 'Size_in_SqFt' in processed_df.columns:
            processed_df['size_category'] = pd.cut(
                processed_df['Size_in_SqFt'],
                bins=[0, 600, 1000, 1500, 2500, float('inf')],
                labels=['Small', 'Medium', 'Large', 'Extra Large', 'Luxury'],
                include_lowest=True
            )
        
        return processed_df
    
    def create_interaction_features(self, df):
        """Create interaction features"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # BHK and Size interaction
        if 'BHK' in processed_df.columns and 'Size_in_SqFt' in processed_df.columns:
            processed_df['BHK_Size_in_SqFt_interaction'] = processed_df['BHK'] * processed_df['Size_in_SqFt']
        
        # Baths and BHK interaction
        if 'Baths' in processed_df.columns and 'BHK' in processed_df.columns:
            processed_df['Baths_BHK_interaction'] = processed_df['Baths'] * processed_df['BHK']
        
        # Age and price interaction
        if 'Age_of_Property' in processed_df.columns and 'Price_numeric' in processed_df.columns:
            processed_df['Age_Price_interaction'] = processed_df['Age_of_Property'] * processed_df['Price_numeric']
        
        return processed_df
    
    def create_log_features(self, df):
        """Create log-transformed features"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Log transform numerical features
        log_features = ['Price_numeric', 'Size_in_SqFt', 'Total_Area']
        
        for feature in log_features:
            if feature in processed_df.columns:
                # Add 1 to handle zero values
                processed_df[f'{feature}_log'] = np.log1p(processed_df[feature])
        
        # Square root transforms
        sqrt_features = ['Price_numeric', 'Size_in_SqFt']
        
        for feature in sqrt_features:
            if feature in processed_df.columns:
                processed_df[f'{feature}_sqrt'] = np.sqrt(processed_df[feature])
        
        return processed_df
    
    def encode_categorical_features(self, df, fit=True):
        """Encode categorical features"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Get categorical columns
        categorical_cols = processed_df.select_dtypes(include=['object', 'category']).columns
        
        for col in categorical_cols:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
            
            # Handle missing values first
            processed_df[col] = processed_df[col].fillna('Unknown')
            
            if fit:
                # Fit and transform
                processed_df[f'{col}_encoded'] = self.encoders[col].fit_transform(processed_df[col].astype(str))
            else:
                # Transform only (for prediction)
                try:
                    processed_df[f'{col}_encoded'] = self.encoders[col].transform(processed_df[col].astype(str))
                except ValueError:
                    # Handle unseen categories
                    processed_df[f'{col}_encoded'] = 0
        
        return processed_df
    
    def create_environmental_score(self, df):
        """Create environmental quality score"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Normalize AQI (lower is better)
        if 'AQI' in processed_df.columns:
            max_aqi = processed_df['AQI'].max()
            processed_df['AQI_normalized'] = 1 - (processed_df['AQI'] / max_aqi)
        
        # Normalize noise levels (lower is better)
        noise_score = 0
        noise_count = 0
        
        if 'Day' in processed_df.columns:
            max_day_noise = processed_df['Day'].max()
            day_score = 1 - (processed_df['Day'] / max_day_noise)
            noise_score += day_score
            noise_count += 1
        
        if 'Night' in processed_df.columns:
            max_night_noise = processed_df['Night'].max()
            night_score = 1 - (processed_df['Night'] / max_night_noise)
            noise_score += night_score
            noise_count += 1
        
        if noise_count > 0:
            processed_df['noise_score'] = noise_score / noise_count
        
        # Combine environmental factors
        env_factors = []
        if 'AQI_normalized' in processed_df.columns:
            env_factors.append('AQI_normalized')
        if 'noise_score' in processed_df.columns:
            env_factors.append('noise_score')
        
        if env_factors:
            processed_df['environmental_score'] = processed_df[env_factors].mean(axis=1)
        
        return processed_df
    
    def create_location_features(self, df):
        """Create location-based features"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Location popularity based on price
        if 'location' in processed_df.columns and 'Price_numeric' in processed_df.columns:
            location_stats = processed_df.groupby('location')['Price_numeric'].agg(['mean', 'count']).reset_index()
            location_stats['location_popularity'] = (
                location_stats['mean'] * np.log(location_stats['count'] + 1)
            ) / (location_stats['mean'].max() * np.log(location_stats['count'].max() + 1))
            
            processed_df = processed_df.merge(location_stats[['location', 'location_popularity']], 
                                            on='location', how='left')
            
            # Log transform location popularity
            processed_df['location_popularity_log'] = np.log1p(processed_df['location_popularity'])
        
        return processed_df

class DataIntegrator:
    """
    Data integration utilities based on integration/logic.ipynb
    """
    
    def __init__(self):
        self.imputers = {}
    
    def merge_datasets(self, housing_df, real_estate_df, air_quality_df, noise_quality_df, on_column='location'):
        """Merge multiple datasets"""
        
        # Standardize location column names
        if 'Locality' in housing_df.columns:
            housing_df = housing_df.rename(columns={'Locality': on_column})
        if 'Location' in real_estate_df.columns:
            real_estate_df = real_estate_df.rename(columns={'Location': on_column})
        if 'City' in air_quality_df.columns:
            air_quality_df = air_quality_df.rename(columns={'City': on_column})
        if 'Station' in noise_quality_df.columns:
            noise_quality_df = noise_quality_df.rename(columns={'Station': on_column})
        
        # Start with housing data
        merged_df = housing_df.copy()
        
        # Merge with real estate data
        merged_df = merged_df.merge(real_estate_df, on=on_column, how='outer', suffixes=('', '_re'))
        
        # Merge with air quality data
        merged_df = merged_df.merge(air_quality_df, on=on_column, how='outer', suffixes=('', '_aq'))
        
        # Merge with noise quality data
        merged_df = merged_df.merge(noise_quality_df, on=on_column, how='outer', suffixes=('', '_nq'))
        
        # Drop duplicates
        merged_df = merged_df.drop_duplicates()
        
        return merged_df
    
    def impute_missing_values(self, df, strategy='mean'):
        """Impute missing values using different strategies"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Separate numeric and categorical columns
        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
        categorical_cols = processed_df.select_dtypes(exclude=[np.number]).columns
        
        # Remove columns that are all null
        null_only_cols = numeric_cols[processed_df[numeric_cols].isnull().all()].tolist()
        valid_numeric_cols = [col for col in numeric_cols if col not in null_only_cols]
        
        if valid_numeric_cols:
            # Impute numeric columns
            if strategy == 'mean':
                imputer = SimpleImputer(strategy='mean')
            elif strategy == 'median':
                imputer = SimpleImputer(strategy='median')
            elif strategy == 'knn':
                imputer = KNNImputer(n_neighbors=5)
            else:
                imputer = SimpleImputer(strategy='mean')
            
            processed_df[valid_numeric_cols] = imputer.fit_transform(processed_df[valid_numeric_cols])
            self.imputers[f'numeric_{strategy}'] = imputer
        
        # Impute categorical columns
        for col in categorical_cols:
            mode_value = processed_df[col].mode()
            if not mode_value.empty:
                processed_df[col] = processed_df[col].fillna(mode_value[0])
            else:
                processed_df[col] = processed_df[col].fillna('Unknown')
        
        return processed_df
    
    def create_target_variable(self, df):
        """Create target variable for modeling"""
        if df is None or df.empty:
            return df
            
        processed_df = df.copy()
        
        # Priority order for price columns
        price_columns = ['Price_numeric', 'Price_in_Lakhs', 'Price', 'price']
        
        target_col = None
        for col in price_columns:
            if col in processed_df.columns and processed_df[col].notna().sum() > 0:
                target_col = col
                break
        
        if target_col:
            processed_df['target_price'] = processed_df[target_col]
            
            # Convert to numeric if needed
            if processed_df['target_price'].dtype == 'object':
                processed_df['target_price'] = pd.to_numeric(processed_df['target_price'], errors='coerce')
            
            # Remove outliers using IQR method
            Q1 = processed_df['target_price'].quantile(0.25)
            Q3 = processed_df['target_price'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Filter outliers
            initial_count = len(processed_df)
            processed_df = processed_df[
                (processed_df['target_price'] >= lower_bound) & 
                (processed_df['target_price'] <= upper_bound) &
                (processed_df['target_price'].notna())
            ]
            
            print(f"Removed {initial_count - len(processed_df)} outliers from target variable")
        
        return processed_df

def create_full_pipeline():
    """Create complete data processing pipeline"""
    
    print("🚀 Starting Full Data Processing Pipeline...")
    
    # Initialize processors
    preprocessor = DataPreprocessor()
    feature_engineer = FeatureEngineer()
    integrator = DataIntegrator()
    
    # Step 1: Load raw datasets
    print("\n📁 Step 1: Loading raw datasets...")
    datasets = preprocessor.load_raw_datasets()
    
    if not datasets:
        print("❌ No datasets loaded. Please check file paths.")
        return None
    
    # Step 2: Preprocess individual datasets
    print("\n🔧 Step 2: Preprocessing individual datasets...")
    
    processed_datasets = {}
    
    if 'air_quality' in datasets:
        processed_datasets['air_quality'] = preprocessor.preprocess_air_quality(datasets['air_quality'])
        print(f"✅ Air quality processed: {processed_datasets['air_quality'].shape}")
    
    if 'noise_quality' in datasets:
        processed_datasets['noise_quality'] = preprocessor.preprocess_noise_quality(datasets['noise_quality'])
        print(f"✅ Noise quality processed: {processed_datasets['noise_quality'].shape}")
    
    if 'real_estate' in datasets:
        processed_datasets['real_estate'] = preprocessor.preprocess_real_estate(datasets['real_estate'])
        print(f"✅ Real estate processed: {processed_datasets['real_estate'].shape}")
    
    if 'housing_prices' in datasets:
        processed_datasets['housing_prices'] = preprocessor.preprocess_housing_prices(datasets['housing_prices'])
        print(f"✅ Housing prices processed: {processed_datasets['housing_prices'].shape}")
    
    # Step 3: Merge datasets
    print("\n🔗 Step 3: Merging datasets...")
    
    required_datasets = ['housing_prices', 'real_estate', 'air_quality', 'noise_quality']
    if all(ds in processed_datasets for ds in required_datasets):
        merged_df = integrator.merge_datasets(
            processed_datasets['housing_prices'],
            processed_datasets['real_estate'],
            processed_datasets['air_quality'],
            processed_datasets['noise_quality']
        )
        print(f"✅ Datasets merged: {merged_df.shape}")
    else:
        print("⚠️ Not all required datasets available for merging. Using available data...")
        merged_df = list(processed_datasets.values())[0]
        for df in list(processed_datasets.values())[1:]:
            try:
                merged_df = pd.concat([merged_df, df], ignore_index=True, sort=False)
            except Exception as e:
                print(f"Warning: Could not concatenate dataset: {e}")
    
    # Step 4: Handle missing values
    print("\n🔄 Step 4: Handling missing values...")
    merged_df = integrator.impute_missing_values(merged_df, strategy='median')
    print(f"✅ Missing values handled: {merged_df.shape}")
    
    # Step 5: Create target variable
    print("\n🎯 Step 5: Creating target variable...")
    merged_df = integrator.create_target_variable(merged_df)
    print(f"✅ Target variable created: {merged_df.shape}")
    
    # Step 6: Feature engineering
    print("\n⚙️ Step 6: Feature engineering...")
    
    # Basic features
    merged_df = feature_engineer.create_basic_features(merged_df)
    print("✅ Basic features created")
    
    # Interaction features
    merged_df = feature_engineer.create_interaction_features(merged_df)
    print("✅ Interaction features created")
    
    # Log features
    merged_df = feature_engineer.create_log_features(merged_df)
    print("✅ Log-transformed features created")
    
    # Environmental score
    merged_df = feature_engineer.create_environmental_score(merged_df)
    print("✅ Environmental score created")
    
    # Location features
    merged_df = feature_engineer.create_location_features(merged_df)
    print("✅ Location features created")
    
    # Encode categorical features
    merged_df = feature_engineer.encode_categorical_features(merged_df, fit=True)
    print("✅ Categorical features encoded")
    
    # Step 7: Final cleanup
    print("\n🧹 Step 7: Final cleanup...")
    
    # Remove any remaining missing values
    merged_df = merged_df.dropna(subset=['target_price'] if 'target_price' in merged_df.columns else [])
    
    # Remove duplicate columns
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
    
    print(f"✅ Final dataset: {merged_df.shape}")
    print(f"📊 Features: {merged_df.shape[1] - 1}")
    print(f"🎯 Target: {'target_price' if 'target_price' in merged_df.columns else 'No target found'}")
    
    return merged_df, preprocessor, feature_engineer, integrator

if __name__ == "__main__":
    # Run the full pipeline
    result = create_full_pipeline()
    
    if result is not None:
        final_df, preprocessor, feature_engineer, integrator = result
        
        # Save the final dataset
        output_path = "../feature_engineering/feature_engineered_complete.csv"
        final_df.to_csv(output_path, index=False)
        print(f"\n💾 Final dataset saved to: {output_path}")
        
        # Save processors for later use
        import joblib
        processors = {
            'preprocessor': preprocessor,
            'feature_engineer': feature_engineer,
            'integrator': integrator
        }
        
        processors_path = "../feature_engineering/data_processors.pkl"
        joblib.dump(processors, processors_path)
        print(f"💾 Data processors saved to: {processors_path}")
        
        print("\n🎉 Full pipeline completed successfully!")
    else:
        print("\n❌ Pipeline failed!")