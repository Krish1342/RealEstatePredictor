import React from 'react';
import PropertyComparison from '../components/PropertyComparison';

const Compare = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto">
        <PropertyComparison />
      </div>
    </div>
  );
};

export default Compare;