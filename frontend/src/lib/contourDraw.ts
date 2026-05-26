import type { Complex } from './complex';

export type CanvasPoint = { x: number; y: number };

export function toCanvas(c: Complex): CanvasPoint {
	return { x: c.real, y: -c.imag };
}

export function drawGrid(
	ctx: CanvasRenderingContext2D,
	cx: number,
	cy: number,
	size: number,
): void {
	const half = size / 2;
	ctx.save();
	ctx.translate(cx, cy);

	ctx.strokeStyle = '#ececec';
	ctx.lineWidth = 1;
	for (let i = -2; i <= 2; i++) {
		if (i === 0) continue;
		ctx.beginPath();
		ctx.moveTo(-half + 14, (i * half) / 2.5);
		ctx.lineTo(half - 14, (i * half) / 2.5);
		ctx.stroke();
		ctx.beginPath();
		ctx.moveTo((i * half) / 2.5, -half + 14);
		ctx.lineTo((i * half) / 2.5, half - 14);
		ctx.stroke();
	}

	ctx.strokeStyle = '#c8c8c8';
	ctx.lineWidth = 1.25;
	ctx.beginPath();
	ctx.moveTo(-half + 14, 0);
	ctx.lineTo(half - 14, 0);
	ctx.moveTo(0, -half + 14);
	ctx.lineTo(0, half - 14);
	ctx.stroke();

	ctx.fillStyle = '#999';
	ctx.font = '500 10px system-ui, sans-serif';
	ctx.fillText('Re', half - 24, 5);
	ctx.fillText('Im', 6, -half + 20);
	ctx.restore();
}

export function drawContourPanel(
	ctx: CanvasRenderingContext2D,
	cx: number,
	cy: number,
	R: number,
	t: number,
	z: Complex,
	integrand: Complex,
	integrandScale: number,
): void {
	ctx.save();
	ctx.translate(cx, cy);

	// full circle
	ctx.strokeStyle = '#e0e0e0';
	ctx.lineWidth = 1.5;
	ctx.beginPath();
	ctx.arc(0, 0, R, 0, Math.PI * 2);
	ctx.stroke();

	// traced arc 0 → t (math CCW; canvas y is flipped)
	if (t > 0.001) {
		ctx.strokeStyle = '#e76f51';
		ctx.lineWidth = 2.5;
		ctx.beginPath();
		ctx.arc(0, 0, R, 0, -t, true);
		ctx.stroke();
	}

	const pos = toCanvas(z);
	ctx.fillStyle = '#e76f51';
	ctx.beginPath();
	ctx.arc(pos.x, pos.y, 5.5, 0, Math.PI * 2);
	ctx.fill();

	const v = toCanvas(integrand);
	const vx = pos.x + integrandScale * v.x;
	const vy = pos.y + integrandScale * v.y;
	ctx.strokeStyle = '#2a6f9d';
	ctx.lineWidth = 2;
	ctx.beginPath();
	ctx.moveTo(pos.x, pos.y);
	ctx.lineTo(vx, vy);
	ctx.stroke();

	// arrowhead
	const dx = vx - pos.x;
	const dy = vy - pos.y;
	const len = Math.hypot(dx, dy) || 1;
	const ux = dx / len;
	const uy = dy / len;
	ctx.fillStyle = '#2a6f9d';
	ctx.beginPath();
	ctx.moveTo(vx, vy);
	ctx.lineTo(vx - 7 * ux + 4 * uy, vy - 7 * uy - 4 * ux);
	ctx.lineTo(vx - 7 * ux - 4 * uy, vy - 7 * uy + 4 * ux);
	ctx.fill();

	ctx.fillStyle = '#1a1a1a';
	ctx.beginPath();
	ctx.arc(0, 0, 3, 0, Math.PI * 2);
	ctx.fill();

	ctx.restore();
}

/** Scale integral-plane coordinates to fit the canvas (values are O(2π), not O(R)). */
export function scaleIntegralPath(path: Complex[], panelHalf: number): CanvasPoint[] {
	if (path.length === 0) return [];

	let maxAbs = 1e-6;
	for (const p of path) {
		maxAbs = Math.max(maxAbs, Math.abs(p.real), Math.abs(p.imag));
	}
	const scale = (panelHalf - 18) / maxAbs;

	return path.map((p) => ({
		x: p.real * scale,
		y: -p.imag * scale,
	}));
}

export function drawIntegralPanel(
	ctx: CanvasRenderingContext2D,
	cx: number,
	cy: number,
	path: CanvasPoint[],
): void {
	ctx.save();
	ctx.translate(cx, cy);

	if (path.length > 1) {
		ctx.strokeStyle = '#5c5ce0';
		ctx.lineWidth = 2.25;
		ctx.lineJoin = 'round';
		ctx.lineCap = 'round';
		ctx.beginPath();
		ctx.moveTo(path[0].x, path[0].y);
		for (let i = 1; i < path.length; i++) {
			ctx.lineTo(path[i].x, path[i].y);
		}
		ctx.stroke();
	}

	const tip = path[path.length - 1];
	if (tip) {
		ctx.fillStyle = '#5c5ce0';
		ctx.beginPath();
		ctx.arc(tip.x, tip.y, 4.5, 0, Math.PI * 2);
		ctx.fill();
	}

	ctx.fillStyle = '#1a1a1a';
	ctx.beginPath();
	ctx.arc(0, 0, 3, 0, Math.PI * 2);
	ctx.fill();

	ctx.restore();
}
