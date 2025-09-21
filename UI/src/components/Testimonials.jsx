import React from 'react';

const Testimonials = () => {
  const testimonials = [
    {
      name: 'Rajesh Kumar',
      role: 'Property Investor',
      comment: '"The prediction was spot on! I used this tool to evaluate a property in Bangalore and it helped me negotiate a better deal."',
      stars: 5
    },
    {
      name: 'Priya Singh',
      role: 'Home Buyer',
      comment: '"I was skeptical at first, but the accuracy of the prediction surprised me. It considered factors I hadn\'t even thought about!"',
      stars: 4.5
    },
    {
      name: 'Amit Patel',
      role: 'Real Estate Agent',
      comment: '"This tool has become an essential part of my business. It helps me provide accurate valuations to my clients quickly."',
      stars: 5
    }
  ];
  
  return (
    <section className="py-16 px-6">
      <div className="container mx-auto">
        <h2 className="text-3xl font-bold text-center mb-4">What Our Users Say</h2>
        <p className="text-gray-600 text-center max-w-2xl mx-auto mb-12">Hear from satisfied users who have used our prediction service</p>
        
        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="property-card bg-white p-6">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 mr-4">
                  <i className="fas fa-user"></i>
                </div>
                <div>
                  <h4 className="font-bold">{testimonial.name}</h4>
                  <p className="text-gray-600">{testimonial.role}</p>
                </div>
              </div>
              <p className="text-gray-700 mb-4">{testimonial.comment}</p>
              <div className="flex text-yellow-400">
                {[...Array(5)].map((_, i) => (
                  <i 
                    key={i} 
                    className={`fas fa-star ${i < Math.floor(testimonial.stars) ? 'text-yellow-400' : (i === Math.floor(testimonial.stars) && testimonial.stars % 1 !== 0) ? 'fas fa-star-half-alt' : 'far fa-star'}`}
                  ></i>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;