$(document).ready(function() {
	$('#futs_selection_form').hide();
	$('#selection_actions li').button();
	$('#show_selection').click(function() {
		$('#futs_selection_form').toggle();
		return false;
	});
	$("#select_all").live('change',function() {
	  	$(".selection:checkbox").attr('checked', this.checked);
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
