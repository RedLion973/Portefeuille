$(document).ready(function() {
	$('#selection_actions li').button();
	$('#show_planning').button();
	$('#show_planning').click(function() {
		$('#modal_planning').dialog("open");
		return false;
	});
	$('#modal_planning').dialog({
		modal: true,
		width: "auto",
		autoOpen: false,
		show: "blind",
		hide: "explode"
	});
});
