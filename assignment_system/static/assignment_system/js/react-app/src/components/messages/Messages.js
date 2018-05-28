import React, { Component } from 'react';
import dateformat from 'dateformat';
import Loader from '../Loader';
import MessageList from './MessageList';
import $ from 'jquery';
import { createMessage, getMessagesByAssignmentId } from '../../api/index'

class Messages extends Component {
    constructor(props) {
        super(props);

        this.state = {
            messages: [],
            isLoading: true,
            assignment_id: props.assignment_id
        }
    }

    componentDidMount() {
        const { assignment_id } = this.state;

        getMessagesByAssignmentId(assignment_id)
            .then(messages => {
                this.setState({
                    messages,
                    isLoading: false
                })
            })
            .catch(err => {
                console.log(err.messages_404);
                if (err.messages_404) {
                    this.setState({
                        isLoading: false
                    });
                }
            })
    }

    addNewMessage(e) {
        e.preventDefault();
        console.log('Button clicked');
        const text = $('input#new_message').val();
        const file = $('input#new_message_file')[0].files[0];
        const { assignment_id } = this.state;
        createMessage(text, assignment_id, file)
            .then((message) => {
                console.log(message);
                const { messages } = this.state;
                messages.push(message);
                this.setState({ messages });
                $('input#new_message').val('');
                $('input#new_message_file').val('');
            })
    }

    render() {
        const { isLoading, messages } = this.state;
        return (
            <div>
                { isLoading ?
                    <Loader /> :
                    <div>
                        <form>
                            <input type="text" className="form-control" id="new_message" aria-describedby="message_help" placeholder="Введіть повідомлення"/>
                            <small id="message_help" className="form-text text-muted">Ваше повідомлення</small>
                            <input type="file" className="form-control-file" id="new_message_file"/>
                            <button className="btn btn-primary" onClick={this.addNewMessage.bind(this)}>Написати</button>
                        </form>
                        <br />
                        <MessageList items={messages}/>
                    </div>
                }
            </div>
        )
    }
}

export default Messages;
