
import { redirect, type Actions } from "@sveltejs/kit"
import { familyService, familyLocalsService } from "$lib/family/family.service"

export const load = async (event) => {
    return {
        error: event.locals.error,
        familyId: event.params.slug
    }
}

export const actions: Actions = {
    default: async (event) => {
        const formData = await event.request.formData()
        const name = formData.get("name")
        const email = formData.get("email")
        const familiyId = event.params.slug!
        const data: any = {}
        data['name'] = name;
        if(email) {
            data['email'] = email;
        }
        try {
            const newMember = await familyService.addMember(familiyId, data)
            familyLocalsService.addMember(event, familiyId, newMember)
            throw redirect(303, '/family/' + familiyId );
        } catch (error: any) {
            if(error.status == 303) {
                throw error
            }
            let message: string = '';
            if(error.status == 400 || error.status == 404) {
                message = error.message?.detail
            }
            if(error.status == 422) {
                message = error.message?.detail[0].msg
            }
            if(!message) {
                message = "Error adding member"
            }
            event.locals.error = message
            return {
                error: message
            }
        }
        

    }
}