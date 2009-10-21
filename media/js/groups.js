function addpull(id){
a=prompt("Please, enter new pull's title:","new pull");
if (a!=null){
$.ajax({
      url: "/create_pull/",
      global: false,
      type: "POST",
      data: ({title : a,group_id:id}),
      success: function(msg){
	if (msg=="Error"){
	 alert("Something gone wrong!"); 
	}
	else{
	    if ($('#grouppulls'+id).html()=="No pulls")
		$('#grouppulls'+id).html("");
	 $('#groupbody'+id).append(msg);
	//id=$("#groupbody"+id+" > .pullbody:last").attr("id").substring(8);
	//$("#createpull").before('<div id="openpull'+id+'" class="rightmenu" onclick="javascript:openpull('+id+');">'+$('.pullheadertext:first').text()+'</div>');

	}
      }
   }
);
}
}

function updategroup(id){
//closeaccordion();
$('#groupbody'+id).html("<img src='/img/loading.gif' />");
$.ajax({
      url: "/group/"+id,
      global: false,
      type: "GET",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    $('#groupbody'+id).replaceWith(msg);
	}
      }
   }
)
}

function togglegroup(a){
//closeaccordion();
$('#grouppulls'+a).toggle();
if ($('#togglegroup'+a).text()=='show')
$('#togglegroup'+a).text('hide');
else
$('#togglegroup'+a).text('show');
}

function purgegroup(a){
//closeaccordion();
if (confirm("Are you SURE?\nThere will be no undo and all data will be lost!")){
$.ajax({
      url: "/purge_group/",
      global: false,
      type: "POST",
      data: ({id : a}),
      success: function(msg){
	if (msg=="Ok"){
	 $("#groupbody"+a).remove();
	 $("#opengroup"+a).remove();
	}
      }
   }
)
}
}

function create_new_group(){
a=prompt("Please, enter new group's title:","new group");
if (a!=null){
$.ajax({
      url: "/create_group/",
      global: false,
      type: "POST",
      data: ({title : a}),
	error: function(e,q){
	    alert("Try another name for your group!");
	},
      success: function(msg){
	 $('.leftpart').prepend(msg);
	id=$(".pullbody:first").attr("id").substring(8);
	$("#creategroup").before('<div id="opengroup'+id+'" class="rightmenu" onclick="javascript:opengroup('+id+');">'+$('.pullheadertext:first').text()+'</div>');
      }
   }
);
}
}

function opengroup(id){
closeaccordion();
$('.leftpart').html("");
$.ajax({
      url: "/group/"+id,
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

function subscribe_group(id){
$.ajax({
      url: "/subscribe_group/"+id,
      global: false,
      type: "POST",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    $('#groupbody'+id).replaceWith(msg);
	}
      }
   }
)
}

function unsubscribe_group(id){
$.ajax({
      url: "/unsubscribe_group/"+id,
      global: false,
      type: "POST",
      data: ({}),
      success: function(msg){
	if (msg!="None"){
	    if ($(".button_disabled").text()!="Search")
		$('#groupbody'+id).replaceWith("");
	else	
	    $('#groupbody'+id).replaceWith(msg);
	}
      }
   }
)
}
