import React, { Component } from 'react';

const getElemValue = id => document.getElementById(id).value;
const getElemContent = id => document.getElementById(id).innerHTML;
const getHiddenvar = id => JSON.parse(getElemContent(id))

class AssignmentsEditor extends Component {
    constructor(props) {
        super(props);

        this.state = {
            assignment: getHiddenvar('assignment')[0],
            assignees: getHiddenvar('assignees'),
            selected_assignees: getHiddenvar('selected_assignees'),
            priorities: getHiddenvar('priorities')
        };
    }

    getTitleSection() {
        const { fields } = this.state.assignment;
        return (
            <div className="form-group">
                <label for="title">Заголовок</label>
                <input type="text" className="form-control" id="title" aria-describedby="titleHelp" placeholder="Введіть заголовок" value={fields.title}/>
                <small id="titleHelp" className="form-text text-muted">короткий опис змісту доручення</small>
            </div>
        )
    }

    getDescriptionSection() {
        const { fields } = this.state.assignment;
        return (
            <div className="form-group">
                <label for="description">Опис</label>
                <textarea className="form-control" id="description" rows="3" value={fields.description}></textarea>
            </div>
        )
    }
    
    getAssigneesSection() {
        const { assignees, selected_assignees } = this.state;
        const options = [];
        for (const a of assignees) {
            const { name, last_name, email } = a.fields;

            let option = '';

            if (selected_assignees.find(s_a => s_a.fields.email === email)) {
                option = <option value={email} selected>
                            {name} {last_name}
                        </option>
            } else {
                option = <option value={email}>
                            {name} {last_name}
                        </option>
            }

            options.push(option);
        }
        return (
            <div className="form-group">
                <label for="assignees">Виконавці</label>
                <select multiple className="form-control" id="assignees">
                    {options}
                </select>
            </div>
        )
    }

    getPriorityLvlSection() {
        const { priorities } = this.state;
        const options = [];

        const capitalize = str => str[0].toUpperCase() + str.slice(1).toLowerCase();

        for (const name of Object.keys(priorities)) {
            options.push(
                <option value={priorities[name]}>{capitalize(name)}</option>
            )
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
        const { fields } = this.state.assignment;
        return (
            <div>
                <label for="deadline" class="col-2 col-form-label">Дата закінчення: </label>
                <input class="form-control" type="datetime-local" id="deadline"/>
            </div>
        )
    }

    getAttachmentsSection() {
        return (
            <div>Attachments</div>
        )
    }

    onSubmit(e) {
        e.preventDefault();
        console.log('Title:', getElemValue('title'));
        console.log('Description:', getElemContent('description'));
        console.log('Piority lvl:', getElemValue('priorities'));
        console.log('DeadLine:', getElemValue('deadline'));
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
                    {this.getAttachmentsSection.call(this)}
                    <button type="submit" class="btn btn-primary" onClick={this.onSubmit}>Підтвердити</button>
                </form>
            </div>
        )
    }
}

export default AssignmentsEditor;
