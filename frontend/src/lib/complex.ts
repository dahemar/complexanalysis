export type Complex = { real: number; imag: number };

export type AddResult = {
	a: Complex;
	b: Complex;
	sum: Complex;
	plot_base64: string;
};

const TAU = 2 * Math.PI;

export function formatComplex(z: Complex): string {
	if (Math.abs(z.real) < 1e-9 && Math.abs(z.imag - TAU) < 1e-6) {
		return '2πi';
	}
	if (Math.abs(z.real) < 1e-9 && Math.abs(z.imag) < 1e-9) {
		return '0';
	}
	const sign = z.imag >= 0 ? '+' : '−';
	const imag = Math.abs(z.imag);
	const imagStr =
		imag === 1 ? 'i' : imag === 0 ? '' : `${trim(imag)}i`;
	if (imagStr === '') {
		return `${trim(z.real)}`;
	}
	if (z.real === 0) {
		const t = Math.abs(z.imag);
		if (Math.abs(t - Math.PI) < 1e-6) return 'πi';
		if (Math.abs(t - TAU) < 1e-6) return '2πi';
		return z.imag === 1 ? 'i' : z.imag === -1 ? '−i' : `${trim(z.imag)}i`;
	}
	return `${trim(z.real)} ${sign} ${imagStr}`.replace('− −', '− ');
}

function trim(n: number): string {
	const s = Number.isInteger(n) ? String(n) : n.toFixed(4).replace(/\.?0+$/, '');
	return s;
}

/** Empty = same origin (Vercel serverless /api or Astro dev proxy). */
const apiBase = import.meta.env.PUBLIC_API_URL?.replace(/\/$/, '') ?? '';

export async function addComplexNumbers(a: Complex, b: Complex): Promise<AddResult> {
	const url = `${apiBase}/api/complex/add`;

	let res: Response;
	try {
		res = await fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ a, b }),
		});
	} catch {
		const hint = apiBase
			? `Cannot reach API at ${apiBase}. Check PUBLIC_API_URL and CORS.`
			: 'Cannot reach /api/complex/add. Redeploy with api/complex/add.py or run the local backend.';
		throw new Error(hint);
	}

	if (!res.ok) {
		const text = await res.text();
		throw new Error(text || `Request failed (${res.status})`);
	}
	return res.json() as Promise<AddResult>;
}
