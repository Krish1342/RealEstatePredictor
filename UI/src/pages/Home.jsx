import React from 'react';
import Hero from '../components/Hero';
import Features from '../components/Features';
import PopularCities from '../components/PopularCities';
import Testimonials from '../components/Testimonials';

const Home = () => {
  return (
    <div>
      <Hero />
      <Features />
      <PopularCities />
      <Testimonials />
    </div>
  );
};

export default Home;