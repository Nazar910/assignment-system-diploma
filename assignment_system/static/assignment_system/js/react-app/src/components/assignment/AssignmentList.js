import React, { Component } from 'react';
import Loader from '../Loader';
import AssignmentsItem from './AssignmentItem';
import { getAssignments } from '../../api';

class AssignmentsList extends Component {
    constructor(props) {
        super(props);

        this.state = {
            assignments: [],
            isLoading: true,
            editableAssignmentId: undefined
        }
    }

    componentDidMount() {
        getAssignments()
            .then(assignments => {
                this.setState({
                    isLoading: false,
                    assignments
                })
            })
    }

    getAssignmentsList() {
        const { assignments, editableAssignmentId } = this.state;
        const result = [];

        for (const assignment of assignments) {
            result.push(
                <AssignmentsItem 
                    assignment={assignment}
                    edit={this.openAssignmentEditor.bind(this)}
                    isEditable={editableAssignmentId === assignment.pk}
                />
            );
        }

        return result;
    }

    openAssignmentEditor(id) {
        this.setState({
            editableAssignmentId: id
        });
    }

    create() {
        window.location.href = '/assignment_system/assignments/new';
    }

    render() {
        const { isLoading } = this.state;
        return (
            <div>
                {
                    isLoading ?
                    <Loader /> :
                    <div>
                        <a className="btn btn-primary" href="/assignment_system/assignments/new">Створити доручення</a>
                        <div className="list-group list-custom">{this.getAssignmentsList.call(this)}</div>
                    </div>
                }
            </div>
        )
    }
}

export default AssignmentsList;
