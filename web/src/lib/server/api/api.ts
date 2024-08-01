import { API_KEY } from '$env/static/private';
const API_URL = "https://api.family-planner.local.com"

let token: string | null = null

export const setToken = (t: string) => {
	token = t
}
export const fetchApi = async (
	url: string,
	options: RequestInit,
	params?: Record<string, string>
) => {
	if (url.startsWith('/')) {
		url = `${API_URL}${url}`;
	}
	if (params) {
		const urlWithParams = new URL(url, API_URL);
		Object.entries(params).forEach(([key, value]) => {
			urlWithParams.searchParams.append(key, value);
		});
		url = urlWithParams.toString();
	}
	// allow self signed certificates
	if (process.env.NODE_ENV === 'development') {
		process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
	}
	options.headers = {
		Authorization: `Bearer ${token}`,
		'Content-Type': 'application/json',
		...(options.headers || {})
	};
	const response = await fetch(url, options);
	const json = await response.json();
	if (response.status !== 200 && response.status !== 201) {
		throw {
			status: response.status,
			message: json
		};
	}
	return json;
};

export type Body = Record<string, any>;
export type Params = Record<string, string>;

export type Api = {
	post: <R = unknown, T extends Body = Body>(url: string, body: T, options?: RequestInit) => Promise<R>;
	put: <R = unknown, T extends Body = Body>(url: string, body: T, options?: RequestInit) => Promise<R>;
	get: <R = unknown, T extends Params = Params>(
		url: string,
		params?: T,
		options?: RequestInit
	) => Promise<R>;
	delete: <R = unknown, T extends Params = Params>(
		url: string,
		params?: T,
		options?: RequestInit
	) => Promise<R>;
};

export const api: Api = {	
	post: async (url, body, options) => fetchApi(url, { method: 'POST', body: JSON.stringify(body), ...options }),
	put: async (url, body, options) => fetchApi(url, { method: 'PUT', body: JSON.stringify(body), ...options }),
	get: async (url, params, options) => fetchApi(url, { method: 'GET', ...options }, params),
	delete: async (url, params, options) => fetchApi(url, { method: 'DELETE', ...options }, params)
};
