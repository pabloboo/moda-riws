import React from 'react';
import ReactDOM from 'react-dom';
import {ReactiveBase, DataSearch, ReactiveList, ResultList} from '@appbaseio/reactivesearch';

const { ResultListWrapper } = ReactiveList;

const App = () => {
  return (
    <ReactiveBase
      app="shein_prod" // Nombre de tu aplicación en Elasticsearch
      url="http://localhost:9200" // URL de tu clúster de Elasticsearch
    >
      <div>
        <h1>Datos de Elasticsearch</h1>
        <DataSearch
          componentId="search"
          dataField="nombre" // Campo en el que se realizará la búsqueda
          placeholder="Buscar productos"
          react={{ and: ['SearchResult'] }}
        />

        <ReactiveList

    componentId="SearchResult"
    dataField = "nombre"
    react={{ and: ['search'] }}
>
    {({ data}) => (
        <ResultListWrapper>
            {
                data.map(item => (
                    <ResultList key={item._id}>
                        <ResultList.Content>
                            <ResultList.Title
                                dangerouslySetInnerHTML={{
                                    __html: item.nombre
                                }}
                            />
                        </ResultList.Content>
                    </ResultList>
                ))
            }
        </ResultListWrapper>
    )}
</ReactiveList>


      </div>
    </ReactiveBase>
  );
};

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
