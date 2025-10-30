import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { BarChart3, TrendingUp, Award, Zap } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";
import { getModelsInfo } from "../services/api";
import toast from "react-hot-toast";

const Analytics = () => {
  const [modelsData, setModelsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModelsInfo();
  }, []);

  const fetchModelsInfo = async () => {
    try {
      const data = await getModelsInfo();
      setModelsData(data);
    } catch (error) {
      console.error("Failed to fetch models info:", error);
      toast.error("Failed to load model analytics");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const modelPerformanceData =
    modelsData?.models.map((model) => ({
      name: model.name,
      R2: (model.metrics.R2 * 100).toFixed(4),
      MAE: model.metrics.MAE,
      weight: model.weight * 100,
    })) || [];

  const radarData =
    modelsData?.models.map((model) => ({
      model: model.name.split(" ")[0], // Shortened name
      Accuracy: (model.metrics.R2 * 100).toFixed(2),
      Weight: model.weight * 100,
      Speed: 100 - model.metrics.MAE / 100, // Inverse MAE for visualization
    })) || [];

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Model Analytics
          </h1>
          <p className="text-xl text-gray-600">
            Deep dive into our ensemble model performance metrics
          </p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          {[
            {
              icon: BarChart3,
              label: "Total Models",
              value: modelsData?.total_models || 0,
              color: "from-blue-500 to-blue-600",
            },
            {
              icon: Award,
              label: "Avg R² Score",
              value: modelsData?.models
                ? `${(
                    (modelsData.models.reduce(
                      (acc, m) => acc + m.metrics.R2,
                      0
                    ) /
                      modelsData.models.length) *
                    100
                  ).toFixed(4)}%`
                : "0%",
              color: "from-green-500 to-green-600",
            },
            {
              icon: TrendingUp,
              label: "Best Model",
              value: modelsData?.models
                ? modelsData.models
                    .reduce((best, m) =>
                      m.metrics.R2 > best.metrics.R2 ? m : best
                    )
                    .name.split(" ")[0]
                : "N/A",
              color: "from-purple-500 to-purple-600",
            },
            {
              icon: Zap,
              label: "Ensemble Power",
              value: "5 Models",
              color: "from-yellow-500 to-yellow-600",
            },
          ].map((stat, index) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="card text-center"
              >
                <div
                  className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-lg flex items-center justify-center mx-auto mb-4`}
                >
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-600">{stat.label}</div>
              </motion.div>
            );
          })}
        </div>

        {/* R² Score Comparison */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card mb-8"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Model R² Score Comparison
          </h2>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={modelPerformanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis
                domain={[99.99, 100]}
                label={{
                  value: "R² Score (%)",
                  angle: -90,
                  position: "insideLeft",
                }}
              />
              <Tooltip formatter={(value) => `${value}%`} />
              <Legend />
              <Bar dataKey="R2" fill="#3d70ff" name="R² Score" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* MAE and Weight */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* MAE Comparison */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="card"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Mean Absolute Error (MAE)
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={modelPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="name"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  tick={{ fontSize: 11 }}
                />
                <YAxis />
                <Tooltip />
                <Bar
                  dataKey="MAE"
                  fill="#ef4444"
                  name="MAE (Lower is Better)"
                />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Model Weights */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="card"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Ensemble Weights
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={modelPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="name"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  tick={{ fontSize: 11 }}
                />
                <YAxis
                  label={{
                    value: "Weight (%)",
                    angle: -90,
                    position: "insideLeft",
                  }}
                />
                <Tooltip formatter={(value) => `${value}%`} />
                <Bar dataKey="weight" fill="#9333ea" name="Weight" />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* Radar Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card mb-8"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Multi-Dimensional Performance
          </h2>
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="model" />
              <PolarRadiusAxis />
              <Radar
                name="Accuracy"
                dataKey="Accuracy"
                stroke="#3d70ff"
                fill="#3d70ff"
                fillOpacity={0.6}
              />
              <Radar
                name="Weight"
                dataKey="Weight"
                stroke="#9333ea"
                fill="#9333ea"
                fillOpacity={0.6}
              />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Model Details Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card overflow-x-auto"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Detailed Model Metrics
          </h2>
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  R² Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  MAE
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  RMSE
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Weight
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {modelsData?.models.map((model, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                    {model.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-green-600 font-semibold">
                    {(model.metrics.R2 * 100).toFixed(6)}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                    {model.metrics.MAE.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                    {model.metrics.RMSE.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${model.weight * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-700">
                        {(model.weight * 100).toFixed(0)}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      {model.loaded ? "Loaded" : "Not Loaded"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </div>
    </div>
  );
};

export default Analytics;
