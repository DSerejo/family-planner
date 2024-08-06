import { familyService } from '$lib/family/family.service.js';
export const load = async (event) => {
	await event.parent()
	const family = await familyService.getFamily(event.params.slug);
    return {
		family
	};
};

export const actions = {
	deleteFamilyMember: async (event) => {
		const formData = await event.request.formData();
		const memberId = formData.get('memberId');
		if(memberId) {
			familyService.deleteFamilyMember(event.params.slug, memberId.toString());
		}
	}
};