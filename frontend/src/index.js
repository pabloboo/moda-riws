import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import {
  ReactiveBase,
  DataSearch,
  ReactiveList,
  SingleDropdownList,
  RangeInput,
  SelectedFilters,
  MultiDropdownList,
} from '@appbaseio/reactivesearch';

const App = () => {
  const [resetKey, setResetKey] = useState(0);

  const handleClearAll = () => {
    // Incrementar la clave de reinicio para forzar la actualización de ReactiveSearch
    setResetKey((prevKey) => prevKey + 1);
  };

  return (
    <ReactiveBase
      app="productos" // Tu nombre de aplicación Elasticsearch
      url="http://localhost:9200" // URL de tu clúster Elasticsearch
      key={resetKey} // Utilizamos la clave de reinicio para forzar la actualización de ReactiveSearch
    >
      <div>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', marginBottom: '1%' }}>
          <h1>Fashion Findr</h1>
        </div>

        {/* Buscador */}
        <DataSearch
          componentId="search"
          dataField="nombre"
          placeholder="Buscar prendas"
          react={{ and: [ 'PriceSlider', 'ColorFilter', 'TallasFilter', 'MarcaFilter'] }}
          style={{ width: '75%', margin: '0 auto' }}
        />

        {/* Filtros */}
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '3%', marginBottom: '5%' }}>
          {/* Filtro de precio */}
          <div style={{ width: '25%', marginRight: '10%', marginLeft: '10%' }}>
            <RangeInput
              componentId='PriceSlider'
              dataField='precio'
              tooltipTrigger='hover'
              range={{
                start: 0,
                end: 500,
              }}
              rangeLabels={{
                start: "0€",
                end: "500€",
              }}
              react={{ and: ['search', 'PriceSlider', 'ColorFilter', 'TallasFilter', 'MarcaFilter'] }}
              title='Precio'
            />
          </div>

          {/* Filtro de color */}
          <div style={{ width: '25%', marginRight: '10%' }}>
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

          {/* Filtro de tallas */}
          <div style={{ width: '25%', marginRight: '10%' }}>
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
          
          
            {/* Filtro de marca */}
          <div style={{ width: '25%', marginRight: '10%' }}>
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

        {/* Filtros seleccionados */}
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
          <SelectedFilters
            showClearAll={true}
            clearAllLabel="Limpiar todo"
            componentId="search"
            onClear={handleClearAll} // Agregamos la lógica de reinicio aquí
          />
        </div>

        {/* Lista de resultados */}
        <ReactiveList
          componentId="SearchResult"
          dataField="nombre"
          react={{ and: ['search', 'PriceSlider', 'ColorFilter', 'TallasFilter', 'MarcaFilter'] }}
        >
          {({ data }) => (
            <ul style={{ listStyleType: 'none', display: 'flex', flexWrap: 'wrap' }}>
              {data.map((item) => (
                <li key={item._id} style={{ flex: '0 0 50%', padding: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <img
                      src={item.imagen}
                      alt={item.nombre}
                      style={{ maxWidth: '20%', height: 'auto' }}
                    />
                    <div style={{ marginLeft: '10px' }}>
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
