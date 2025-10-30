import { motion } from "framer-motion";
import {
  Brain,
  Target,
  Award,
  Users,
  Code,
  Database,
  TrendingUp,
  Shield,
  Zap,
  Github,
} from "lucide-react";

const About = () => {
  const technologies = [
    {
      category: "Machine Learning",
      icon: Brain,
      items: [
        "Extra Trees Regressor",
        "Random Forest",
        "Decision Tree",
        "LightGBM",
        "XGBoost",
      ],
    },
    {
      category: "Backend",
      icon: Code,
      items: ["FastAPI", "Python 3.8+", "Uvicorn", "Pydantic", "Joblib"],
    },
    {
      category: "Frontend",
      icon: Zap,
      items: ["React 18", "Vite", "Tailwind CSS", "Framer Motion", "Recharts"],
    },
    {
      category: "Data Processing",
      icon: Database,
      items: [
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Feature Engineering",
        "70+ Features",
      ],
    },
  ];

  const features = [
    {
      icon: Target,
      title: "Accurate Predictions",
      description:
        "Ensemble of 5 top-performing models with 99.99% R² accuracy on Bangalore real estate data.",
    },
    {
      icon: Shield,
      title: "Reliable & Tested",
      description:
        "Trained on 21,000+ verified property records with comprehensive validation and testing.",
    },
    {
      icon: TrendingUp,
      title: "Real-time Insights",
      description:
        "Instant predictions with detailed insights, confidence scores, and price range analysis.",
    },
    {
      icon: Users,
      title: "User-Friendly",
      description:
        "Intuitive interface designed for both real estate professionals and home buyers.",
    },
  ];

  const modelMetrics = [
    { model: "Extra Trees", r2: "99.9999%", mae: "130.67", rmse: "1,004.53" },
    { model: "Random Forest", r2: "99.9999%", mae: "262.83", rmse: "1,866.99" },
    { model: "Decision Tree", r2: "99.9998%", mae: "338.73", rmse: "3,252.90" },
    { model: "LightGBM", r2: "99.9992%", mae: "1,677.42", rmse: "6,988.41" },
    { model: "XGBoost", r2: "99.9942%", mae: "7,009.06", rmse: "18,394.10" },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 via-purple-600 to-secondary-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              About Real Estate AI Predictor
            </h1>
            <p className="text-xl text-gray-100 max-w-3xl mx-auto">
              An advanced machine learning system that leverages ensemble models
              to provide accurate real estate price predictions for Bangalore
              properties.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto text-center"
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-6">
              Our Mission
            </h2>
            <p className="text-lg text-gray-600 mb-4">
              To democratize real estate valuation by providing accurate,
              AI-powered price predictions that help buyers, sellers, and
              investors make informed decisions.
            </p>
            <p className="text-lg text-gray-600">
              We combine state-of-the-art machine learning techniques with
              comprehensive property data to deliver predictions you can trust.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Why Choose Us?
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="card text-center card-hover"
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Technology Stack
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {technologies.map((tech, index) => {
              const Icon = tech.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="card"
                >
                  <div className="flex items-center mb-4">
                    <Icon className="w-6 h-6 text-primary-600 mr-2" />
                    <h3 className="text-lg font-bold text-gray-900">
                      {tech.category}
                    </h3>
                  </div>
                  <ul className="space-y-2">
                    {tech.items.map((item, idx) => (
                      <li key={idx} className="text-gray-600 flex items-center">
                        <span className="w-1.5 h-1.5 bg-primary-600 rounded-full mr-2"></span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Model Performance */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Model Performance Metrics
          </h2>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="card overflow-x-auto"
          >
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
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {modelMetrics.map((metric, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                      {metric.model}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-green-600 font-semibold">
                      {metric.r2}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                      {metric.mae}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                      {metric.rmse}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </motion.div>
        </div>
      </section>

      {/* Dataset Information */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Dataset & Training
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: "Training Data",
                value: "21,388+",
                description: "Verified property records from Bangalore",
              },
              {
                title: "Features",
                value: "70+",
                description:
                  "Engineered features including location, size, amenities, and environmental factors",
              },
              {
                title: "Validation",
                value: "Cross-Validated",
                description:
                  "Rigorous testing with multiple validation techniques",
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card text-center"
              >
                <div className="text-4xl font-bold text-primary-600 mb-2">
                  {item.value}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-600">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary-600 to-secondary-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-6">
            Ready to Experience AI-Powered Predictions?
          </h2>
          <p className="text-xl mb-8 text-gray-100">
            Try our predictor now and discover the true value of your property
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/predict"
              className="inline-flex items-center justify-center px-8 py-4 bg-white text-primary-700 rounded-lg font-bold text-lg hover:bg-gray-100 transition-all duration-300 shadow-xl"
            >
              Start Predicting
            </a>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-bold text-lg hover:bg-white hover:text-primary-700 transition-all duration-300"
            >
              <Github className="w-5 h-5 mr-2" />
              View on GitHub
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
