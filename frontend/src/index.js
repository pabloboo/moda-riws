import React from 'react';
import ReactDOM from 'react-dom';
import { ReactiveBase, DataSearch, ReactiveList, SingleDropdownList, RangeInput, ReactiveComponent } from '@appbaseio/reactivesearch';

const App = () => {
  return (
    <ReactiveBase
      app="hym_prod" // Your Elasticsearch application name
      url="http://localhost:9200" // URL of your Elasticsearch cluster
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
          react={{ and: ['SearchResult', 'PriceSlider', 'ColorFilter'] }}
          style={{ width: '75%', margin: '0 auto' }}
        />

        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '3%', marginBottom: '5%' }}>
          <div style={{ width: '25%', marginRight: '10%', marginLeft: '10%'}}>
            {/* Filtro de precio */}
            <RangeInput
              componentId='PriceSlider'
              dataField='precio'
              tooltipTrigger='hover'
              range={{
                start: 0,
                end: 1000,
              }}
              rangeLabels={{
                start: "0€",
                end: "1000€",
              }}
              react={{and: ['SearchResult', 'search', 'ColorFilter'],}}
              title='Precio'
            />
          </div>

          {/* Filtro de color */}
          <div style={{ width: '25%', marginRight: '10%' }}>
            <SingleDropdownList
              componentId="ColorFilter"
              dataField="color"
              title="Colores"
              size={100} // Adjust the number of colors to display
              showSearch={true}
              showMissing={true}
              placeholder="Buscar colores"
              react={{
                and: ['SearchResult', 'search', 'PriceSlider'],
              }}
            />
          </div>
          
        </div>

        {/* Lista de resultados */}
        <ReactiveList
          componentId="SearchResult"
          dataField="nombre"
          react={{ and: ['search', 'PriceSlider', 'ColorFilter'] }}
        >
          {({ data }) => (
            <ul style={{ listStyleType: 'none', display: 'flex', flexWrap: 'wrap' }}>
              {data.map(item => (
                <li key={item._id} style={{ flex: '0 0 50%', padding: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <img
                      src={item.imagen}
                      alt={item.nombre}
                      style={{ maxWidth: '20%', height: 'auto' }}
                    />
                    <div style={{ marginLeft: '10px' }}>
                      <h3>{item.nombre}</h3>
                      <p>Precio: {item.precio}</p>
                      <p>Color: {item.color}</p>
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