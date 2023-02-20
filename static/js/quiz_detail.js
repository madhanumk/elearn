if (localStorage.getItem("quizarray") === null) {
    localStorage.setItem("quizarray", JSON.stringify([]));
}

$(function(){
    retrive_answer();
});

function retrive_answer() {

    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    
    var lim = quizarray.length;
    for (var i = 0; i < lim; i++) {
      
        $('input:radio[value=' + quizarray[i].valueid + ']').prop('checked', true);
        $('input:checkbox[value=' + quizarray[i].valueid + ']').prop('checked', true);
        
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$('#quizdetail').click(function () {
    var r = confirm("Quiz will be closed! Have you completed the quiz? Do You want to submit? ");
    if(r==true)
    {
        var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    var csrftoken = getCookie('csrftoken');
    var lim =quizarray.length;
    var quizName = $('#quiz_name').text();
    var questionCount = $('#question_count').attr('value');

        
    if(lim!=0 && (quizName != "VAK Learning Style" || (quizName == "VAK Learning Style"  && questionCount == lim)))
    { 
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url : "/quiz/quizdetail",
        data : JSON.stringify(quizarray),
        dataType: "json",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) { 

            localStorage.clear();
            location.href="/quiz/my_scores";
  
        }
        }); 
    }
    else{

        if(quizName == "VAK Learning Style"){
            alert('To submit this test, you must answer all of the questions.');
        }
        else{
            alert('No Questions Answered!!!');
        }
        
    }


    }
    
});

$('#ques_window').on('click','input:radio',function () {

   

    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    var lim = quizarray.length;

    var flag = 0;
  
        for (var i = 0; i < lim; i++) {
            if ( quizarray[i].valueid == $(this).attr("value")){
                flag=1;
                break;
            }
            if (quizarray[i].questionid == $(this).attr("question")) {
                $('input:radio[value=' + quizarray[i].valueid + ']').prop('checked', false);
                quizarray[i].optionid = $(this).attr("option");
                quizarray[i].valueid = $(this).attr("value");
                flag = 1;
                break;
            }
    
        }
    
    

    if (flag == 0 ) {

        
        
        quizarray.push({
            quizid: $('#test_id').attr("test"),
            assignmentid: $(this).attr("assignment"),
            questionid: $(this).attr("question"),
            optionid: $(this).attr("option"),
            valueid: $(this).attr("value"),
        });


    }
    localStorage.setItem("quizarray", JSON.stringify(quizarray));   
   



});


$('#ques_window').on('click','input:checkbox',function () {

   
    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
     var lim = quizarray.length;
 
     var flag = 0;
   
         for (var i = 0; i < lim; i++) {
             if ( quizarray[i].valueid == $(this).attr("value")){
                 flag=1;
                 break;
             }
     
     
         }
     
     if ( flag == 0 ) {
         
         quizarray.push({
             quizid: $('#test_id').attr("test"),
             assignmentid: $(this).attr("assignment"),
             questionid: $(this).attr("question"),
             optionid: $(this).attr("option"),
             valueid: $(this).attr("value"),
         });
 
 
     }
     localStorage.setItem("quizarray", JSON.stringify(quizarray));   
    
 
 
 
 });



$(function () {

    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    var lim = quizarray.length;
    for (var i = 0; i < lim; i++) {
        $('input:radio[value=' + quizarray[i].valueid + ']').prop('checked', true);
        $('input:checkbox[value=' + quizarray[i].valueid + ']').prop('checked', true);
    }

});



$('#ques_window').on('click','input:checkbox',function () {
    var json = JSON.parse(localStorage["quizarray"]);
    $('input:checkbox').not(':checked').each(function()
    {
      uncheckedvalue=$(this).attr("value");
      uncheckedQuestionValue=$(this).attr("questionid");

       
        for (i=0;i<json.length;i++)
           if (json[i]. valueid ==  uncheckedvalue)

           
              json.splice(i,1);
              localStorage["quizarray"] = JSON.stringify(json);

           });  

        
      
    
       
});


$(document).ready(function()
{
    $('#prev_ques').hide();
    
    $('.ques_nav').click(function()
    {
        event.preventDefault();
        no = $(this).attr('ques_no');
        test = $('#test_id').attr('test');
        
        $.ajax({
            url : '/quiz/load_question/',
            data:{'question_no':no,'test':test},
            method:'get',
            success:function(data){

                
                $('#ques_window').html(data.question);
                $('#prev_ques').attr('ques_no',data.question_no-1);
                $('#next_ques').attr('ques_no',data.question_no+1);

                if(data.question_no==data.question_count-1)
                {
                    $('#next_ques').hide();
                }
                else{
                    $('#next_ques').show();
                }

                if(data.question_no==0)
                {
                    $('#prev_ques').hide();
                }
                else{
                    $('#prev_ques').show();
                }

               retrive_answer();
               MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
                
            }
        });

    });

});