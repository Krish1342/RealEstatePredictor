import React from 'react';
import { Link } from 'react-router-dom';

const Hero = () => {
  return (
    <section className="pt-32 pb-20 px-6">
      <div className="container mx-auto hero-section py-16 px-8 text-center text-white">
        <h1 className="text-4xl md:text-5xl font-bold mb-6">Smart Property Valuation in Minutes</h1>
        <p className="text-xl max-w-2xl mx-auto mb-10">AI-powered real estate price prediction using advanced machine learning algorithms and comprehensive data analysis</p>
        <Link to="/predict" className="btn-primary px-8 py-4 text-lg font-semibold inline-block">Get Started <i className="ml-2 fas fa-arrow-right"></i></Link>
      </div>
    </section>
  );
};

export default Hero;