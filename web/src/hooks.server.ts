
import { SvelteKitAuth } from "@auth/sveltekit" 
import {GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, AUTH_TRUST_HOST, AUTH_SECRET} from "$env/static/private" 
import Google from "@auth/core/providers/google"; 
import { sequence } from "@sveltejs/kit/hooks";
import { AuthHandle } from "$lib/server/auth";
import { setEnvDefaults } from "@auth/core";

const config = {
    providers: [Google({ clientId: GOOGLE_CLIENT_ID, clientSecret: GOOGLE_CLIENT_SECRET })],
    secret: AUTH_SECRET,
}
setEnvDefaults({
    AUTH_TRUST_HOST: AUTH_TRUST_HOST,
    AUTH_SECRET: AUTH_SECRET
}, config)
const {handle: authInitHandle} = SvelteKitAuth(config);

console.log(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, AUTH_TRUST_HOST)



export const handle = sequence(authInitHandle, AuthHandle);