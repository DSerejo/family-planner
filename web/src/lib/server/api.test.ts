import { fetchApi, api } from './api';
import { describe, it, expect, vi, beforeEach, type Mock } from 'vitest';

global.fetch = vi.fn();
const API_URL = process.env.API_URL;
describe('API functions', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it('fetchApi should append API_URL to relative URLs', async () => {
		const url = '/test';
		const options = { method: 'GET' };
		const response = { data: 'test' };
		(global.fetch as Mock).mockResolvedValueOnce({
			json: vi.fn().mockResolvedValueOnce(response),
			status: 200
		});

		const result = await fetchApi(url, options);

		expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/test`, options);
		expect(result).toEqual(response);
	});

	it('fetchApi should append query params to URL', async () => {
		const url = '/test';
		const options = { method: 'GET' };
		const params = { key: 'value' };
		const response = { data: 'test' };
		(global.fetch as Mock).mockResolvedValueOnce({
			json: vi.fn().mockResolvedValueOnce(response),
			status: 200
		});

		const result = await fetchApi(url, options, params);

		expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/test?key=value`, options);
		expect(result).toEqual(response);
	});

	it('api.post should call fetchApi with POST method', async () => {
		const url = '/test';
		const body = { key: 'value' };
		const response = { data: 'test' };
		(global.fetch as Mock).mockResolvedValueOnce({
			json: vi.fn().mockResolvedValueOnce(response),
			status: 200
		});

		const result = await api.post(url, body);

		expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/test`, expect.objectContaining({
				method: 'POST',
				body: JSON.stringify(body)
			})
		);
		expect(result).toEqual(response);
	});

	it('api.put should call fetchApi with PUT method', async () => {
		const url = '/test';
		const body = { key: 'value' };
		const response = { data: 'test' };
		(global.fetch as Mock).mockResolvedValueOnce({
			json: vi.fn().mockResolvedValueOnce(response),
			status: 200
		});

		const result = await api.put(url, body);

		expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/test`, expect.objectContaining({
				method: 'PUT',
				body: JSON.stringify(body)
			})
		);
		expect(result).toEqual(response);
	});

	it('api.get should call fetchApi with GET method and params', async () => {
		const url = '/test';
		const params = { key: 'value' };
		const response = { data: 'test' };
		(global.fetch as Mock).mockResolvedValueOnce({
			json: vi.fn().mockResolvedValueOnce(response),
			status: 200
		});

		const result = await api.get(url, params);

		expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/test?key=value`, expect.objectContaining({
				method: 'GET'
			})
		);
		expect(result).toEqual(response);
	});

	it('api.delete should call fetchApi with DELETE method and params', async () => {
		const url = '/test';
		const params = { key: 'value' };
		const response = { data: 'test' };
		(global.fetch as Mock).mockResolvedValueOnce({
			json: vi.fn().mockResolvedValueOnce(response),
			status: 200
		});

		const result = await api.delete(url, params);

		expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/test?key=value`, expect.objectContaining({
				method: 'DELETE'
			})
		);
		expect(result).toEqual(response);
	});
});
