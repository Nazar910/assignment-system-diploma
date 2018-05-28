import React, { Component } from 'react';
import dateformat from 'dateformat';
import Loader from '../Loader';
import MessageList from './MessageList';
import $ from 'jquery';

function createMessage(messageBody) {
    return new Promise(resolve => {
        resolve({
            pk: Math.floor(Math.random() * 100),
            fields: {
                text: messageBody.text,
                author_id: 5,
                author_full_name: 'Mr Johns',
                created_at: dateformat(new Date(), 'dd.mm.yyyy' )
            }
        });
    });
}

class Messages extends Component {
    constructor(props) {
        super(props);

        const stubMessages = [
            {
                pk: 1,
                fields: {
                    text: 'Blah-blah',
                    author_id: 5,
                    author_full_name: 'Mr Johns',
                    created_at: dateformat(new Date(), 'dd.mm.yyyy' )
                }
            },
            {
                pk: 2,
                fields: {
                    text: 'Ye, you\'re right!',
                    author_id: 5,
                    author_full_name: 'Mr Johns',
                    created_at: dateformat(new Date(), 'dd.mm.yyyy' )
                }
            }
        ];

        this.state = {
            messages: [],
            isLoading: true,
            assignment_id: props.assignment_id, 
            stubMessages
        }
    }

    getMessages(assignment_id) {
        return new Promise(resolve => setTimeout(() => resolve(this.state.stubMessages), 500))
    }

    componentDidMount() {
        const { assignment_id } = this.state;

        this.getMessages(assignment_id)
            .then(messages => {
                this.setState({
                    messages,
                    isLoading: false
                })
            })
    }

    addNewMessage(e) {
        e.preventDefault();
        const messageBody = {
            text: $('input#new_message').val()
        }
        createMessage(messageBody)
            .then(message => {
                const { messages } = this.state;
                messages.push(message);
                this.setState({ messages });
                $('input#new_message').val('');
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
