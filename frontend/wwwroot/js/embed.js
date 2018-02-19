var init = function(form, records) {
    var input = form.find('#chat-input')
	input.keypress(function(e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		if ((code == 8)	// BS or delete
		|| ((33 <= code) && (code <= 40))){	// up/down, right/left, page up/down
			// just ignore (this is for firefox)
			return;
		}
		var currentText = input.val();
		switch (code) {
		case 13:	// enter
			e.preventDefault();
            submitChat(form, records);
			break;
		}
	});
	input.focus();
}

var initLayout = function(body, form, records) {
	var totalHeight = body.height()
	var formHeight = form.height()
	// Set the height of records div based on the total height (HTML body)
	// and the form div where the form div height is constant.
	// This work is required to make the records div scrollable. To make div
	// scrollable its height needs to be explicitly set while 'overflow' is
	// set to 'auto' in CSS.
	records.height(totalHeight - formHeight)
}

var submitChat = function(form, records) {
    var input = form.find('#chat-input')
	var text = input.val();
	text = text.trim();
	if (text == '')
		return;
	input.attr("placeholder", "");
	showBusyImage(form);
	$.ajax({
		url : "http://localhost:5000/infer",
		type : "POST",
        dataType : "json",
        contentType : "text/plain",
		data : text,
		success : function(resp) {
			if (resp != null) {
                hideMessage(form);
                input.val('');
                populateList(records, resp);
			}
			else {
				showMessage(form, "<strong>Sorry!</strong> Internal error happened.");
			}
			hideBusyImage(form);
		},
		error : function(xhr, status, error) {
			showMessage(form, "<strong>Sorry!</strong> Internal error happened.");
			hideBusyImage(form);
		}
	});
}

var populateList = function(records, text) {
    var tableBody = records.find('tbody')
    // prepend the current HTML content so that the latest text comes at top.
    var current = tableBody.html();
    var newText = ''
    newText += '<tr>';
    newText += '<td><blockquote>' + text + '</blockquote></td>'
    newText += '</tr>';
    tableBody.html(newText + current);
}

var showMessage = function(form, message) {
	form.find('#show-message').show().html(
			'<p><b>' + message + '</b></p>');
}

var hideMessage = function(form) {
	form.find('#show-message').hide();
}

var showBusyImage = function(form) {
    form.find('#chat-input').addClass('chat-input-busy');
}

var hideBusyImage = function(form) {
	form.find('#chat-input').removeClass('chat-input-busy');
}