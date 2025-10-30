import { Link } from "react-router-dom";
import {
  ArrowRight,
  TrendingUp,
  BarChart3,
  Cpu,
  Shield,
  Zap,
  Users,
} from "lucide-react";
import { motion } from "framer-motion";

const Home = () => {
  const features = [
    {
      icon: Cpu,
      title: "AI-Powered Predictions",
      description:
        "Ensemble of 5 top machine learning models with 99.99% accuracy",
    },
    {
      icon: Zap,
      title: "Real-time Analysis",
      description: "Instant property valuations with comprehensive insights",
    },
    {
      icon: Shield,
      title: "Data-Driven",
      description:
        "Trained on thousands of Bangalore properties with verified data",
    },
    {
      icon: BarChart3,
      title: "Detailed Analytics",
      description:
        "In-depth analysis with confidence scores and prediction ranges",
    },
  ];

  const stats = [
    { label: "ML Models", value: "5", suffix: "+" },
    { label: "Accuracy", value: "99.99", suffix: "%" },
    { label: "Features Analyzed", value: "70", suffix: "+" },
    { label: "Properties Evaluated", value: "21K", suffix: "+" },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
    },
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-purple-600 to-secondary-600 text-white">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Predict Bangalore
              <br />
              <span className="text-yellow-300">Real Estate Prices</span>
              <br />
              with AI Precision
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-gray-100 max-w-3xl mx-auto">
              Leverage the power of ensemble machine learning to get accurate
              property valuations in seconds
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/predict"
                className="inline-flex items-center justify-center px-8 py-4 bg-white text-primary-700 rounded-lg font-bold text-lg hover:bg-gray-100 transition-all duration-300 shadow-xl hover:shadow-2xl transform hover:scale-105"
              >
                Start Predicting
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/analytics"
                className="inline-flex items-center justify-center px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-bold text-lg hover:bg-white hover:text-primary-700 transition-all duration-300"
              >
                View Analytics
              </Link>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                variants={itemVariants}
                className="text-center"
              >
                <div className="text-4xl md:text-5xl font-bold mb-2">
                  {stat.value}
                  <span className="text-yellow-300">{stat.suffix}</span>
                </div>
                <div className="text-gray-200">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* Wave Shape */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg
            viewBox="0 0 1440 120"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="w-full h-auto"
          >
            <path
              d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z"
              fill="#f9fafb"
            />
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Our Platform?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Built with cutting-edge technology and trained on extensive real
              estate data
            </p>
          </div>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid md:grid-cols-2 lg:grid-cols-4 gap-8"
          >
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  variants={itemVariants}
                  className="card card-hover text-center"
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Get accurate predictions in three simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Enter Property Details",
                description:
                  "Provide information about the property including size, location, amenities, and more",
              },
              {
                step: "02",
                title: "AI Analysis",
                description:
                  "Our ensemble of 5 ML models analyzes 70+ features to predict the optimal price",
              },
              {
                step: "03",
                title: "Get Results",
                description:
                  "Receive detailed predictions with confidence scores, insights, and price ranges",
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2 }}
                viewport={{ once: true }}
                className="relative"
              >
                <div className="text-7xl font-bold text-primary-100 mb-4">
                  {item.step}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  {item.title}
                </h3>
                <p className="text-gray-600 text-lg">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-secondary-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Predict Your Property Value?
          </h2>
          <p className="text-xl mb-8 text-gray-100">
            Get started now and discover the true value of your Bangalore
            property
          </p>
          <Link
            to="/predict"
            className="inline-flex items-center px-8 py-4 bg-white text-primary-700 rounded-lg font-bold text-lg hover:bg-gray-100 transition-all duration-300 shadow-xl hover:shadow-2xl transform hover:scale-105"
          >
            Start Predicting Now
            <TrendingUp className="ml-2 w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
