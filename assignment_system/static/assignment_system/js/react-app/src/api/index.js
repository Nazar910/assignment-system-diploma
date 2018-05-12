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

export async function getEventsStartedforAssignment(id) {
    try {
        return await get(`assignments_started/assignment/${id}`);
    } catch (e) {
        if (e.response.status === 404) {
            return [];
        }
        throw e;
    }
}

export async function getEventsFinishedforAssignment(id) {
    try {
        return await get(`assignments_finished/assignment/${id}`);
    } catch (e) {
        if (e.response.status === 404) {
            return [];
        }
        throw e;
    }
}