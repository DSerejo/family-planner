
import { SvelteKitAuth } from "@auth/sveltekit" 
import {GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET} from "$env/static/private" 
import Google from "@auth/core/providers/google"; 
import { sequence } from "@sveltejs/kit/hooks";
import { AuthHandle } from "$lib/server/auth";
const {handle: authInitHandle} = SvelteKitAuth({
	providers: [Google({ clientId: GOOGLE_CLIENT_ID, clientSecret: GOOGLE_CLIENT_SECRET })] 
});



export const handle = sequence(authInitHandle, AuthHandle);