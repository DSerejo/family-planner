import { api } from "$lib/server/api/api";
import { redirect } from "@sveltejs/kit";

export const actions = {
	default: async (event) => {
		const formData = await event.request.formData();
		const familyName = formData.get('familyName');
		await api.post('/family', { name: familyName });
		throw redirect(302, '/family');
	}
};