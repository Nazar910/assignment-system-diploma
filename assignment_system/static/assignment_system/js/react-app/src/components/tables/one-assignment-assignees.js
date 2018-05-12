import React, { Component } from 'react';
import dateformat from 'dateformat';
import { 
    getAssignment,
    getAssignmentAssignees,
    getEventsStartedforAssignment,
    getEventsFinishedforAssignment
} from '../../api';

class OneAssignmentAssignees extends Component {
    constructor(props) {
        super(props);

        this.state = {
            assignment: {},
            assignees: [],
            assigneeMap: new Map(),
            isLoading: true,
        };
    }

    componentDidMount() {
        let { assignment_id } = this.props;

        if (!assignment_id) {
            assignment_id = prompt('Введіть номер потрібного доручення!', '6');
        }
        Promise.all([
            getAssignment(assignment_id),
            getAssignmentAssignees(assignment_id),
            getEventsStartedforAssignment(assignment_id),
            getEventsFinishedforAssignment(assignment_id)
        ])
        .then(([
            assignment,
            assignees,
            assignments_started,
            assignments_finished
        ]) => {
            const assignmentsFinishedMap = new Map();
            
            const assigneeMap = new Map();

            assignees.forEach(a => {
                const finished = assignments_finished.filter(af => af.fields.assignee === a.pk);
                const started = assignments_started.filter(as => as.fields.assignee === a.pk);
                assigneeMap.set(a, [...finished, ...started])
            })

            this.setState({
                assignment,
                assignees,
                assigneeMap,
                isLoading: false
            })
        });
    }

    getAssigneesTrs() {
        const result = [];
        const { assigneeMap, assignment } = this.state;
        const { deadline = 'Без дедлайну' } = assignment;
        for (const [assignee, events] of assigneeMap.entries()) {
            let status = <td> </td>;

            const stEvent = events.find(e => e.fields.event_type === 'st');
            const fnEvent = events.find(e => e.fields.event_type === 'fn');

            if (fnEvent) {
                status = <td><div onClick={() => alert('Дедлайн: ' + deadline + '\nЗакінчено: ' + fnEvent.fields.date)}>V</div></td>
            } else if (stEvent) {
                status = <td><div onClick={() => alert('Дедлайн:' + deadline)}>Виконується</div></td>
            }

            result.push(<tr>
                <td scope="row">{assignee.fields.name} {assignee.fields.last_name}</td>
                <td>{assignee.fields.position}</td>
                {status}
            </tr>)
        }
        return result;
    }

    render() {
        const { assignment, isLoading } = this.state;
        return (
            <div>
                {
                    isLoading ? 
                    <div id="loading"></div> :
                    <div>
                        Статус виконання доручення № {assignment.pk}
                        <table className="table table-bordered">
                            <tr>
                                <th colSpan="2" scope="col">Виконавці</th>
                                <th scope="col">Доручення</th>
                            </tr>
                            <tr>
                                <th scope="col">ПІБ</th>
                                <th scope="col">Посада</th>
                                <th scope="col">
                                    "{assignment.fields.title}"
                                    № {assignment.pk} від 
                                    {dateformat(new Date(assignment.fields.created_at), 'dd.mm.yyyy' )}
                                </th>
                            </tr>
                            {this.getAssigneesTrs.call(this)}
                        </table>
                    </div>
                }
            </div>
        )
    }
}

export default OneAssignmentAssignees;
