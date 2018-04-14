import React from 'react';
import ReactDOM from 'react-dom';

const title = 'Hi from react page';

ReactDOM.render(
    <div>{title}</div>,
    document.getElementById('home-page')
)

module.hot.accept();
