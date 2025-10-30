import { Github, Heart } from "lucide-react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-white text-lg font-bold mb-4">
              Real Estate AI Predictor
            </h3>
            <p className="text-gray-400 mb-4">
              AI-powered real estate price prediction for Bangalore properties
              using state-of-the-art ensemble machine learning models.
            </p>
            <div className="flex items-center space-x-2 text-sm">
              <span>Made with</span>
              <Heart className="w-4 h-4 text-red-500 fill-current" />
              <span>using FastAPI & React</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <a href="/" className="hover:text-white transition-colors">
                  Home
                </a>
              </li>
              <li>
                <a
                  href="/predict"
                  className="hover:text-white transition-colors"
                >
                  Predict Price
                </a>
              </li>
              <li>
                <a
                  href="/analytics"
                  className="hover:text-white transition-colors"
                >
                  Analytics
                </a>
              </li>
              <li>
                <a href="/about" className="hover:text-white transition-colors">
                  About
                </a>
              </li>
            </ul>
          </div>

          {/* Technology */}
          <div>
            <h4 className="text-white font-semibold mb-4">Technology</h4>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-primary-500 rounded-full"></span>
                <span>FastAPI Backend</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-secondary-500 rounded-full"></span>
                <span>React + Vite</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                <span>Ensemble ML Models</span>
              </li>
              <li className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                <span>Tailwind CSS</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col sm:flex-row justify-between items-center">
          <p className="text-sm text-gray-400">
            © {currentYear} Real Estate AI Predictor. All rights reserved.
          </p>
          <div className="flex items-center space-x-4 mt-4 sm:mt-0">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
