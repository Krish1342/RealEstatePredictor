import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Home, TrendingUp, BarChart3, Info, Menu, X } from "lucide-react";
import { healthCheck } from "../services/api";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [apiStatus, setApiStatus] = useState("checking");
  const location = useLocation();

  useEffect(() => {
    checkApiHealth();
    const interval = setInterval(checkApiHealth, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  const checkApiHealth = async () => {
    try {
      await healthCheck();
      setApiStatus("connected");
    } catch (error) {
      setApiStatus("disconnected");
    }
  };

  const navLinks = [
    { path: "/", name: "Home", icon: Home },
    { path: "/predict", name: "Predict", icon: TrendingUp },
    { path: "/analytics", name: "Analytics", icon: BarChart3 },
    { path: "/about", name: "About", icon: Info },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center transform group-hover:scale-110 transition-transform">
                <Home className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                Estate AI
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 ${
                    isActive(link.path)
                      ? "bg-primary-50 text-primary-700 font-semibold"
                      : "text-gray-600 hover:bg-gray-100"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.name}</span>
                </Link>
              );
            })}
          </div>

          {/* API Status & Mobile Menu Button */}
          <div className="flex items-center space-x-4">
            {/* API Status */}
            <div className="flex items-center space-x-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  apiStatus === "connected"
                    ? "bg-green-500 animate-pulse"
                    : apiStatus === "disconnected"
                    ? "bg-red-500"
                    : "bg-yellow-500 animate-pulse"
                }`}
              />
              <span className="text-xs text-gray-600 hidden sm:inline">
                {apiStatus === "connected"
                  ? "API Online"
                  : apiStatus === "disconnected"
                  ? "API Offline"
                  : "Checking..."}
              </span>
            </div>

            {/* Mobile menu button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              {isOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden bg-white border-t border-gray-200">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  onClick={() => setIsOpen(false)}
                  className={`block px-3 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 ${
                    isActive(link.path)
                      ? "bg-primary-50 text-primary-700 font-semibold"
                      : "text-gray-600 hover:bg-gray-100"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
