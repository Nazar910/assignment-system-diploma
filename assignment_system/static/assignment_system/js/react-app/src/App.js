import React, { Component } from 'react';
import axios from 'axios';
import cookies from 'js-cookie';
import AssigneeAssignmentTable from './components/tables/assignments-assignees';
import OneAssignmentAssignees from './components/tables/one-assignment-assignees';
import { Tabs, TabList, Tab, TabPanel } from 'react-tabs';

class App extends Component {
    constructor(...args) {
        super(...args);

        this.state = {
            assignment_id: 0,
            selectedIndex: 0
        }

        this.openSingleAssignmentTable = this.openSingleAssignmentTable.bind(this);
        this.openAllAssignments = this.openAllAssignments.bind(this);
    }

    openSingleAssignmentTable(assignment_id) {
        this.setState({
            selectedIndex: 1,
            assignment_id
        });
    }

    openAllAssignments() {
        this.setState({
            selectedIndex: 0
        })
    }

    render() {
        return (
            <div>
                <Tabs selectedIndex={this.state.selectedIndex}>
                    <TabList>
                        <Tab onClick={this.openAllAssignments}>Відстежити виконання всіх доручень за період</Tab>
                        <Tab onClick={() => this.openSingleAssignmentTable()}>Відстежити виконання одного доручення</Tab>
                    </TabList>
                    <TabPanel><AssigneeAssignmentTable openAssignment={this.openSingleAssignmentTable}/></TabPanel>
                    <TabPanel><OneAssignmentAssignees assignment_id={this.state.assignment_id}/></TabPanel>
                </Tabs>
            </div>
        )
    }
}

export default App;
