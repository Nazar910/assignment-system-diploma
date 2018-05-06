import React, { Component } from 'react';
import axios from 'axios';
import cookies from 'js-cookie';
import AssigneeAssignmentTable from './components/tables/assignments-assignees';
import { Tabs, TabList, Tab, TabPanel } from 'react-tabs';

const title = 'Hi from react App component page';

async function doRequest() {
    console.log('Requesting');
    const data = {
        a: 'b'
    };
    console.log(cookies.get('csrftoken'));
    const resp = await axios({
        url: '/assignment_system/assignees/1',
        headers: {
            'X-CSRFToken': cookies.get('csrftoken')
        },
        data,
        method: 'POST'
    });
    console.log('Done');
    console.log(resp);
}

class App extends Component {
    constructor(...args) {
        super(...args);

        this.state = {}
    }

    render() {
        return (
            <div>
                <Tabs>
                    <TabList>
                        <Tab>Відстежити виконання всіх доручень за період</Tab>
                        <Tab>Відстежити виконання одного доручення</Tab>
                    </TabList>
                    <TabPanel><AssigneeAssignmentTable /></TabPanel>
                    <TabPanel>asdsa</TabPanel>
                </Tabs>
            </div>
        )
    }
}

export default App;
