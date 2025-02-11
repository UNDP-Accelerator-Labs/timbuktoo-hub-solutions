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
		// 'reason',
		// 'smart citities and mobility',
		// 'trade logistics and ecommerce',
		// 'manufacturing',
		// 'green tech climate and energy',
		// 'health tech',
		// 'mine tech',
		// 'creatives',
		// 'fin tech',
		// 'argi tech',
		// 'tourism',
		// 'ed tech',
		// 'pad_id',
		"reason",
		"cities/mobility",
		"ecommerce/logistics",
		"manufacturing",
		"green/climate/energy",
		"healthtech",
		"minetech",
		"creative",
		"fintech",
		"agritech",
		"tourism",
		"edtech",
		"pad_id"
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

	// const radars = data.map(d => {
	// 	const { shape } = drawRadar(d, main_categories.filter(c => !['reason', 'pad_id'].includes(c)), size);
	// 	return shape;
	// });
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
		.attr('transform', `translate(${[width/2, height/2]})`);
	
	g.addElems('circle', 'ring', rings)
		.attr('r', d => d);
	
	g.addElems('line', 'axis-interaction', axes)
	.attrs({ 
		'x1': d => d[0][0], 
		'y1': d => d[0][1], 
		'x2': d => d[1][0], 
		'y2': d => d[1][1],
	}).on('click', async (evt, d) => {
		const dimension = d[2];
		const limit = 50;
		const focus = data.filter(c => c[dimension] > 0)
		focus.sort((a, b) => b[dimension] - a[dimension]);
		const padIds = focus.map(c => c.pad_id).slice(0, limit);
		const token = d3.select('input[name="token"]').node().value.trim()
		let padData = [];
		const params = new URLSearchParams();
		if (token.length) params.set('token', token);
		if (padIds.length) {
			padIds.forEach(c => {
				params.append('pads', c);
			});
			const endpoint = `https://solutions.sdg-innovation-commons.org/apis/fetch/pads?${params.toString()}`;
			// LOAD THE PADS
			padData = await fetchData(endpoint);
		}
		// JOIN THE SCORES
		padData = padData.map(c => {
			const obj = focus.find(b => b.pad_id === c.pad_id) || {}
			return {...c, ...obj}
		});
		padData.sort((a, b) => b[dimension] - a[dimension]);

		const section = d3.select('section.pads')
			.classed('open', true);
		section.addElems('h1', 'category-title')
			.html(dimension)
		const pads = section.addElems('div', 'pad', padData);
		
		const header = pads.addElems('div', 'header')
		const sm_size = 100
		const radar = header.addElems('svg')
			.attrs({
				'width': sm_size,
				'height': sm_size,
			})
		.addElems('g', 'radar-group', c => {
			return [drawRadar(c, main_categories.filter(c => !['reason', 'pad_id'].includes(c)), sm_size)];
		}).attr('transform', `translate(${[sm_size/2, sm_size/2]})`)
		
		radar.addElems('circle', 'ring', c => c.rings)
			.attr('r', c => c)
			.styles({
				'fill': 'none',
				'stroke': 'rgba(255,255,255,.33)'
			});
		radar.addElems('line', 'axis', c => c.axes)
		.attrs({ 
			'x1': c => c[0][0], 
			'y1': c => c[0][1], 
			'x2': c => c[1][0], 
			'y2': c => c[1][1],
		}).styles({
			'fill': 'none',
			'stroke': 'rgba(255,255,255,.33)'
		});
		radar.addElems('path', 'radar', c => {
			console.log(c.shape)
			return [c.shape]
		})
		.attrs({
			'd': c => `${line(c)} Z`,
		}).styles({
			'fill': 'none',
			'stroke': '#FFF'
		});

		header.addElems('h2')
		.addElems('a')
			.attrs({
				'href': c => `https://${c.source}`,
				'target': '_blank',
			}).html(c => c.title.trim());
		pads.addElems('img', 'vignette', c => c.vignette ? [c.vignette] : [])
			.attr('src', c => c);

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
	});
}

if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', function () {
		onLoad();
	});
} else {
	(async () => { await onLoad() })();
}