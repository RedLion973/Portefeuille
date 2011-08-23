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
    		$('input:text[name=username]').val('phantomjs');
    		$('input:password[name=password]').val('riddim973++973++');
    		$('#login_form').submit();
    	});
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            page.onLoadFinished = function (status) {
			page.render(output);
            phantom.exit();
	    };
        }
    });
}
