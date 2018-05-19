import React, { Component } from 'react';
import AssignmentsEditor from './AssignmentEditor';

class AssignmentsItem extends Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        const { assignment } = this.props;
        return (
                <a href={ "assignments/" + assignment.pk} className="list-group-item">
                    {assignment.fields.title}
                </a>
        )
    }
}

export default AssignmentsItem;
