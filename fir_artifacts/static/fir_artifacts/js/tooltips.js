$(function () {

	var tooltipTimer = false;
	var timeout = 500;

	function sticky_tooltip(){
		var tooltip = $('.tooltip');
		tooltip.on('mouseover', function() { clearTimeout(tooltipTimer) })
		.on('mouseleave', function() {
			setTimeout(function(){
				tooltip.prev().tooltip('hide')
			}, timeout);
		})
	}

	$('span.artifact_tooltip').tooltip({'html':true, 'trigger':'manual', 'delay': {'show':100, 'hide':200} })
	.on('mouseover', function(){
		clearTimeout(tooltipTimer);
		$(this).tooltip('show');
		sticky_tooltip();
	})
	.on('mouseleave', function() {
		tooltipTimer = setTimeout(function(){$('.tooltip').prev().tooltip('hide')}, timeout);
	});
});
