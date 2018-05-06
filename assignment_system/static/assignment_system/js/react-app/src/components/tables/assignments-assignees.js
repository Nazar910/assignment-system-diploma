import React, { Component } from 'react';
import axios from 'axios';
import cookies from 'js-cookie';
import dateformat from 'dateformat';

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
            assignments: [],
            assignees: [],
            tableReference: new Map(),
            assignments_finished: []
        }

        this.getTableReferencesAsTrs = this.getTableReferencesAsTrs.bind(this);
    }

    componentDidMount() {
        Promise.all([
            getList('assignees'),
            getList('assignments'),
            getList('assignments_finished')
        ]).then(([assignees, assignments, assignments_finished]) => {
            this.updateTableReference({
                assignees,
                assignments
            });
            this.updateAssignmentsFinished({
                assignees,
                assignments_finished
            });
        })
    }

    updateTableReference({ assignees, assignments, date_limit }) {
        const { tableReference } = this.state;
        console.log('Assignees', assignees);
        console.log('Assignments', assignments);
    
        if (date_limit) {
            assignments = assignments.filter(a => new Date(a.fields.assigned_at) > date_limit);
        }

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
        this.setState({tableReference, assignments, assignees});
    }

    updateAssignmentsFinished({ assignments_finished }) {
        console.log('AssigneesFinished', assignments_finished);
        this.setState({assignments_finished});
    }

    showAssignmentStatus() {

    }

    getTableReferencesAsTrs(tableReference, assignments) {
        const result = [];
        const { assignments_finished } = this.state;
        for (const [key,value] of tableReference.entries()) {
            console.log('Key', key);
            console.log('Value', value);
            result.push(<tr>
                <td scope="row">{key.fields.name} {key.fields.last_name}</td>
                <td>{key.fields.position}</td>
                <td></td>
                {assignments.map(a => {
                    if (value.has(a)) {
                        const { deadline = 'Без дедлайну' } = a;
                        const finished_assignment = assignments_finished.find(af => af.fields.assignment === a.pk);
                        if (finished_assignment) {
                            return <td><div onClick={() => alert('Дедлайн: ' + deadline + '\nЗакінчено: ' + finished_assignment.fields.finished_at)}>V</div></td>
                        }

                        return <td><div onClick={() => alert('Дедлайн:' + deadline)}>Виконується</div></td>
                    }
                    return <td> </td>
                })}
            </tr>)
        }
        return result;
    }

    getAssignmentsAsArrayOfTh(assignments) {
        const result = [];
        for (const assignment of assignments) {
            console.log('assignment', assignment);
            const date = new Date(assignment.fields.created_at);
            result.push(<th scope="col">№ {assignment.pk} від {dateformat(date, 'dd.mm.yyyy' )}</th>)
        }
        return result;
    }

    onSelectedTimeChange({target}) {
        console.log(target.value);

        if (target.value === 'all') {
            this.setState({tableReference: new Map()});
            Promise.all([
                getList('assignees'),
                getList('assignments'),
                getList('assignments_finished')
            ]).then(([assignees, assignments, assignments_finished]) => {
                this.updateTableReference({
                    assignees,
                    assignments
                });
                this.updateAssignmentsFinished({
                    assignees,
                    assignments_finished
                });
            })
            return;
        }
        
        const { assignees, assignments } = this.state;
        this.updateTableReference({
            assignees,
            assignments,
            date_limit: target.value
        });
    }

    render() {
        return (
            <div>
                Статус виконання доручень за 
                <select onChange={this.onSelectedTimeChange.bind(this)}>
                    <option value="all" selected="selected">весь час</option>
                    <option value={new Date(Date.now() - 1000 * 60 * 60 * 24 * 31)}>місяць</option>
                    <option value={new Date(Date.now() - 1000 * 60 * 60 * 24 * 7)}>тиждень</option>
                </select>
                <table className="table table-bordered">
                    <tr>
                        <th scope="col">Виконавець</th>
                        <th scope="col">Посада</th>
                        <th scope="col">\</th>
                        {this.getAssignmentsAsArrayOfTh(this.state.assignments)}
                    </tr>
                    {this.getTableReferencesAsTrs(this.state.tableReference, this.state.assignments)}
                </table>
            </div>
        )
    }
}

export default AssignmentAssignee;
