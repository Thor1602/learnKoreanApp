$(document).ready(function () {
    $("#dropdown_quiz").on('click', function (event) {
        $('#quiz_topic_table').show();
        $('#translation_table').hide();
        $('#question_table').hide();
        $('#discussion_table').hide();
        $('#post_table').hide();
        $('#reply_table').hide();
        $('#subreply_table').hide();
    });
    $("#dropdown_translation").on('click', function (event) {
        $('#translation_table').show();
        $('#quiz_topic_table').hide();
        $('#question_table').hide();
        $('#discussion_table').hide();
        $('#post_table').hide();
        $('#reply_table').hide();
        $('#subreply_table').hide();
    });
    $("#dropdown_question").on('click', function (event) {
        $('#question_table').show();
        $('#quiz_topic_table').hide();
        $('#translation_table').hide();
        $('#discussion_table').hide();
        $('#post_table').hide();
        $('#reply_table').hide();
        $('#subreply_table').hide();
    });
    $("#dropdown_discussion").on('click', function (event) {
        $('#discussion_table').show();
        $('#quiz_topic_table').hide();
        $('#translation_table').hide();
        $('#question_table').hide();
        $('#post_table').hide();
        $('#reply_table').hide();
        $('#subreply_table').hide();
    });
    $("#dropdown_post").on('click', function (event) {
        $('#post_table').show();
        $('#quiz_topic_table').hide();
        $('#translation_table').hide();
        $('#question_table').hide();
        $('#discussion_table').hide();
        $('#reply_table').hide();
        $('#subreply_table').hide();
    });
    $("#dropdown_reply").on('click', function (event) {
        $('#reply_table').show();
        $('#quiz_topic_table').hide();
        $('#translation_table').hide();
        $('#question_table').hide();
        $('#discussion_table').hide();
        $('#post_table').hide();
        $('#subreply_table').hide();
    });
    $("#dropdown_subreply").on('click', function (event) {
        $('#subreply_table').show();
        $('#quiz_topic_table').hide();
        $('#translation_table').hide();
        $('#question_table').hide();
        $('#discussion_table').hide();
        $('#post_table').hide();
        $('#reply_table').hide();
    });
    {% for query in database['translation_data'] %}
        $("#translation_edit_{{ query[0] }}").on("click", function () {
            $('#adminOverviewModalTranslation').modal("show");
        });
    {% endfor %}
    {% for query in database['quiz_data'] %}
        $("#quiz_edit_{{ query[0] }}").on("click", function () {
            $('#adminOverviewModalQuizTopic').modal("show");
        });
    {% endfor %}
    {% for query in database['question_data'] %}
        $("#question_edit_{{ query[0] }}").on("click", function () {
            $('#adminOverviewModalQuestion').modal("show");
        });
    {% endfor %}
    {% for query in database['discussion_data'] %}
        $("#discussion_edit_{{ query[0] }}").on("click", function () {
            $('#adminOverviewModalDiscussion').modal("show");
        });
    {% endfor %}
    {% for query in database['post_data'] %}
        $("#post_edit_{{ query[0] }}").on("click", function () {
            $('#adminOverviewModalPost').modal("show");
        });
    {% endfor %}
    {% for query in database['reply_data'] %}
        $("#reply_edit_{{ query[0] }}").on("click", function () {
            $('#adminOverviewModalReply').modal("show");
        });
    {% endfor %}
     {% for query in database['subreply_data'] %}
        $("#subreply_edit_{{ query[0] }}").on("click", function () {
            $('#adminOverviewModalSubreply').modal("show");
        });
    {% endfor %}


})