import React, { Component } from 'react';

const getElemValue = id => document.getElementById(id).value;
const getElemContent = id => document.getElementById(id).innerHTML;
const getHiddenvar = id => JSON.parse(getElemContent(id))

class AssignmentsEditor extends Component {
    constructor(props) {
        super(props);

        this.state = {
            assignment: getHiddenvar('assignment')[0],
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
        return (
            <div>Assigneeeeees</div>
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
            <div>
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
                <label for="example-datetime-local-input" class="col-2 col-form-label">Date and time</label>
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
