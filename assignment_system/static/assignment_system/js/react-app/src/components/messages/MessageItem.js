import React, { Component } from 'react';

class MessageItem extends Component {
    constructor(props) {
        super(props);

        this.state = {
            message: props.message
        }
    }

    render() {
        const { message } = this.state;
        const { text, author_full_name, created_at } = message.fields;
        return (
            <div>
                <a href="#" className="list-group-item list-group-item-action flex-column align-items-start">
                    <div className="d-flex w-100 justify-content-between">
                        <small>{created_at}</small>
                    </div>
                    <p className="mb-1">{text}</p>
                    <small>{author_full_name}</small>
                </a>
            </div>
        )
    }
}

export default MessageItem;
