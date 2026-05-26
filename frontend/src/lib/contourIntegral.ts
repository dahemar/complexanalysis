export type Point = { x: number; y: number };

export const RADIUS = 88;
export const DT = 0.028;
export const INTEGRAND_SCALE = 42;
export const PATH_SCALE = 1.85;

/** z(t) = R e^{it} on the circle |z| = R. */
export function zOnCircle(R: number, t: number): Point {
	return { x: R * Math.cos(t), y: R * Math.sin(t) };
}

/**
 * Integrand f(z) dz for f(z) = 1/z^n and z(t) = R e^{it}.
 * Equivalent to i R^{1-n} e^{-i(n-1)t} in complex form.
 */
export function integrand(n: number, R: number, t: number): Point {
	const mag = Math.pow(R, 1 - n);
	const angle = -(n - 1) * t;
	return {
		x: -mag * Math.sin(angle),
		y: mag * Math.cos(angle),
	};
}

/** Closed-path value is 0 for n > 1 and 2πi for n = 1 (unit circle, R = 1). */
export function expectedResidueNote(n: number): string {
	if (n === 1) {
		return 'For n = 1 the path encloses a simple pole: ∮ 1/z dz = 2πi (nonzero).';
	}
	return `For n > 1 the pole at 0 has order ${n}: the contour integral is 0.`;
}

export function drawPanel(
	ctx: CanvasRenderingContext2D,
	cx: number,
	cy: number,
	size: number,
): void {
	const half = size / 2;
	ctx.save();
	ctx.translate(cx, cy);

	ctx.strokeStyle = '#ebebeb';
	ctx.lineWidth = 1;
	for (let i = -2; i <= 2; i++) {
		if (i === 0) continue;
		ctx.beginPath();
		ctx.moveTo(-half + 12, i * (half / 2.5));
		ctx.lineTo(half - 12, i * (half / 2.5));
		ctx.stroke();
		ctx.beginPath();
		ctx.moveTo(i * (half / 2.5), -half + 12);
		ctx.lineTo(i * (half / 2.5), half - 12);
		ctx.stroke();
	}

	ctx.strokeStyle = '#bbb';
	ctx.lineWidth = 1.25;
	ctx.beginPath();
	ctx.moveTo(-half + 12, 0);
	ctx.lineTo(half - 12, 0);
	ctx.moveTo(0, -half + 12);
	ctx.lineTo(0, half - 12);
	ctx.stroke();

	ctx.fillStyle = '#888';
	ctx.font = '10px system-ui, sans-serif';
	ctx.fillText('Re', half - 22, 4);
	ctx.fillText('Im', 5, -half + 18);

	ctx.restore();
}

export function drawLeftPanel(
	ctx: CanvasRenderingContext2D,
	cx: number,
	cy: number,
	n: number,
	t: number,
): void {
	const R = RADIUS;
	ctx.save();
	ctx.translate(cx, cy);

	ctx.strokeStyle = '#ccc';
	ctx.lineWidth = 1.5;
	ctx.beginPath();
	ctx.arc(0, 0, R, 0, Math.PI * 2);
	ctx.stroke();

	const pos = zOnCircle(R, t);
	ctx.fillStyle = '#e76f51';
	ctx.beginPath();
	ctx.arc(pos.x, pos.y, 5, 0, Math.PI * 2);
	ctx.fill();

	const v = integrand(n, R, t);
	ctx.strokeStyle = '#2a6f9d';
	ctx.lineWidth = 2;
	ctx.beginPath();
	ctx.moveTo(pos.x, pos.y);
	ctx.lineTo(pos.x + INTEGRAND_SCALE * v.x, pos.y - INTEGRAND_SCALE * v.y);
	ctx.stroke();

	ctx.fillStyle = '#1a1a1a';
	ctx.beginPath();
	ctx.arc(0, 0, 3, 0, Math.PI * 2);
	ctx.fill();

	ctx.restore();
}

export function drawRightPanel(
	ctx: CanvasRenderingContext2D,
	cx: number,
	cy: number,
	path: Point[],
): void {
	ctx.save();
	ctx.translate(cx, cy);

	if (path.length > 1) {
		ctx.strokeStyle = '#5c5ce0';
		ctx.lineWidth = 2;
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
		ctx.arc(tip.x, tip.y, 4, 0, Math.PI * 2);
		ctx.fill();
	}

	ctx.fillStyle = '#1a1a1a';
	ctx.beginPath();
	ctx.arc(0, 0, 3, 0, Math.PI * 2);
	ctx.fill();

	ctx.restore();
}
