var readtracking = new Object()

readtracking.selectedText = function() {

    // For safari
    if (window.getSelection) {
        return window.getSelection();
    }

    // For Firefox
    if (document.getSelection) {
      return document.getSelection();
    } 
    
    //For IE
    if (document.selection && document.selection.createRange) {
      var range = document.selection.createRange();
      return range.text;
    }

    return "Sorry, this is not possible with your browser.";
}

