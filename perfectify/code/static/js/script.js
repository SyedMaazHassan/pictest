if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

function allowdrop(event){
    event.preventDefault();
    var THIS = event.target;
    $(THIS).addClass("dragover");
    $("#showing_div").css("display", "none");

}

function now_drop(event){
    event.preventDefault();
    input = document.getElementById("target_file");
    input.files = event.dataTransfer.files;
    readURL(input, 'showing_div');
}

function previous_state(event){
      var THIS = event.target;
      $(THIS).removeClass("dragover");
}

function submit_form() {
    if($("#target_file").val()){
        $("#my-form").submit();
    }
}

function upload_file(whick_input) {
    $("#"+whick_input).click();
}

function readURL(input, show) {
    $("#"+show).css('display', 'none');
    nameFile = input.files[0].name.split(".");
    nameFile = nameFile[nameFile.length-1];
    
    //console.log(nameFile);
    if(nameFile=="png" || nameFile=="jpg" || nameFile=="jpeg" || nameFile=="JPG"){
        if (input.files && input.files[0]) {
            $("#file-error-msg").text("");

            var reader = new FileReader();

            // if (nameFile == "docx") {
            //     show = show+"_2";
            // }

            reader.onload = function (e) {
                var result_to_show = e.target.result;
                //console.log(result_to_show)
                $("#"+show).css('display', '');
                $("#"+show).prop("class", "decrease-s-width");
                $('#'+show)
                    .attr('src', result_to_show)
                    .width('100%')
                    .height('');

                // $("#preview").modal("show");
                open_modal();
                $("#showing_div").show();
                $("#image_error").hide();
                $("#submit_button").show();
            };

            if (!(nameFile == "docx" || nameFile == "doc")) {
                $("#see_docs_file").css('display', 'none');
                reader.readAsDataURL(input.files[0]);
            }else{
                $("#see_docs_file").css('display', '');
                reader.readAsDataURL(input.files[0]);
            }

            $("#success-msg").css('display', '');

        }
    }else{
        open_modal();
        $("#target_file").val(null);    
        $("showing_div").removeClass("dragover");
        $("#showing_div").hide();
        $("#image_error").show();
        $("#submit_button").hide();

    }

    $("#dropzone").removeClass("dragover");
}




// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
// var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

function open_modal(){
    let modal = document.getElementById("myModal");
    modal.style.display = "block";  
}

function close(){
    let modal = document.getElementById("myModal");
    modal.style.display = "none";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}
