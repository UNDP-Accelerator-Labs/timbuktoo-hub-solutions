export const draw = function (d, dimensions, size) {
	const arr = []
	const radialScale = d3.scaleLinear()
		.domain([0, 4])
		.range([10, size * .75 /2])

	dimensions.forEach((c, j) => {
		const angle = -(Math.PI / 2) + (2 * Math.PI * j / dimensions.length)
		arr.push(polarToCartesian(angle, radialScale(+d[c] || 0)))
	});
	if (dimensions.length === 1) arr.push([0, 0])

	const axes = dimensions.map((c, j) => {
		const angle = -(Math.PI / 2) + (2 * Math.PI * j / dimensions.length)
		const start = polarToCartesian(angle, radialScale(0)) 
		const end = polarToCartesian(angle, radialScale(Math.max(...radialScale.domain()))) 
		return [start, end, c, radianToDegree(angle)];
	});

	const rings = (new Array(Math.max(...radialScale.domain()))).fill(0).map((d, i) => radialScale(i));
	
	return { shape: arr, axes, rings };
}

function polarToCartesian (angle, length, offset) {
	if (!offset) offset = [0, 0];
	var x = Math.cos(angle) * length + offset[0];
	var y = Math.sin(angle) * length + offset[1];
	return [x, y];
}

function radianToDegree (radian) {
	return (radian >= 0 ? radian : (2 * Math.PI + radian)) * 360 / (2 * Math.PI)
}