import type { Family } from '$lib/family/family.interface.js';
import { signOut } from '$lib/server/auth/auth.js';
import { getUserWithFamilies } from '$lib/server/user/user.queries.js';
export const load = async (event): Promise<{ families?: Family[] }> => {
    let user;
    const googleSession = await event.locals.auth()
    if(googleSession) {
      user = await getUserWithFamilies(googleSession?.user?.email!).catch(
        (error) => {
        if(error.message === "Unauthorized") {
          signOut(event)
        }
        return null
      }
      )
    }
	return {
		families: user?.data.user.families
	};
};

export const actions = {
	default: async (event) => {
        event.locals.families = [{id: '1', name: "Family 1"}, {id: '2', name: "Family 2"}]
        return {success: true}
	}
};
