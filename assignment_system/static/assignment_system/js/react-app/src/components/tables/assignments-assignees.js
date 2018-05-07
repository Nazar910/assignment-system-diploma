import React, { Component } from 'react';
import dateformat from 'dateformat';
import { getList } from '../../api';

const PAGE_SIZE = 3;

class AssignmentAssignee extends Component {
    constructor(props) {
        super(props);

        this.state = {
            assignments: [],
            assignees: [],
            tableReference: new Map(),
            assignments_finished: [],
            page: 0
        }

        this.getTableReferencesAsTrs = this.getTableReferencesAsTrs.bind(this);
        this.getCurrentAssignmentsBatch = this.getCurrentAssignmentsBatch.bind(this);
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

    getCurrentAssignmentsBatch() {
        const { assignments, page } = this.state;
        return assignments.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)
    }

    getTableReferencesAsTrs() {
        const result = [];
        const { assignments_finished, page, tableReference } = this.state;
        for (const [key,value] of tableReference.entries()) {
            console.log('Key', key);
            console.log('Value', value);
            result.push(<tr>
                <td scope="row">{key.fields.name} {key.fields.last_name}</td>
                <td>{key.fields.position}</td>
                <td></td>
                <td></td>
                {this.getCurrentAssignmentsBatch().map(a => {
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

    getAssignmentsAsArrayOfTh() {
        const result = [];
        const assignments = this.getCurrentAssignmentsBatch();
        for (const assignment of assignments) {
            console.log('assignment', assignment);
            const date = new Date(assignment.fields.created_at);
            result.push(<th scope="col">"{assignment.fields.title}" № {assignment.pk} від {dateformat(date, 'dd.mm.yyyy' )}</th>)
        }
        return result;
    }

    updatePage(page) {
        if (page < 0) {
            return;
        }

        if (page > this.state.assignments.length / PAGE_SIZE) {
            return;
        }

        this.setState({
            page
        });
    }

    pageIncrease() {
        const { page } = this.state;
        this.updatePage(page+1);
    }

    pageDecrease() {
        const { page } = this.state;
        this.updatePage(page-1);
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
                        <th scope="col"><div className="btn btn-success" onClick={this.pageDecrease.bind(this)}>&#8592;</div></th>
                        {this.getAssignmentsAsArrayOfTh.call(this)}
                        <th scope="col"><div className="btn btn-success" onClick={this.pageIncrease.bind(this)}>&#8594;</div></th>
                    </tr>
                    {this.getTableReferencesAsTrs.call(this)}
                </table>
            </div>
        )
    }
}

export default AssignmentAssignee;
