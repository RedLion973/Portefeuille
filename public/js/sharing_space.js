$(document).ready(function() {
	$('#tree').treeview();
	$('#add_folder').click(function() {
		var $dialog = $('#sharing_dialog').load($(this).attr('to_load')).dialog({
        		autoOpen: false,
       	 		modal: true,
        		draggable: false,
        		resizable: false,
        		title: 'Ajouter un dossier',
        		width: 300,
        		height: 300,
			close: function() {
				window.location.reload();
			}
    		});

    		$dialog.dialog('open');
    		return false;
	});
});
