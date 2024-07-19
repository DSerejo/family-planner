import type { Family } from '$lib/family/family.interface.js';

import { api } from '$lib/server/api.js';
export const load = async (event): Promise<{ family?: Family[] }> => {
    const hello = await api.get('/');
    
	return {
		family: event.locals.family
		//   family: [{id: '1', name: "Family 1"}, {id: '2', name: "Family 2"}]
	};
};

export const actions = {
	default: async (event) => {
        event.locals.family = [{id: '1', name: "Family 1"}, {id: '2', name: "Family 2"}]
        return {success: true}
	}
};
