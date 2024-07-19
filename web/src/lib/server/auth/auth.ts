import type { Handle, RequestEvent } from '@sveltejs/kit';
import { api } from '../api';
import type { ApiSession } from './auth.interface';
import type { Session } from '@auth/sveltekit';
import type { ApiUser } from '$lib/user.interface';

export const AuthHandle: Handle = async ({ event, resolve }) => {
	event.locals.session = resolveSession(event);
	return resolve(event);
};

export const signOut = (event: RequestEvent) => {
	const sessionFromCookie = getFromCookies(event);
	if (sessionFromCookie) {
		api.get(`/session/${sessionFromCookie.token}/signout`);
	}
	event.cookies.delete('session', { path: '/', httpOnly: true, sameSite: 'strict', secure: true });
};

function resolveSession(event: RequestEvent) {
	return async () => {
		if (!await event.locals.auth()) {
			signOut(event);
			return undefined;
		}
		let session = await resolveFromCookies(event);
		if (!session) {
			session = await resolveFromServer(event, await event.locals.auth());
		}
		return session;
	};
}
async function resolveFromCookies(event: RequestEvent) {
	const session = getFromCookies(event);
	if (session) {
		return session;
	}
}

const resolveFromServer = async (event: RequestEvent, googleSession: Session | null) => {
	if (googleSession) {
		const session = await createSession(googleSession);
		if (session) {
			saveToCookies(event, session);
			return session;
		}
	}
};

function saveToCookies(event: RequestEvent, session: ApiSession) {
	const base64 = Buffer.from(JSON.stringify(session)).toString('base64');
	event.cookies.set('session', base64, {
		path: '/',
		httpOnly: true,
		sameSite: 'strict',
		secure: true
	});
}

function getFromCookies(event: RequestEvent): ApiSession | undefined {
	const base64 = event.cookies.get('session');
	if (base64) {
		const session = JSON.parse(Buffer.from(base64, 'base64').toString('utf8'));
		return session;
	}
	return undefined;
}

const createUserWithGoogleSession = (googleSession: Session) => {
	return api.post<ApiUser>('/user', { ...googleSession.user });
};

async function createSession(googleSession: Session): Promise<ApiSession | undefined> {
	try {
		return await api.post<ApiSession>('/session', { ...googleSession.user });
	} catch (error: any) {
		if (error.status === 401) {
			return createUserWithGoogleSession(googleSession).then(() => {
				return createSession(googleSession);
			});
		}
		throw error;
	}
}
