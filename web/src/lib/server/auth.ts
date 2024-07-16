import type { Handle } from "@sveltejs/kit"
// Generate a random ID
const getUniqueId = () => {
	return Math.random().toString(36).substring(2, 9);
}

export const AuthHandle: Handle = async ({event, resolve}) => {
    
    event.locals.requestId = getUniqueId();
    console.log(event.cookies.getAll())
	return await resolve(event)
}