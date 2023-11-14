import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import {
  ReactiveBase,
  DataSearch,
  ReactiveList,
  SelectedFilters,
  MultiDropdownList,
  RangeSlider
} from '@appbaseio/reactivesearch';

import './App.css'; // Agrega el archivo de estilos

const App = () => {
  const [resetKey, setResetKey] = useState(0);

  return (
    <ReactiveBase
      app="productos"
      url="http://localhost:9200"
      key={resetKey}
    >
      <div className="app-container">
        <div className="header">
          <h1>Fashion Findr</h1>
        </div>

        <DataSearch
          componentId="search"
          dataField="nombre"
          placeholder="Buscar prendas"
          react={{ and: ['PriceSlider', 'ColorFilter', 'TallasFilter', 'MarcaFilter'] }}
          style={{ width: '75%', margin: '0 auto', marginBottom: '20px' }}
        />

        <div className="filters-container">
          <div className="filter-section">
            <RangeSlider
              componentId='PriceSlider'
              dataField='precio'
              tooltipTrigger='hover'
              range={{
                start: 0,
                end: 250,
              }}
              rangeLabels={{
                start: "0€",
                end: "250€",
              }}
              react={{ and: ['search', 'PriceSlider', 'ColorFilter', 'TallasFilter', 'MarcaFilter'] }}
              title='Precio'
              showHistogram={false}
            />
          </div>

          <div className="filter-section">
            <MultiDropdownList
              componentId="ColorFilter"
              dataField="color"
              title="Colores"
              size={100}
              sortBy="count"
              showCount={true}
              placeholder="Buscar colores"
              react={{
                and: ['search', 'PriceSlider', 'TallasFilter', 'MarcaFilter']
              }}
              showFilter={true}
              filterLabel="Colores"
              URLParams={false}
              loader="Loading ..."
            />
          </div>

          <div className="filter-section">
            <MultiDropdownList
              componentId="TallasFilter"
              dataField="tallas"
              title="Tallas"
              size={100}
              sortBy="count"
              showCount={true}
              placeholder="Buscar tallas"
              react={{
                and: ['search', 'PriceSlider', 'ColorFilter', 'MarcaFilter']
              }}
              showFilter={true}
              filterLabel="Tallas"
              URLParams={false}
              loader="Loading ..."
            />
          </div>

          <div className="filter-section">
            <MultiDropdownList
              componentId="MarcaFilter"
              dataField="marca"
              title="Marcas"
              size={100}
              sortBy="count"
              showCount={true}
              placeholder="Buscar marcas"
              react={{
                and: ['search', 'PriceSlider', 'ColorFilter', 'TallasFilter']
              }}
              showFilter={true}
              filterLabel="Marcas"
              URLParams={false}
              loader="Loading ..."
            />
          </div>
        </div>

        <div className="selected-filters">
          <SelectedFilters
            showClearAll={true}
            clearAllLabel="Limpiar todo"
            componentId="search"
          />
        </div>

        <ReactiveList
          componentId="SearchResult"
          dataField="nombre"
          react={{ and: ['search', 'PriceSlider', 'ColorFilter', 'TallasFilter', 'MarcaFilter'] }}
        >
          {({ data }) => (
            <ul className="result-list">
              {data.map((item) => (
                <li key={item._id} className="result-item">
                  <div className="result-item-container">
                    <img
                      src={item.imagen}
                      alt={item.nombre}
                      className="result-item-image"
                    />
                    <div className="result-item-details">
                      <h3>{item.nombre}</h3>
                      <p>Precio: {item.precio} €</p>
                      <p>Color: {item.color}</p>
                      <p>Tallas: {item.tallas}</p>
                      <p>Marca: {item.marca}</p>
                      <a href={item.url} target="_blank" rel="noopener noreferrer">
                        Ver producto
                      </a>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </ReactiveList>
      </div>
    </ReactiveBase>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
