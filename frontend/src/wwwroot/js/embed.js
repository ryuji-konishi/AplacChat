var urlChatInferAddress;		// Chat inference request URL given by environment configuration.

var init = function(chatInferAddress, divForm, divScroll, divRecords) {
	urlChatInferAddress = chatInferAddress;
	var input = divForm.find('#chat-input')
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
			submitChat(divForm, divScroll, divRecords);
			break;
		}
	});
	input.focus();
}

var initLayout = function(body, divForm, divScroll) {
	var totalHeight = body.height()
	var formHeight = divForm.height()
	// Set the height of scroll div based on the total height (HTML body)
	// and the form div where the form div height is constant.
	// This work is required to make the scroll div scrollable. To make div
	// scrollable its height needs to be explicitly set while 'overflow' is
	// set to 'auto' in CSS.
	var h = totalHeight - formHeight;
	divScroll.height(h)
	// Setting 'max-height' is not for scroll div but its child div.
	// The child div's max-height is set to 'inherit' so eventually
	// the child div inherits the same value in max-height.
	// By setting a distinct height, the child div can be aligned at bottom.
	divScroll.css('max-height', h)
}

var submitChat = function(divForm, divScroll, divRecords) {
	var input = divForm.find('#chat-input')
	var text = input.val();
	text = text.trim();
	if (text == '')
		return;
	appendChatSend(divScroll, divRecords, text)
	showBusyImage(divForm);
	$.ajax({
		url : urlChatInferAddress,
		type : "POST",
		dataType : "json",
		contentType : "text/plain",
		data : text,
		success : function(resp) {
			if (resp != null) {
				hideMessage(divForm);
				input.val('');
				appendChatReceive(divScroll, divRecords, resp)
			}
			else {
				showMessage(divForm, "<strong>Sorry!</strong> Internal error happened.");
			}
			hideBusyImage(divForm);
		},
		error : function(xhr, status, error) {
			showMessage(divForm, "<strong>Sorry!</strong> Internal error happened.");
			hideBusyImage(divForm);
		}
	});
}

var appendChatSend = function(divScroll, divRecords, text) {
	appendChatText(divScroll, divRecords, text, 'chat-send-record', 'chat-send-decorate');
}

var appendChatReceive = function(divScroll, divRecords, text) {
	appendChatText(divScroll, divRecords, text, 'chat-receive-record', 'chat-receive-decorate');
}

var appendChatText = function(divScroll, divRecords, text, classNameRec, classNameDec) {
	// Append to the current HTML content so that the latest text comes at bottom.
	var htm = divRecords.html();	// Current HTML content.
	
	// Decorate div. This div contains the text and style formatted.
	var decDiv = '<div class="' + classNameDec + '">';
	decDiv += text
	decDiv += '</div>';
	
	// Outer div. This div piles up the div layer as records.
	// Its content is horizontally aligned.
	var outDiv = '<div class="' + classNameRec + '">';
	outDiv += decDiv;
	outDiv += '</div>';

	divRecords.html(htm + outDiv);
	
	// Scroll down the div section to the bottom so that the last record
	// is shown at the bottom.
	// divScroll.scrollTop(Number.MAX_SAFE_INTEGER)
	divScroll.scrollTop(divScroll.prop('scrollHeight') - divScroll.height())
}

var showMessage = function(divForm, message) {
	divForm.find('#show-message').show().html(
			'<p><b>' + message + '</b></p>');
}

var hideMessage = function(divForm) {
	divForm.find('#show-message').hide();
}

var showBusyImage = function(divForm) {
	divForm.find('#chat-input').addClass('chat-input-busy');
}

var hideBusyImage = function(divForm) {
	divForm.find('#chat-input').removeClass('chat-input-busy');
}

