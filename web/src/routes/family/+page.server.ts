import type { Family } from '$lib/family/family.interface.js';
import { signOut } from '$lib/server/auth/auth.js';
import { getUserWithFamilies } from '$lib/server/user/user.queries.js';
import {api} from '$lib/server/api/api'
import { redirect } from '@sveltejs/kit';
export const load = async (event): Promise<{ families?: Family[] }> => {
	await event.parent();
	let user;
	const googleSession = await event.locals.auth();
	if (googleSession) {
		user = await getUserWithFamilies(googleSession?.user?.email!).catch((error) => {
			if (error.message === 'Unauthorized') {
				signOut(event);
			}
			return null;
		});
	}
	return {
		families: user?.data.user.families
	};
};

export const actions = {
	delete: async (event) => {
    const formData = await event.request.formData();
    const familyId = formData.get('familyId');
    await api.delete(`/family/${familyId}`);
    return {success: true};
  }
}