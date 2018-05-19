import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import AssignmentList from './components/assignment/AssignmentList';
import AssignmentEditor from './components/assignment/AssignmentEditor';

const apps = {
    'home-page': <App />,
    'assignment-list-page': <AssignmentList />,
    'assignment-editor-page': <AssignmentEditor />
};

for (const app of Object.keys(apps)) {
    const elem = document.getElementById(app);
    if (elem) {
        ReactDOM.render(
            apps[app],
            elem
        )
        break;
    }
}
