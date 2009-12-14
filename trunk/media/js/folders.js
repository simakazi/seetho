function tweetentry(text,id){
window.open('http://twitter.com/home?status='+encodeURIComponent(text),'twitter','toolbar=0,status=0');
/*
$("#upyachka").remove();
$("#main").append("<iframe width='0' height='0' frameborder='0' style='display:none' id='upyachka' name='upyachka'></iframe>");
$("#upyachka").append("<form id='callme' target='upyachka' action='http://twitter.com/statuses/update.xml' method='post'><input name='status'' value='"+text+"'><input type='submit'></input></form>");
$("#callme").trigger("submit");
$("a[name='tweet"+id+"']").replaceWith("<i>tweeted</i>");
*/

/*$.post("http://twitter.com/statuses/update.json", { status: text },
  function(data){
    alert("Data Loaded: " + data);
  });
/*
$.ajax({
        url:"http://twitter.com/statuses/update.json",
        global:false,
        type:"POST",
        data:({"status":text}),
        succes: function(msg){
         alert(msg);
        }
  
    });
*/
}

function facebook_share(u,t){
window.open('http://www.facebook.com/sharer.php?u='+encodeURIComponent(u)+'&t='+encodeURIComponent(t),'sharer','toolbar=0,status=0,width=626,height=436');
}

function bookmark_on_delicious(u,t){
window.open('http://delicious.com/save?v=5&noui&jump=close&url='+encodeURIComponent(u)+'&title='+encodeURIComponent(t),'delicious','toolbar=550,status=550');
}


function openfolder(id){
closeaccordion();
$('.leftpart').html("");
$.ajax({
      url: "/folder/"+id,
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

function updatefolder(id){
closeaccordion();
$('#folderbody'+id).html("<img src='/img/loading.gif' />");
$.ajax({
      url: "/folder/"+id,
      global: false,
      type: "POST",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    $('#folderbody'+id).replaceWith(msg);
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

function togglefolder(a){
closeaccordion();
$('#folderbody'+a+' > .entry').toggle();
if ($('#togglefolder'+a).text()=='show')
$('#togglefolder'+a).text('hide');
else
$('#togglefolder'+a).text('show');
}

function cleanfolder(a){
closeaccordion();
if (confirm("Are you SURE?\nThere will be no undo and all data will be lost!")){
$('#folderbody'+a).html("<img src='/img/loading.gif' />");
$.ajax({
      url: "/clean_folder/",
      global: false,
      type: "POST",
      data: ({id : a}),
      success: function(msg){
	
	
	$("#folderbody"+a).replaceWith(msg);

      }
   }
)
}
}


function more_folder(a,more){
closeaccordion();
$.ajax({
      url: "/more_folder/"+a+"/"+more,
      global: false,
      type: "GET",
      success: function(msg){
        $("[name='more"+a+"']").replaceWith(msg);
      }
   }
)
}

function purgefolder(a){
closeaccordion();
if (confirm("Are you SURE?\nThere will be no undo and all data will be lost!")){
$.ajax({
      url: "/purge_folder/",
      global: false,
      type: "POST",
      data: ({id : a}),
      success: function(msg){
	if (msg!="Ok"){
	 alert("Something gone wrong");
	}
	else{
	 $("#folderbody"+a).remove();
	 $("#openfolder"+a).remove();
	}
      }
   }
)
}
}

function addfeed(id){

if ($("#folderbody"+id+" #accordion").attr("id")=="accordion"){
$("#accordion").toggle();
}
else{
$("#accordionform").insertAfter("#folderheader"+id);
$("#accordion").show();
$("#id_folder_id").attr("value",id);
}
//$("#id_folder_title").attr("value",id);
}

function closeaccordion(){
$("#accordion").hide();
$("#accordionform").insertBefore("#footer");
}


function create_new_folder(){
a=prompt("Please, enter new folder's title:","new folder");
if (a!=null){
$.ajax({
      url: "/create_folder/",
      global: false,
      type: "POST",
      data: ({title : a}),
      success: function(msg){
	if (msg=="Error"){
	 alert("Something gone wrong!"); 
	}
	else{
	 $('.leftpart').prepend(msg);
	id=$(".folderbody:first").attr("id").substring(8);
	$("#createfolder").before('<div id="openfolder'+id+'" class="rightmenu" onclick="javascript:openfolder('+id+');">'+$('.folderheadertext:first').text()+'</div>');

	}
      }
   }
);
}
}

function add_feed_to_folder(){
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
	folder_title : $("#id_folder_title").attr("value"),
	folder_id : $("#id_folder_id").attr("value")
}),
    error: function(q,w){
	$("<div>"+q.responseText+"</div>").dialog({
	    modal:true,
	    overlay: {
				backgroundColor: '#000',
				opacity: 0.5
			},
	    "dialogClass":"errordialog",   
	    
	    minHeight:20,
	   buttons: {"Close": function() { $(this).dialog("close"); }}
	});
    },
      success: function(msg){
	 closeaccordion();
	 $("#folderbody"+$("#id_folder_id").attr("value")).replaceWith(msg);
      }
   }
)

}

