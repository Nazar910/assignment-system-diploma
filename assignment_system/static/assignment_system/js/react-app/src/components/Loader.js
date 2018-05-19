import React, { Component } from 'react';

class Loader extends Component {
    constructor(...args) {
        super(...args);

        this.state = {}
    }

    render() {
        return (
            <div id="loading"></div>
        )
    }
}

export default Loader;
