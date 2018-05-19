import React, { Component } from 'react';
import dateformat from 'dateformat';
import Loader from '../Loader';
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
            assignment_id: props.assignment_id
        };

        this.displayErrorMessage = this.displayErrorMessage.bind(this);
        this.cleanError = this.cleanError.bind(this);
        this.onAssignmentIdChange = this.onAssignmentIdChange.bind(this);
    }

    componentDidMount() {
        let { assignment_id } = this.state;

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
            });
            document.getElementById('assignment-id').value = assignment_id;
        })
        .catch(e => {
            console.error('Something bad happened', e);
            if (e.assignee_404) {
                this.displayErrorMessage(`Доручення з номером ${assignment_id} не знайдено!`);
            }
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

            result.push(<tr className="one-assignment-table-trs">
                <td scope="row">{assignee.fields.name} {assignee.fields.last_name}</td>
                <td>{assignee.fields.position}</td>
                {status}
            </tr>)
        }
        return result;
    }

    displayErrorMessage(msg) {
        this.setState({
            errorMessage: msg
        });
    }

    cleanError() {
        this.setState({
            errorMessage: ''
        });
    }

    onAssignmentIdChange({target}) {
        const { value } = target;

        if (!value) {
            this.displayErrorMessage('Пусті вхідні дані!');
            return;
        }

        if (isNaN(value)) {
            this.displayErrorMessage('Номер доручення має бути числом!');
            return;
        }

        this.cleanError();
        this.setState({
            assignment_id: value,
            isLoading: true
        }, () => this.componentDidMount());
    }

    render() {
        const { assignment, isLoading, errorMessage } = this.state;
        return (
            <div>
                Статус виконання доручення № <input type="text" id="assignment-id" onChange={this.onAssignmentIdChange}/>
                {
                    errorMessage ? 
                    <div class="alert alert-danger">
                        { errorMessage }
                    </div> :
                    ""
                }
                {
                    isLoading ? 
                    <Loader /> :
                    <div>
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
