$(document).ready(function() {

Survey
    .JsonObject
    .metaData
    .addProperty("question", "tag");
// Change the order of name and title properties, remove the startWithNewLine property and add a tag property
SurveyEditor
    .SurveyQuestionEditorDefinition
    .definition["question"]
    .properties = [
        "title",
        "name", {
            name: "tag",
            title: "Tag"
        }, {
            name: "visible",
            category: "checks"
        }, {
            name: "isRequired",
            category: "checks"
        }
    ];
// make visibleIf tab the second after general for all questions
SurveyEditor
    .SurveyQuestionEditorDefinition
    .definition["question"]
    .tabs = [
        {
            name: "visibleIf",
            index: 1
        }
    ];

var editorOptions = {};
var editor = new SurveyEditor.SurveyEditor("editorElement", editorOptions);
}
