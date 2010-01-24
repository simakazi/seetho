function updatetopic(id){
$('#topicbody'+id).html("<img src='/img/loading.gif' />");
$.ajax({
      url: "/topic/"+id,
      global: false,
      type: "GET",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    $('#topicbody'+id).replaceWith(msg);
	}
	else{
	}
      }
   }
)
}

function updategrouptopic(group_id,id){
$('#topicbody'+id).html("<img src='/img/loading.gif' />");
$.ajax({
      url: "/group/"+group_id+"/topic/"+id,
      global: false,
      type: "GET",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    $('#topicbody'+id).replaceWith(msg);
	}
	else{
	}
      }
   }
)
}

function toggletopic(a){
$('#topicbody'+a+' > .entry').toggle();
if ($('#toggletopic'+a).text()=='show')
$('#toggletopic'+a).text('hide');
else
$('#toggletopic'+a).text('show');
}

function cleantopic(a){
if (confirm("Are you SURE?\nThere will be no undo and all data will be lost!")){
$('#topicbody'+a).html("<img src='/img/loading.gif' />");
$.ajax({
      url: "/clean_topic/",
      global: false,
      type: "POST",
      data: ({id : a}),
      success: function(msg){
	
	
	$("#topicbody"+a).replaceWith(msg);

      }
   }
)
}
}

function purgetopic(a){
if (confirm("Are you SURE?\nThere will be no undo and all data will be lost!")){
$.ajax({
      url: "/purge_topic/",
      global: false,
      type: "POST",
      data: ({id : a}),
      success: function(msg){
	if (msg!="Ok"){
	 alert("Something gone wrong");
	}
	else{
	 $("#topicbody"+a).remove();
	}
      }
   }
)
}
}

function addcomment(topic_id,comment_text){
$.ajax({
      url: "/add_comment/",
      global: false,
      type: "POST",
      data: ({topic : topic_id,text:comment_text}),
      success: function(msg){
	if (msg=="Error"){
	 alert("Something gone wrong!"); 
	}
	else{
	 updatetopic(topic_id);
	}
      }
   }
);
}

function group_addcomment(group_id,topic_id,comment_text){
$.ajax({
      url: "/add_comment/",
      global: false,
      type: "POST",
      data: ({topic : topic_id,text:comment_text}),
      success: function(msg){
	if (msg=="Error"){
	 alert("Something gone wrong!"); 
	}
	else{
	 document.location.reload();
	}
      }
   }
);
}

function newtopic(id){
a=prompt("Please, enter new topic's title:","new topic");
if (a!=null){
$.ajax({
      url: "/start_group_topic/",
      global: false,
      type: "POST",
      data: ({title : a,group_id:id}),
      success: function(msg){
	if (msg=="Error"){
	 alert("Something gone wrong!"); 
	}
	else{
	    $('#grouptopics'+id).append(msg);
	}
      }
   }
);
}
}
