import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navigation from './components/Navigation';
import Landing from './pages/Landing';
import Home from './pages/Home';
import Predict from './pages/Predict';
import About from './pages/About';
import Contact from './pages/Contact';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Footer from './components/Footer';
import Compare from './pages/Compare';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in from localStorage
    const loggedIn = localStorage.getItem('isLoggedIn') === 'true';
    setIsLoggedIn(loggedIn);
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    localStorage.setItem('isLoggedIn', 'true');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem('isLoggedIn');
  };

  return (
    <Router>
      <div className="App">
        {isLoggedIn && <Navigation isLoggedIn={isLoggedIn} onLogout={handleLogout} />}
        <Routes>
          <Route 
            path="/" 
            element={isLoggedIn ? <Home /> : <Landing />} 
          />
          <Route 
            path="/login" 
            element={isLoggedIn ? <Navigate to="/" /> : <Login onLogin={handleLogin} />} 
          />
          <Route 
            path="/signup" 
            element={isLoggedIn ? <Navigate to="/" /> : <Signup onLogin={handleLogin} />} 
          />
          <Route 
            path="/predict" 
            element={isLoggedIn ? <Predict /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/about" 
            element={isLoggedIn ? <About /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/contact" 
            element={isLoggedIn ? <Contact /> : <Navigate to="/login" />} 
          />
          <Route path="/compare" 
          element={isLoggedIn ? <Compare /> : <Navigate to="/login" />} 
          />
        </Routes>
        {isLoggedIn && <Footer />}
      </div>
    </Router>
  );
}

export default App;