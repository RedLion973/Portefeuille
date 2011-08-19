$(document).ready(function() {
	$("#id_scheduled_start_date_0").datepicker({ dateFormat: 'dd/mm/yy' });
	$("#id_scheduled_start_date_1").datepicker({ dateFormat: 'dd/mm/yy' });
	$("#id_scheduled_end_date_0").datepicker({ dateFormat: 'dd/mm/yy' });
	$("#id_scheduled_end_date_1").datepicker({ dateFormat: 'dd/mm/yy' });
	$("#id_effective_start_date_0").datepicker({ dateFormat: 'dd/mm/yy' });
	$("#id_effective_start_date_1").datepicker({ dateFormat: 'dd/mm/yy' });
	$("#id_effective_end_date_0").datepicker({ dateFormat: 'dd/mm/yy' });
	$("#id_effective_end_date_1").datepicker({ dateFormat: 'dd/mm/yy' });
	$('#reset').click(function() {
		$(":input").val('');
		$('#filter_form').submit();
	});
});
