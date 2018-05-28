import React, { Component } from 'react';
import Messages from '../messages/Messages';
import { updateAssignment, createAssignment } from '../../api/index';
import $ from 'jquery';

const getElemValue = id => document.getElementById(id).value;
const getElemContent = id => document.getElementById(id).innerHTML;
const getHiddenvar = id => JSON.parse(getElemContent(id))

class AssignmentsEditor extends Component {
    constructor(props) {
        super(props);

        this.state = {
            is_new: getHiddenvar('is_new'),
            assignment: getHiddenvar('assignment')[0],
            assignees: getHiddenvar('assignees'),
            selected_assignees: getHiddenvar('selected_assignees'),
            priorities: getHiddenvar('priorities')
        };
    }

    componentDidMount() {
        if (this.state.is_new) {
            return;
        }

        const { selected_assignees } = this.state;
        const { fields } = this.state.assignment;
        $('#title').val(fields.title);
        $('#description').val(fields.description);
        const deadline = (fields.deadline || '').replace('Z', '')
        $('input#deadline').val(deadline);

        for (const s_a of selected_assignees) {
            $(`select#assignees_select option[value="${s_a.pk}"]`)[0].selected = true;
        }
    }

    getTitleSection() {
        return (
            <div className="form-group">
                <label for="title">Заголовок</label>
                <input type="text" className="form-control" id="title" aria-describedby="titleHelp" placeholder="Введіть заголовок"/>
                <small id="titleHelp" className="form-text text-muted">короткий опис змісту доручення</small>
            </div>
        )
    }

    getDescriptionSection() {
        return (
            <div className="form-group">
                <label for="description">Опис</label>
                <textarea className="form-control" id="description" rows="3"></textarea>
            </div>
        )
    }
    
    getAssigneesSection() {
        const { assignees, selected_assignees } = this.state;
        const options = [];
        for (const a of assignees) {
            const { name, last_name } = a.fields;

            let option = '';

            if (selected_assignees.find(s_a => s_a.pk === a.pk)) {
                option = <option key={a.pk} value={a.pk} selected="selected">
                            {name} {last_name}
                        </option>
            } else {
                option = <option key={a.pk} value={a.pk}>
                            {name} {last_name}
                        </option>
            }

            options.push(option);
        }
        return (
            <div className="form-group">
                <label for="assignees_select">Виконавці</label>
                <select multiple className="form-control" id="assignees_select">
                    {options}
                </select>
            </div>
        )
    }

    getPriorityLvlSection() {
        const { priorities, assignment } = this.state;
        const options = [];

        const capitalize = str => str[0].toUpperCase() + str.slice(1).toLowerCase();

        for (const name of Object.keys(priorities)) {
            if (assignment && assignment.fields.priority_level === priorities[name]) {
                options.push(
                    <option selected value={priorities[name]}>{capitalize(name)}</option>
                )
            }
            else {
                options.push(
                    <option value={priorities[name]}>{capitalize(name)}</option>
                )
            }
        }

        return (
            <div className="form-group">
                <label for="priorities">Пріорітет</label>
                <select className="form-control" id="priorities">
                    {options}
                </select>
            </div>
        )
    }

    getDeadLineSection() {
        return (
            <div>
                <label for="deadline" className="col-2 col-form-label">Дата закінчення: </label>
                <input className="form-control" type="datetime-local" id="deadline"/>
            </div>
        )
    }

    onSubmit(e) {
        e.preventDefault();
        console.log('Title:', getElemValue('title'));
        console.log('Description:', $('textarea#description').val());
        console.log('Piority lvl:', getElemValue('priorities'));
        console.log('DeadLine:', $('input#deadline').val());
        console.log('Assignees:', $('#assignees_select').val());
        const body = {
            title: getElemValue('title'),
            description: $('textarea#description').val(),
            priority: getElemValue('priorities'),
            deadline: getElemValue('deadline'),
            assignees: $('#assignees_select').val()
        }

        if (this.state.is_new) {
            console.log('About to create one');
            createAssignment(body).then(([data]) => window.location.href = '/assignment_system/assignments/edit/' + data.pk);
            return;
        }

        const id = this.state.assignment.pk;
        updateAssignment(id, body);
    }

    render() {
        return (
            <div>
                <form>
                    {this.getTitleSection.call(this)}
                    {this.getDescriptionSection.call(this)}
                    {this.getAssigneesSection.call(this)}
                    {this.getPriorityLvlSection.call(this)}
                    {this.getDeadLineSection.call(this)}
                    <button type="submit" className="btn btn-primary" onClick={this.onSubmit.bind(this)}>Підтвердити</button>
                    <h5>Повідомлення</h5>
                    <Messages />
                </form>
            </div>
        )
    }
}

export default AssignmentsEditor;
