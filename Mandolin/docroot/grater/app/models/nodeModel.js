
App.Node = DS.Model.extend({
	name: DS.attr('string'),
	type:  DS.attr('string'),
	display: DS.attr('boolean', false)
});
