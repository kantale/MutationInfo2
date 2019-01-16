
function ajax(question) {
    $.ajax({
        data: {
            question: question
        },
        url: "answer/", 
        success: function(result){
            //$("#div1").html(result);
            //alert(result);
            //console.log(result);
            $("#answer").html(result.reply);
        },
        error(xhr,status,error) {
            console.log(xhr);
            console.log(status);
            console.log(error);
        }
    });
}

function go_clicked() {
    var question = $('#question').val();
    //alert(question);
    ajax(question);
}


