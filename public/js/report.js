$(document).ready(function() {
	$("#id_scheduled_start_date").datepicker();
	$("#id_scheduled_end_date").datepicker();
	$("#id_effective_start_date").datepicker();
	$("#id_effective_end_date").datepicker();
	$('#reset').click(function() {
		$(":input").val('');
		$('#filter_form').submit();
	});
});
