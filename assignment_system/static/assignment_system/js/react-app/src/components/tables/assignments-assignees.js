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
            page: 0,
            isLoading: true
        }

        this.getTableReferencesAsTrs = this.getTableReferencesAsTrs.bind(this);
        this.getCurrentAssignmentsBatch = this.getCurrentAssignmentsBatch.bind(this);
    }

    componentDidMount() {
        console.log('Parent');
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
            this.setState({
                isLoading: false
            })
        })
    }

    updateTableReference({ assignees, assignments, date_limit }) {
        const { tableReference } = this.state;
    
        if (date_limit) {
            assignments = assignments.filter(a => new Date(a.fields.created_at) > date_limit);
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
        const onMouseFuncs = (assigneeId, assignmentId) => {
            return {
                onEnter() {
                    const assignee = document.getElementById(`assignee-${assigneeId}`);
                    const assignment = document.getElementById(`assignment-${assignmentId}`);
                    const cell = document.getElementById(`assignee-${assigneeId}-assignment-${assignmentId}`);
                    assignee.style['background-color'] = 'lightblue';
                    assignment.style['background-color'] = 'lightblue';
                    cell.style['background-color'] = 'lightblue';
                },
                onLeave() {
                    const assignee = document.getElementById(`assignee-${assigneeId}`);
                    const assignment = document.getElementById(`assignment-${assignmentId}`);
                    const cell = document.getElementById(`assignee-${assigneeId}-assignment-${assignmentId}`);
                    assignee.style['background-color'] = 'transparent';
                    assignment.style['background-color'] = 'transparent';
                    cell.style['background-color'] = 'transparent';
                }
            }
        };
        for (const [key,value] of tableReference.entries()) {
            result.push(<tr>
                <td id={"assignee-" + key.pk} scope="row">{key.fields.name} {key.fields.last_name}</td>
                <td>{key.fields.position}</td>
                <td></td>
                {this.getCurrentAssignmentsBatch().map(a => {
                    const { onEnter, onLeave } = onMouseFuncs(key.pk, a.pk);
                    if (value.has(a)) {
                        const { deadline = 'Без дедлайну' } = a;
                        const finished_assignment = assignments_finished.find(af => af.fields.assignee === key.pk && af.fields.event_type === 'fn');
                        if (finished_assignment) {
                            const onClick = () => alert('Дедлайн: ' + deadline + '\nЗакінчено: ' + finished_assignment.fields.finished_at);
                            return <td id={`assignee-${key.pk}-assignment-${a.pk}`}><div onClick={onClick} onMouseEnter={onEnter} onMouseLeave={onLeave}>V</div></td>
                        }

                        return <td id={`assignee-${key.pk}-assignment-${a.pk}`}><div onClick={() => alert('Дедлайн:' + deadline)} onMouseEnter={onEnter} onMouseLeave={onLeave}>Виконується</div></td>
                    }
                    return <td id={`assignee-${key.pk}-assignment-${a.pk}`} onMouseEnter={onEnter} onMouseLeave={onLeave}> </td>
                })}
            </tr>)
        }
        return result;
    }

    getAssignmentsAsArrayOfTh() {
        const result = [];
        const assignments = this.getCurrentAssignmentsBatch();
        for (const assignment of assignments) {
            const date = new Date(assignment.fields.created_at);
            const onClick = () => this.props.openAssignment(assignment.pk);
            result.push(<th id={"assignment-" + assignment.pk} scope="col" onClick={onClick}>"{assignment.fields.title}" № {assignment.pk} від {dateformat(date, 'dd.mm.yyyy' )}</th>)
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
        
        console.log('Date_limit', target.value);
        const { assignees, assignments } = this.state;
        this.updateTableReference({
            assignees,
            assignments,
            date_limit: target.value
        });
    }

    render() {
        const { isLoading } = this.state;
        return (<div>
            {isLoading ?
            <div id="loading"></div> :
            <div>
                Статус виконання доручень за 
                <select onChange={this.onSelectedTimeChange.bind(this)}>
                    <option value="all" selected="selected">весь час</option>
                    <option value={new Date(Date.now() - 1000 * 60 * 60 * 24 * 31)}>місяць</option>
                    <option value={new Date(Date.now() - 1000 * 60 * 60 * 24 * 7)}>тиждень</option>
                </select>
                <table className="table table-bordered">
                    <tr>
                        <th colSpan="2" scope="col">Виконавці</th>
                        <th colSpan={PAGE_SIZE+2} scope="col">Доручення</th>
                    </tr>
                    <tr>
                        <th scope="col">ПІБ</th>
                        <th scope="col">Посада</th>
                        <th scope="col"><div className="btn btn-success" onClick={this.pageDecrease.bind(this)}>&#8592;</div></th>
                        {this.getAssignmentsAsArrayOfTh.call(this)}
                        <th scope="col"><div className="btn btn-success" onClick={this.pageIncrease.bind(this)}>&#8594;</div></th>
                    </tr>
                    {this.getTableReferencesAsTrs.call(this)}
                </table>
            </div>}
        </div>
        )
    }
}

export default AssignmentAssignee;
