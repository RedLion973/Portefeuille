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
	$("#select_all").live('change',function() {
	  	$(".selection:checkbox").attr('checked', this.checked);
	});
	$(".selected").live('change',function() {
	  	$(this).attr('checked', true);
	});
	$('#select_fut').click(function() {
		if($('input[name="futs"]:checked').length > 0) {
			$('#futs_selection_form').submit();
		}
		else {
			alert("Vous devez sélectionner au moins un FUT à inclure dans la synthèse !");	
		}
		return false;
	});
});
