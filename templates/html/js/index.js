var editorOptions = {
          questionTypes:["text","checkbox","radiogroup","dropdown"],
          showPropertyGrid: false,
          showPagesToolbox: false
          }

var editor = new SurveyEditor.SurveyEditor("editorElement", editorOptions);

editor.saveSurveyFunc = function (saveNo, callback) {
    $.ajax({
        url: "UrlToYourWebService",
        type: "POST",
        data: {
            surveyId: yourEditUniqueSurveyI,
            surveyText : editor.text
        },
        success: function (data) {
            callback(saveNo, data.isSuccess);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            callback(saveNo, false);
            alert(thrownError);
        }
    });
}
