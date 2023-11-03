import React from 'react';
import ReactDOM from 'react-dom';
import { ReactiveBase, DataSearch, ReactiveList } from '@appbaseio/reactivesearch';

const App = () => {
  return (
    <ReactiveBase
      app="hym_prod" // Your Elasticsearch application name
      url="http://localhost:9200" // URL of your Elasticsearch cluster
    >
      <div>
        <h1>Elasticsearch Data</h1>
        <DataSearch
          componentId="search"
          dataField="nombre"
          placeholder="Search for products"
          react={{ and: ['SearchResult'] }}
        />

        <ReactiveList
          componentId="SearchResult"
          dataField="nombre"
          react={{ and: ['search'] }}
        >
          {({ data }) => (
            <ul style={{ listStyleType: 'none' }}>
              {data.map(item => (
                <li key={item._id}>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <img
                      src={item.imagen}
                      alt={item.nombre}
                      style={{ maxWidth: '10%', height: 'auto' }}
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
