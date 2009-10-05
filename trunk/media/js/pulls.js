function openpull(id){
closeaccordion();
$('.leftpart').html("");
$.ajax({
      url: "/pull/"+id,
      global: false,
      type: "GET",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    $('.leftpart').html(msg);
	}
	else{
	}
      }
   }
)
}

function updatepull(id){
closeaccordion();
$('#pullbody'+id).html("Please wait...");
$.ajax({
      url: "/pull/"+id,
      global: false,
      type: "GET",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    $('#pullbody'+id).replaceWith(msg);
	}
	else{
	}
      }
   }
)
}


function findFeed(){
q=$("#id_feed_url").attr('value');
$("#id_feed_url").attr("value","please wait...");
$.ajax({
      url: "/find_feed/",
      global: false,
      type: "GET",
      data: ({url : q}),
      success: function(msg){
	if (msg!="None"){
	 $("#id_feed_url").css("color","black");
         $("#id_feed_url").attr("value",msg);
	 $("#id_feed_cheked").attr("value","True");
	}
	else{
	 $("#id_feed_url").css("color","red");
         $("#id_feed_url").attr("value","No feeds found!");
	 $("#id_feed_cheked").attr("value","False");
	}
      }
   }
)
}

function suggest_feed(){
/*q=$("#id_feed_url").attr('value');
$.post("/suggest_feed/",
    {control_id : "id_feed_url",div_id:"suggest_feed_div",first_chars:q},
    function(data){
	$("#suggest_feed_div").html(data);
	$("#suggest_feed_div").show("fast");
    }
);*/
}

function togglepull(a){
closeaccordion();
$('#pullbody'+a+' > .entry').toggle();
if ($('#togglepull'+a).text()=='show')
$('#togglepull'+a).text('hide');
else
$('#togglepull'+a).text('show');
}

function cleanpull(a){
closeaccordion();
if (confirm("Are you SURE?\nThere will be no undo and all data will be lost!")){
$.ajax({
      url: "/clean_pull/",
      global: false,
      type: "POST",
      data: ({id : a}),
      success: function(msg){
	if (msg!="Ok"){
	 alert("Something gone wrong");
	}
	else{
	$('#pullbody'+a+' > .entry').remove();
	 //$("#pullbody"+a).text("");
	}
      }
   }
)
}
}

function purgepull(a){
closeaccordion();
if (confirm("Are you SURE?\nThere will be no undo and all data will be lost!")){
$.ajax({
      url: "/purge_pull/",
      global: false,
      type: "POST",
      data: ({id : a}),
      success: function(msg){
	if (msg!="Ok"){
	 alert("Something gone wrong");
	}
	else{
	 $("#pullbody"+a).remove();
	 $("#openpull"+a).remove();
	}
      }
   }
)
}
}

function addfeed(id){
$("#accordionform").insertAfter("#pullheader"+id);
$("#accordion").toggle("normal");
$("#id_pull_id").attr("value",id);
//$("#id_pull_title").attr("value",id);
}

function closeaccordion(){
$("#accordion").hide();
$("#accordionform").insertBefore("#footer");
}


function create_new_pull(){
a=prompt("Please, enter new pull's title:","new pull");
if (a!=null){
$.ajax({
      url: "/create_pull/",
      global: false,
      type: "POST",
      data: ({title : a}),
      success: function(msg){
	if (msg=="Error"){
	 alert("Something gone wrong!"); 
	}
	else{
	 $('.leftpart').prepend(msg);
	id=$(".pullbody:first").attr("id").substring(8);
	$("#createpull").before('<div id="openpull'+id+'" class="rightmenu" onclick="javascript:openpull('+id+');">'+$('.pullheadertext:first').text()+'</div>');

	}
      }
   }
);
}
}

function add_feed_to_pull(){
$.ajax({
      url: "/add_feed/",
      global: false,
      type: "POST",
      data: ({
	feed_url : $("#id_feed_url").attr("value"),
	feed_cheked : $("#id_feed_cheked").attr("value"),
	filter_must : $("#id_filter_must").attr("value"),
	filter_may : $("#id_filter_may").attr("value"),
	filter_not : $("#id_filter_not").attr("value"),
	pull_title : $("#id_pull_title").attr("value"),
	pull_id : $("#id_pull_id").attr("value")
}),
    error: function(q,w){
	alert("Check entered URL, please!");
    },
      success: function(msg){
	 closeaccordion();
	 $("#pullbody"+$("#id_pull_id").attr("value")).replaceWith(msg);
      }
   }
)

}

