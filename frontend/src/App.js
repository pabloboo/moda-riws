import React, { Component } from 'react';

class App extends Component {

  state = {
    data: [],
  };

  componentDidMount() {
    // Realiza una solicitud a tu punto final de Elasticsearch utilizando fetch
    fetch('http://localhost:9200/shein_prod/_search?size=600')
      .then(response => {
        if (!response.ok) {
          throw new Error('La solicitud a Elasticsearch falló');
        }
        return response.json();
      })
      .then(data => {
        // Maneja la respuesta de Elasticsearch y actualiza el estado con los datos recibidos
        this.setState({ data: data.hits.hits });
      })
      .catch(error => {
        // Maneja los errores en caso de que la solicitud falle
        console.error('Error al obtener datos de Elasticsearch:', error);
      });
  }

  render() {
    return (
      <div>
        <h1>Datos de Elasticsearch</h1>
        <ul>
          {this.state.data.map((item, index) => (
            <li key={index}>
              <a href={item._source.url}>{item._source.nombre}</a>
              <br />
              Color: {item._source.color}
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default App;
