import axios from 'axios';
import cookies from 'js-cookie';

async function get(url) {
    console.log('Url is', url);
    return (
        await axios({
            url: `/assignment_system/${url}`,
            headers: {
                'X-CSRFToken': cookies.get('csrftoken'),
                'Accept': 'application/json'
            },
            method: 'GET'
        })
    ).data;
}

export async function getList(resourceType, args = '') {
    return (
        await axios({
            url: `/assignment_system/${resourceType}${args}`,
            headers: {
                'X-CSRFToken': cookies.get('csrftoken'),
                'Accept': 'application/json'
            },
            method: 'GET'
        })
    ).data;
}

export async function getOne(resourceType, id) {
    return (await get(`${resourceType}/${id}`))[0];
}

export function getAssignment(id) {
    return getOne('assignments', id);
}

export function getAssignmentAssignees(id) {
    return get(`assignees/assignment/${id}`);
}

export function getEventsStartedforAssignment(id) {
    return get(`assignments_started/assignment/${id}`);
}

export function getEventsFinishedforAssignment(id) {
    return get(`assignments_finished/assignment/${id}`);
}