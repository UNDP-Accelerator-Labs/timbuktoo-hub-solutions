import { setup as setupSVG } from './svg.mjs';
import { draw as drawRadar } from './radar.mjs';

function fetchData (path) {
	return fetch(decodeURI(path))
	.then(res => res.json())
	.catch(err => console.log(err));
}

async function onLoad () {
	let data = await fetchData('./data/full_dataset.json');
	const main_categories = [
		'reason',
		'smart citities and mobility',
		'trade logistics and ecommerce',
		'manufacturing',
		'green tech climate and energy',
		'health tech',
		'mine tech',
		'creatives',
		'fin tech',
		'argi tech',
		'tourism',
		'ed tech',
		'pad_id',
	];
	console.log(data.length)
	data = data.filter(d => {
		const keys = Object.keys(d);
		return keys.every(c => main_categories.includes(c))
	});
	console.log(data.length)
	
	// const categories = data.map(d => Object.keys(d))
	// .flat().filter((value, index, array) => {
  	// 	return array.indexOf(value) === index;
	// });
	// const values = data.map(d => {
	// 	const { pad_id, reason, ...categories } = d;
	// 	return Object.values(categories)
	// })
	// .flat()
	// .filter((value, index, array) => {
  	// 	return array.indexOf(value) === index;
	// });
	// console.log(values)
	
	// SET UP SVG
	const { svg, width, height } = setupSVG();
	const size = Math.min(width, height);

	const radars = data.map(d => {
		const { shape } = drawRadar(d, main_categories.filter(c => !['reason', 'pad_id'].includes(c)), size);
		return shape;
	});
	const avgRadar = {}
	main_categories.filter(c => !['reason', 'pad_id'].includes(c))
	.forEach(d => {
		const values = data.map(c => c[d]);
		avgRadar[d] = d3.mean(values);
	});
	console.log(avgRadar)

	const line = d3.line()
		.x(d => d[0])
		.y(d => d[1])

	// svg.addElems('path', 'radar', radars)
	const { shape, axes, rings } = drawRadar(avgRadar, Object.keys(avgRadar), size);
	const g = svg.addElems('g')
		.attr('transform', `translate(${[width/2, height/2]})`)
	
	g.addElems('circle', 'ring', rings)
		.attr('r', d => d)
	
	g.addElems('line', 'axis-interaction', axes)
	.attrs({ 
		'x1': d => d[0][0], 
		'y1': d => d[0][1], 
		'x2': d => d[1][0], 
		'y2': d => d[1][1],
	}).on('click', async (evt, d) => {
		const limit = 50;
		const focus = data.filter(c => c[d[2]] > 0).sort((a, b) => b[d[2]] - a[d[2]]);
		const padIds = focus.map(c => c.pad_id).slice(0, limit).join('&pads=');
		const endpoint = `https://solutions.sdg-innovation-commons.org/apis/fetch/pads?pads=${padIds}`;

		// LOAD THE PADS
		let padData = await fetchData(endpoint);
		// JOIN THE SCORES
		padData = padData.map(d => {
			const obj = focus.find(c => c.pad_id === d.pad_id) || {}
			return {...d, ...obj}
		});

		const section = d3.select('section.pads')
			.classed('open', true);
		section.addElems('h1', 'category-title')
			.html(d[2])
		const pads = section.addElems('div', 'pad', padData);
		pads.addElems('h2')
			.html(c => `${c.title} (${c[d[2]]})`);
		pads.addElems('img')
			.attr('src', c => c.vignette);
		pads.addElems('p')
			.html(c => c.reason);

	});
	g.addElems('line', 'axis', axes)
	.attrs({ 
		'x1': d => d[0][0], 
		'y1': d => d[0][1], 
		'x2': d => d[1][0], 
		'y2': d => d[1][1],
	});

	g.addElems('text', 'axis-label', axes)
	.attrs({ 
		'transform': d => {
			if (d[3] < 90 || d[3] >= 270) return `translate(${[d[1][0], d[1][1]]})rotate(${d[3]})`;
			else return `translate(${[d[1][0], d[1][1]]})rotate(${d[3]})scale(-1)`;
		}
	}).styles({
		'text-anchor': d => {
			if (d[3] < 90 || d[3] >= 270) return 'end';
			else return 'start';
		}
	}).text(d => d[2]);

	g.addElems('path', 'radar', [shape])
	.attrs({
		'd': d => `${line(d)} Z`,
	}).styles({
		'fill': 'none',
		'stroke': '#000'
	})
}

if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', function () {
		onLoad();
	});
} else {
	(async () => { await onLoad() })();
}