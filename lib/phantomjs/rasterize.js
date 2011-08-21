var page = new WebPage(),
    address, output, size;

if (phantom.args.length < 2 || phantom.args.length > 3) {
    console.log('Usage: rasterize.js URL filename');
    phantom.exit();
} else {
    address = phantom.args[0];
    output = phantom.args[1];
    page.viewportSize = { width: 600, height: 600 };
    page.open(address, function (status) {
    	page.evaluate(function() {
    		$('input:text[name=username]').val('ludovic');
    		$('input:password[name=password]').val('riddim');
    		$('#login_form').submit();
    	});
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            window.setTimeout(function () {
                page.render(output);
            	console.log('OK');
                phantom.exit();
            }, 200);
        }
    });
}
