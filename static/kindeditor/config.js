 KindEditor.ready(function(K) {
     window.editor = K.create('#id_content',{
         width:800,
         height:600,
         uploadJson:"/upload_img/",
         extraFileUploadParams:{
             csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
         },
         filePostName:"put_img"

     });
 });