import axios from 'axios';
import cookies from 'js-cookie';

export async function getList(resourceType) {
    const resp = await axios({
        url: `/assignment_system/${resourceType}`,
        headers: {
            'X-CSRFToken': cookies.get('csrftoken'),
            'Accept': 'application/json'
        },
        method: 'GET'
    });
    return resp.data
}
