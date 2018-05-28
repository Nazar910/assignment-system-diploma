import React, { Component } from 'react';
import MessageItem from './MessageItem';

class MessageList extends Component {
    constructor(props) {
        super(props);

        this.state = {
            messages: props.items
        }
    }

    mapMessages() {
        const {  messages } = this.state;
        const items = [];

        for (const m of messages) {
            items.push(
                <MessageItem key={m.pk} message={m} />
            )
        }

        return items;
    }

    render() {
        return (
            <div class="list-group">
                {this.mapMessages.call(this)}
            </div>
        )
    }
}

export default MessageList;
