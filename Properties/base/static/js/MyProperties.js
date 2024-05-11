import React, { useState, useEffect } from 'react';

function MyProperties({ userId }) {
  const [properties, setProperties] = useState([]);  // State to hold properties

  useEffect(() => {
    // Fetch data from the Django API
    fetch(`/api/myproperties/${userId}`)
      .then(response => response.json())
      .then(data => {
        // Update state with fetched properties
        setProperties(data.map(property => ({
          ...property,
          image: property['images__image']  // Adjust according to your actual image field
        })));
      })
      .catch(error => console.error('Error fetching properties:', error));
  }, [userId]);  // Dependency array with userId to refetch when userId changes

  return (
    <div className="card-container">
      {properties.length > 0 ? properties.map(({ id, title, price, location, area, num_bedrooms, num_bathrooms, image }) => (
        <div key={id} className="property-card">
          {image ? (
            <a href={`/property/${id}`}>
              <img src={image} alt={`${title} - Image`} className="property-image" />
            </a>
          ) : (
            <p className="no-image">No image available</p>
          )}
          {/* Additional property details here */}
        </div>
      )) : (
        <div className="no-property">No properties available at the moment.</div>
      )}
    </div>
  );
}

export default MyProperties;
