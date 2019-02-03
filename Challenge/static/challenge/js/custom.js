$(document).ready(function(){
   toastr.options = {
  "closeButton": true,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-full-width",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}



   $(".like_shop").on('click', function(){
      var url = $(this).attr('url');
      var csrf_token = $(this).attr('csrf_token');
      var shop = $(this).attr('shop');
      $.ajax({
            url: url,
            type: 'POST',
            data: {'shop': shop, 'csrfmiddlewaretoken': csrf_token},
            success: function(response){
               if( response.status ){
                  toastr["success"](response.message);
               }else{
                  toastr["error"](response.message);
               }
            },
            error: function(response){

            }
        });
   });

   $(".dislike_shop").on('click', function(){
      var url = $(this).attr('url');
      var csrf_token = $(this).attr('csrf_token');
      var shop = $(this).attr('shop');
      $.ajax({
            url: url,
            type: 'POST',
            data: {'shop': shop, 'csrfmiddlewaretoken': csrf_token},
            success: function(response){
               if( response.status ){
                  toastr["success"](response.message);
                  $("#shop"+shop).remove();
                  if( response.no_more_shops ){
                     $('<div class="alert alert-info  mt-3" style="padding: 10px;font-size:12px;font-weight:bold;width: 100%;">\n' +
                         '            <i class="fa fa-exclamation-triangle"></i>&nbsp;No shop found!\n' +
                         '        </div>').insertBefore(".card-deck:first");
                     $("#paginator").remove();
                  }
               }else{
                  toastr["error"](response.message);
               }
            },
            error: function(response){

            }
        });
   });

   $(".remove_shop").on('click', function(){
      var url = $(this).attr('url');
      var csrf_token = $(this).attr('csrf_token');
      var shop = $(this).attr('shop');
      $.ajax({
            url: url,
            type: 'POST',
            data: {'shop': shop, 'csrfmiddlewaretoken': csrf_token},
            success: function(response){
               if( response.status ){
                  toastr["success"](response.message);
                  $("#shop"+shop).remove();
                  if( response.no_more_shops ){
                     $('<div class="alert alert-info  mt-3" style="padding: 10px;font-size:12px;font-weight:bold;width: 100%;">\n' +
                         '            <i class="fa fa-exclamation-triangle"></i>&nbsp;No shop found in your list!\n' +
                         '        </div>').insertBefore(".card-deck:first");
                     $("#paginator").remove();
                  }
               }else{
                  toastr["error"](response.message);
               }
            },
            error: function(response){

            }
        });
   });

});


