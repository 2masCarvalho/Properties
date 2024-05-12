import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import './index.css'; // Ensure you have your styles defined here or imported appropriately

const Properties = () => {
    const [properties, setProperties] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/myproperties/1/') // Adjust URL as needed
            .then(response => {
                setProperties(response.data);
            })
            .catch(error => console.error('Error fetching properties:', error));
    }, []);

    return (
        <div className="card-container">
            {properties.length > 0 ? properties.map(({ id, title, first_image, price, location, area, num_bedrooms, num_bathrooms }) => (
                <div key={id} className="property-card">
                    {first_image ? (
                        <a href={`/property_detail/${id}`} className="">
                            <img src={first_image} alt={`${title} - Image`} className="property-image" />
                        </a>
                    ) : (
                        <p className="no-image">Nenhuma imagem disponível</p>
                    )}
                    <button className="favorites-button" title="Add to favorites"><i className="fa-regular fa-heart"></i></button>
                    <p className="property-price"><strong>{price} €</strong></p>
                    <p className="property-location">{location.charAt(0).toUpperCase() + location.slice(1)}</p>
                    <div className="property-details">
                        <p className="detail-item">
                            <i className="fa-solid fa-house"></i>
                            <strong>{area} m<sup>2</sup></strong>
                        </p>
                        <p className="detail-item">
                            <i className="fas fa-bed"></i>
                            <strong>{num_bedrooms}</strong>
                        </p>
                        <p className="detail-item">
                            <i className="fas fa-bath"></i>
                            <strong>{num_bathrooms}</strong>
                        </p>
                    </div>
                </div>
            )) : (
                <div className="no-property">
                    Nenhum imóvel disponível no momento.
                </div>
            )}
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Properties />);
