import type { Complex } from './complex';

export type ContourTrace = {
	n: number;
	R: number;
	tau: number;
	dt: number;
	steps: number;
	integrand_scale: number;
	display_extent: number;
	note: string;
	closed_integral: Complex;
	closed_label: string;
	z_points: Complex[];
	integrand_points: Complex[];
	path: Complex[];
	plot_base64: string;
};

const apiBase = import.meta.env.PUBLIC_API_URL?.replace(/\/$/, '') ?? '';

export async function fetchContourTrace(n: number): Promise<ContourTrace> {
	const url = `${apiBase}/api/contour/trace`;
	let res: Response;
	try {
		res = await fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ n }),
		});
	} catch {
		throw new Error(
			apiBase
				? `Cannot reach API at ${apiBase}.`
				: 'Cannot reach /api/contour/trace. Start the backend or redeploy Vercel.',
		);
	}
	if (!res.ok) {
		const text = await res.text();
		throw new Error(text || `Request failed (${res.status})`);
	}
	return res.json() as Promise<ContourTrace>;
}
