import { API_KEY } from '$env/static/private';

const API_URL = process.env.API_URL;

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
		...(options.headers || {}),
		Authorization: `Bearer ${API_KEY}`,
		'Content-Type': 'application/json'
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
	post: <R = unknown, T extends Body = Body>(url: string, body: T) => Promise<R>;
	put: <R = unknown, T extends Body = Body>(url: string, body: T) => Promise<R>;
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
	post: async (url, body) => fetchApi(url, { method: 'POST', body: JSON.stringify(body) }),
	put: async (url, body) => fetchApi(url, { method: 'PUT', body: JSON.stringify(body) }),
	get: async (url, params, options) => fetchApi(url, { method: 'GET', ...options }, params),
	delete: async (url, params, options) => fetchApi(url, { method: 'DELETE', ...options }, params)
};
