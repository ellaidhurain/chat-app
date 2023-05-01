import React from 'react';
import ReactDOM from 'react-dom';
import App from './Home/App';
import ChatAdmin from './ChatAdmin/ChatAdmin';

const path = window.location.pathname

ReactDOM.render(
  <React.StrictMode>
    { path.indexOf('/support') === -1 ? <App /> : <ChatAdmin /> }
  </React.StrictMode>,
  document.getElementById('root')
);
