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

    render() {
        const { isLoading } = this.state;
        return (
            <div>
                {
                    isLoading ?
                    <Loader /> :
                    <div>
                        filter search (by different criteria)
                        sort asc/desc
                        <div className="list-group list-custom">{this.getAssignmentsList.call(this)}</div>
                    </div>
                }
            </div>
        )
    }
}

export default AssignmentsList;
