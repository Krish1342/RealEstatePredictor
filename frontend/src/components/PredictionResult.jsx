import { motion } from "framer-motion";
import {
  DollarSign,
  TrendingUp,
  Activity,
  CheckCircle,
  AlertCircle,
  BarChart3,
  Lightbulb,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const PredictionResult = ({ data }) => {
  const {
    ensemble_prediction,
    formatted_price,
    confidence,
    individual_predictions,
    insights,
    prediction_range,
    feature_importance,
    model_performance,
  } = data;

  const COLORS = ["#3d70ff", "#9333ea", "#10b981", "#f59e0b", "#ef4444"];

  // Prepare data for individual predictions chart
  const modelChartData = individual_predictions.map((pred, index) => ({
    name: pred.name,
    price: pred.prediction / 100000, // Convert to lakhs
    weight: pred.weight,
  }));

  // Prepare data for feature importance
  const featureChartData = feature_importance.slice(0, 8).map((item) => ({
    name: item.feature.replace(/_/g, " "),
    importance: (item.importance * 100).toFixed(2),
  }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-8"
    >
      {/* Main Prediction Card */}
      <div className="card bg-gradient-to-br from-primary-600 to-secondary-600 text-white">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <DollarSign className="w-12 h-12" />
          </div>
          <h2 className="text-2xl font-semibold mb-2">Predicted Price</h2>
          <div className="text-5xl md:text-6xl font-bold mb-4">
            {formatted_price}
          </div>
          <div className="flex items-center justify-center space-x-4 text-lg">
            <div className="flex items-center">
              <Activity className="w-5 h-5 mr-2" />
              <span>Confidence: {confidence}</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 mr-2" />
              <span>{individual_predictions.length} Models</span>
            </div>
          </div>
        </div>
      </div>

      {/* Price Range */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-sm font-semibold text-gray-600 mb-2">
            Minimum Price
          </div>
          <div className="text-2xl font-bold text-gray-900">
            {prediction_range.formatted_min}
          </div>
        </div>
        <div className="card text-center bg-primary-50 border-2 border-primary-200">
          <div className="text-sm font-semibold text-primary-700 mb-2">
            Predicted Price
          </div>
          <div className="text-2xl font-bold text-primary-900">
            {formatted_price}
          </div>
        </div>
        <div className="card text-center">
          <div className="text-sm font-semibold text-gray-600 mb-2">
            Maximum Price
          </div>
          <div className="text-2xl font-bold text-gray-900">
            {prediction_range.formatted_max}
          </div>
        </div>
      </div>

      {/* Insights */}
      <div className="card">
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <Lightbulb className="w-6 h-6 mr-2 text-yellow-500" />
          AI-Generated Insights
        </h3>
        <div className="grid gap-4">
          {insights.map((insight, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg border border-blue-100"
            >
              <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <p className="text-gray-700">{insight}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Model Predictions */}
      <div className="card">
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
          <BarChart3 className="w-6 h-6 mr-2 text-primary-600" />
          Individual Model Predictions
        </h3>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Bar Chart */}
          <div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={modelChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="name"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  tick={{ fontSize: 12 }}
                />
                <YAxis
                  label={{
                    value: "Price (Lakhs)",
                    angle: -90,
                    position: "insideLeft",
                  }}
                />
                <Tooltip
                  formatter={(value) => [`₹${value.toFixed(2)} Lakhs`, "Price"]}
                />
                <Legend />
                <Bar dataKey="price" fill="#3d70ff" name="Predicted Price" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Model Details */}
          <div className="space-y-3">
            {individual_predictions.map((pred, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded-lg">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-bold text-gray-900">{pred.name}</h4>
                    <p className="text-sm text-gray-600">
                      Weight: {pred.weight.toFixed(0)}%
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-primary-700">
                      {pred.formatted_price}
                    </div>
                  </div>
                </div>
                {pred.metrics && (
                  <div className="grid grid-cols-3 gap-2 mt-2 text-xs text-gray-600">
                    <div>R²: {pred.metrics.R2?.toFixed(6)}</div>
                    <div>MAE: {pred.metrics.MAE?.toFixed(2)}</div>
                    <div>RMSE: {pred.metrics.RMSE?.toFixed(2)}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Feature Importance */}
      {feature_importance && feature_importance.length > 0 && (
        <div className="card">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">
            Top Influential Features
          </h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={featureChartData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                type="number"
                label={{ value: "Importance (%)", position: "bottom" }}
              />
              <YAxis
                dataKey="name"
                type="category"
                width={150}
                tick={{ fontSize: 12 }}
              />
              <Tooltip formatter={(value) => `${value}%`} />
              <Bar dataKey="importance" fill="#9333ea" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Model Performance Summary */}
      <div className="card bg-gray-50">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">
          Model Performance Summary
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-primary-700">
              {model_performance.total_models}
            </div>
            <div className="text-sm text-gray-600 mt-1">Ensemble Models</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {(model_performance.average_r2 * 100).toFixed(4)}%
            </div>
            <div className="text-sm text-gray-600 mt-1">Average R² Score</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {model_performance.best_model}
            </div>
            <div className="text-sm text-gray-600 mt-1">
              Best Performing Model
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button onClick={() => window.print()} className="btn-secondary">
          Print Report
        </button>
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          className="btn-primary"
        >
          Make Another Prediction
        </button>
      </div>
    </motion.div>
  );
};

export default PredictionResult;
