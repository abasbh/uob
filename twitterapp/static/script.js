$(function (){
 

	$topics = [{'Main': 'عام',
          'Sub': ['عام']
          },
         {'Main': 'الكليات',
          'Sub': ['تقنية المعلومات',
                  'العلوم',
                  'التربية',
                  'الحقوق',
                  'الهندسة',
                  'التعليم التطبيقي',
                  'الآداب',
                  'كلية المعلمين',
                  'ادارة الاعمال',
                  'التربية الرياضية والعلاج الطبيعي',
                  'العلوم الصحية',
                  'محاضرات',
                  'دكاترة',
                  'مختبرات',
                  'صفوف دراسية',
                  'المواد الدراسية',
                  'الموقع الإلكتروني',
                  'الاختبارات'
                  ]
          },
         {'Main': 'التسجيل',
          'Sub': [
              'المواد الدراسية',
              'الموقع الإلكتروني',
              'الصفوف الدراسية',
              'المقاعد',
              'تعارض',
              'الدفع',
              'تخصص',
              'دكاترة'
              ]
          },
         {'Main': 'ادارة الجامعة',
          'Sub': [
              'الرئيس',
              'مجلس ادارة',
              'قوانين'
              ]
          },
         {'Main': 'فعاليات و احتفالات',
          'Sub': [
              'احتفال',
              'مهرجان',
              'ضيوف',
              'رعاية',
              'العيد الوطني',
              'أعياد',
              'مشاركة',
              'ورش عمل',
              'فعالية'
              ]
          },
         {'Main': 'المكتبة',
          'Sub': [
              'المكتبة العامة',
              'مكتبة العلوم',
              'الكتب',
              'المؤلفات',
              'المجلات',
              'كاتب',
              'طباعة',
              'الهدوء',
              'الفوضى',
              'الموظفين'
              ]
          },
         {'Main': 'شؤون الطلبة',
          'Sub': [
              'المتخرجون',
              'الدراسات العليا',
              'بحث علمي',
              'الطلبة الجدد'
              ]
          },
         {'Main': 'الحياة الجامعية',
          'Sub': [
              'المطاعم',
              'النظافة',
              'المظهر الشخصي'
              ]
          }
         
         ];
		 
	count = 0;
  j = setInterval(ajax_call,10000);
  ajax_call()
  
function ajax_call(){
  count++;
  console.log(count)
if ($('div.panel').length) {
    var x = $("div.container").children("div.panel").first().attr("id");

$.ajax({
      "type": "POST",
      "async": false,
      "dataType": "html",
      "url": "/data/",
      "data":{"id":x},
      "success": function(result){

		 $(".container").prepend(result);
		 twemoji.parse(document.body);
      }
  });
  


}
else {
$.ajax({
      "type": "GET",
      "async": false,
      "dataType": "html",
      "url": "/data/",
      "data":{id:''},
      "success": function(result){
		  
        $(".container").prepend(result);
		
		twemoji.parse(document.body);
      }
  });
}

}

$(document).on('focus','form #mainTopic',function(e){
    e.preventDefault();
	var x = $(this).find('option:selected').val();
		
	var t = '';
	for (var i in $topics) {
//alert($topics[i].Main);
				t += "<option>"+ $topics[i].Main + "</option>" ;
	} 

	$(this).html(t);
	if (typeof x !== 'undefined'){
	$(this).val(x).attr('selected','selected');
	
	}
	else{
		$(this).attr('selectedIndex', 0);
		$(this).change();
	}
	});
$(document).on('change','form #mainTopic',function(e){
	$(this).parents("form").find("#subTopic").attr('disabled',false);
	$(this).parents("form").find("#submit").attr('disabled',false);
    e.preventDefault();

		//alert('ok!');
	var topic = $(this).find("option:selected").val();
	var t = '';
	for (var i in $topics) {
		if ($topics[i].Main == topic){
			for (var j in $topics[i].Sub)
			{
				t += "<option>"+ $topics[i].Sub[j] + "</option>" ;
			}
		}
	} 

	$(this).parents("form").find("#subTopic").html(t);
	});

$(document).on('click','form #submit',function(e){	
    e.preventDefault();
		$tid = $(this).parents(".panel").attr("id");
		var sent = $(this).parents("form").find('#sentiment option:selected').val();
		$(this).parents(".panel-heading").find(".SentimentR").text(sent);
		var main = $(this).parents("form").find('#mainTopic option:selected').val();
		$(this).parents(".panel-heading").find(".mainTopicR").text(main);
		var subt = $(this).parents("form").find('#subTopic option:selected').val();
		$(this).parents(".panel-heading").find(".subTopicR").text(subt);
		//alert($tid);
		$this = $(this);
		$.ajax({
      "type": "POST",
      "async": false,
      "dataType": "html",
      "url": "/label/",
      "data":{id:$tid,
	  sent:sent,main:main,subt:subt},
      "success": function(result){
		 // alert("success");
		$this.parents(".panel-heading").find("#lable").show();
		$this.parents("#formlable").remove();	
      },
	   "error": function(){
        alert("Error");
    }
	  
  });
		
    });
});