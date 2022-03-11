function hs_displayExonType(inId){
	var x = document.getElementById("hregtab").rows[3].cells;
	var exonSeqDiv = document.getElementById('hsexo');
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

function dm_displayExonType(inId){
	var x = document.getElementById("dregtab").rows[3].cells;
	var exonSeqDiv = document.getElementById('dmexo');
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

function mm_displayExonType(inId){
	var x = document.getElementById("mregtab").rows[3].cells;
	var exonSeqDiv = document.getElementById('mmexo');
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



