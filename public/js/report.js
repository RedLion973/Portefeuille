$(document).ready(function() {
	$("#id_scheduled_start_date_0").datepicker();
	$("#id_scheduled_start_date_1").datepicker();
	$("#id_scheduled_end_date_0").datepicker();
	$("#id_scheduled_end_date_1").datepicker();
	$("#id_effective_start_date_0").datepicker();
	$("#id_effective_start_date_1").datepicker();
	$("#id_effective_end_date_0").datepicker();
	$("#id_effective_end_date_1").datepicker();
	$('#reset').click(function() {
		$(":input").val('');
		$('#filter_form').submit();
	});
});
