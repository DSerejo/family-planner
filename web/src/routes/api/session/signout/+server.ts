import { signOut } from "$lib/server/auth/auth";
import type { RequestEvent } from "./$types";

export function GET(event: RequestEvent) {
    signOut(event);
    return {
        status: 200,
        body: {
            message: "Signed out"
        }
    }
}