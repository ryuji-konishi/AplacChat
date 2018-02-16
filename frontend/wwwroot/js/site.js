var init = function() {
	$('#formula-input').keypress(function(e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		if ((code == 8)	// BS or delete
		|| ((33 <= code) && (code <= 40))){	// up/down, right/left, page up/down
			// just ignore (this is for firefox)
			return;
		}
		var currentText = $('#formula-input').val();
		switch (code) {
		case 13:	// enter
			e.preventDefault();
            submitFormula();
			break;
		}
	});
	$('#formula-input').focus();
}

var submitFormula = function() {
	var text = $('#formula-input').val();
	text = text.trim();
	if (text == '')
		return;
	$("#formula-input").attr("placeholder", "");
	showBusyImage();
	$.ajax({
		url : "http://localhost:5000/infer",
		type : "POST",
        dataType : "json",
        contentType : "text/plain",
		data : text,
		success : function(resp) {
			if (resp != null) {
                hideHint();
                hideMessage();
                $('#formula-input').val('');
                populateList(resp);
			}
			else {
				showMessage("<strong>Sorry!</strong> Internal error happened.");
			}
			hideBusyImage();
		},
		error : function(xhr, status, error) {
			showMessage("<strong>Sorry!</strong> Internal error happened.");
			hideBusyImage();
		}
	});
}

var populateList = function(text) {
    // creating the table content
    var htm = '';
    htm += '<tr>';
    htm += '<td><blockquote>' + text + '</blockquote></td>'
    htm += '</tr>';
    $('#calc-records-tbody').html(htm);
}

var showMessage = function(message) {
	$('#show-message').show().html(
			'<p><b>' + message + '</b></p>');
}

var hideMessage = function() {
	$('#show-message').hide();
}

var showHint = function(message) {
	$('#show-hint').show().html(
			'<p>' + message + '</p>');
}

var hideHint = function() {
	$('#show-hint').hide();
}

var showBusyImage = function() {
	$('#formula-input').addClass('formula-input-busy');
}

var hideBusyImage = function() {
	$('#formula-input').removeClass('formula-input-busy');
}