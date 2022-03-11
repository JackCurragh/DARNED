$(document).ready(function(){
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


//For Drosophila


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



});
