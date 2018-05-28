import React, { Component } from 'react';
import AssignmentsEditor from './AssignmentEditor';

class AssignmentsItem extends Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        const { assignment } = this.props;
        const { pk } = assignment;
        const { title } = assignment.fields;
        return (
                <a href={ "assignments/" + assignment.pk} className="list-group-item">
                    {`№ ${pk}: ${title}`}
                </a>
        )
    }
}

export default AssignmentsItem;
