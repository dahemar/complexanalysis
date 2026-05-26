import fs from 'node:fs';
import path from 'node:path';

function backendAppDir(): string {
	const candidates = [
		path.resolve(process.cwd(), '../backend/app'),
		path.resolve(process.cwd(), 'backend/app'),
	];
	for (const dir of candidates) {
		if (fs.existsSync(dir)) return dir;
	}
	throw new Error('backend/app directory not found');
}

export function readPythonModule(filename: string): string {
	const filePath = path.join(backendAppDir(), filename);
	return fs.readFileSync(filePath, 'utf-8');
}
