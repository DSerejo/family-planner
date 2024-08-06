// See https://kit.svelte.dev/docs/types#app

import type { ApiSession } from "$lib/server/auth/auth.interface";
import type { Session } from "@auth/sveltekit";

// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			session: () => Promise<ApiSession | undefined>
			families?: Family[]
			mappedFamilies?: { [key: string]: Family }
			error?: string
		}
		interface PageData {
			googleSession: Session
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
