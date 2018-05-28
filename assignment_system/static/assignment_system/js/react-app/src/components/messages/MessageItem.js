import React, { Component } from 'react';
import dateformat from 'dateformat';
import { getFile } from '../../api/index';

class MessageItem extends Component {
    constructor(props) {
        super(props);

        this.state = {
            message: props.message
        }
    }

    fileDownload(file) {
        const fileName = file.split('/')[1];
        console.log('Filename is', fileName);
        getFile(fileName);
    }

    render() {
        const { message } = this.state;
        console.log('Message is', message);
        const { text, author_full_name, created_at, file } = message.fields;
        return (
            <div>
                <a href="#" className="list-group-item list-group-item-action flex-column align-items-start">
                    <div className="d-flex w-100 justify-content-between">
                        <small>{dateformat(new Date(created_at.replace('T', ' ').replace('Z', '')), 'dd.mm.yyyy hh:MM:ss')}</small>
                        <small><a href={`/assignment_system/files/${message.pk}`} target="_blank">{file}</a></small>
                    </div>
                    <p className="mb-1">{text}</p>
                    <small>{author_full_name}</small>
                </a>
            </div>
        )
    }
}

export default MessageItem;
