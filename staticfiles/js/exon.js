#This need to change

$(document).ready(function(){
    var org = $("#org").val();
    if (org=="hu"){
    $('#h1').submit(function() {
        var error = 0;
        var start = $('#id_start').val();
        if (start == '') {
            error = 1;
            alert('Start cannot be empty');
        }
	var end = $('#id_end').val();
        if (end == '') {
            error = 1;
            alert('End cannot be empty');
        }
	var flank = $('#id_flank').val();
        if (flank == '') {
            error = 1;
            alert('Flanking Sequence Length cannot be empty');
        }

        if(error){
            return false;
        }else{
            return true;
        }

    });

$('#h2').submit(function() {
        var error = 0;
        var seqid = $('#id_seqid').val();
        if (seqid == '') {
            error = 1;
            alert('Name cannot be empty');
        }
        if(error){
            return false;
        }else{
            return true;
        }

    });


$('#h3').submit(function() {
        var error = 0;
        var seq = $('#id_seq').val();
        if (seq == '') {
            error = 1;
            alert('You must enter sequence');
        }
        if(error){
            return false;
        }else{
            return true;
        }

    });
    }


//For Drosophila

else{
    $('#d1').submit(function() {
        var error = 0;
        var start = $('#id_start').val();
        if (start == '') {
            error = 1;
            alert('Start cannot be empty');
        }
	var end = $('#id_end').val();
        if (end == '') {
            error = 1;
            alert('End cannot be empty');
        }
	var flank = $('#id_flank').val();
        if (flank == '') {
            error = 1;
            alert('Flanking Sequence Length cannot be empty');
        }

        if(error){
            return false;
        }else{
            return true;
        }

    });

$('#d2').submit(function() {
        var error = 0;
        var seqid = $('#id_seqid').val();
        if (seqid == '') {
            error = 1;
            alert('Name cannot be empty');
        }
        if(error){
            return false;
        }else{
            return true;
        }

    });


$('#d3').submit(function() {
        var error = 0;
        var seq = $('#id_seq').val();
        if (seq == '') {
            error = 1;
            alert('You must enter sequence');
        }
        if(error){
            return false;
        }else{
            return true;
        }

    });
}


});









function displayExonType(inId){
	var x = document.getElementById("hregionTable").rows[3].cells;
	var exonSeqDiv = document.getElementById('exons');
	var seqTypeIdVal = document.getElementById(inId);
	if(seqTypeIdVal.value == 'E'){ 
		exonSeqDiv.style.display='block';
		x[0].colSpan="1";
		x[1].colSpan="1";
		}
	else{
		exonSeqDiv.style.display='none';
		x[0].colSpan="2";
		x[1].colSpan="0";
		}

}
