import type { Complex } from './complex';

const SIZE = 300;
const PAD = 36;

type PlotPoints = { a: Complex; b: Complex; sum: Complex };

export function drawArgandPlane(
	svg: SVGSVGElement,
	points: PlotPoints | null,
): void {
	if (!svg) return;

	svg.setAttribute('viewBox', `0 0 ${SIZE} ${SIZE}`);
	svg.innerHTML = '';

	const g = el('g');
	svg.appendChild(g);

	if (!points) {
		const extent = 3;
		drawAxes(g, extent, makeScale(extent));
		return;
	}

	const extent = extentFor(
		Math.max(
			...[
				points.a.real,
				points.a.imag,
				points.b.real,
				points.b.imag,
				points.sum.real,
				points.sum.imag,
			].map(Math.abs),
			1,
		),
	);

	const scale = makeScale(extent);
	drawAxes(g, extent, scale);

	const o = { x: scale.x(0), y: scale.y(0) };
	const tipA = { x: scale.x(points.a.real), y: scale.y(points.a.imag) };
	const tipB = { x: scale.x(points.b.real), y: scale.y(points.b.imag) };
	const tipS = { x: scale.x(points.sum.real), y: scale.y(points.sum.imag) };

	line(g, o.x, o.y, tipA.x, tipA.y, '#e76f51', 2);
	line(g, o.x, o.y, tipB.x, tipB.y, '#2a9d8f', 2);
	dashedLine(g, tipA.x, tipA.y, tipS.x, tipS.y, '#2a9d8f');
	dashedLine(g, tipB.x, tipB.y, tipS.x, tipS.y, '#e76f51');
	line(g, o.x, o.y, tipS.x, tipS.y, '#5c5ce0', 2.5);

	dot(g, tipA, '#e76f51', 'a');
	dot(g, tipB, '#2a9d8f', 'b');
	dot(g, tipS, '#5c5ce0', 'z');
}

function extentFor(maxAbs: number): number {
	return Math.max(2, Math.ceil(maxAbs * 1.2));
}

function makeScale(extent: number) {
	const span = SIZE - 2 * PAD;
	const center = SIZE / 2;
	const unit = span / (2 * extent);
	return {
		x: (real: number) => center + real * unit,
		y: (imag: number) => center - imag * unit,
	};
}

function drawAxes(
	g: SVGGElement,
	extent: number,
	scale: ReturnType<typeof makeScale>,
): void {
	const axisColor = '#bbb';
	const gridColor = '#ebebeb';
	const zeroX = scale.x(0);
	const zeroY = scale.y(0);

	for (let i = -extent; i <= extent; i++) {
		if (i === 0) continue;
		const x = scale.x(i);
		const y = scale.y(i);
		line(g, x, PAD, x, SIZE - PAD, gridColor, 1);
		line(g, PAD, y, SIZE - PAD, y, gridColor, 1);
	}

	line(g, PAD, zeroY, SIZE - PAD, zeroY, axisColor, 1.25);
	line(g, zeroX, PAD, zeroX, SIZE - PAD, axisColor, 1.25);

	const reLabel = el('text', {
		x: String(SIZE - PAD + 2),
		y: String(zeroY + 4),
		fill: '#888',
		'font-size': '10',
	});
	reLabel.textContent = 'Re';
	g.appendChild(reLabel);

	const imLabel = el('text', {
		x: String(zeroX + 5),
		y: String(PAD - 6),
		fill: '#888',
		'font-size': '10',
	});
	imLabel.textContent = 'Im';
	g.appendChild(imLabel);
}

function line(
	g: SVGGElement,
	x1: number,
	y1: number,
	x2: number,
	y2: number,
	stroke: string,
	width: number,
): void {
	g.appendChild(
		el('line', {
			x1: String(x1),
			y1: String(y1),
			x2: String(x2),
			y2: String(y2),
			stroke,
			'stroke-width': String(width),
			'stroke-linecap': 'round',
		}),
	);
}

function dashedLine(
	g: SVGGElement,
	x1: number,
	y1: number,
	x2: number,
	y2: number,
	stroke: string,
): void {
	g.appendChild(
		el('line', {
			x1: String(x1),
			y1: String(y1),
			x2: String(x2),
			y2: String(y2),
			stroke,
			'stroke-width': '1.25',
			'stroke-dasharray': '5 4',
			opacity: '0.65',
		}),
	);
}

function dot(
	g: SVGGElement,
	p: { x: number; y: number },
	fill: string,
	label: string,
): void {
	g.appendChild(
		el('circle', {
			cx: String(p.x),
			cy: String(p.y),
			r: '4',
			fill,
		}),
	);
	const t = el('text', {
		x: String(p.x + 7),
		y: String(p.y - 6),
		fill,
		'font-size': '11',
		'font-weight': '600',
	});
	t.textContent = label;
	g.appendChild(t);
}

function el<K extends keyof SVGElementTagNameMap>(
	tag: K,
	attrs?: Record<string, string>,
): SVGElementTagNameMap[K] {
	const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
	if (attrs) {
		for (const [k, v] of Object.entries(attrs)) {
			node.setAttribute(k, v);
		}
	}
	return node;
}
