
App.Node = DS.Model.extend({
	name: DS.attr('string'),
	type:  DS.attr('string'),
	display: DS.attr('boolean', false),
	color: DS.attr('string'),
	opacity: DS.attr('number', 1.0),
	pointsize: DS.attr('number', 1.0),
	type: DS.attr('string', 'TRIANGLES')
});
