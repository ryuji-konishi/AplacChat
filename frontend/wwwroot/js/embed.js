var init = function(form, scroll, records) {
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
            submitChat(form, scroll, records);
			break;
		}
	});
	input.focus();
}

var initLayout = function(body, form, scroll) {
	var totalHeight = body.height()
	var formHeight = form.height()
	// Set the height of scroll div based on the total height (HTML body)
	// and the form div where the form div height is constant.
	// This work is required to make the scroll div scrollable. To make div
	// scrollable its height needs to be explicitly set while 'overflow' is
	// set to 'auto' in CSS.
	var h = totalHeight - formHeight;
	scroll.height(h)
	// Setting 'max-height' is not for scroll div but its child div.
	// The child div's max-height is set to 'inherit' so eventually
	// the child div inherits the same value in max-height.
	// By setting a distinct height, the child div can be aligned at bottom.
	scroll.css('max-height', h)
}

var submitChat = function(form, scroll, records) {
    var input = form.find('#chat-input')
	var text = input.val();
	text = text.trim();
	if (text == '')
		return;
	appendChatSend(scroll, records, text)
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
				appendChatReceive(scroll, records, resp)
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

var appendChatSend = function(scroll, records, text) {
	appendChatText(scroll, records, text, 'chat-send-record', 'chat-send-decorate');
}

var appendChatReceive = function(scroll, records, text) {
	appendChatText(scroll, records, text, 'chat-receive-record', 'chat-receive-decorate');
}

var appendChatText = function(scroll, records, text, classNameRec, classNameDec) {
    // Append to the current HTML content so that the latest text comes at bottom.
	var htm = records.html();	// Current HTML content.
	
	// Decorate div. This div contains the text and style formatted.
    var decDiv = '<div class="' + classNameDec + '">';
    decDiv += text
	decDiv += '</div>';
	
	// Outer div. This div piles up the div layer as records.
	// Its content is horizontally aligned.
	var outDiv = '<div class="' + classNameRec + '">';
	outDiv += decDiv;
	outDiv += '</div>';

	records.html(htm + outDiv);
	
	// Scroll down the div section to the bottom so that the last record
	// is shown at the bottom.
	scroll.scrollTop(Number.MAX_SAFE_INTEGER)
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

