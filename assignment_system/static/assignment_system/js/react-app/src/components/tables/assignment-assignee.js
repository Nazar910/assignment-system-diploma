import React, { Component } from 'react';
import axios from 'axios';
import cookies from 'js-cookie';

const title = 'Hi from react App component page';

async function getList(resourceType) {
    const resp = await axios({
        url: `/assignment_system/${resourceType}`,
        headers: {
            'X-CSRFToken': cookies.get('csrftoken'),
            'Accept': 'application/json'
        },
        method: 'GET'
    });
    return resp.data
}

class AssignmentAssignee extends Component {
    constructor(props) {
        super(props);

        this.state = {
            assignees: [],
            assignments: [],
            tableReference: new Map()
        }

        // this.updateTableReference = this.updateTableReference.bind(this);

    }

    componentDidMount() {
        Promise.all([
            getList('assignees'),
            getList('assignments')
        ]).then(([assignees, assignments]) => {
            this.updateTableReference({
                assignees,
                assignments
            });
        })
    }

    updateTableReference({ assignees, assignments }) {
        const { tableReference } = this.state;
        console.log('Assignees', assignees);
        console.log('Assignments', assignments);
    
        for (const assignee of assignees) {
            const assignedAssignments = tableReference.get(assignee);
            if (assignedAssignments) {
                assignedAssignments.add(
                    assignments.filter(({fields}) => fields.assignees.find(a => a === assignee.pk)
                ));
                tableReference.set(assignee, assignedAssignments);
                continue;
            }
            tableReference.set(
                assignee,
                new Set(assignments.filter(({fields}) => fields.assignees.find(a => a === assignee.pk)))
            );
        }

        console.log(tableReference);
        this.setState({tableReference});
    }

    getTableReferencesAsTrs(tableReference) {
        const result = [];
        for (const [key,value] of tableReference.entries()) {
            console.log('Key', key);
            console.log('Value', value);
            result.push(<tr>
                <td>Assignee {key.pk}</td>
                <td>{[...value].map(a => a.pk).join('; ')}</td>
            </tr>)
        }
        return result;
    }

    render() {
        return (
            <div>
                TableReference:<br/>
                <table className="table">
                    <tr>
                        <th>Виконавець</th>
                        <th>Посада</th>
                        <th>\</th>
                    </tr>
                    {this.getTableReferencesAsTrs(this.state.tableReference)}
                </table>
            </div>
        )
    }
}

export default AssignmentAssignee;
